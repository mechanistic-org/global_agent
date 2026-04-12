---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "sync-assets"
description: "The official protocol for syncing local *-assets staging directories to Cloudflare R2 buckets."
version: "2.0.0"

inputs:
  target: "string (e.g., mechanistic, eriknorris, mootmoat, hyphen)"
  flags: "string (e.g., --dry-run or --prune)"
returns: 
  type: "json"
  schema: "file://schemas/skill-returns/sync-assets_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/sync_assets)"
    - "User requests to mirror local media to R2"
  required_context:
    - "Target string matching the bucket map"
  exclusion_criteria:
    - "Do not trigger if target bucket is undeclared in the python script map"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Python script successfully finishes boto3 sync."
  failure_state: "Authentication failure or missing directory."
  max_iterations: 1
  handoff_protocol: "Output sync logs and yield execution."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the R2 Sync:

1. **Safety Verification:** Check if `--dry-run` was requested.
2. **Actuation (Level 3):** Use `run_command` in powershell to run `python scripts/sync_r2.py --target {target} {flags}`.
3. **Termination (T):** Yield execution.
