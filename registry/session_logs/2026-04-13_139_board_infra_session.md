---
title: 'Session 2026-04-13 Decisions - #139 + Board Infrastructure'
date: '2026-04-13'
context_node: session_close
---

## Decisions

- GitHub Projects is a display layer, not a metadata store. Two-step creation (issue then project wiring) has a gap where issues exist but are not on the board. Silent failures are the norm, not the exception.
- Solution adopted: keep Projects as Kanban board, replace 5-rule auto-add UI limit with GitHub Actions (board-sync.yml + reusable workflow in .github org repo). One workflow file per repo, no rule limit, scales linearly with new repos.
- create-issue SKILL.md bumped to v3.0.0. Key change: freeform body replaced with structured inputs (source_ref = exact path or URL, assets[] = all session links, dod_items[] = forward actions only). Step 0 validation before any GitHub call. Step 4 read-back verification after project field writes.
- Assets/DoD split: anything that already exists at ticket creation belongs in an Assets section with a file path or URL reference. DoD items must be forward actions beginning with action verbs. Pre-checked items are state descriptions, not tasks - structural error.
- ADD_TO_PROJECT_PAT (PAT with repo + project scopes) was given to an agent session on 2026-03-11 and never wired as an org secret. Root cause: that session had no DoD and no closing artifact. The token existed in context only, which did not survive session close. Exact failure mode #138 was written to prevent.
- sprint_board.py --current-iteration flag was entirely absent despite being the mandatory first step in the CLAUDE.md session ritual. Now implemented with full argparse.
- TEMPLATE_client has branch protection requiring PRs on main. Admin push bypasses with logged warning. Rule is correct - keep it.
- mootmoat local clone had stale remote pointing to mootmoat/mootmoat (old location). Updated to mechanistic-org/mootmoat.
- 18 legacy GWS skill files (gws-calendar, gws-docs, gws-drive, gws-gmail, gws-sheets variants) deleted. Deprecated by native gws MCP server. CLAUDE.md explicitly prohibits using these skills when the MCP server is active.

## Blockers

- None. All infrastructure work shipped and verified.

## Next

- #138: implement create-issue --capture mode (fast intake, no DoD required, Status: Backlog). v3.0.0 is --execute only.
- #138: build triage-promote skill (reads Backlog ticket, asks 3 questions, rewrites to Execution template, moves to Ready).
- #138: add session_open gate - halt if focal ticket is Capture tier, run triage-promote first.
- #139: LinkedIn post publish (post draft + carousel ready, needs persona review then publish).
- sprint_board.py: paginate beyond 100 items (board has >100 items, query truncates).