---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "update-linkedin-profile"
description: "Drafts a proposed change to a section of linkedin_master.ts in ME Builder voice, presents a full diff for operator review, and requires explicit LGTM before writing."
version: "1.0.0"

inputs:
  section: "string"          # Required. One of: about | experience | tagline
  source_material: "string"  # Required. Absolute path to reference content (session log, mine dump, registry doc, etc.)
  entry_target: "string"     # Conditional. Company name string when section=experience; empty string otherwise.
returns:
  type: "json"
  schema: "file://schemas/skill-returns/update-linkedin-profile_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Operator explicitly invokes /update-linkedin-profile slash command"
    - "Operator requests a draft change to the About section, tagline, or an experience blurb in linkedin_master.ts"
  required_context:
    - "section input is one of: about | experience | tagline"
    - "source_material resolves to a readable file path"
    - "entry_target is provided when section=experience"
  exclusion_criteria:
    - "Do not trigger if operator intent is resume-only (no linkedin_master.ts involvement) — route to update-resume skill instead"
    - "Do not trigger if no source_material is specified — drafts without reference content violate Anti-Ghost Action constraint"
    - "Do not trigger if section is not one of the three canonical values"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Operator has issued explicit LGTM and the target section in linkedin_master.ts has been updated with the approved diff. Return JSON written."
  failure_state: "Operator rejects draft, source_material is unreadable, or section value is invalid. No write occurs."
  max_iterations: 3
  handoff_protocol: "If operator requests revisions, re-enter at Step 4 with operator feedback as additional constraint. Do not re-read source_material unless operator explicitly supplies new material. Halt after max_iterations and yield to operator with current draft state."

# ==========================================
# (A) Assertions: The Spec IS the Eval
# ==========================================
assertions:
  success_assertions:
    - id: "SA-01"
      description: "Output JSON conforms to update-linkedin-profile_summary.json schema"
      check: "returns output with status, section, and entry_target fields present and typed correctly"
    - id: "SA-02"
      description: "No content written to linkedin_master.ts before explicit operator LGTM"
      check: "filesystem diff on linkedin_master.ts shows no change at the time the draft is presented"
    - id: "SA-03"
      description: "Draft contains no forbidden patterns from ERIK_VOICE_PRIMER.md"
      check: "draft output contains none of: em-dash, TIR structure headers (The Challenge/The Intervention/The Result), first-person win declarations without architectural specifics, forbidden terms (game-changer, delve, revolutionary, synergy)"
    - id: "SA-04"
      description: "All draft content is traceable to source_material — no hallucinated biographical facts"
      check: "every claim in the draft has a corresponding passage in the source_material file read in Step 3"
  failure_assertions:
    - id: "FA-01"
      description: "Required input missing or invalid"
      check: "section is null/empty/not in [about, experience, tagline], OR source_material is null/empty, OR entry_target is null/empty when section=experience"
    - id: "FA-02"
      description: "Exclusion criterion matched"
      check: "any exclusion_criteria condition is true at execution time"
    - id: "FA-03"
      description: "Max iterations exceeded without LGTM"
      check: "iteration_count > max_iterations"
    - id: "FA-04"
      description: "Write attempted before LGTM — hard gate violation"
      check: "any tool call attempts to write linkedin_master.ts before operator has issued explicit LGTM in the current turn"
  assertion_log: "registry/global_agent/assertion_logs/update-linkedin-profile.jsonl"

# ==========================================
# PROMOTION GATE
# ==========================================
promotion:
  status: "draft"
  promoted_by: ""
  promoted_date: ""
  fail_scenario_verified: false
  pass_scenario_verified: false
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

When this skill is triggered, execute the following sequence precisely:

## Step 1 - Assertion Pre-check

Before doing anything else, verify no failure_assertions are already true from the inputs alone.

- If FA-01 is true: halt immediately. Output: `{ "status": "failure", "section": "<value or null>", "entry_target": "<value or null>", "halt_reason": "FA-01: required input missing or invalid" }`. Log to assertion_log. Do not proceed.
- If FA-02 is true: halt immediately. Output: `{ "status": "failure", "section": "<value>", "entry_target": "<value>", "halt_reason": "FA-02: exclusion criterion matched" }`. Log to assertion_log. Do not proceed.

## Step 2 - Read Voice Constraints

Read `D:/GitHub/global_agent/registry/linkedin/ERIK_VOICE_PRIMER.md` in full. Extract and hold in working context:
- Typography rules (no em-dash, no sycophancy)
- Forbidden terms list
- ME Builder in Public persona definition
- Controlled Stillness principle
- Anti-patterns for profile and resume contexts (Section 9)

Do not proceed past this step without confirming the file was read successfully.

## Step 3 - Read Source Material

Read the file at `source_material`. If the read fails (file not found, permission error), halt with:
`{ "status": "failure", "section": "<value>", "entry_target": "<value>", "halt_reason": "source_material unreadable: <path>" }`

If `section=experience`, also read the current `entry_target` blurb from `D:/GitHub/portfolio/src/config/linkedin_master.ts` to establish the existing baseline for that company. This read is informational only - it cannot be skipped.

## Step 4 - Synthesize Draft

Synthesize the proposed content using exclusively the material from Steps 2 and 3. Constraints are absolute:

