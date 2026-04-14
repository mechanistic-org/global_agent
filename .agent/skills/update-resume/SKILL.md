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
  success_state: "resume_master.ts updated with operator LGTM received, headless PDF generated, and R2 script uploads successfully."
  failure_state: "Headless browser crash, LINKEDIN_READY.txt absent, or operator does not confirm synthesis draft."
  max_iterations: 1
  handoff_protocol: "Output completion and link to live URL."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the Resume Pipeline:

0. **Pre-flight Gate (HALT if failed):** Before any synthesis, verify that `LINKEDIN_READY.txt`
   exists in the portfolio repo root. If it does not exist, HALT immediately and output:
   "HALT: LINKEDIN_READY.txt not found. This file must be operator-written and reviewed before
   the update-resume skill can run. Do not substitute linkedin_master.ts alone. Create
   LINKEDIN_READY.txt with the curated content you want injected, then re-invoke this skill."
   Do NOT create LINKEDIN_READY.txt yourself. Do NOT proceed with linkedin_master.ts as a
   substitute. LINKEDIN_READY.txt is a formal staging artifact - its absence is a hard stop.

   Then, output a pre-flight summary for operator review:
   - Which sections of `resume_master.ts` will be modified and why
   - The specific source material being ingested from `LINKEDIN_READY.txt`
   - Any ambiguities or data gaps that will require a judgment call

1. **Synthesis Draft (Level 2 - Data Migration, HALT before write):** Read
   `src/config/linkedin_master.ts` and `LINKEDIN_READY.txt`. Synthesize new data into standard
   engineering impact bullets: action verb + specific technical problem + measurable outcome.
   Do not use bold drama headers (e.g., "The Trigger:", "The Intervention:", "The Result:"),
   incident-report structure, or Trigger/Intervention/Result framing. Specificity of mechanism
   is the credential - not dramatic structure. *DO NOT GUESS IMAGINARY DATA.*

   Output the full synthesis draft to the operator for review. Then HALT and wait for explicit
   operator LGTM before writing any file. The exact phrase required is "LGTM" or "confirmed" or
   "proceed". Any ambiguous response must be treated as a HALT - re-ask for confirmation.
   Do not interpret silence or continuation of conversation as approval.

2. **File Write (after LGTM only):** Inject the approved bullets into `src/config/resume_master.ts`
   using `multi_replace_file_content`. Only after receiving explicit operator confirmation from
   Step 1.

3. **PDF Actuation (Level 3 - Headless):** Use `run_command` to execute:
   `node scripts/generate_resume_pdf.cjs`. This spins up an isolated server and prints the PDF
   to `public/assets/resume/Erik_Norris_Resume_Current.pdf`.

4. **Cloudflare Deploy Actuation (Level 3 - Hotfix):** Use `run_command` to hot-swap the PDF
   directly to R2: `python scripts/upload_resume_hotfix.py`.

5. **Termination (T):** Notify the user with: "Update complete. Please verify the deployed resume
   at https://resume.eriknorris.com."
