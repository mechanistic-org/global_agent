# EN-OS Daemon Operations Guide
> Ticket: [#73 — Always-On Router: Cloudflare Tunnel + FastAPI Webhook Daemon](https://github.com/mechanistic-org/global_agent/issues/73)

## Overview

Two processes must run locally for the Event Bridge to be active:

| Process | Command | Port |
|---------|---------|------|
| Webhook Daemon | `uvicorn scripts.webhook_daemon:app --host 127.0.0.1 --port 8001` | 8001 |
| Cloudflare Tunnel | `cloudflared tunnel run enos-webhook` | (external) |

---

## Phase 1: One-Time Setup

### 1. Install cloudflared

```powershell
winget install Cloudflare.cloudflared
# Verify:
cloudflared --version
```

### 2. Authenticate with Cloudflare

```powershell
cloudflared tunnel login
# Opens browser → log into your Cloudflare account → authorize mechanistic.com
```

### 3. Create the tunnel

```powershell
cloudflared tunnel create enos-webhook
# Output:
#   Created tunnel enos-webhook with id <UUID>
#   Credentials written to C:\Users\erik\.cloudflared\<UUID>.json
```

### 4. Update the config file

Open `.cloudflared/config.yml` and replace `<TUNNEL_UUID>` with the UUID from step 3.

### 5. Add CNAME in Cloudflare DNS

Go to: **Cloudflare Dashboard → mechanistic.com → DNS Records → Add record**

| Field | Value |
|-------|-------|
| Type | CNAME |
| Name | `hooks` |
| Target | `<UUID>.cfargotunnel.com` |
| Proxy | DNS only (grey cloud — do NOT orange-cloud a tunnel) |

---

## Phase 2: Configure GitHub Webhook

Go to: **https://github.com/mechanistic-org/global_agent/settings/hooks → Add webhook**

| Field | Value |
|-------|-------|
| Payload URL | `https://hooks.mechanistic.com/webhook` |
| Content type | `application/json` |
| Secret | *(set this value — copy it to `.env` as `GITHUB_WEBHOOK_SECRET`)* |
| Events | `Issue comments`, `Projects v2 items` (or "Send me everything" for testing) |
| Active | ✅ |

---

## Phase 3: Daily Start Sequence

```powershell
# Terminal 1 — Webhook Daemon
cd D:\GitHub\global_agent
uvicorn scripts.webhook_daemon:app --host 127.0.0.1 --port 8001

# Terminal 2 — Cloudflare Tunnel
cloudflared tunnel run enos-webhook
```

Health check:
```powershell
curl http://localhost:8001/health
# {"status":"online","nanoclaw_enabled":false,"timestamp":"..."}
```

---

## Phase 4: Local Smoke Test (no tunnel needed)

```powershell
# Trigger A: /execute comment (should 202)
python scripts/test_webhook.py

# Trigger B: Project V2 move (should 202)
python scripts/test_webhook.py --trigger b

# Bad signature test (should 401)
python scripts/test_webhook.py --bad-sig
```

---

## Phase 5: Arm NanoClaw (after #61 is built)

When `nanoclaw:latest` Docker image is built:

1. Add to `.env`: `NANOCLAW_ENABLED=true`
2. Restart the daemon
3. Trigger A live test: post a comment `/execute` on any open issue in `mechanistic-org/global_agent`
4. Confirm in **repo Settings → Webhooks → Recent Deliveries** that GitHub shows a green `202`
5. Confirm `registry/global_agent/daemon_audit.log` shows `IGNITION:` log line

---

## Operational Notes

- **The daemon never waits for the container.** It validates, fires `Popen`, and returns `202` in milliseconds. GitHub's 10-second timeout will never be hit.
- **Project V2 Trigger B:** GitHub's `projects_v2_item` payload does not include issue number directly. After the first live test, inspect `daemon_audit.log` for the `content_node_id` and run `gh api graphql -f query='{ node(id: "...") { ... on Issue { number } } }'` to verify the traversal path.
- **Audit log:** `registry/global_agent/daemon_audit.log` — append-only. Commit periodically or add to `.gitignore` if volume gets high.
- **Port 8001:** FastMCP SSE Router runs on 8000. The webhook daemon runs on 8001. Never bind to 0.0.0.0 — tunnel handles external routing.