**Voice requirements (ME Builder in Public / Controlled Stillness):**
- Write from inside the build. The camera points at the system, not at the reader.
- Authority comes from mechanism specificity, not from positioning statements.
- Sentence rhythm is deliberate. No escalating urgency. No emotional climax.
- Use vocabulary from the favorable terms list: constraint cages, deterministic pipelines, flat-file registries, system primitives, privilege isolation, sovereign execution, actuarial accuracy, triage routing.

**Structural requirements by section:**
- `experience`: Continuous prose or flat descriptive headers only. No TIR structure (no "The Challenge:", "The Intervention:", "The Result:" or equivalent). No bolded drama headers. Lead with what was built and what constraint it solved. Bullets permitted for specific technical achievements but must carry mechanism detail, not just outcomes.
- `about`: Extend the existing narrative voice. Do not introduce new rhetorical frames. No audience-orientation.
- `tagline`: Concise, non-hyperbolic. Reflects current primary focus.

**Hard prohibitions:**
- No em-dashes. Use space-dash-space ( - ) if a dash is needed.
- No forbidden terms (game-changer, delve, revolutionary, synergy, chatbots, AI companions).
- No embedded commands, scarcity whispers, emotional ignition triggers, or identity installation framing.
- No first-person win declarations without concrete architectural specifics.
- No hallucinated biographical details - every claim must be traceable to source_material.

## Step 5 - Present Diff for Review

Output the full proposed change in diff format. Show:
1. The exact text being replaced (or "NEW ENTRY" if adding a new experience object).
2. The exact proposed replacement text.
3. A one-paragraph synthesis rationale: what source passages inform the draft and why the ME Builder framing was applied as it was.

Then halt. Do not write to `linkedin_master.ts`. Output:

```
DRAFT READY FOR REVIEW
======================
[diff block]

RATIONALE
---------
[one paragraph]

Awaiting operator LGTM to proceed with write. Type LGTM to apply, or provide revision instructions.
```

## Step 6 - LGTM Gate

This step executes ONLY after the operator has issued an explicit LGTM in their response to Step 5 output. No implicit approval. No inferred approval from silence or positive feedback. The word "LGTM" or "approved" must appear in the operator's message.

If the operator provides revision instructions instead of LGTM: increment iteration counter, apply revisions as constraints, return to Step 4. If iteration_count > max_iterations, halt and yield with: "Max revision iterations reached. Current draft state preserved above. Operator action required."

## Step 7 - Write and Confirm

After LGTM is confirmed:
1. Apply the approved diff to `D:/GitHub/portfolio/src/config/linkedin_master.ts` using `Edit` tool.
2. Run assertion post-check: SA-01, SA-02 (verify no unintended writes occurred), SA-03, SA-04.
3. If any assertion fails: log failure to assertion_log, report to operator, do not proceed.
4. Log pass result to assertion_log.
5. Return terminal JSON:

```json
{
  "status": "success",
  "section": "<section>",
  "entry_target": "<entry_target or null>",
  "file_written": "D:/GitHub/portfolio/src/config/linkedin_master.ts",
  "notes": "<optional: any warnings or follow-up items>"
}
```

---

# Assertions Reference

## Pass Scenario

*(Prove the skill can succeed before promotion.)*

**Input:**
```
section: "experience"
source_material: "D:/GitHub/global_agent/registry/session_logs/2026-04-14_153.md"
entry_target: "MECHANISTIC"
```

**Expected output:**
- Diff block presented in Step 5 output
- No write to `linkedin_master.ts` until LGTM issued
- After LGTM: `{ "status": "success", "section": "experience", "entry_target": "MECHANISTIC", "file_written": "D:/GitHub/portfolio/src/config/linkedin_master.ts" }`

**Assertions that must pass:** SA-01, SA-02, SA-03, SA-04

## Fail Scenario

*(Prove the skill can fail before promotion. Run this first.)*

**Input:**
```
section: "experience"
source_material: null
entry_target: ""
```

**Expected behavior:** Skill halts at Step 1 Assertion Pre-check. FA-01 fires. Nothing is written. No draft is generated. Failure logged to `registry/global_agent/assertion_logs/update-linkedin-profile.jsonl`.

**This scenario must be verified BEFORE the pass scenario.**

---

# Behavioral Coverage

| Decision Point | Governing Clause | Assertion |
|---|---|---|
| Skill fires or does not fire | applicability.exclusion_criteria | FA-02 |
| Input accepted or rejected | inputs contract (FA-01 check) | FA-01 |
| Voice constraints applied | ERIK_VOICE_PRIMER.md read in Step 2 | SA-03 |
| Content traceable to source | Anti-Ghost Action / Step 3 read | SA-04 |
| Draft presented without write | termination policy / Step 5 halt | SA-02 |
| Write proceeds only after LGTM | Step 6 LGTM Gate | FA-04 |
| Output conforms to schema | returns.schema | SA-01 |
| Skill declares success | termination.success_state | SA-01, SA-02, SA-03, SA-04 |
| Skill declares failure | termination.failure_state | FA-01, FA-02, FA-03, FA-04 |
| Max revisions exceeded | termination.max_iterations | FA-03 |

*Any agent behavior not in this table is undocumented. Add it or remove it.*
