import hmac
import hashlib
import urllib.request
import json
import time

SECRET = b"4ed0d1fc8c91ceec8daa9bb1dda62944f08f7396fc452b2aaf245a41e24fd1c6"
URL = "http://127.0.0.1:8001/webhook"

def send_mock(event_type, payload):
    body = json.dumps(payload).encode("utf-8")
    signature = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json",
        "x-github-event": event_type,
        "x-hub-signature-256": signature
    })
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[{event_type}] SUCCESS: {resp.read().decode('utf-8')}")
    except Exception as e:
        print(f"[{event_type}] ERROR: {e}")

print("Sending PLAN Trigger (Project Board: In progress)...")
payload_plan = {
    "action": "edited",
    "projects_v2_item": {"content_node_id": "PVTI_lADOEA3Ajc4BSLlfzgK9S6M"},
    "changes": {"field_value": {"field_name": "Status", "to": {"name": "In progress"}}},
    "repository": {"full_name": "mechanistic-org/global_agent"}
}
send_mock("projects_v2_item", payload_plan)

time.sleep(2)

print("Sending EXEC Trigger (Comment /execute)...")
payload_exec = {
    "action": "created",
    "issue": {"number": 103},
    "comment": {"body": "/execute please"},
    "repository": {"full_name": "mechanistic-org/global_agent"}
}
send_mock("issue_comment", payload_exec)
