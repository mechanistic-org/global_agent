---
name: "prd-scaffolder"
description: "A deterministic engine that ingests fuzzy problem statements and generates rigid agile Epic PRDs embedded into the project registry."
version: "1.0.0"

inputs:
  title: "string (Epic short title)"
  problem: "string (The market problem or assumption)"
  project: "string (Target project namespace)"
returns: 
  type: "filesystem"
  schema: "Markdown file saved under registry/[project]/epics/[date]_[safe_title].md"

applicability:
  trigger_events:
    - "User asks to scaffold an Epic or write a PRD."
    - "A ticket requires formalization of an architecture."
  required_context:
    - "Must have a project namespace."
    - "Must have a title and a description of the problem."
  exclusion_criteria:
    - "Do not use to write unstructured meeting notes."

termination:
  success_state: "The python script explicitly prints the PRD filepath."
  failure_state: "The python script exits with an error."
  max_iterations: 3
  handoff_protocol: "Return the path of the generated PRD to the user."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When this skill is triggered, you must execute the following sequence precisely:

1. **Parameter Verification:** Ensure you have the `title`, `problem`, and `project`.
2. **Deterministic Execution (Level 3):** Use the `run_command` tool to execute: 
   `python scripts/prd_scaffolder.py --title "[title]" --problem "[problem]" --project "[project]"`
   * *Anti-Ghost Action Constraint:* NEVER hallucinate outputs. You must rely solely on the programmatic return of the subprocess or the explicit filesystem diff.
3. **Termination:** Parse the terminal output. Present the final structured PRD path to the user.
