---
title: Actionable Pydantic validation error strings enable agents to self-correct and retry without human intervention.
date: 2026-03-22
context_node: conversation_miner
---

Pydantic `ValidationError` messages are now returned as actionable strings, rather than raising exceptions. This design allows agents to read field-level errors, self-correct their `frontmatter_dict`, and retry the operation without requiring human intervention, significantly improving agent autonomy.