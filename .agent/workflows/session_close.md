---
description: Session close ritual — commit work, update sprint board, persist decisions, end the conversation.
---

# /session_close

Run this when: (a) the DoD for the session ticket is met, OR (b) you notice context drift symptoms (déjà vu, tool amnesia, misattribution). Do not keep working through drift.

## ⚠️ Issue Creation Protocol (applies DURING session, not just at close)

Whenever a new GitHub issue is created in ANY session, the agent MUST immediately:

```powershell
# 1. Create the issue (agent writes structured body with context)
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

Do NOT leave tickets as orphaned issues. Every issue = project board entry = full metadata. The board IS the sprint.

## Steps

1. **State outcome** — what shipped, what didn't, any blockers. One paragraph.

2. **Update GitHub Project board status** (primary surface):
   - If DoD met → move ticket to `Done`
   - If blocked → move to `Backlog`, leave a comment with blocker
   - If partial → leave in `In progress`, comment with exactly where things stand

// turbo
3. **Commit all changes:**
```powershell
cd D:\GitHub\global_agent
git add .
git commit -m "Session close: [ticket#] - [one line summary]"
git push
```

// turbo
4. **Mine the session** — extract Gold and route to registry:
```powershell
cd D:\GitHub\global_agent
python scripts\mine_session.py --conversation-id <uuid>
# or 'python scripts\mine_session.py' for the most recent brain dir
# add --dry-run to preview without writing files
```
Routes items to: `linkedin_drafts/`, `colophon.md`, ChromaDB, `testimonials/`, `law_candidates/`.

// turbo
5. **Push a forensic doc** with key decisions made this session (decisions only — not a summary of work):
```python
# Via MCP tool call — split signature from #66:
push_forensic_doc(
    project_name="session_logs",
    component_name="YYYY-MM-DD_[ticket]",
    markdown_body="## Decisions\n- [decision 1]\n- [decision 2]\n\n## Blockers\n- [any]\n\n## Next: [what next session picks up]",
    frontmatter_dict={"title": "Session [ticket#] Decisions", "date": "YYYY-MM-DD", "context_node": "session_close"}
)
```

6. **Update Sprint_Plan.md** — mark completed items `~~strikethrough~~`, promote next Sprint Now item if applicable.

7. **Close this conversation. Open a new one for the next ticket.**

## Drift Symptoms — Close Immediately If You See These

- Agent corrects something already confirmed earlier in session
- Agent proposes a command that contradicts a decision already made
- You feel déjà vu explaining something you explained an hour ago
- Agent blames a failure on something that doesn't make sense given the timeline

**When drift appears: run steps 3-5 and close. Don't try to fix the session.**

## Notes

- The conversation is closed whether the ticket is done or not. Work survives in git and GitHub Issues. The session is disposable.
- Next session starts with `/session_open` — the sprint board and forensic doc tell the new agent everything it needs.
