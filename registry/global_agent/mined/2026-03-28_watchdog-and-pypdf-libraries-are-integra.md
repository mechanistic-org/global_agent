---
title: `watchdog` and `pypdf` libraries are integrated for robust filesystem monitoring and PDF text extraction.
date: 2026-03-28
context_node: conversation_miner
---

The `requirements.txt` has been updated to include two critical libraries: `watchdog` and `pypdf`. The `watchdog` library enables cross-platform background filesystem event monitoring, which is fundamental for the `ingest_watchdog.py` daemon's ability to detect new files. `pypdf` facilitates local text extraction from PDF assets, a key capability for processing diverse input types.