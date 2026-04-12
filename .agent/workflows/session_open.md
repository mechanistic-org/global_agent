---
description: Session open ritual — orient the agent, pick a ticket, confirm system health before doing any work.
---

# /session_open

Run this at the start of **every new conversation**. Paste `/session_open` as your first message.

---

## Step 0 — Memory Preload *(future: pending #133)*
> When `enos_router.preload_memory` is available, call it here with the session scope before anything else. Skip for now.

---

## Step 1 — Fetch Live Sprint Board

```powershell
python D:\GitHub\global_agent\scripts\sprint_board.py --current-iteration
```

---

## Step 2 — System Health Check

```powershell
cd D:\GitHub\global_agent && python scripts\diag.py
```

Interpret results:
- `enos_router` offline → `pm2 restart enos-router`
- Ollama offline → `ollama run qwen2.5-coder:32b --keepalive -1`
- `gws` auth failing → `gws auth login`

Do not proceed past this step if any P0 service is down.

---

## Step 3 — Declare Session Scope

State the single ticket for this session. Format:

> **Session scope: [repo]#[number] — [ticket title]**
> **DoD:** [one sentence definition of done]

Source from the sprint board in Step 1. Do not invent a ticket.

---

## Step 4 — Begin Work

Only after Step 3 is stated clearly.

---

## Notes

- Do NOT start executing work until Step 3 is confirmed.
- The GitHub Project board (Project 5, `mechanistic-org`) is the **exclusive sprint surface**. Do not look for static markdown sprint plans.
- Claude Code users: use `.claude/commands/session_open.md` — it is the environment-native shim for this workflow.
