---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "update-resume"
description: "The pipeline for transferring updated narrative data into the Master Resume, generating the PDF, and deploying it."
version: "2.0.0"

inputs:
  none: "boolean"
returns: 
  type: "json"
  schema: "file://schemas/skill-returns/update-resume_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/update_resume)"
    - "User prompts to update resume to reflect new LinkedIn or Portfolio data"
  required_context:
    - "User intent to rebuild PDF"
  exclusion_criteria:
    - "Do not trigger for simple typo fixes without user instruction to deploy"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "resume_master.ts updated, headless PDF generated, and R2 script uploads successfully."
  failure_state: "Headless browser crash."
  max_iterations: 1
  handoff_protocol: "Output completion and link to live URL."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the Resume Pipeline:

1. **Synthesis (Level 2 - Data Migration):** If updating content, read `src/config/linkedin_master.ts` and `LINKEDIN_READY.txt`. Synthesize new data into standard engineering impact bullets: action verb + specific technical problem + measurable outcome. Do not use bold drama headers (e.g., "The Trigger:", "The Intervention:", "The Result:"), incident-report structure, or Trigger/Intervention/Result framing. Specificity of mechanism is the credential - not dramatic structure. Inject the new bullets into `src/config/resume_master.ts` using `multi_replace_file_content`. *DO NOT GUESS IMAGINARY DATA.* Wait for user review if ambiguous.
2. **PDF Actuation (Level 3 - Headless):** Use `run_command` to execute: `node scripts/generate_resume_pdf.cjs`. This spins up an isolated server and prints the PDF to `public/assets/resume/Erik_Norris_Resume_Current.pdf`.
3. **Cloudflare Deploy Actuation (Level 3 - Hotfix):** Use `run_command` to hot-swap the PDF directly to R2: `python scripts/upload_resume_hotfix.py`.
4. **Termination (T):** Notify the user with: "Update complete. Please verify the deployed resume at https://resume.eriknorris.com."
