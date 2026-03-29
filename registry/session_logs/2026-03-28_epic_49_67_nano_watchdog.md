---
title: Session Epic 67/49 Decisions
date: '2026-03-28'
context_node: session_close
---

## Decisions
- We explicitly enforced the NanoClaw container boundary by making `ingest_watchdog.py` a completely stateless event listener, rather than building a python monolith script. This isolates the execution layer seamlessly.
- We confirmed the failure protocol works: NanoClaw safely bubbles up Exit Code 1 when the FastMCP router `host.docker.internal` connection fails, and the watchdog successfully abandons the file in the `inbox/` without creating infinite loops or lost data.
- We explicitly pruned 77 redundant UI recipes and persona stubs from the Google Workspace MCP payload, caching only the 18 specific action primitives to maximize the agent's context window.

## Blockers
- None.

## Next
- Moving to Epic #88.