---
name: "matrix-generator"
description: "A constrained visualization engine that converts fuzzy market assumptions into standalone or raw Markdown SWOT, TOWS, and Mermaid Ishikawa matrices."
version: "1.0.0"

inputs:
  input_string: "string (the problem statement or assumption)"
  matrix_type: "enum: swot | tows | ishikawa | all"
  project: "string (target registry namespace, e.g., 'portfolio')"
  output_mode: "enum: standalone | raw (default is raw)"
returns: 
  type: "filesystem_or_stdout"
  schema: "Raw Markdown grid OR a standalone markdown file path."

applicability:
  trigger_events:
    - "User asks to generate a SWOT, TOWS, or Ishikawa (Fishbone) diagram."
    - "A fuzzy market assumption needs quantification."
  required_context:
    - "Must have the input string to feed into the generator."
    - "Must have an explicit project scope assigned."
  exclusion_criteria:
    - "Do not use for generating arbitrary UI diagrams."

termination:
  success_state: "The python script explicitly prints raw markdown or a standalone file path."
  failure_state: "The python script exits with an error."
  max_iterations: 3
  handoff_protocol: "If raw, inject the output into the user's active context. If standalone, return the file path."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When this skill is triggered, you must execute the following sequence precisely:

1. **Parameter Verification:** Ensure you have the `input_string` and a specific `project` namespace (e.g., `portfolio`, `active_projects/hyphen`). Determine if the user asked for a standalone document or raw injection (`output_mode`). Default to `raw`.
2. **Deterministic Execution (Level 3):** Use the `run_command` tool to execute: 
   `python scripts/matrix_generator.py --input-string "[string]" --matrix-type "[type]" --project "[project]" --output-mode "[mode]"`
   * *Anti-Ghost Action Constraint:* NEVER hallucinate outputs. You must rely solely on the programmatic return of the subprocess or the explicit filesystem diff.
3. **Termination:** Parse the terminal output. Present the final retained markdown path (if standalone) or inject/summarize the raw markdown to the user.
