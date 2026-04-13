---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "create-issue"
description: "Create a new GitHub issue AND wire it fully to the global project board in one operation."
version: "3.0.0"

inputs:
  title: "string — concise, action-oriented. Must name the deliverable, not describe the session."
  source_ref: "string — REQUIRED. Exact file path or URL of the artifact this ticket relates to. No paraphrasing. If it cannot be expressed as a path or URL, the ticket lacks a concrete anchor and must not be created."
  assets: "array of strings — ALL links, file paths, and chat URLs present in the triggering session context. If the operator passed any URLs or file paths, they go here. An empty array when context contains links is a validation failure."
  dod_items: "array of strings — forward actions only. Each item must begin with an action verb (Draft, Publish, Validate, Review, etc.). Describing past state here is a structural error — past state belongs in assets."
  metadata: "object containing Iteration, Priority, Size, Node, Impact, Status"
returns:
  type: "json"
  schema: "file://schemas/skill-returns/create-issue_summary.json"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Call from explicit slash command (/create_issue)"
    - "Agent natively decides an issue must be generated from triage"
  required_context:
    - "Valid title"
    - "source_ref resolving to a concrete path or URL"
    - "At least one unchecked dod_item"
    - "All 5 metadata fields populated: Iteration, Priority, Size, Node, Impact"
  exclusion_criteria:
    - "Reject if source_ref is absent"
    - "Reject if source_ref appears to be a prose description rather than a file path or URL"
    - "Reject if dod_items is empty"
    - "Reject if any dod_item describes past state rather than a future action (e.g. 'Draft written', 'Comment added' are state descriptions, not DoD items — move them to assets)"
    - "Warn loudly if assets array is empty but session context contains URLs or file paths"
    - "Reject if any metadata field is null or unset — a ticket with missing project fields is noise, not signal"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "GitHub Issue created, all 5 project board fields verified non-null via read-back, Issue URL emitted."
  failure_state: "Validation failure at Step 0, GitHub CLI failure, or any project field null after wiring."
  max_iterations: 1
  handoff_protocol: "Output the Issue URL and Project Item ID. Do NOT post a session_close comment on this ticket within the same session that created it — the ticket is open, not done."
---

# Policy ($\pi$)

*(This block is only injected if the Applicability Conditions match)*

## Step 0 - Input Validation (halt before touching GitHub if any check fails)

Before executing anything, verify:

- `source_ref` contains a `/`, `\`, or `http` — if it reads like a sentence, reject and ask for the exact path or URL.
- `assets` captures every URL and file path mentioned in the triggering request. Cross-check against session context. Missing links are a hard warning — confirm with operator before proceeding.
- Every item in `dod_items` begins with an action verb and describes work that has NOT yet been done. If an item describes something that already exists (e.g. "Draft written"), move it to `assets` with a file path reference and remove it from `dod_items`.
- All 5 metadata fields are non-null. If any are missing, halt and prompt the operator.

## Step 1 - Body Assembly

Assemble the issue body from the following template. Do not improvise structure.

```
## Source
{source_ref}

## Assets
<!-- Everything that exists at ticket creation. Paths and URLs only — no prose descriptions. -->
{assets as markdown bullet list — if empty after Step 0 validation, flag as WARNING in the body}

## Definition of Done
<!-- Forward actions only. All boxes unchecked. If a box is pre-checked, it does not belong here. -->
{dod_items rendered as unchecked markdown checkboxes: - [ ] item}

## Notes
{any additional context passed in the triggering session — verbatim where possible}
```

## Step 2 - Issue Creation

Run `gh issue create` with `--repo`, `--title`, `--label`, and `--body` (assembled body from Step 1). Capture the returned Issue URL as `$ISSUE_URL`.

## Step 3 - Project Wiring

Run `gh project item-add 5 --owner mechanistic-org --url {$ISSUE_URL} --format json` to get `$ITEM_ID`.

Then set all 5 fields — skipping any is a failure, not a warning:

- Iteration (`--field-id PVTIF_lADOEA3Ajc4BSLlfzg_ynvU`)
- Priority (`--field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI`)
- Size (`--field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM`)
- Node (`--field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY`)
- Impact (`--field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc`)

## Step 4 - Wiring Verification

Read back the project item to confirm all 5 fields are non-null:

```bash
gh project item-list 5 --owner mechanistic-org --format json \
  | jq --arg id "$ITEM_ID" '.items[] | select(.id == $id) | {iteration, priority, size, node, impact}'
```

If any field is null, re-run the corresponding `item-edit` command and verify again. Do not proceed to Step 5 with a null field.

## Step 5 - Termination

Emit the Issue URL and Project Item ID. Yield.

Do NOT post a session_close comment on this ticket in the same session that created it. The ticket has just been opened — its DoD items are all unchecked by definition. A session_close comment at creation time is a timing error.
