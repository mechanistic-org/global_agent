---
title: Session Feature Acquisition Decisions
date: '2026-04-05'
context_node: session_close
---

## Decisions
- Decided to adopt Karpathy's LLM-wiki `log.md` and `index.md` architecture to enhance deterministic context retrieval.
- Decided to adopt DocMason's explicit provenance mapping by enforcing `sources: []` tracking in markdown frontmatter.
- Decided to formally expand asset ingestion by creating a new MCP pipeline for OTF conversion of PDFs, Word, and Spreadsheets.

## Blockers
- None

## Next
- Prioritization and execution of tickets #113, #114, #115, and #116 in the upcoming sprint.