---
description: Session close ritual — commit work, update sprint board, persist decisions, end the conversation.
---

# /session_close

Run when: (a) the DoD for the session ticket is met, OR (b) context drift symptoms appear. Do not keep working through drift.

**Drift symptoms — close immediately:**
- Agent corrects something already confirmed earlier in session
- Agent proposes a command contradicting a prior decision
- Déjà vu — you are re-explaining something from earlier in the session
- Agent blames failure on something inconsistent with the session timeline

---

## ⚠️ Issue Creation Protocol (applies DURING session, not just at close)

Whenever a new GitHub issue is created in ANY session, the agent MUST immediately:

```powershell
# 1. Create the issue
$url = gh issue create --repo mechanistic-org/REPO --title "..." --label "..." --body "..."

# 2. Add to global project board
gh project item-add 5 --owner mechanistic-org --url $url

# 3. Wire all metadata fields (get item-id from step 2 output first)
# Iteration field: PVTIF_lADOEA3Ajc4BSLlfzg_ynvU
# Priority field:  PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI (P0/P1/P2/P3)
# Size field:      PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM (Epic/Enhancement/Task)
# Node field:      PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY (portfolio/mechanistic/global_agent...)
# Impact field:    PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc (Revenue/Sovereignty/Aesthetic/R&D)
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id ITEM_ID \
  --field-id PVTIF_lADOEA3Ajc4BSLlfzg_ynvU --iteration-id ITER_ID
```

Do NOT leave tickets as orphaned issues. Every issue = project board entry = full metadata.

---

## Step 1 — State Outcome

One paragraph: what shipped, what did not, any blockers. Reference file paths and issue numbers specifically.

> **Focal Ticket Authority Only:** Per `.agent/rules/ticket_closure.md`, only execute closure (Steps 2-3) on the focal ticket declared at session open. Collateral tickets satisfied incidentally — mention them in the outcome, wait for explicit human triage before closing.

---

## Step 2 — Issue Hygiene and Ticket Closure (if DoD is met)

```powershell
# Check off DoD boxes via MCP GitHub tool (avoids PowerShell markdown parsing errors)
# Use mcp_github_update_issue to push updated body with [x] checkboxes

# Post receipt and close
gh issue comment <ticket#> --repo mechanistic-org/<repo> --body "Session closed. [execution summary]"
gh issue close <ticket#> --repo mechanistic-org/<repo>
```

---

## Step 3 — Update Project Board Status

- DoD met → move ticket to `Done`
- Blocked → move to `Backlog`, comment with exact blocker
- Partial → leave `In Progress`, comment with exactly where things stand

---

## Step 4 — Commit Changes

Stage surgically — never `git add .` or `git add -A`:

```powershell
cd D:\GitHub\global_agent

# Review working tree first
git status --short

# Stage only files explicitly modified this session
git add <file1> <file2>

# Verify staged content before committing
git diff --cached --stat

git commit -m "Session close: [ticket#] - [one line summary]"
git push
```

---

## Step 5 — Mine the Session

```powershell
cd D:\GitHub\global_agent
venv\Scripts\python.exe scripts\mine_session.py --conversation-id <uuid>
# omit --conversation-id to use most recent brain dir
# add --dry-run to preview without writing
```

Routes to: `linkedin_drafts/`, `colophon.md`, ChromaDB, `law_candidates/`.

> **Sequential gate:** Wait for `mine_session.py` to fully exit before Step 6. Both write to ChromaDB. Concurrent execution causes SQLite WAL lock deadlock.

---

## Step 6 — Memory Flush *(future: pending #133)*
> When `enos_router` session-close flush is implemented, call it here to persist curated session findings to ChromaDB. Skip for now.

---

## Step 7 — Push Forensic Doc

Persist key decisions (decisions only — not a work summary):

```python
# Via MCP tool call
push_forensic_doc(
    project_name="session_logs",
    component_name="YYYY-MM-DD_[ticket]",
    markdown_body="## Decisions\n- [decision 1]\n\n## Blockers\n- [any]\n\n## Next\n[what next session picks up]",
    frontmatter_dict={"title": "Session [ticket#] Decisions", "date": "YYYY-MM-DD", "context_node": "session_close"}
)
```

---

## Step 8 — Append to Timeline

```powershell
$date = Get-Date -Format "yyyy-MM-dd"
Add-Content -Path "D:\GitHub\global_agent\registry\timeline.md" -Value "## [$date] action: session_close | ticket: [ticket#] | agent: Antigravity"
```

---

## Step 9 — Close

Close this conversation. Open a new one for the next ticket. Work survives in git and GitHub Issues — the session is disposable.

---

## Notes

- Claude Code users: use `.claude/commands/session_close.md` — it is the environment-native shim for this workflow.
- The `// turbo` annotation used in prior versions of this file was Antigravity-specific. It has been removed. Antigravity executes bash blocks automatically regardless.
