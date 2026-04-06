---
title: Session global_agent#75 Decisions
date: '2026-04-05'
context_node: session_close
---

## Decisions
- Bypassed network FastMCP loop for direct Python `os.write` and `chroma.upsert` persistence of matrices to ensure tight project-silo routing without ChromaDB SQLite lock collisions.
- Delegated semantic extraction exclusively to the local AI model (for mapping narrative features to failures), while completely overriding arithmetical AI RPN hallucination using fixed Python variables for true engineering determinism.

## Blockers
- None

## Next:
- PRD Linter / Scaffolding Engine Implementation (Epic #110 / Issue #74)