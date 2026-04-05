---
title: Session Hotfix: MCP JSON RPC SQLite Lock Patch
date: 2026-04-04
context_node: session_close
---

## Decisions
- Attempted to patch `push_forensic_doc` via `mcp_registry_server.py` to prevent SQLite locks from bubbling out during ChromaDB upsert.
- Discovered upon re-running the MCP tool that the `invalid character '-' in numeric literal` crash persists. This isolates the failure to the underlying `FastMCP` / `Uvicorn` HTTP communication layer (likely Uvicorn default logging or FastMCP strict JSON Pydantic translation bounds breaking the GO SSE parser) rather than just an uncaught SQLite locking trace.

## Next
- Pick up next priority sprint task. (Agent must abandon using `push_forensic_doc` over MCP for now and exclusively write flat `.md` files via `write_to_file` during this sprint until the Python SSE dependency layer is fundamentally rewritten or resolved.)
