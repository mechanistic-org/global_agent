---
title: The FastMCP router must be actively listening at `http://host.docker.internal:8000/sse` for NanoClaw ingestion.
date: 2026-04-07
context_node: conversation_miner
---

The FastMCP router is an essential architectural dependency for the NanoClaw ingestion pipeline. It must be actively listening at `http://host.docker.internal:8000/sse` to facilitate proper communication and data streaming required for the ingestion process to function correctly.