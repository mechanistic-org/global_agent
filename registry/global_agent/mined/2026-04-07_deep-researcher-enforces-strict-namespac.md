---
title: Deep Researcher enforces strict namespace isolation by tagging ChromaDB vectors with explicit project metadata.
date: 2026-04-07
context_node: conversation_miner
---

The Deep Research Engine implements a strict namespace strategy for data provenance and integrity. It deterministically dumps formatted markdown into `registry/[project]/assets/[pdf_name].md` and immediately maps the vectors into ChromaDB using explicit `{"project": "[namespace]"}` metadata, ensuring no cross-project data pollution.