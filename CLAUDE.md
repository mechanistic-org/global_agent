# EN-OS Sovereign Agent Context

This file is injected automatically into every Claude Code session.
Read it fully before taking any action.

---

## Execution Rules (Absolute)

1. **Never recursively scan directories.** No `ls -R`, `find .`, or `Get-ChildItem -Recurse`.
2. **All context retrieval goes through the MCP router.** The `enos_router` is at `http://127.0.0.1:8000/mcp`.
3. **Every session must declare a DoD** before work begins, sourced from the live sprint board.
4. **All ephemeral findings must be persisted** via `push_forensic_doc` before ending the session.

---

## MCP Router Tools

Connect via: `claude mcp add --transport http enos_router http://127.0.0.1:8000/mcp`

| Tool | Use |
|---|---|
| `semantic_search` | Conceptual / thematic context from ChromaDB |
| `search_registry` | Find structural layouts and active markdown docs |
| `read_forensic_doc` | Exact flat-file retrieval (registry-scoped only) |
| `push_forensic_doc` | Persist findings into ChromaDB + flat-file registry |
| `read_design_system` | Retrieve law_002_design_system.md (Dark Hangar aesthetic) |
| `router_health_check` | Verify SSE daemon is alive |
| `patch_astro_component` | AST surgical patcher for Astro components |

If the router is unreachable: `pm2 restart enos-router` from `D:\GitHub\global_agent`.

---

## Repository Map

| Repo | Role |
|---|---|
| `D:\GitHub\global_agent` | Core brain — registry, router, orchestrators |
| `D:\GitHub\hyphen` | Active client — Hyphen LID (Astro + Cloudflare) |
| `D:\GitHub\mechanistic` | Truth engine — architectural history + constraints |
| `D:\GitHub\portfolio` | Proof-of-work — Portrait API + diagnostic terminal |

---

## Session Ritual

1. Call `router_health_check` → confirm online
2. Run `python D:\GitHub\global_agent\scripts\sprint_board.py --current-iteration`
3. State: **Session scope: [repo]#[number] — [title]** + **DoD: [one sentence]**
4. Begin work only after step 3 is confirmed

---

## Local Model Routing

```
ANTHROPIC_BASE_URL=http://localhost:11434
ANTHROPIC_AUTH_TOKEN=ollama
```

Recommended model selection:
- `qwen2.5-coder:32b` — daily coding, feature work
- `deepseek-r1:32b` — hard problems, architecture, complex debugging
- `claude-...` (cloud) — visual review, strategic reasoning, when reasoning quality matters more than cost

---

## Design Law

All UI work must comply with the Dark Hangar aesthetic. Before touching any UI:
```
Call: read_design_system
```
No generic colors. No MVPs. No Bootstrap templates.
