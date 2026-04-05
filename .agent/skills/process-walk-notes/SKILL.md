---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "process-walk-notes"
description: "Ingest, synthesize, and formalize unstructured Google Drive walk notes into ChromaDB, the flat-file registry, and actionable GitHub tickets."
version: "2.0.0"

inputs:
  folder_id: "string (Google Drive Folder ID containing walk notes)"
returns: 
  type: "json"
  schema: "file://assets/processed_notes_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/process_walk_notes)"
    - "System detects a new Google Drive folder following 'walk-notes_<topic-slug>' convention"
  required_context:
    - "Valid Google Drive folder ID"
  exclusion_criteria:
    - "Do not trigger if folder is empty or contains strictly compiled binary formats"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Synthesized intelligence note committed to registry, ChromaDB embedded via push_forensic_doc, and GitHub tickets created (if applicable)."
  failure_state: "Google Workspace extraction failure, or folder inaccessible."
  max_iterations: 3
  handoff_protocol: "Summarize tickets and registry components created, then yield control to the user."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When this skill is triggered, you must execute the Walk Note pipeline:

1. **Parameter Verification:** Read the `folder_id` parameter. Ensure node.js GWS shims (`C:\tmp\gws-drive-list.js` and `gws-doc-export.js`) are available to bypass Windows CMD escaping bugs.
2. **Ingestion (Level 3 Actuation):** Run `run_command` on `node C:\tmp\gws-drive-list.js {folder_id}` to retrieve target Docs.
3. **Extraction:** Sequentially iterate through file IDs using `node C:\tmp\gws-doc-export.js {file_id} C:\tmp\walk_doc_{id}.txt`.
4. **Synthesis:** Read all exported temporary text files. Draft a structured registry intelligence note containing:
   - Frontmatter (`title`, `date`, `source_folder_id`, `status: processed`, `linked_tickets`)
   - Thematic sections aggregating the walk text.
   - Formal Action Items list.
5. **Ticketing Actuation:** Map actionable engineering tasks to new GitHub tickets natively via `mcp_github`.
6. **Registry Actuation:** 
   - Execute `write_to_file` to save the synthesis to `registry/global_agent/intelligence/YYYY-MM-DD_<topic-slug>.md`.
   - Call the `push_forensic_doc` MCP tool to simultaneously stream the Markdown and Frontmatter into ChromaDB.
7. **Termination (T):** Use `run_command` to Git commit and push the updated `intelligence/` folder. Yield control.
