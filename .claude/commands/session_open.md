# /session_open

You are operating in Claude Code. Execute the following steps precisely and in order. Do not begin any work until Step 4 is stated.

---

## Step 0 — Memory Preload *(future: pending #133)*
> When `enos_router.preload_memory` is available, call it here with the session scope before anything else. Skip for now.

---

## Step 1 — Fetch Live Sprint Board

Run the sprint board script and display the full output:

```bash
python D:/GitHub/global_agent/scripts/sprint_board.py --current-iteration
```

---

## Step 2 — System Health Check

Run diagnostics and report status of each service:

```bash
cd D:/GitHub/global_agent && python scripts/diag.py
```

Interpret the output:
- If Ollama is offline: run `ollama run qwen2.5-coder:32b --keepalive -1` before proceeding
- If `gws` auth is failing: run `gws auth login` before proceeding
- If `enos_router` is offline: run `pm2 restart enos-router` before proceeding

Do not proceed past this step if any P0 service is down.

---

## Step 3 — Declare Session Scope

State the single ticket you are working this session. Format exactly:

> **Session scope: [repo]#[number] — [ticket title]**
> **DoD:** [one sentence definition of done]

Source this from the sprint board output in Step 1. Do not invent a ticket.

---

## Step 4 — Begin Work

Only after Step 3 is stated clearly. Do not start executing work before this point.

---

## Environment Notes (Claude Code specific)

- Use the `Bash` tool for all script execution — not PowerShell syntax
- Use native `gh` CLI or GitHub MCP tools for all issue and project board operations
- Use `enos_router` MCP tools for all context retrieval — do not scan directories for context
- The canonical full workflow is at `.agent/workflows/session_open.md` — this command is the Claude Code shim
