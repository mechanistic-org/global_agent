---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "deploy-production"
description: "Build, Commit, and Push to Main (Triggering Cloudflare)."
version: "2.0.0"

inputs:
  commit_message: "string"
returns: 
  type: "json"
  schema: "file://assets/deploy_production_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/deploy_production)"
    - "User explicitly asks to push to main or deploy"
  required_context:
    - "Uncommitted changes or commits waiting to push"
  exclusion_criteria:
    - "Do not trigger if npm run build fails locally"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Git push reaches remote origin without error."
  failure_state: "Build failure or merge conflict."
  max_iterations: 1
  handoff_protocol: "Output success and link to production site."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the deployment safely:

1. **Safety Protocol (Level 3):** Run `git status`. Run `npm run build` to mathematically prove the site compiles. *If this fails, STOP.*
2. **Git Commit (Level 3):** `git add .` and `git commit -m "{message}"` (Use default "chore: content update" if not specified).
3. **Git Push (Level 3):** `git push origin main`.
4. **Termination (T):** Yield with: "Pushed to main. Cloudflare Pages build triggered. Remind user to check https://eriknorris.com in 2 minutes."
