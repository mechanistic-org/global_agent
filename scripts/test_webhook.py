"""
test_webhook.py — Local smoke test for webhook_daemon.py
=========================================================
Sends a correctly HMAC-signed fake GitHub webhook to the running daemon
and verifies the correct 202 response.

Usage:
    # Start daemon first:
    uvicorn scripts.webhook_daemon:app --host 127.0.0.1 --port 8001

    # Then run this test:
    python scripts/test_webhook.py
    python scripts/test_webhook.py --trigger b   # test Project V2 trigger
    python scripts/test_webhook.py --bad-sig      # verify 401 on bad signature
"""

import argparse
import hmac
import hashlib
import json
import os
import sys
from dotenv import load_dotenv

try:
    import requests
except ImportError:
    print("ERROR: pip install requests first (or it's in requirements.txt)")
    sys.exit(1)

load_dotenv()
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
DAEMON_URL = f"http://127.0.0.1:{os.getenv('WEBHOOK_DAEMON_PORT', '8001')}/webhook"


def make_sig(payload: bytes, secret: str) -> str:
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    return "sha256=" + mac.hexdigest()


def send(payload: dict, event_type: str, corrupt_sig: bool = False) -> None:
    body = json.dumps(payload).encode()
    sig = make_sig(body, WEBHOOK_SECRET if not corrupt_sig else "BAD_SECRET")

    print(f"\n{'='*60}")
    print(f"POST {DAEMON_URL}")
    print(f"X-GitHub-Event: {event_type}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"{'='*60}")

    try:
        r = requests.post(
            DAEMON_URL,
            data=body,
            headers={
                "Content-Type": "application/json",
                "X-GitHub-Event": event_type,
                "X-Hub-Signature-256": sig,
                "X-GitHub-Delivery": "test-delivery-001",
            },
            timeout=5,
        )
        print(f"Status : {r.status_code}")
        print(f"Body   : {r.json()}")

        if corrupt_sig:
            assert r.status_code == 401, f"FAIL: Expected 401, got {r.status_code}"
            print("[PASS] Correctly rejected bad signature (401)")
        elif event_type in ("issue_comment",):
            assert r.status_code == 202, f"FAIL: Expected 202, got {r.status_code}"
            print("[PASS] Trigger A accepted (202)")
        else:
            print(f"[INFO] Status {r.status_code} -- check daemon logs for details")

    except requests.ConnectionError:
        print("[ERROR] Cannot connect to daemon. Is it running?")
        print(f"   Start with: uvicorn scripts.webhook_daemon:app --host 127.0.0.1 --port 8001")
        sys.exit(1)


if __name__ == "__main__":
    if not WEBHOOK_SECRET:
        print("ERROR: GITHUB_WEBHOOK_SECRET not set in .env")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--trigger", choices=["a", "b"], default="a",
                        help="a=issue_comment /execute  b=projects_v2_item move")
    parser.add_argument("--bad-sig", action="store_true",
                        help="Send a request with invalid HMAC signature (should 401)")
    args = parser.parse_args()

    # Trigger A: issue_comment with /execute
    TRIGGER_A = {
        "action": "created",
        "issue": {"number": 73, "title": "Test issue"},
        "comment": {"body": "/execute", "id": 999},
        "repository": {"full_name": "mechanistic-org/global_agent"},
        "sender": {"login": "eriknorris"},
    }

    # Trigger B: projects_v2_item moved to In progress
    TRIGGER_B = {
        "action": "edited",
        "changes": {
            "field_value": {
                "field_name": "Status",
                "to": {"name": "In progress"},
            }
        },
        "projects_v2_item": {"content_node_id": "I_kwDORlq64c711EO_"},
        "repository": {"full_name": "mechanistic-org/global_agent"},
    }

    if args.bad_sig:
        send(TRIGGER_A, "issue_comment", corrupt_sig=True)
    elif args.trigger == "b":
        send(TRIGGER_B, "projects_v2_item")
    else:
        send(TRIGGER_A, "issue_comment")

    # Always also test the health endpoint
    try:
        r = requests.get(DAEMON_URL.replace("/webhook", "/health"), timeout=3)
        print(f"\n/health -> {r.json()}")
    except Exception as e:
        print(f"\n/health check failed: {e}")
