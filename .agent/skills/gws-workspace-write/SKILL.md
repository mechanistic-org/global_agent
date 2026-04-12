---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "gws-workspace-write"
description: "Write, send, or mutate data in Google Workspace (Gmail, Calendar, Drive, Docs, Sheets) via the native gws MCP server. Enforces mandatory human confirmation before any destructive or outbound operation."
version: "1.0.0"

inputs:
  service: "string (gmail | calendar | drive | docs | sheets)"
  operation: "string (create | update | delete | send | move)"
  intent: "string (human-readable description of what will be written or mutated and why)"
  payload: "object (service-specific content — see Policy for per-service payload shapes)"
returns:
  type: "confirmation object with operation ID and mutated resource reference"
  schema: "varies by service — see Policy for per-service return shapes"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Operator explicitly requests sending an email, creating a calendar event, uploading to Drive, writing to a Doc or Sheet"
    - "A skill or workflow produces an output that requires GWS delivery (e.g. client deliverable to Drive, meeting creation)"
  required_context:
    - "gws MCP server must be active and authenticated"
    - "Operator must have confirmed the operation explicitly — no implied or inferred writes"
    - "All payload content must be finalised before invoking this skill — do not draft and send in the same step"
  exclusion_criteria:
    - "Do NOT send any email without displaying the full draft to the operator and receiving explicit 'send it' confirmation"
    - "Do NOT delete any GWS resource — present the delete intent to the operator and require typed confirmation"
    - "Do NOT create calendar events on behalf of others without operator review of attendee list"
    - "Do NOT write to a shared Drive folder or shared Doc without operator confirming the sharing scope"
    - "Do NOT use this skill if the gws MCP server is unavailable — do not fall back to CLI without operator confirmation"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Operation confirmed by MCP tool response with resource ID. Operator notified of result."
  failure_state: "MCP tool call returns error, auth failure, or operator declines confirmation gate."
  max_iterations: 1
  handoff_protocol: "Return operation result and resource reference to operator. Do not chain write operations without returning to operator between each."
---

# Policy ($\pi$)

*(This block is only injected if Applicability Conditions match)*

## The Confirmation Gate (Non-Negotiable)

Every write operation requires a **mandatory human confirmation step** before execution. There are no exceptions.

The gate format for every operation:

> **GWS Write Pending**
> - Service: `[gmail | calendar | drive | docs | sheets]`
> - Operation: `[create | update | delete | send | move]`
> - Target: `[recipient / resource name / file ID]`
> - Content preview: `[first 200 chars of payload or full summary]`
>
> **Type "confirm" to proceed or "cancel" to abort.**

Do not proceed until the operator responds with explicit confirmation.

## Pre-flight Auth Check

Before any write operation, confirm the `gws` MCP server is reachable and authenticated. If unavailable:
- Halt immediately
- Do NOT attempt the write via CLI binary as a fallback
- Surface the auth failure and suggested recovery to the operator

## Transport

Use the **native `gws` MCP server tools** exclusively. Do not shell to the `gws` CLI for write operations. Write operations via MCP are:
- Atomic (the tool call either succeeds or fails — no partial state)
- Auditable (logged in MCP tool call history)
- Revocable (surface the resource ID immediately so the operator can undo manually if needed)

## Per-Service Write Constraints

### Gmail — Send
1. Display full email: To, Cc, Subject, Body — in a code block
2. Confirmation gate (required)
3. Send via `gws` MCP → `gmail.messages.send`
4. Return: message ID and thread ID

**Hard rules:**
- Never Bcc without operator explicitly setting it
- Never reply-all without operator reviewing the full recipient list first
- Never send to a distribution list or multiple recipients without explicit review

### Calendar — Create / Update
1. Display full event details: title, date/time, attendees, location, description
2. Confirmation gate (required)
3. Create/update via `gws` MCP → `calendar.events.insert` or `calendar.events.patch`
4. Return: event ID and calendar link

**Hard rules:**
- Never set a recurring event without operator specifying the recurrence rule explicitly
- Never invite external attendees (outside mechanistic-org domain) without operator confirmation of each address

### Drive — Upload / Move / Delete
1. Display: file name, destination folder, MIME type, sharing scope
2. Confirmation gate (required — **stricter for delete: require operator to type the file name**)
3. Execute via `gws` MCP → `drive.files.create`, `drive.files.update`, or `drive.files.delete`
4. Return: file ID and Drive URL

**Hard rules:**
- Never delete without requiring the operator to type the resource name as confirmation
- Never change sharing permissions to "anyone with link" without explicit operator instruction
- Never move files between shared drives without operator confirming the destination ownership

### Docs — Write / Append
1. Display: document name, content to be written, insertion point
2. Confirmation gate (required)
3. Write via `gws` MCP → `docs.documents.batchUpdate`
4. Return: document ID and revision number

**Hard rules:**
- Never overwrite existing content — always append unless operator explicitly instructs a replace
- Surface the full proposed content before writing, not just a summary

### Sheets — Write / Append
1. Display: spreadsheet name, target range, row data preview
2. Confirmation gate (required)
3. Write via `gws` MCP → `sheets.spreadsheets.values.append` or `sheets.spreadsheets.values.update`
4. Return: updated range reference and rows written count

**Hard rules:**
- Never clear a range (`sheets.spreadsheets.values.clear`) without operator explicitly naming the range
- Never write formulae that reference external sheets without operator review

## Post-Write Logging

After a successful write, log the operation to the session forensic doc:
```
GWS write: [service] [operation] | resource: [ID] | timestamp: [ISO]
```

Do not log payload content (email body, doc content) to the registry without operator sign-off.
