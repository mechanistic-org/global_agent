---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "triage"
description: "Run a structured 25-minute board triage session: pull all unassigned issues, apply the 3-question rubric from board_governance.md, and leave zero issues without a milestone."
version: "1.0.0"

inputs:
  focus_milestone: "string — optional. If provided, triage only issues within that milestone rather than all unassigned issues. E.g. 'Toolmaker v1'."
returns:
  type: "json"
  schema: "file://schemas/skill-returns/triage_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Explicit operator invocation: /triage"
    - "Session open reveals unassigned issues and operator confirms triage intent"
    - "Weekly cadence: if board_governance.md triage history shows last entry > 7 days ago"
  required_context:
    - "GitHub CLI (gh) accessible and authenticated"
    - "registry/global_agent/board_governance.md readable"
    - "At least one open issue with no milestone"
  exclusion_criteria:
    - "Do not trigger if operator has declared a specific issue scope for the session and triage would interrupt it"
    - "Do not trigger if zero unassigned issues exist — emit a clean board confirmation and yield"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Zero open issues without a milestone. Triage history block in board_governance.md updated with today's date, count processed, and actions taken."
  failure_state: "25-minute cap reached with unprocessed issues remaining — remaining issues bulk-moved to Icebox, cap breach logged."
  max_iterations: 50
  handoff_protocol: "Emit triage_summary.json. Yield to operator. Do not begin sprint work in the same response that closes triage."

# ==========================================
# (A) Assertions: The Spec IS the Eval
# ==========================================
assertions:
  success_assertions:
    - id: "SA-01"
      description: "Zero open issues with null milestone after triage completes"
      check: "gh issue list --no-milestone --state open returns empty array"
    - id: "SA-02"
      description: "board_governance.md triage history updated with current date"
      check: "triage history block contains an entry matching today's date"
    - id: "SA-03"
      description: "Every action taken is traceable to a rubric outcome — no unilateral decisions"
      check: "each closed or milestone-assigned issue has a documented rubric answer in the session log"
  failure_assertions:
    - id: "FA-01"
      description: "board_governance.md not readable — rubric cannot be loaded"
      check: "file read of registry/global_agent/board_governance.md returns error or empty"
    - id: "FA-02"
      description: "GitHub CLI unauthenticated or unreachable"
      check: "gh auth status returns non-zero"
    - id: "FA-03"
      description: "Max iterations exceeded"
      check: "iteration_count > max_iterations"
  assertion_log: "registry/global_agent/assertion_logs/triage.jsonl"

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

## Step 0 - Pre-check

Before doing anything, verify:

1. Run `gh auth status` — if non-zero, halt. FA-02 fires. Yield to operator with instruction to authenticate.
2. Read `registry/global_agent/board_governance.md` — if unreadable, halt. FA-01 fires.
3. Run `gh issue list --no-milestone --state open --json number,title,labels,milestone --limit 100` — capture as `$QUEUE`.
4. If `$QUEUE` is empty: SA-01 is already satisfied. Emit "Board is clean - zero unassigned issues." Yield. Do not proceed.
5. Announce to operator: "Triage session starting. **25-minute cap.** `{count}` issues in queue. Anything not processed will be moved to Icebox."

## Step 1 - Load Rubric

State the rubric before processing any issue. Do not assume the operator has it memorized:

```
TRIAGE RUBRIC (from board_governance.md)

3 Questions per issue:
  Q1: Is it still relevant? (not superseded, not abandoned)
  Q2: Does it have acceptance criteria or DoD?
  Q3: Does it have a milestone?

3 Outcomes only:
  KEEP    - relevant + has/can write AC → assign milestone
  ICEBOX  - valid but no current traction → move to Icebox milestone
  CLOSE   - stale, superseded, or no foreseeable action → close with one-line reason
```

## Step 2 - Process Queue

For each issue in `$QUEUE`, present it in this exact format:

```
--- ISSUE #{number} ---
Title: {title}
Labels: {labels or "none"}
Body preview: {first 100 chars of body or "(no body)"}

Q1 Still relevant?  [ ]
Q2 Has AC or DoD?   [ ]
Q3 Has milestone?   [ ] (answer is always No — it's in the queue)

Proposed action: {KEEP → suggest milestone | ICEBOX | CLOSE}
```

Wait for operator confirmation or override before executing. Do not batch-decide without operator input.

**On operator confirmation, execute immediately:**
- KEEP: `gh issue edit {n} --milestone "{milestone}"` — then optionally draft AC if Q2 was No
- ICEBOX: `gh issue edit {n} --milestone "Icebox"`
- CLOSE: `gh issue close {n} --comment "{one-line reason}"`

Track elapsed time. At 20 minutes, warn: "5 minutes remaining. `{n}` issues left."

At 25 minutes: halt processing. Move all remaining unprocessed issues to Icebox in a single batch:
```bash
for n in {remaining_ids}; do
  gh issue edit $n --milestone "Icebox"
done
```

Log the cap breach in the triage summary.

## Step 3 - Update Triage History

Append a new row to the triage history table in `registry/global_agent/board_governance.md`:

```
| {YYYY-MM-DD} | Processed {N} issues: {kept} assigned, {icebox} icebox, {closed} closed. {notes if cap hit} |
```

## Step 4 - Termination

Run `gh issue list --no-milestone --state open --json number --limit 10` to verify SA-01.

Emit triage summary:

```
Triage complete.
  Processed: {n} issues
  Assigned:  {n}
  Icebox:    {n}
  Closed:    {n}
  Duration:  {elapsed} min
  Board clean: {Yes / No — n remaining}
```

Yield. Do not begin sprint work in this response.

---

# Assertions Reference

## Pass Scenario

**Input:** Board has 3+ open issues with no milestone.

**Expected behavior:**
- Rubric is stated before processing begins
- Each issue is presented in the structured format
- Operator confirms or overrides each decision
- All issues assigned, icebox'd, or closed
- board_governance.md triage history updated
- SA-01: zero unassigned issues confirmed via read-back

**Assertions that must pass:** SA-01, SA-02, SA-03

## Fail Scenario

**Input:** `gh auth status` returns non-zero (unauthenticated).

**Expected behavior:** Skill halts at Step 0. FA-02 fires. No issues are read or modified. Failure logged to assertion_log. Operator instructed to run `gh auth login`.

**This scenario must be verified BEFORE the pass scenario.**

---

# Behavioral Coverage

| Decision Point | Governing Clause | Assertion |
|---|---|---|
| Skill fires or does not fire | applicability.exclusion_criteria | FA-02 |
| Queue is empty - early exit | Step 0 check | SA-01 |
| Rubric stated before processing | Step 1 | SA-03 |
| Each issue presented before action | Step 2 format | SA-03 |
| Operator confirms before execution | Step 2 wait | SA-03 |
| 25-min cap enforced | Step 2 timer | termination.failure_state |
| Remaining issues bulk-Icebox'd on cap | Step 2 cap breach | termination.failure_state |
| Triage history updated | Step 3 | SA-02 |
| Board verified clean after triage | Step 4 read-back | SA-01 |
