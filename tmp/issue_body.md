## Context
The sovereign system requires a dedicated "Single Pane of Glass" to monitor infrastructure, deployment states, and financial constraints. Past references confused this with conceptual portfolio/notion-clone concepts. This Epic exists distinctly for the EN-OS operational dashboard.

## Scope & Components
- **Infrastructure Monitoring:** Unified UI overlaying both PM2 node daemons and native Windows Services (e.g., Cloudflared ingress).
- **Telemetry & Cost Ledger:** Real-time extraction and graphing of `.system_generated/logs/token_ledger.json` to monitor the Active Agentic Engineering burn rate across Fast/Frontier models.
- **Fail Loop & Limit Switch Triggers:** Dead-man's switch visualization for when the `global_agent` encounters a wall-clock break, daily token limit, or loop-detection halt.
- **Dark Hangar Aesthetic:** Strict adherence to `law_002_design_system.md` (Dark Hangar) across the UI layer.

## DoD
- [ ] Bootstrap new EN-OS Dashboard UI shell.
- [ ] Connect dashboard to local PM2/Service APIs.
- [ ] Connect dashboard to `.system_generated/logs/token_ledger.json`.
- [ ] Implement "Dead Man's Switch" visual alerts for agent halts.
