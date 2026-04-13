---
title: "Identified potential ChromaDB concurrency issues between `enos_router` and `mine_session.py`, suggesting SSE for inter-process communication."
date: 2026-03-28
context_node: conversation_miner
---

A potential concurrency issue was identified where the `enos_router` daemon, running via PM2, might hold an active lock on `.chroma_db`. This could lead to 'database is locked' errors if `mine_session.py` attempts concurrent access, highlighting a need for `mine_session.py` to communicate via SSE as an MCP client for robust inter-process interaction.