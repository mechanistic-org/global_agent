---
description: Session open ritual — orient the agent, pick a ticket, confirm system health before doing any work.
---

# /session_open

Run this at the start of **every new conversation**. Paste `/session_open` as your first message.

## Steps

// turbo
1. Read the current sprint board from GitHub Projects:
```powershell
gh project item-list 5 --owner mechanistic-org --format json --limit 20 2>&1 | python -c "import sys,json; items=json.load(sys.stdin).get('items',[]); [print(f'[{i[\"status\"]}] {i[\"title\"]} (#{i.get(\"number\",\"?\")})'  ) for i in items if i.get('status') in ['Ready','In progress','Backlog']]"
```

2. Read the local sprint plan cache:
```
D:\GitHub\global_agent\registry\portfolio\audits\2026-03-22_Sprint_Plan.md
```

// turbo
3. Run `diag.py` to confirm system health before touching anything:
```powershell
cd D:\GitHub\global_agent && python scripts\diag.py
```

4. State the single ticket you are working on this session in your reply. Format:
   > **Session scope: [repo]#[number] — [ticket title]**
   > **DoD:** [one sentence definition of done]

5. If `gws` auth is ❌ in diag output, run `gws auth login` before proceeding.

## Notes

- Do NOT start executing work until step 4 is stated clearly.
- If diag shows Ollama ❌, models are cold — run `ollama run qwen2.5-coder:32b --keepalive -1` before firing any agent.
- The GitHub Project board (Project 5, `mechanistic-org`) is the **primary sprint surface**. The local Sprint_Plan.md is a cache — read it for human context, trust GitHub for status.
