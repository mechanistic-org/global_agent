---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "scaffold-project"
description: "Scaffold a new project entry using the production-grade C24 career matrix schema."
version: "2.0.0"

inputs:
  slug: "string (snake_case)"
  title: "string"
  employer: "string"
returns: 
  type: "json"
  schema: "file://schemas/skill-returns/scaffold-project_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/scaffold_project)"
  required_context:
    - "Slug, Title, and Employer parameters"
  exclusion_criteria:
    - "Do not trigger if project slug already exists"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Directory created, strict C24 index.mdx is saved on disk, and R2 asset path verified."
  failure_state: "Filesystem lock or schema validation failure."
  max_iterations: 1
  handoff_protocol: "Notify user the shell is ready and exit."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the C24 Scaffolding:

1. **Parameter Prompting:** If inputs are missing, ask the user for `slug` (snake_case), `title`, and `employer`.
2. **Directory Actuation (Level 3):** Use `run_command` or native tools to create `src/content/projects/{slug}`.
3. **Schema Actuation (Level 3):** Run `write_to_file` on `src/content/projects/{slug}/index.mdx` using the exact layout defined in the C24 master schema (including metrics, financial, cyberspace layout, phase_stats, and Isomorphic Proofs stubs). Ensure the `heroImage` links to `/assets/r2/{slug}/hero.webp`.
4. **Sovereignty Verification (Level 3):** Use local tools to check if `d:\GitHub\portfolio-assets\R2_STAGING\{slug}` exists. If it does not exist, explicitly warn the user to create the folder and symlink the assets according to strict Sovereignty Rules.
5. **Termination (T):** Yield execution.
