"""
webhook_daemon.py — EN-OS Event Bridge
=======================================
State Machine: GitHub Webhook → NanoClaw Container Ignition

State 0: IDLE_LISTEN    — FastAPI listening on localhost:8001/webhook
State 1: AUTH_GATE      — HMAC SHA256 signature validation (timing-safe)
State 2: PAYLOAD_PARSE  — Parse event type, extract issue# and repo
State 3: NANOCLAW_IGNITION — Detached subprocess.Popen(docker run) + 202 return

Engineering rule: The daemon never waits for the container. GitHub webhooks
time out after 10 seconds; the daemon validates, ignites, and walks away.

Usage:
    uvicorn scripts.webhook_daemon:app --host 127.0.0.1 --port 8001
"""

import os
import hmac
import hashlib
import logging
import subprocess
from pathlib import Path
from datetime import datetime, UTC

from fastapi import FastAPI, Request, HTTPException, status
from dotenv import load_dotenv

# ── State 0: IDLE_LISTEN — Environment Setup ───────────────────────────────

load_dotenv()
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
NANOCLAW_ENABLED = os.getenv("NANOCLAW_ENABLED", "false").lower() == "true"
WEBHOOK_DAEMON_PORT = int(os.getenv("WEBHOOK_DAEMON_PORT", "8001"))

if not GITHUB_WEBHOOK_SECRET:
    raise ValueError(
        "CRITICAL: GITHUB_WEBHOOK_SECRET not set. "
        "Copy .env.example → .env and add your webhook secret."
    )

# Audit log — append-only, written to registry so it's in version control
LOG_PATH = Path(__file__).parent.parent / "registry" / "global_agent" / "daemon_audit.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(LOG_PATH), encoding="utf-8"),
    ],
)
logger = logging.getLogger("EN-OS.Daemon")

app = FastAPI(
    title="EN-OS Event Bridge",
    description="GitHub webhook → NanoClaw container ignition. State machine, no wait.",
    version="1.0.0",
)


# ── State 1: AUTH_GATE ─────────────────────────────────────────────────────

def verify_signature(payload_body: bytes, signature_header: str | None) -> bool:
    """
    Cryptographic validation of GitHub payload via HMAC-SHA256.
    hmac.compare_digest() prevents timing analysis attacks.
    """
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    hash_object = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode("utf-8"),
        msg=payload_body,
        digestmod=hashlib.sha256,
    )
    expected = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected, signature_header)


# ── State 3: NANOCLAW_IGNITION ─────────────────────────────────────────────

def ignite_nanoclaw(issue_number: int, repo_name: str, agent_mode: str = "plan") -> None:
    """
    Fire a fully isolated NanoClaw container and immediately drop the reference.
    The daemon does NOT wait for the container — it returns 202 instantly.
    """
    logger.info(f"IGNITION: NanoClaw queued for {repo_name}#{issue_number}")

    if not NANOCLAW_ENABLED:
        logger.warning(
            f"SIMULATION: NANOCLAW_ENABLED=false — would run: "
            f"docker run --rm nanoclaw:latest for {repo_name}#{issue_number}"
        )
        return

    cmd = [
        "docker", "run", "--rm",
        "--env-file", str(Path(__file__).parent.parent / ".env"),
        "--label", f"enos.mode={agent_mode}",
        "-e", f"AGENT_MODE={agent_mode}",
        "-e", f"TARGET_ISSUE={issue_number}",
        "-e", f"TARGET_REPO={repo_name}",
        "nanoclaw:latest",
    ]

    try:
        # Popen detaches the process. stdout/stderr → DEVNULL; the container
        # must write its own forensic telemetry to ChromaDB/registry.
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        logger.error("IGNITION FAILED: Docker not found or nanoclaw:latest not built (#61)")
    except Exception as e:
        logger.error(f"IGNITION FAILED: {e}")


# ── Webhook Route (States 1→2→3) ───────────────────────────────────────────

