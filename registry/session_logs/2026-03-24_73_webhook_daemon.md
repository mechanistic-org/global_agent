---
title: Session 73 Decisions
date: '2026-03-24'
context_node: session_close
---

## Decisions
- hooks.mechanistic.com chosen (not os.mechanistic.com) — generic, path-routable
- Port 8001 for daemon; 8000 = FastMCP SSE
- NANOCLAW_ENABLED=false default; arms after #61
- dotenv CWD trap in PS jobs: pass GITHUB_WEBHOOK_SECRET as explicit env var
- projects_v2_item is org-level only; Trigger B deferred
- filter-repo cleaned venv/ torch DLLs from 14 unpushed commits
- SentenceTransformer removed from mcp_registry_server.py (was 30s+ cold start)

## Blockers
- NanoClaw arming blocked on #61
- Trigger B requires org-level webhook

## Next
#74 mcp_prd_linter or #75 mcp_fmea_generator — both fully spec from walk notes. Or #80 publish_post.
