---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "evidence-extraction"
description: "Extract agent evidence (e.g., .webp recordings), push to R2 Asset Sovereignty, format live URLs, and close GitHub Issues autonomously."
version: "2.0.0"

inputs:
  issue_number: "string (GitHub Issue ID)"
  recordings: "array of strings (paths to local .webp files)"
returns: 
  type: "json"
  schema: "file://schemas/skill-returns/evidence-extraction_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/evidence-extraction)"
    - "Agent successfully completes a systemic/visual browser verification task"
  required_context:
    - "Local .webp forensics existing in the .gemini/brain directory"
    - "Active tracking issue number against the repository"
  exclusion_criteria:
    - "Do not trigger if the verification task failed or crashed"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Image moved to R2 proxy context, walkthrough updated with live URL, and GitHub issue securely closed with comment."
  failure_state: "R2 staging directory missing, or GitHub CLI returns error."
  max_iterations: 1
  handoff_protocol: "Output the Live Asset URL and Issue Closure confirmation."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the R2 Bridge & closure loop:

1. **Extraction Actuation (Level 3):** Use `run_command` in powershell to `Move-Item` the `.webp` recordings out of the local OS agent directory (`.gemini/brain/...`) directly into `D:\GitHub\portfolio-assets\R2_STAGING\forensics\`.
2. **Metadata Formulation:** Mentally calculate the final MootMoat R2 live proxy URL (format: `https://assets.eriknorris.com/forensics/[filename].webp`).
3. **Artifact Restructuring:** Modify the local `walkthrough.md` to cleanly embed the *Live URL* rather than the local `C:\` drive path.
4. **Issue Appending & Closure Actuation (Level 3):** 
   *   *Anti-Ghost Action:* Do not just leave the markdown file locally. You MUST use the `run_command` native `gh` cli or `mcp_github` tools to publish the exact contents of `walkthrough.md` as the final comment on the target GitHub Issue.
   *   Execute the closure action on the GitHub Issue.
5. **Termination (T):** Yield execution.
