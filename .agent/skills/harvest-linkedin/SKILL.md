---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "harvest-linkedin"
description: "Harvest project data and compile the master LINKEDIN_READY.txt artifact for social publishing."
version: "2.0.0"

inputs:
  none: "boolean"
returns: 
  type: "json"
  schema: "file://assets/linkedin_harvest_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/harvest_linkedin)"
    - "User has just completed a project MDX refactor or updated the linkedin_master.ts file"
  required_context:
    - "Target workspace must contain src/content/projects/"
  exclusion_criteria:
    - "Do not trigger if the master TypeScript file was not recently edited or requested to be pulled"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "LINKEDIN_READY.txt successfully built."
  failure_state: "Python script exception."
  max_iterations: 1
  handoff_protocol: "Notify the user the harvest is complete and output the path."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the LinkedIn compiler:

1. **Pre-Check (C):** Verify `linkedin_master.ts` is up-to-date. If the user explicitly requested data updates, ensure they are written.
2. **Harvest Actuation (Level 3):** Use `run_command` to execute the local compiler script: `python scripts/harvest_linkedin.py`.
   *   *Note:* The script automatically extracts YAML blocks from `index.mdx` files and appends them to the master structure.
3. **Verification (Level 3):** Use `view_file` to read `src/content/prompts/LINKEDIN_READY.txt` to mathematically prove the build succeeded.
4. **Termination (T):** Output the exact file path and yield control back to the operator for manual copy-pasting into the LinkedIn frontend.
