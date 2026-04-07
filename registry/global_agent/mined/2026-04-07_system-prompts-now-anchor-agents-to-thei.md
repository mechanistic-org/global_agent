---
title: System prompts now anchor agents to their 'plan' or 'exec' mode privilege scope.
date: 2026-04-07
context_node: conversation_miner
---

Specific boundary statements were enforced in system prompts for `run_agent.py` to anchor language models to their privilege scope. In 'plan' mode, agents are directed to await `/execute` approval, while in 'exec' mode, they are explicitly notified of authorized spawning, preventing context window drift and unauthorized actions.