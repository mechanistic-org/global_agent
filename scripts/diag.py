#!/usr/bin/env python3
"""
diag.py — Sovereign EN-OS Health Harness
=========================================
Runs before any Apex Router swarm execution (PRD, FMEA, mining campaigns).
Validates that all pipeline dependencies are alive and authenticated.

Usage:
    python diag.py            # Full check, hard exit on failure
    python diag.py --warn     # Warn on failure, do not exit (advisory mode)
    python diag.py --json     # Machine-readable JSON output
    python diag.py --check ollama  # Run a single named check

Checks performed:
    1. Ollama VRAM  — localhost:11434 is up and at least one model is loaded
    2. ChromaDB     — Sovereign Registry collection is queryable
    3. GWS Auth     — gws auth status confirms token is valid
    4. SA Key       — GOOGLE_APPLICATION_CREDENTIALS key file exists and is parseable

Issue: mechanistic-org/global_agent#48
"""

import sys
import os
import json
import subprocess
import shutil
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Bootstrap: load global_config so .env (GOOGLE_APPLICATION_CREDENTIALS) is set
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
import global_config  # noqa: F401 — side effect: loads .env

WARN_ONLY = "--warn" in sys.argv
JSON_MODE = "--json" in sys.argv

# ---------------------------------------------------------------------------
# ANSI colour helpers (suppressed in JSON mode)
# ---------------------------------------------------------------------------
def _c(code: str, text: str) -> str:
    if JSON_MODE:
        return text
    return f"\033[{code}m{text}\033[0m"

OK   = lambda t: _c("32", f"✅  {t}")
FAIL = lambda t: _c("31", f"❌  {t}")
WARN = lambda t: _c("33", f"⚠️  {t}")
INFO = lambda t: _c("90", f"    {t}")

# ---------------------------------------------------------------------------
# Check: Ollama
# ---------------------------------------------------------------------------
OLLAMA_URL = "http://localhost:11434"

def check_ollama() -> dict:
    """Ping Ollama and verify at least one model is loaded in VRAM."""
    result = {"name": "Ollama VRAM", "status": "FAIL", "detail": ""}
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=4) as resp:
            data = json.loads(resp.read())
        models = data.get("models", [])
        if not models:
            result["detail"] = "Ollama is up but NO models are loaded. Run: ollama run <model>"
        else:
            names = [m.get("name", "?") for m in models]
            result["status"] = "OK"
            result["detail"] = f"{len(names)} model(s) loaded: {', '.join(names[:3])}"
    except urllib.error.URLError as e:
        result["detail"] = f"Connection refused — is Ollama running? ({e.reason})"
    except Exception as e:
        result["detail"] = str(e)
    return result

# ---------------------------------------------------------------------------
# Check: ChromaDB (via Python client, not HTTP — matches mcp_registry_server.py)
# ---------------------------------------------------------------------------
CHROMA_DB_PATH = str(Path(__file__).resolve().parent.parent / "registry" / ".chroma_db")

def check_chromadb() -> dict:
    """Verify the ChromaDB Sovereign Registry collection is queryable."""
    result = {"name": "ChromaDB Registry", "status": "FAIL", "detail": ""}
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collections = client.list_collections()
        names = [c.name for c in collections]
        if "forensic_telemetry" not in names:
            result["detail"] = f"Collection 'forensic_telemetry' missing. Collections found: {names or 'none'}"
        else:
            col = client.get_collection("forensic_telemetry")
            count = col.count()
            result["status"] = "OK"
            result["detail"] = f"forensic_telemetry: {count} document(s) indexed"
    except ModuleNotFoundError:
        result["status"] = "WARN"
        result["detail"] = "chromadb not in active Python env. Run from venv: cd scripts && pip install chromadb"
    except Exception as e:
        result["detail"] = f"ChromaDB error: {str(e)}"
    return result

# ---------------------------------------------------------------------------
# Check: GWS Auth Status
# ---------------------------------------------------------------------------
# Resolve gws binary — npm global install puts it in AppData on Windows
_GWS_NPM_FALLBACK = Path(os.environ.get("APPDATA", "")) / "npm" / "gws"
_GWS_BIN = shutil.which("gws") or (str(_GWS_NPM_FALLBACK) if _GWS_NPM_FALLBACK.exists() else None)

