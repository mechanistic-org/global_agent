---
title: LLMs are dynamically informed of previous crashes via prompt injection to optimize recovery efficiency.
date: 2026-04-07
context_node: conversation_miner
---

A critical design decision for Crash Resurrection is the injection of a specific warning string into the LLM's payload prompt. This ensures the model is dynamically aware that it's continuing a failed run, allowing it to execute tasks efficiently and avoid repeating timeout failures, thereby optimizing recovery.