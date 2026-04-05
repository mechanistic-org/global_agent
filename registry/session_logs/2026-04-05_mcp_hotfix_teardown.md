---
title: Session MCP Hotfix Decisions
date: 2026-04-05
context_node: session_close
---
## Decisions
- Fully acknowledged systemic JSON-RPC `invalid character '-' in numeric literal` crashes when executing `push_forensic_doc` over the FastMCP router.
- Enforced protocol exception: Agents will inherently bypass the `push_forensic_doc` tool and use native `write_to_file` exclusively for all forensic telemetry drops until infrastructure repair is complete.

## Next
- Pick up next high-priority ticket from the global sprint board.
