---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "intake-dump"
description: "Process unstructured external AI output dumps (Google Docs, voice notes, analysis files) into triaged GitHub tickets and colophon registry."
version: "2.0.0"

inputs:
  payload_location: "string (Google Drive Folder ID or local path)"
returns: 
  type: "json"
  schema: "file://assets/triage_results.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Explicit user invocation via slash command (/intake_dump)"
    - "New files deposited into Antigravity_Shared_Bus Google Drive folder"
    - "New files dropped into D:\\GitHub\\global_agent\\inbox\\"
  required_context:
    - "Target files must contain unstructured text, transcripts, or analysis logs"
  exclusion_criteria:
    - "Do not trigger if the files are compiled code, images, or previously triaged documents"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Actionable items generated as GitHub issues AND strategic insights committed via push_forensic_doc."
  failure_state: "Payload unreadable or Github API rejection."
  max_iterations: 3
  handoff_protocol: "Output a summary of tickets created and yield control to user."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When this skill is triggered, you must execute the triage pipeline completely:

1. **Parameter Verification:** Locate the input source. If Google Docs, verify `os-daemon@mechanistic-gmail-mcp` has read access. If local, verify files exist in `inbox`.
2. **Ingestion (Level 3):** Execute the text extraction by calling the Python parser (e.g. `scripts/read_intake_docs.py` ported from tmp) to read the Google Docs API and aggregate text.
3. **Triage Classification:** Strictly classify all extracted content into the following schema:
   - *Net-New Infrastructure* $\rightarrow$ Route to `global_agent` ticket.
   - *Net-New Portfolio Feature* $\rightarrow$ Route to `portfolio` ticket.
   - *Duplicate/Already Ticketed* $\rightarrow$ Skip or append comment to existing ticket.
   - *Strategic Framing Only* $\rightarrow$ Do NOT create a ticket. Flag for Registry.
4. **Actuation - Ticketing:** Use the `create_walk_tickets.py` Level 3 script or the native `mcp_github` tools to generate issues. Tickets MUST include Iteration, Size, and Phase metadata.
5. **Actuation - Registry Injection:** Take all "Strategic Framing" data and use the `push_forensic_doc` MCP tool to embed it into ChromaDB (Component ID: `intake_dump_YYYY-MM-DD`). 
6. **Termination (T):** Run a `git commit` routine summarizing the N tickets created, print the summary to the console, and Yield.
