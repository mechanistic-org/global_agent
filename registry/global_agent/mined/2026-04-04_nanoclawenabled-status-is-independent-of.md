---
title: `nanoclaw_enabled` status is independent of Cloudflare tunnel connectivity.
date: 2026-04-04
context_node: conversation_miner
---

It was clarified that the `nanoclaw_enabled` status, observed in the health endpoint response, is controlled by the `.env` file and is entirely unrelated to the operational status or connectivity of the Cloudflare ingress tunnel. This distinction is important for debugging and configuration understanding.