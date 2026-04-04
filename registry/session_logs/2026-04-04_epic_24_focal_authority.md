---
title: "Session Epic 24 Decisions"
date: "2026-04-04"
context_node: "session_close"
---
## Decisions
- Formally recognized the structural danger of probabilistic LLM behavior spanning across multiple tickets within the context of automated headless workers (NanoClaw).
- Established the **Focal Ticket Authority** rule (1 Session = 1 Issue).
- Drafted `.agent/rules/ticket_closure.md` to officially prevent the agent from silently resolving and auto-closing collateral tickets without express human permission.
- Bound the `/session_close` workflow to this constraint using a strict warning modifier.
- Closed Portfolio #24 as a collateral satisfaction of #23's engineering output.

## Blockers
- The native `enos_router` MCP endpoint remains unstable (JSON parser / `-` numeric character crash), rendering ChromaDB push/search functions volatile, and forcing local `gh` / text pipeline fallbacks.

## Next
- Fix the `enos_router` environment dependencies, or return to resolving `hyphen#7` (Cloudflare Access for the EN-OS universal dashboard).