@app.post("/webhook", status_code=status.HTTP_202_ACCEPTED)
async def github_webhook(request: Request):
    """
    Main entry point for all GitHub webhook events.

    Trigger A: issue_comment.created with '/execute' in body
    Trigger B: projects_v2_item.edited — item moved to 'In progress'
    All other events: acknowledged and dropped.
    """
    payload_body = await request.body()
    signature = request.headers.get("x-hub-signature-256")
    event_type = request.headers.get("x-github-event", "unknown")

    # ── STATE 1: AUTH GATE ─────────────────────────────────────────────────
    if not verify_signature(payload_body, signature):
        logger.warning("AUTH GATE FAILED: Invalid or missing HMAC signature.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature validation failed",
        )

    # ── STATE 2: PAYLOAD PARSE ─────────────────────────────────────────────
    try:
        payload = await request.json()
    except Exception:
        logger.warning("PAYLOAD PARSE FAILED: Malformed JSON body.")
        return {"status": "ignored", "reason": "malformed_json"}

    target_issue: int | None = None
    target_repo: str = payload.get("repository", {}).get(
        "full_name", "mechanistic-org/global_agent"
    )

    target_mode = "plan"

    # Trigger A: Manual /execute comment on any issue
    if event_type == "issue_comment" and payload.get("action") == "created":
        body = payload.get("comment", {}).get("body", "")
        if "/execute" in body.lower() or "/exec" in body.lower():
            target_issue = payload.get("issue", {}).get("number")
            target_mode = "exec"
            logger.info(f"TRIGGER A: /execute detected → {target_repo}#{target_issue} [EXEC MODE]")

    # Trigger B: Project V2 item moved to "In progress"
    elif event_type == "projects_v2_item" and payload.get("action") == "edited":
        changes = payload.get("changes", {})
        field_value = changes.get("field_value", {})
        field_name = field_value.get("field_name", "")
        to_name = field_value.get("to", {}).get("name", "")

        if field_name == "Status" and to_name in ("In progress", "Sprint Now"):
            # Project V2 payloads don't include issue number directly.
            # Log the node_id so we can inspect the raw payload shape and
            # tighten the traversal after a live test.
            node_id = payload.get("projects_v2_item", {}).get("content_node_id", "unknown")
            logger.info(
                f"TRIGGER B: Item moved to '{to_name}'. "
                f"content_node_id={node_id} — resolve to issue# via gh api if needed."
            )
            # TODO (#73-followup): Resolve node_id → issue number via gh API
            # target_issue = resolve_node_to_issue(node_id)

    # ── STATE 3: NANOCLAW IGNITION ─────────────────────────────────────────
    if target_issue:
        ignite_nanoclaw(target_issue, target_repo, agent_mode=target_mode)
        return {
            "status": "accepted",
            "message": f"NanoClaw ignition queued for {target_repo}#{target_issue} in {target_mode.upper()} mode.",
        }

    # Noise — acknowledge and drop cleanly
    logger.debug(f"IGNORED: event={event_type} action={payload.get('action')}")
    return {"status": "ignored", "message": "Payload did not match ignition triggers."}


# ── Health check ───────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "online",
        "nanoclaw_enabled": NANOCLAW_ENABLED,
        "timestamp": datetime.now(UTC).isoformat(),
    }


# ── Entrypoint ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 60)
    logger.info("BOOTING EN-OS EVENT BRIDGE")
    logger.info(f"  Endpoint : http://127.0.0.1:{WEBHOOK_DAEMON_PORT}/webhook")
    logger.info(f"  NanoClaw : {'LIVE' if NANOCLAW_ENABLED else 'SIMULATION (set NANOCLAW_ENABLED=true to arm)'}")
    logger.info("=" * 60)

    uvicorn.run(
        "webhook_daemon:app",
        host="127.0.0.1",
        port=WEBHOOK_DAEMON_PORT,
        reload=False,
    )
