---
title: Cloudflared Tunnel Residency Migration
date: '2026-04-04'
context_node: global_agent/infrastructure
---

# Cloudflared Tunnel Residency Migration

## Context
As part of Epic #99 (Circuit Breakers), we identified a single point of failure in the `enos-webhook` ingress: it was managed as an ephemeral process via PM2. This caused silent offline states upon system reboots or PM2 daemon crashes.

## Implementation
The tunnel has been migrated to a native Windows Service for maximum persistence.

### Actions Taken
1.  **Deresualization:** Removed `enos-ingress-tunnel` from PM2 management.
2.  **Configuration Lock:** Modified `ecosystem.config.js` to comment out the tunnel application block.
3.  **Service Binding:** Registered `cloudflared.exe` as a system service named `Cloudflared` (Display Name: `Cloudflared agent`).
4.  **Token Persistence:** The service is configured to run with the following command line:
    `"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel run --token <VERIFIED_TOKEN>`

## Verification
- **Service Name:** `Cloudflared`
- **Status:** `RUNNING`
- **Start Type:** `AUTO_START`
- **Endpoint:** `https://hooks.mechanistic.com/health` returns `200 OK` with daemon heartbeat.

## Outcome
The EN-OS ingress is now system-resilient. It will boot automatically with the host OS, independent of the PM2 process tree.
