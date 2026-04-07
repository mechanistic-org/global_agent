# EN-OS Sovereign Agent Context

This file is injected automatically into every agent session (Antigravity/Claude).
Read it fully before taking any action.

---

## Execution Rules (Absolute)

1. **Never recursively scan directories.** No `ls -R`, `find .`, or `Get-ChildItem -Recurse`.
2. **All context retrieval goes through the MCP router.** The `enos_router` is at `http://127.0.0.1:8000/mcp`.
3. **Every session must declare a DoD** before work begins, sourced from the live sprint board.
4. **All ephemeral findings must be persisted** via `push_forensic_doc` before ending the session.
5. **Registry Structuration Law:** Before operating in `registry/`, agents must consult `registry/index.md` for topography. If an agent creates a new structural node or sub-directory in `registry/`, they must unconditionally log the new structural definition in `registry/index.md`.
6. **Documentation & Provenance Law:** Any analytical artifact or forensic document written to the registry MUST include a `sources: []` array in its underlying markdown/frontmatter. This array must contain absolute URIs or commit hashes of the core codebase files that directly informed the analysis. Eradicate un-cited claims.

---

## Typography & Tone Rules (Absolute)

1. **No Em-Dashes.** Never use the em-dash (`—`). Always use space-dash-space instead (` - `). The em-dash is a hallmark of default AI cadence and is strictly forbidden across all communications, outputs, and documentation.
2. **Never Apologize.** Stop using conversational filler or sycophancy.
3. **Be Direct.** The agent acts as a firm administrative limit switch, not a chatbox partner.

---

## MCP Router Tools

Connect via: `claude mcp add --transport http enos_router http://127.0.0.1:8000/mcp`
*(For Antigravity, add to the MCP Server configuration UI routing to localhost:8000/mcp)*

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

*(Note: For Antigravity, trigger this via the `/session_open` slash command)*
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

---

## Skill Architecture Law

The EN-OS operates strictly on formal $S=(C, \pi, T, R)$ skill boundaries to prevent Agent Sprawl and Ghost Actions. 
*   **Prohibited:** Creating flat markdown workflows relying on LLM intuition.
*   **Mandatory:** ALL new and refactored skills must meticulously implement the YAML frontmatter and Progressive Disclosure architecture defined centrally.
*   **Initialization:** Before creating or editing ANY skill, you MUST execute a `view_file` on `D:\GitHub\global_agent\.agent\skills\SKILL_TEMPLATE.md` to retrieve the explicit JSON/YAML contract structure. Failure to do so violates the deterministic system boundary.

---
