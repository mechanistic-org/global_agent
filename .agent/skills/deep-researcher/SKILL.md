---
name: "deep-researcher"
description: "A constrained extraction claw that reads a local PDF, generates a markdown summary strictly formatted against Dark Hangar aesthetics, and natively pushes it into ChromaDB scoped by project."
version: "1.0.0"

inputs:
  pdf_path: "string (absolute path to PDF)"
  project: "string (target registry namespace, e.g., 'portfolio')"
  query: "string (optional specific research extraction parameters)"
returns: 
  type: "filesystem_and_chromadb"
  schema: "Markdown file written to registry/[project]/assets/[pdf_name]_research.md and indexed under {"project": "[project]"}"

applicability:
  trigger_events:
    - "User asks to ingest or research a PDF"
    - "A ticket explicitly assigns an asset extraction task"
  required_context:
    - "Must have a valid absolute path to a local PDF"
    - "Must have an explicit project scope assigned"
  exclusion_criteria:
    - "Do not trigger for .docx or .xlsx files (use normalize_local_asset first)"

termination:
  success_state: "The python script explicitly prints '[DeepResearcher] Successfully embedded into ChromaDB'."
  failure_state: "The python script exits with an error or fails to write."
  max_iterations: 3
  handoff_protocol: "Confirm success and return the path of the saved markdown file."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When this skill is triggered, you must execute the following sequence precisely:

1. **Parameter Verification:** Ensure you have an absolute `pdf_path` and a specific `project` namespace (e.g., `portfolio`, `active_projects/hyphen`). If not explicitly stated, halt and ask the user for the project namespace.
2. **Deterministic Execution (Level 3):** Use the `run_command` tool to execute: 
   `python scripts/deep_researcher.py --pdf-path "[pdf_path]" --project "[project]" [--query "your query here"]`
   * *Anti-Ghost Action Constraint:* NEVER hallucinate outputs. You must rely solely on the programmatic return of the subprocess or the explicit filesystem diff.
3. **Termination:** Parse the terminal output. Present the final retained markdown path `registry/[project]/assets/...` to the user and confirm the ChromaDB namespace was respected.
