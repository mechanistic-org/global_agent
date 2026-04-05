---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "create-issue"
description: "Create a new GitHub issue AND wire it fully to the global project board in one operation."
version: "2.0.0"

inputs:
  title: "string"
  body: "string"
  metadata: "object containing Iteration, Priority, Size, Node, Impact, Status"
returns: 
  type: "json"
  schema: "file://assets/create_issue_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/create_issue)"
    - "Agent natively decides an issue must be generated from triage"
  required_context:
    - "Valid title and structured markdown body"
  exclusion_criteria:
    - "Do not trigger if body is empty or lacks clear definition of done (DoD)"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "GitHub Issue created, attached to global Project Board, and all 5 GraphQL nodes correctly set."
  failure_state: "GitHub CLI or authentication failure."
  max_iterations: 1
  handoff_protocol: "Output the final Project Item ID and Issue URL."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the native Project wiring:

1. **Issue Creation (Level 3):** Run `gh issue create` with the required repo, title, labels. Never skip metadata. Title + body alone is noise. Iteration + Node = signal.
2. **Project Wiring (Level 3):** 
   *   Run `gh project item-add 5 --owner mechanistic-org --url {ISSUE_URL} --format json` to get the `$ITEM_ID`.
   *   Set Iteration (`--field-id PVTIF_lADOEA3Ajc4BSLlfzg_ynvU`)
   *   Set Priority (`--field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI`)
   *   Set Size (`--field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM`)
   *   Set Node (`--field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY`)
   *   Set Impact (`--field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc`)
3. **Termination (T):** Emit the created URL and yield.
