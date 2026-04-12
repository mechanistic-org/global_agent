---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "run-mining-campaign"
description: "Automated workflow for orchestrating a NotebookLM Mining Campaign via the MCP CLI to bypass browser UI interactions."
version: "2.0.0"

inputs:
  notebook_name: "string"
returns: 
  type: "json"
  schema: "file://schemas/skill-returns/run-mining-campaign_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/run_mining_campaign)"
  required_context:
    - "Notebook name provided by user"
  exclusion_criteria:
    - "Do not trigger if nlm.exe is missing from the environment"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Python orchestration script completes without crash, payloads deposited into _raw_nlm."
  failure_state: "NLM CLI error or unauthenticated."
  max_iterations: 1
  handoff_protocol: "Output confirmation of downloaded payloads and yield execution to the Hydration workflow."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the automated NLM extraction:

1. **Connection Verification (Level 3 Actuation):** Formulate a test query `nlm.exe query "Hello" --notebook {NOTEBOOK_NAME}`. Read the notebook ID from the metadata.
2. **Orchestration Generation (Level 2):** Create a robust `run_campaign.py` script. Do NOT pass multi-line prompts via powershell arguments (to avoid whitespace escaping bugs). Instead, instruct `python` to read from the target `public\assets\prompts\...` files and write to `src\content\_raw_nlm\...` natively via the `subprocess` module targeting `nlm.exe`.
3. **Execution (Level 3 Actuation):** Run the generated `run_campaign.py`. This will sequentially call NotebookLM for Bolus, Report, Vignettes, Team, BOM, and Timeline payloads and save the JSON/MD files locally.
4. **Context Smell Handoff (Level 2):** Pause and allow the user to provide any manual ad-hoc queries based on the run. Wait for input.
5. **Audio Generation (Level 3 Actuation):** Append or run a python script to trigger the `PODCAST_NLM-INPUT.txt` audio briefing using the native NLM CLI's async `studio status` checks. Guarantee the `.m4a` file is saved to `R2_STAGING/[SLUG]` securely without clobbering hand-made assets.
6. **Termination (T):** Handoff flow instantly to the `/hydrate_project` skill.
