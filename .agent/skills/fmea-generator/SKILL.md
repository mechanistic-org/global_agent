---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "fmea-generator"
description: "Ingests raw PRD markdown, semantically identifies mechanical failure modes, strictly overrides RPN calculations in Python, and records the liability matrix."
version: "1.0.0"

inputs:
  payload_path: "string (absolute path to PRD markdown)"
  target_param: "string (project registry alias, e.g. test_project)"
returns: 
  type: "markdown"
  schema: "file://registry/TARGET_PARAM/fmea.md"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "User requests to generate an FMEA"
    - "User requires strict liability constraint assessment of hardware mechanical modes"
  required_context:
    - "Must have a path to a narrative or PRD detailing the mechanical implementation"
    - "Must have a target project name to associate the output with"
  exclusion_criteria:
    - "Do not trigger for pure software code reviews"
    - "Do not trigger if PRD/markdown pathway is explicitly missing"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "SUCCESS string confirming flat-file write and ChromaDB embed."
  failure_state: "CRITICAL or WARNING output from Python script with exit code > 0."
  max_iterations: 3
  handoff_protocol: "Output completion state with file location and yield to user."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When this skill is triggered, you must execute the following sequence precisely:

1. **Parameter Verification:** Read `payload_path` (PRD input file) and `target_param` (project name). Halt and trigger Failure State if either is missing or invalid.
2. **Deterministic Execution:** Use the `run_command` tool to execute `python D:\GitHub\global_agent\scripts\mcp_fmea_generator.py --input {payload_path} --project {target_param}`. 
   * *Anti-Ghost Action Constraint:* NEVER hallucinate outputs. You must rely solely on the programmatic return of the script.
3. **Validation:** Read the returned console output. It must state SUCCESS.
4. **Conclusion Statement:** Formally log the location (`registry/{target_param}/fmea.md`) and yield completion.
