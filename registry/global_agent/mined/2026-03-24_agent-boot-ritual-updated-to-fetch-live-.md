---
title: Agent boot ritual updated to fetch live sprint board data directly.
date: 2026-03-24
context_node: conversation_miner
---

The agent's boot ritual (`session_open.md`) is being updated to remove references to old static sprint plans. Instead, it will directly execute `sprint_board.py` to fetch and display the live GitHub sprint board status at the start of every session, providing immediate, actionable scope and ensuring agents are always up-to-date.