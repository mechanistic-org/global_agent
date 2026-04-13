---
title: "Project-specific scripts were retained in `portfolio` due to strict data structure dependencies, avoiding unnecessary coupling."
date: 2026-04-04
context_node: conversation_miner
---

During the script centralization, project-specific domain scripts such as `audit_keystatic_compliance.py`, `check_schema_parity.py`, and `harvest_linkedin.py` were intentionally retained within the `portfolio` repository. This decision was made due to their strict dependencies on `portfolio`'s unique data structures, preventing unnecessary coupling with `global_agent` and maintaining project integrity.