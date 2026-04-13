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
  # Convention: all skill return schemas live in D:/GitHub/global_agent/schemas/skill-returns/
  # Name the file after the skill: <skill-name>_summary.json
  schema: "file://schemas/skill-returns/output_schema.json"

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

# ==========================================
# (A) Assertions: The Spec IS the Eval
# ==========================================
#
# These are machine-readable conditions the agent evaluates against its own
# output after every execution. The spec is the test. The test is the eval.
# No separate test file. No separate eval rubric.
#
# success_assertions: conditions that MUST all be true for the skill to
#   declare success. If any assertion fails, the skill has failed regardless
#   of what the subprocess returned.
#
# failure_assertions: conditions that MUST trigger a halt. If any is true,
#   the skill must stop, log the failure, and yield to the human.
#   These are NOT error handlers — they are spec violations.
#
# assertion_log: path where pass/fail results are appended after each run.
#   Format: { timestamp, skill, version, input_hash, assertions: [{id, result, actual}] }
#   This log is the memory that enables cross-session failure pattern detection.
#
assertions:
  success_assertions:
    - id: "SA-01"
      description: "Output matches expected schema"
      check: "returns output conforming to returns.schema"
    - id: "SA-02"
      description: "No hallucinated outputs — all values traceable to programmatic return"
      check: "every field in output has a named source (subprocess stdout, API response, filesystem read)"
  failure_assertions:
    - id: "FA-01"
      description: "Required input missing or malformed"
      check: "any required input field is null, empty, or fails type check"
    - id: "FA-02"
      description: "Exclusion criterion matched — skill should not have fired"
      check: "any exclusion_criteria condition is true at execution time"
    - id: "FA-03"
      description: "Max iterations exceeded"
      check: "iteration_count > max_iterations"
  assertion_log: "registry/global_agent/assertion_logs/<skill-name>.jsonl"

# ==========================================
# PROMOTION GATE
# ==========================================
# A skill MUST NOT be marked active until:
# 1. The fail scenario below has been run and the skill correctly REJECTED the input
# 2. The pass scenario below has been run and all success_assertions passed
# 3. Both results are recorded in the assertion_log
# This is the fail-first gate. The spec must prove it can fail before it proves it can pass.
promotion:
  status: "draft"  # draft | active | deprecated
  promoted_by: ""
  promoted_date: ""
  fail_scenario_verified: false
  pass_scenario_verified: false
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When this skill is triggered, execute the following sequence precisely:

1. **Assertion Pre-check:** Before doing anything, verify no failure_assertions are already true from the inputs alone. If FA-01 or FA-02 are true, halt immediately and log to assertion_log. Do not proceed.
2. **Parameter Verification:** Read all inputs. Confirm types match the inputs contract.
3. **Deterministic Execution (Level 3):** Defer logic. Use the `run_command` tool to execute `python scripts/executable.py --input {payload_path}`.
   - *Anti-Ghost Action Constraint:* NEVER hallucinate outputs. Rely solely on the programmatic return of the subprocess or the explicit filesystem diff.
4. **Assertion Post-check:** Run all success_assertions against the output. If any fail, log the failure to assertion_log and halt. Do not declare success.
5. **Termination:** Execute the `mcp_github` or `push_forensic_doc` command to formally log completion. Append pass result to assertion_log. Yield.

---

# Assertions Reference

## Pass Scenario
*(Prove the skill can succeed before promotion. Run this. Confirm all success_assertions pass.)*

**Input:**
```
payload_path: "path/to/valid/test/input"
target_param: "valid_value"
```

**Expected output:**
```json
{
  "result": "expected_value"
}
```

**Assertions that must pass:** SA-01, SA-02

## Fail Scenario
*(Prove the skill can fail before promotion. Run this first. Confirm the skill halts and does NOT produce output.)*

**Input:**
```
payload_path: null
target_param: ""
```

**Expected behavior:** Skill halts at Assertion Pre-check. FA-01 fires. Nothing is written to output. Failure logged to assertion_log.

**This scenario must be verified BEFORE the pass scenario. A spec that cannot fail is not a spec — it is a rubber stamp.**

---

# Behavioral Coverage

*(List every decision point in the Policy and which spec clause governs it. If a behavior cannot be traced to a clause below, it is dark behavior and must be eliminated or formalized.)*

| Decision Point | Governing Clause | Assertion |
|---|---|---|
| Skill fires or does not fire | applicability.exclusion_criteria | FA-02 |
| Input accepted or rejected | inputs contract | FA-01 |
| Output accepted or rejected | returns.schema | SA-01 |
| Subprocess output trusted | Anti-Ghost Action Constraint | SA-02 |
| Skill declares success | termination.success_state | SA-01, SA-02 |
| Skill declares failure | termination.failure_state | FA-01, FA-02, FA-03 |

*Any agent behavior not in this table is undocumented. Add it or remove it.*
