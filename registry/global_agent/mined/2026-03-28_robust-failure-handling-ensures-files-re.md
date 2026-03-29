---
title: Robust failure handling ensures files remain in `inbox/` for review upon ingestion errors, preventing data loss.
date: 2026-03-28
context_node: conversation_miner
---

The `ingest_watchdog.py` daemon incorporates robust failure handling to prevent data loss. If the NanoClaw container exits with a non-zero status code (e.g., Code 1), the watchdog observes this failure, emits a `logger.error()`, and crucially abandons the standard archiving process. This design ensures that problematic files remain in the `inbox/` for human review, preventing silent failures and maintaining data integrity.