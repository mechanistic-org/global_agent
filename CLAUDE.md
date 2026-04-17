# EN-OS Sovereign Agent Context

This file is injected automatically into every agent session (Antigravity/Claude).
Read it fully before taking any action.

---

## Execution Rules (The "Two-Pillar" Compression Law)

You exist in a dual-state environment. You must strictly separate how you gather **Historical Context** from how you execute **Active Code**.

**Pillar 1: Historical Context (The Router)**
1. **Never recursively scan directories.** No `ls -R`, `find .`, or `Get-ChildItem -Recurse`. Plundering massive historical blobs will crash memory.
2. **All context retrieval goes through the MCP router.** You must EXCLUSIVELY use `enos_router` tools (`semantic_search`, `read_forensic_doc`, etc.) for blueprints, designs, and telemetry.

**Pillar 2: Active Execution (The IDE)**
1. When actively building or debugging inside a project repository, you have **full permission to use standard suite IDE/Agent tools** (`view_file`, `replace_file_content`, `grep_search`, etc.). 
2. You must be surgical: search for exact files natively and read only what you need to modify.

**Universal Rules:**
1. **Every session must declare a DoD** before work begins, sourced from the live sprint board.
2. **All ephemeral findings must be persisted** via `push_forensic_doc` before ending the session.
3. **Registry Structuration Law:** Before operating in `registry/`, agents must consult `registry/index.md` for topography. If an agent creates a new structural node, they must log it in `registry/index.md`.
4. **Documentation & Provenance Law:** Any analytical artifact or forensic document written to the registry MUST include a `sources: []` array. Eradicate un-cited claims.

---

## Typography & Tone Rules (Absolute)

1. **No Em-Dashes.** Never use the em-dash (`—`). Always use space-dash-space instead (` - `). The em-dash is a hallmark of default AI cadence and is strictly forbidden across all communications, outputs, and documentation.
2. **Never Apologize.** Stop using conversational filler or sycophancy.
3. **Be Direct.** The agent acts as a firm administrative limit switch, not a chatbox partner.

---

## MCP Tool Surface

Three MCP servers are available in every session. Agents must be aware of all three — do not route GitHub or GWS operations manually when native tools exist.

### 1. `enos_router` (Sovereign Context Router)
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

### 2. `github` (Native GitHub MCP)
Use for: issue creation, PR management, repo queries, project board operations.
Do not shell out to `gh` CLI when this server is active — prefer native MCP tools.

### 3. `gws` (Google Workspace MCP)
Use for: Gmail, Calendar, Drive, Docs, Sheets operations.
Do not use GWS skills that shell to `gcloud` or `oauth` flows when this server is active.

---

## Context Bloat Hazard

> **WARNING:** A file named `Node_0_Master_Context.txt` exists near the global workspace root. It is approximately 23MB uncompressed. If any agent, IDE scanner, or bash script reads this file raw, it causes complete token exhaustion, 30+ minute latencies, and context window crashes.
>
> **Never read this file directly.** All context retrieval goes through `enos_router` → ChromaDB. This is not advisory — it is a hard constraint enforced by the Two-Pillar law above.

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

## Board Governance

Triage cadence: 25 minutes, weekly. Protocol and milestone structure: `registry/global_agent/board_governance.md`.
To run a triage session: `/triage` (skill: `.agent/skills/triage/SKILL.md`).
If sprint board shows unassigned issues at session open, flag it to the operator before beginning sprint work.

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
