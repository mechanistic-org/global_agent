---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "publish-post"
description: "The official ritual for moving a drafted LinkedIn post to published status, syncing OS file states with the public feed."
version: "2.0.0"

inputs:
  filename: "string (The target markdown file base name)"
returns: 
  type: "json"
  schema: "file://schemas/skill-returns/publish-post_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/publish_post)"
    - "User states they have published the target post"
  required_context:
    - "A finished markdown draft exists in registry/linkedin/drafts/"
  exclusion_criteria:
    - "Do not trigger if the draft frontmatter does not exist or post is already published"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Files moved to posted directory, Frontmatter updated, and Git parity reached."
  failure_state: "File system error."
  max_iterations: 1
  handoff_protocol: "Output completion status and yield."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

Execute the Publishing Sync:

1. **Operator Sync:** Read the draft file. Display the *clean plain-text* to the user for copy-pasting. Wait for the operator to reply with the Live URL.
2. **Metadata Actuation (Level 3):** Extract the self-comment and remind the operator to post it within 90 minutes. Update the draft frontmatter to `status: posted`, `pubDate: [Today]`, and `post_url`. If part of an arc, update the global thread ledger.
3. **File Migration Actuation (Level 3):** Use `run_command` in powershell to physically move the files:
   *   `Move-Item -Path "registry\linkedin\drafts\{filename}.md" -Destination "registry\linkedin\posted\"`
   *   `Move-Item -Path "registry\linkedin\drafts\comments\{filename}_comment.md" -Destination "registry\linkedin\posted\comments\"`
4. **Git Actuation (Level 3):** Run `git add registry/linkedin/`, `git commit -m "chore: linkedin post published - {filename}"`, and `git push`.
5. **Termination (T):** Yield execution.
