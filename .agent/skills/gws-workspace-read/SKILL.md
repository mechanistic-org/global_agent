---
# ==========================================
# (R) Reusable Interface: Signature & Discovery
# ==========================================
name: "gws-workspace-read"
description: "Read data from Google Workspace (Gmail, Calendar, Drive, Docs, Sheets) via the native gws MCP server. Governs when and what an agent is permitted to read."
version: "1.0.0"

inputs:
  service: "string (gmail | calendar | drive | docs | sheets)"
  intent: "string (human-readable description of what is being retrieved and why)"
returns:
  type: "structured data from GWS MCP tool response"
  schema: "varies by service — see Policy for per-service return shapes"

# ==========================================
# (C) Applicability Conditions: When to Wake Up
# ==========================================
applicability:
  trigger_events:
    - "Operator requests information from Gmail, Calendar, Drive, Docs, or Sheets"
    - "A skill or workflow requires GWS data as an input (e.g. scheduling, content triage)"
    - "Session open ritual needs to check calendar for context"
  required_context:
    - "gws MCP server must be active and authenticated — verify via mcp.json"
    - "Operator intent must be explicitly stated before any read operation"
  exclusion_criteria:
    - "Do NOT read GWS data speculatively or to 'orient' without explicit operator instruction"
    - "Do NOT read email content in bulk — single message or bounded list only"
    - "Do NOT read Drive files outside of explicitly named paths or IDs"
    - "Do NOT use this skill if the gws MCP server is unavailable — do not fall back to CLI without operator confirmation"

# ==========================================
# (T) Termination Conditions: When to Sleep
# ==========================================
termination:
  success_state: "Requested data returned, summarised, and surfaced to operator or passed to calling skill."
  failure_state: "MCP tool call returns error, auth failure, or empty result with no retry possible."
  max_iterations: 2
  handoff_protocol: "Return retrieved data to operator or calling skill. Do not cache GWS data in registry without explicit instruction."
---

# Policy ($\pi$)

*(This block is only injected if Applicability Conditions match)*

## Pre-flight Auth Check

Before any read operation, confirm the `gws` MCP server is reachable. If unavailable:
- Halt and inform the operator
- Do NOT silently fall back to the `gws` CLI binary without confirmation
- Suggested recovery: `gws auth login` then restart the MCP server

## Transport

Use the **native `gws` MCP server tools** exclusively. Do not shell to the `gws` CLI binary for reads when the MCP server is active. The MCP path is:
- Lower latency (no subprocess spawn)
- Structured return (no CLI output parsing)
- Auditable via MCP tool call log

If you need a CLI operation not exposed by the MCP server, surface that gap to the operator rather than silently shelling out.

## Per-Service Read Scope

### Gmail
- Read a **single message** by ID, or a **bounded list** (max 20) with explicit filter criteria
- Always state the filter: sender, subject keyword, date range, label
- Never dump an entire inbox
- Preferred tool: `gws` MCP → `gmail.messages.list` + `gmail.messages.get`

### Calendar
- Read events for a **specific date range** (max 14 days forward unless operator specifies otherwise)
- Return: event title, time, attendees, location — do not expose internal meeting notes unless asked
- Preferred tool: `gws` MCP → `calendar.events.list`

### Drive
- Read only **explicitly named files or folders** — never browse Drive speculatively
- Operator must provide a file ID, folder name, or exact search query
- Do not expose sharing permissions or owner details unless specifically requested
- Preferred tool: `gws` MCP → `drive.files.get` or `drive.files.list` with explicit `q` param

### Docs
- Read the **latest version** of a named document
- Surface the document body; strip internal revision metadata unless requested
- Preferred tool: `gws` MCP → `docs.documents.get`

### Sheets
- Read a **named range or sheet tab** — never read an entire spreadsheet without explicit range
- Return as structured rows, not raw API response
- Preferred tool: `gws` MCP → `sheets.spreadsheets.values.get`

## Output Contract

- Summarise retrieved data concisely before passing it on — do not dump raw API JSON to the operator
- If the data retrieved is sensitive (email content, calendar attendees), confirm with operator before logging it to the registry
- Never push raw GWS content to ChromaDB without operator sign-off
