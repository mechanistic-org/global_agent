---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "draft-linkedin-reply"
description: "Scaffold a structured interaction log for significant inbound LinkedIn replies to permanently capture architectural stances."
version: "2.0.0"

inputs:
  interlocutor_name: "string"
  inbound_text: "string (Raw comment text)"
returns: 
  type: "json"
  schema: "file://assets/linkedin_reply_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/draft_linkedin_reply)"
    - "System detects high-value inbound architectural challenge on social monitor"
  required_context:
    - "Raw inbound comment text"
  exclusion_criteria:
    - "Do not trigger on simple noise replies (e.g., 'Great post!', 'Agreed')"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Interaction logged in registry/linkedin/interactions/ and response draft populated."
  failure_state: "Failed to write directory or file."
  max_iterations: 1
  handoff_protocol: "Output the file path of the scaffolded interaction log. Yield control."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When triggered, execute the OS synchronization loop:

1. **Parameter Verification:** Read `interlocutor_name` and `inbound_text`.
2. **Directory Actuation (Level 3):** Use `run_command` in powershell to ensure `registry\linkedin\interactions` exists.
3. **Scaffolding Actuation (Level 3):** Write the canonical interaction markdown file using the format: `YYYY-MM-DD_[Name]_[Topic].md`.
   *   Must include strict Frontmatter (`interlocutor`, `topic`, `project_node`, `stance_taken`, `status`).
4. **Synthesis (Level 2):** Fill out the markdown structure autonomously.
   *   **OS Analysis:** Analyze the inbound comment against EN-OS laws. Does it violate sovereignty? Is it a pitch?
   *   **Drafted Response:** Generate the response strictly conforming to the "Hired Gun" persona.
5. **Termination (T):** Use `write_to_file` to save the synthesis locally. Yield control so the human can review before copy-pasting.
