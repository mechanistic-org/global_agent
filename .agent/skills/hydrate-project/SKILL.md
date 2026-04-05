---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "hydrate-project"
description: "The official protocol for enriching project files using the 'Three Vector' Mining Campaign via Python scripts."
version: "2.0.0"

inputs:
  slug: "string (Project identifier linking to notebook_dumps/)"
returns: 
  type: "json"
  schema: "file://assets/hydration_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/hydrate_project)"
    - "User requests to 'titrate' or 'hydrate' a project"
  required_context:
    - "Valid slug parameter"
    - "Raw NotebookLM dumps exist in appropriate directories"
  exclusion_criteria:
    - "Do not trigger if raw dumps are missing, or if project is strictly Tier 1/2 manual lock"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "index.mdx hydrated and MINING_LOG updated."
  failure_state: "Python script exception."
  max_iterations: 1
  handoff_protocol: "Confirm execution, warn user to avoid touching AGENCY_MEMORY.md, and yield."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the Hydration Pipeline:

1. **Parameter Verification:** Read the `slug`. Check that `notebook_dumps/{slug}.txt` or `.md` exists.
2. **Actuation (Level 3):** 
   *    *Critical Check:* Do NOT manually edit body text or JSON metadata. 
   *    Use `run_command` to execute: `python scripts/hydrate_content.py --slug {slug} --force`.
   *    This utilizes `smart_merge_lists` under the hood.
3. **Verification (Level 2):** Read the final `index.mdx` file to verify the "Forensic Report" header is present. Ensure no 404 errors by matching the R2 Virtual Bridge constraints.
4. **Log Actuation (Level 3):** Use `replace_file_content` or `write_to_file` to update `src/content/docs/project/MINING_LOG.md`, setting the status for the project to 🟢. Do NOT update `AGENCY_MEMORY.md`.
5. **Termination (T):** Yield execution to the user.
