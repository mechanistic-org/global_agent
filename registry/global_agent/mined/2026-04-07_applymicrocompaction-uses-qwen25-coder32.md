---
title: "`apply_microcompaction` uses `qwen2.5-coder:32b` to compress payloads over 8000 characters, integrated into `semantic_search` and `read_forensic_doc`."
date: 2026-04-07
context_node: conversation_miner
---

The `mcp_registry_server.py` utilizes `apply_microcompaction()` to intercept and compress payloads exceeding 8000 characters. This process leverages the `qwen2.5-coder:32b` model and is integrated into both `semantic_search` and `read_forensic_doc` functions, ensuring efficient handling of large context inputs.