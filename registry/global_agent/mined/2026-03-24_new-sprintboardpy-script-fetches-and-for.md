---
title: New `sprint_board.py` script fetches and formats live GitHub sprint data for agents.
date: 2026-03-24
context_node: conversation_miner
---

A new Python script, `global_agent/scripts/sprint_board.py`, is being developed to query the GitHub GraphQL API directly for Project #5. This script will automatically identify the current iteration, filter tasks, sort by priority, and provide clean terminal output for agents, ensuring real-time, actionable scope at the start of a session.