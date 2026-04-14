---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "draft-linkedin-post"
description: "Start a new LinkedIn post ticket and scaffold the corresponding draft and self-comment files in the registry."
version: "2.0.0"

inputs:
  topic: "string (The core subject or working title of the post)"
  persona: "string (Optional: 'me_builder' or 'hired_gun'. Defaults to 'me_builder')"
returns: 
  type: "json"
  schema: "file://schemas/skill-returns/draft-linkedin-post_summary.json"

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

1. **Parameter Verification & Tone Check:** 
   * Read the `topic` and `persona` variables. 
   * If `persona` is not explicitly provided, analyze the `topic`. If the topic sounds highly reactive, defensive, or aimed at tearing down an industry standard, HALT and use `ask_question` to ask the operator: "This topic leans toward a 'Hired Gun' tone. Should I proceed with the default 'me_builder' or switch to 'hired_gun'?"
   * Otherwise, default to `me_builder`.
   * **Hard tone constraints (apply to all personas):** Before scaffolding any draft, verify the framing does not contain: (1) edgy hooks designed to spike novelty through provocation or shock, (2) preachy conclusions that tell the audience what lesson to draw, or (3) any passage that lectures the reader about what they should be doing differently. The camera points at the work, not at the audience. Violating these constraints requires HALT and operator confirmation before proceeding.
2. **Context Injection:** Execute `view_file` to strictly read the exact contents of `D:\GitHub\global_agent\registry\linkedin\ERIK_VOICE_PRIMER.md`. You must not proceed without understanding the requested persona constraints from this document.
3. **Actuation - Ticketing (Level 3):** Use `mcp_github` to create a tracking issue connecting the post to the project board.
   *   Title: "Draft LinkedIn Post: [Topic]"
   *   Body: Must include checkboxes for Draft written, Comment written, and Persona validation.
   *   Labels: ["content"]
4. **Actuation - Scaffolding (Level 3):** Use `run_command` in powershell to create the physical files. Do not rewrite existing files.
   *   File 1 (Draft): `registry\linkedin\drafts\$(Get-Date -Format 'yyyy-MM-dd')_$topicSlug.md`. Must contain strict Keystatic frontmatter. Embed the selected persona tone strictly mirroring `ERIK_VOICE_PRIMER.md`.
   *   File 2 (Comment): `registry\linkedin\drafts\comments\$(Get-Date -Format 'yyyy-MM-dd')_$topicSlug_comment.md`.
5. **Termination (T):** Verify files exist on disk. Yield control to the operator, confirming the exact voice/gear that was deployed based on `ERIK_VOICE_PRIMER.md`.
