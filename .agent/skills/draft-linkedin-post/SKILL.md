---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "draft-linkedin-post"
description: "Start a new LinkedIn post ticket and scaffold the corresponding draft and self-comment files in the registry."
version: "2.0.0"

inputs:
  topic: "string (The core subject or working title of the post)"
returns: 
  type: "json"
  schema: "file://assets/linkedin_scaffold_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/draft_linkedin_post)"
    - "Agent determines a new piece of registry intelligence warrants public sharing"
  required_context:
    - "Topic string"
  exclusion_criteria:
    - "Do not trigger if the draft already exists in registry/linkedin/drafts/"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "GitHub issue generated, Draft MD scaffolded, and Comment MD scaffolded."
  failure_state: "Failed to write local files or GitHub authentication error."
  max_iterations: 1
  handoff_protocol: "Output the file paths and GitHub issue link, then yield control to the user/operator."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When triggered, execute the strict scaffolding pipeline:

1. **Parameter Verification:** Read the `topic` variable.
2. **Actuation - Ticketing (Level 3):** Use `mcp_github` to create a tracking issue connecting the post to the project board.
   *   Title: "Draft LinkedIn Post: [Topic]"
   *   Body: Must include checkboxes for Draft written, Comment written, and Persona validation.
   *   Labels: ["content"]
3. **Actuation - Scaffolding (Level 3):** Use `run_command` in powershell to create the physical files. Do not rewrite existing files.
   *   File 1 (Draft): `registry\linkedin\drafts\$(Get-Date -Format 'yyyy-MM-dd')_$topicSlug.md`. Must contain strict Keystatic frontmatter (title, pubDate, status, post_url, thread_id, arc_position, tags).
   *   File 2 (Comment): `registry\linkedin\drafts\comments\$(Get-Date -Format 'yyyy-MM-dd')_$topicSlug_comment.md`.
4. **Termination (T):** Verify files exist on disk. Yield control to the operator, reminding them to apply `law_004_linkedin_persona.md` rules during the actual writing phase.
