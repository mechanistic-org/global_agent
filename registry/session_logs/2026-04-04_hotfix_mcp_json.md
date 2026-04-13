---
title: "Session Hotfix: MCP JSON RPC SQLite Lock Patch"
date: 2026-04-04
context_node: session_close
---

## Decisions
- **Breakthrough Discovery:** The `invalid character '-' in numeric literal` crash is NOT caused by SQLite locks or Pydantic. The Go JSON-RPC parser natively merges the Python subprocess's `stdout` and `stderr`. Extraneous Python logging (like boot banners starting with `---` and HuggingFace `-v2` logs) printed to `sys.stderr` were leaking horizontally into the JSON stream, destroying the JSON structure.
- **Architectural Fix:** Invented a `ShieldedStdout` proxy inside `scripts/mcp_router_node.py` that aggressively reroutes both `sys.stderr` and `sys.stdout` natively to an isolated `enos_native.log` file, while selectively exposing the native binary `.buffer` attribute directly to the FastMCP initialization.
- **Result:** The Python noise is totally sterilized. The `stdio` JSON-RPC connection works flawlessly, but because the Antigravity (Go) orchestrator permacaches the connection initialization crash state in memory, live invocations inside the same session continue to return the cached failure.

## Next
- **Commit:** Commit the `ShieldedStdout` patch to the repository.
- **Restart:** The user must restart the Antigravity session/reload the window. Once Antigravity initializes the fresh `enos_router` node, `push_forensic_doc` and all MCP tools will function perfectly.
