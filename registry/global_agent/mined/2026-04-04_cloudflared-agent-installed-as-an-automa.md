---
title: Cloudflared agent installed as an automatic Windows service via `setup_ingress.ps1`.
date: 2026-04-04
context_node: conversation_miner
---

The `setup_ingress.ps1` script is now responsible for registering `cloudflared.exe` as a native Windows system service, configured for automatic startup. This ensures the Cloudflare agent is always active and bound to the correct tunnel token, providing persistent ingress.