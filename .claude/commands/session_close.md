# /session_close

Run when: (a) the DoD for the session ticket is met, OR (b) context drift is detected. Do not keep working through drift.

**Drift symptoms — close immediately if you see these:**
- Agent corrects something already confirmed earlier in session
- Agent proposes a command contradicting a earlier decision
- Déjà vu — you are explaining something you explained an hour ago
- Agent blames failure on something inconsistent with the session timeline

---

## Step 1 — State Outcome

One paragraph: what shipped, what did not, any blockers. Be specific — reference file paths, issue numbers, command outputs.

---

## Step 2 — Issue Hygiene and Ticket Closure

> **Focal Ticket Authority Only.** Only close the focal ticket declared in `/session_open`. If collateral tickets were satisfied, mention them in Step 1 and wait for explicit human triage.

If DoD is met:

```bash
# Check off DoD boxes via API (avoids markdown parsing errors)
gh issue edit <ticket#> --repo mechanistic-org/<repo> --body "<updated body with [x] checkboxes>"

# Post closing receipt and close
gh issue comment <ticket#> --repo mechanistic-org/<repo> --body "Session closed. [one paragraph summary of execution results]"
gh issue close <ticket#> --repo mechanistic-org/<repo>
```

---

## Step 3 — Update Project Board Status

- DoD met → move ticket to `Done`
- Blocked → move to `Backlog`, comment with exact blocker
- Partial → leave `In Progress`, comment with exactly where things stand

---

## Step 4 — Commit Changes

Stage surgically — never `git add .`:

```bash
cd D:/GitHub/global_agent

# Stage only files you explicitly modified this session
git add <file1> <file2> ...

# Verify what is staged before committing
git diff --cached --stat

git commit -m "Session close: [ticket#] - [one line summary]"
git push
```

If unsure what changed: `git status --short` first, then stage by name.

---

## Step 5 — Mine the Session

Extract intelligence and route to registry:

```bash
cd D:/GitHub/global_agent
python scripts/mine_session.py --conversation-id <uuid>
# or omit --conversation-id to use the most recent Antigravity brain dir
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
    markdown_body="## Decisions\n- [decision 1]\n\n## Blockers\n- [any]\n\n## Next\n[what the next session picks up]",
    frontmatter_dict={"title": "Session [ticket#] Decisions", "date": "YYYY-MM-DD", "context_node": "session_close"}
)
```

---

## Step 8 — Append to Timeline

```bash
$date = Get-Date -Format "yyyy-MM-dd"
Add-Content -Path "D:/GitHub/global_agent/registry/timeline.md" -Value "## [$date] action: session_close | ticket: [ticket#] | agent: Claude"
```

Or via Bash:
```bash
echo "## [$(date +%Y-%m-%d)] action: session_close | ticket: [ticket#] | agent: Claude" >> D:/GitHub/global_agent/registry/timeline.md
```

---

## Step 9 — Close

Close this conversation. Open a new one for the next ticket. Work survives in git and GitHub Issues — the session is disposable.

---

## Environment Notes (Claude Code specific)

- Use `Bash` tool for all script execution
- Use native `gh` CLI or GitHub MCP for all issue and board operations
- The canonical full workflow is at `.agent/workflows/session_close.md` — this command is the Claude Code shim
- Issue creation during the session: every issue must be added to Project 5 with full metadata — see `.agent/workflows/session_close.md` for field IDs