def check_gws_auth() -> dict:
    """Check gws auth status — confirms User OAuth token is valid."""
    result = {"name": "GWS Auth (User OAuth)", "status": "FAIL", "detail": ""}
    if not _GWS_BIN:
        result["detail"] = "gws not found on PATH or npm AppData. Install: npm i -g @googleworkspace/cli"
        return result
    try:
        proc = subprocess.run(
            [_GWS_BIN, "auth", "status"],
            capture_output=True,
            text=True,
            timeout=15,
            shell=True  # Required on Windows for .cmd scripts via AppData
        )
        output = (proc.stdout + proc.stderr).strip()
        # gws auth status outputs JSON — find and parse the JSON block
        json_start = output.find("{")
        json_end   = output.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            status_data = json.loads(output[json_start:json_end])
            token_valid = status_data.get("token_valid", False)
            token_error = status_data.get("token_error", "")
            project     = status_data.get("project_id", "?")
            if token_valid:
                result["status"] = "OK"
                result["detail"] = f"Token valid | project: {project} | method: {status_data.get('auth_method','oauth2')}"
            else:
                # Attempt auto-refresh (issue #70)
                try:
                    subprocess.run([_GWS_BIN, "auth", "refresh"], capture_output=True, timeout=15, shell=True)
                    proc2 = subprocess.run([_GWS_BIN, "auth", "status"], capture_output=True, text=True, timeout=15, shell=True)
                    output2 = (proc2.stdout + proc2.stderr).strip()
                    json_start2 = output2.find("{")
                    json_end2   = output2.rfind("}") + 1
                    if json_start2 >= 0 and json_end2 > json_start2:
                        status_data2 = json.loads(output2[json_start2:json_end2])
                        if status_data2.get("token_valid", False):
                            result["status"] = "OK"
                            result["detail"] = f"Token auto-refreshed | project: {project} | method: {status_data2.get('auth_method','oauth2')}"
                            return result
                except Exception:
                    pass

                err_msg = f"token_error: {token_error}" if token_error else "token_valid=false"
                result["detail"] = f"{err_msg} | project: {project} — Run: gws auth login"
        else:
            result["detail"] = output[:200] if output else "No output from gws auth status"
    except subprocess.TimeoutExpired:
        result["detail"] = "gws auth status timed out (>15s)"
    except Exception as e:
        result["detail"] = str(e)
    return result

# ---------------------------------------------------------------------------
# Check: GCP Service Account Key
# ---------------------------------------------------------------------------
def check_service_account() -> dict:
    """Verify GOOGLE_APPLICATION_CREDENTIALS key file exists and is parseable."""
    result = {"name": "SA Key (GOOGLE_APPLICATION_CREDENTIALS)", "status": "FAIL", "detail": ""}
    key_path_str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    if not key_path_str:
        result["detail"] = "GOOGLE_APPLICATION_CREDENTIALS is not set in environment / .env"
        return result

    key_path = Path(key_path_str)
    if not key_path.exists():
        result["detail"] = f"Key file not found: {key_path}"
        return result

    try:
        key_data = json.loads(key_path.read_text(encoding="utf-8"))
        sa_type  = key_data.get("type", "unknown")
        sa_email = key_data.get("client_email", "unknown")
        project  = key_data.get("project_id", "unknown")

        if sa_type != "service_account":
            result["detail"] = f"Expected type=service_account, got '{sa_type}'"
            return result

        result["status"] = "OK"
        result["detail"] = f"{sa_email} | project: {project}"
    except json.JSONDecodeError as e:
        result["detail"] = f"Key file is not valid JSON: {e}"
    except Exception as e:
        result["detail"] = str(e)
    return result

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
CHECKS = [check_ollama, check_chromadb, check_gws_auth, check_service_account]

def run_all() -> list[dict]:
    results = []
    for check_fn in CHECKS:
        r = check_fn()
        results.append(r)
    return results

def print_report(results: list[dict]) -> bool:
    """Pretty-print results. Returns True if all checks passed."""
    all_ok = all(r["status"] == "OK" for r in results)
    print()
    print(_c("1;37", "━━━  EN-OS DIAGNOSTIC HARNESS  ━━━"))
    print()
    for r in results:
        label = r["name"].ljust(40)
        if r["status"] == "OK":
            print(f"  {OK(label)}")
        else:
            print(f"  {FAIL(label)}")
        if r["detail"]:
            print(f"  {INFO(r['detail'])}")
    print()
    if all_ok:
        print(_c("32;1", "  🟢  ALL SYSTEMS NOMINAL — Router may proceed."))
    else:
        failed = [r["name"] for r in results if r["status"] != "OK"]
        print(_c("31;1", f"  🔴  {len(failed)} CHECK(S) FAILED: {', '.join(failed)}"))
        if not WARN_ONLY:
            print(_c("31", "  Swarm execution BLOCKED. Resolve failures above."))
    print()
    return all_ok

def main():
    results = run_all()

    if JSON_MODE:
        print(json.dumps({"checks": results, "all_ok": all(r["status"] == "OK" for r in results)}, indent=2))
        sys.exit(0 if all(r["status"] == "OK" for r in results) else 1)

    all_ok = print_report(results)

    if not all_ok and not WARN_ONLY:
        sys.exit(1)

if __name__ == "__main__":
    main()
