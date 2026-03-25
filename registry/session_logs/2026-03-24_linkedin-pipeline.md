---
title: "Session 2026-03-24 LinkedIn Pipeline Execution Decisions"
date: "2026-03-24"
context_node: "session_close"
---

## Decisions

- **Pipeline Over API:** Actively rejected writing API connectors for LinkedIn OAuth. EN-OS relies on Git as the state substrate, so `linkedin_tracker.py` was built to operate exclusively on the local Keystatic frontmatter.
- **Workflow Orchestration:** Created `/draft_linkedin_post` and `/publish_post` to strictly constrain the creation and mutation of posts, guaranteeing self-comments are attached.
- **Extraction Overload:** Extracted raw LinkedIn drafts that were initially buried in the intelligence read-out files and correctly deposited them into `registry/linkedin/drafts/`.
- **Thread Scaling:** Deprecated the `trilogy_` thread naming convention. Implemented `arc_001` ledger to scale indefinitely without hard limits, refactoring all existing `posted/` markdown artifacts in the process.

## Blockers

- ⚠️ SQLite WAL locking still affects ChromaDB teardown processes. Logged as Epic 0 unblocker.

## Next: Execute **Issue #82: [Fix] Resolve ChromaDB SQLite locking hangs in session_close**
