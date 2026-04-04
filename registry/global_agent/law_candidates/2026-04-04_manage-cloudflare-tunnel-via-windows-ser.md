# LAW CANDIDATE — 2026-04-04

**Rule:** Manage Cloudflare tunnel via Windows Service Control Manager, not PM2.

The Cloudflare ingress tunnel is now exclusively managed by the Windows Service Control Manager (`services.msc` or `sc.exe`). Agents must no longer attempt to manage or monitor the `enos-ingress-tunnel` via PM2, as it has been removed from PM2's process list.

**Tags:** pm2, windows-service, operations, tooling, rule
