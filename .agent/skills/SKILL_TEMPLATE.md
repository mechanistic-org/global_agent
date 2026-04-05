---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "skill-name"
description: "A single, focused sentence describing exactly what outcome this skill achieves."
version: "1.0.0"

inputs:
  payload_path: "string"
  target_param: "string"
returns: 
  type: "json"
  schema: "file://assets/output_schema.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Exact phrase or system event that warrants executing this logic"
    - "File creation event in specific directory"
  required_context:
    - "List explicit data requirements (e.g., 'must have audio file path')"
  exclusion_criteria:
    - "List explicit anti-triggers (e.g., 'do not trigger if the payload is purely code review')"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Explicit deterministic proof of success (e.g., JSON file written to registry)."
  failure_state: "Explicit proof of failure (e.g., subprocess exit code > 0)."
  max_iterations: 3
  handoff_protocol: "Instruction on how to yield to user or pass to next agent."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When this skill is triggered, you must execute the following sequence precisely:

1. **Parameter Verification:** Read inputs. Halt and trigger Failure State if invalid.
2. **Deterministic Execution (Level 3):** Defer logic. Use the `run_command` tool to execute `python scripts/executable.py --input {payload_path}`.
   * *Anti-Ghost Action Constraint:* NEVER hallucinate outputs. You must rely solely on the programmatic return of the subprocess or the explicit filesystem diff.
3. **Validation:** Compare the result against `returns.schema`.
4. **Termination:** Execute the `mcp_github` or `push_forensic_doc` command to formally log completion and output the final location. Yield.
