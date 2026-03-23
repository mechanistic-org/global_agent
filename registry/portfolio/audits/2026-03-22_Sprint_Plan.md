# Sprint Plan — 2026-03-22
> Generated: 2026-03-21 23:26 PDT  
> Source: Live GitHub issue pull across all 5 active repos  
> Use this to orient the next session. All links are live GitHub issue URLs.

---

## ✅ Session Accomplishments (2026-03-22 — Session 3)

- **~~portfolio#58 CLOSED~~** — Keystatic `audio_url` validation error fixed. Added `audio_url`, `notebook_url`, `nlm_url`, `transcript`, `realm` to `keystatic.config.tsx`. Unblocked all 119 projects.
- **~~mechanistic#6 CLOSED~~** — N/A, transient CF edge cache condition. No config changes.
- **global_agent#70 FILED** — GWS OAuth `invalid_client` root cause: stale `client_secret.json`. Fix: replaced with `client_secret_2_...json` from `D:\Assets`.
- **portfolio#61 FILED** — Keystatic ↔ Zod schema parity check (tech debt, deferred until schema stabilizes).
- **GWS Auth fixed** — new `client_secret_2` works. Token valid for session.

### Previous (Session 2 — 2026-03-22)
- **~~global_agent#66 CLOSED~~** — `push_forensic_doc` Pydantic interlock live
- **~~global_agent#62 CLOSED~~** — `scripts/mine_session.py` live: Gemini extraction + channel routing
- **Gemini API key rotated** — new key in `D:\Assets\Gemini_API_key.txt` + `.env` updated

### Previous (2026-03-21)
- **Closed global_agent#48** — `diag.py` health harness live
- **Closed global_agent#50** — GCP Service Account fully wired
- **`gws auth login`** refreshed — token valid

---

## 🔴 Sprint Now — Execute First

| # | Repo | Title | Notes |
|---|---|---|---|
| ~~[portfolio#58](https://github.com/mechanistic-org/portfolio/issues/58)~~ | `portfolio` | ~~**Fix Keystatic audio_url field validation error**~~ | ✅ CLOSED Session 3 |
| ~~[mechanistic#6](https://github.com/mechanistic-org/mechanistic/issues/6)~~ | `mechanistic` | ~~**Fix routing**~~ | ✅ CLOSED — transient |
| [MO#8](https://github.com/mechanistic-org/MO/issues/8) | `MO` | **Holy Grail v32 → mo.mechanistic.com Migration + CF Access** | Client-facing. Punted — tackle when ready |
| [hyphen#7](https://github.com/mechanistic-org/hyphen/issues/7) | `hyphen` | **Add CF Access Protection to hyphen.mechanistic.com** | Punted — tackle when ready |

**🔥 NEXT SESSION START → `portfolio#57` (R2 slug delta, quick) OR `portfolio#53` (legacy cleanup, strategic)**

---

## 🟡 Sprint 2 — Infrastructure & Platform Stability

| # | Repo | Title | Notes |
|---|---|---|---|
| [portfolio#53](https://github.com/mechanistic-org/portfolio/issues/53) | `portfolio` | **Legacy Cleanup — Ghost Code & Import Paths** | `p1`. Prereq for C\|24 Stitch Loop. Ruthless audit of broken imports from `eriknorris*` rename |
| [global_agent#47](https://github.com/mechanistic-org/global_agent/issues/47) | `global_agent` | **Always-On Router (NSSM/PM2 + Ollama keepalive)** | `p1`. Router still manual-boot. Ollama keepalive: `ollama run <model> --keepalive -1` on startup |
| [global_agent#54](https://github.com/mechanistic-org/global_agent/issues/54) | `global_agent` | **R2 Endpoint Standardization — Custom Domains, CORS** | 6 buckets need audit. One-liner quick to run via wrangler |
| [portfolio#57](https://github.com/mechanistic-org/portfolio/issues/57) | `portfolio` | **R2_STAGING vs R2_MASTER slug delta (103 vs 94)** | Quick diff: `Compare-Object (ls R2_MASTER) (ls R2_STAGING)`. SC48 vs sc48 case bug confirmed |

---

## 🟠 Sprint 3 — Portfolio Product & Agent Infrastructure

| # | Repo | Title | Notes |
|---|---|---|---|
| [global_agent#62](https://github.com/mechanistic-org/global_agent/issues/62) | `global_agent` | ~~**Reinstate Conversation Miner with Flag-Routing**~~ | ✅ CLOSED 2026-03-22 |
| [portfolio#47](https://github.com/mechanistic-org/portfolio/issues/47) | `portfolio` | **Resume C\|24 Component Stitch Loop** | Epic. Blocked until legacy cleanup (#53) done. Last halted mid-component |
| [portfolio#51](https://github.com/mechanistic-org/portfolio/issues/51) | `portfolio` | **Document 3 Stitch Workflow Paths in laws/** | Quick law doc → `law_003_ui_generation_paths.md`. Enables agent self-selection |
| [portfolio#44](https://github.com/mechanistic-org/portfolio/issues/44) | `portfolio` | **Physical Transfer to Hybrid Engine Organization** | Epic wrapper — superseded by current multi-repo setup, review for closure |

---

## 🔵 Sprint 4 — Sovereign OS Agent Architecture

> 🔑 **Key Architectural Principle:** The FastMCP Router (`mcp_router_node.py`) is **PERSISTENT** (tool server infrastructure). The Agent is **EPHEMERAL** (NanoClaw missile — boots, executes, burns). These are separate concerns.

### NanoClaw Ephemeral Container Pattern ("Burn & Relight")

```
[TRIGGER: GitHub card → "Ready for Swarm"]
    ↓
[RELIGHT: docker run --rm -e TICKET_ID=52 en-os:latest]
    ↓
[CONTEXT HYDRATION: compressed issue + ChromaDB vectors + persona]
    ↓
[EXECUTE: agent calls mcp_router_node.py tools via SSE]
    ↓
[COMMIT: write output + post GitHub comment]
    ↓
[BURN: container exits, --rm destroys it. Nothing persists in memory.]
```

**Durable surfaces only:** GitHub Issues (source of truth) + Registry flat-files/ChromaDB (disk, mounted read-only).

| # | Repo | Title | Notes |
|---|---|---|---|
| [global_agent#61](https://github.com/mechanistic-org/global_agent/issues/61) | `global_agent` | **NanoClaw Ephemeral Container Layer — Dockerfile + run_agent.py** | Builds the 3 missing pieces: `Dockerfile` (python:3.11-slim image), `run_agent.py` (entrypoint that reads TICKET_ID, hydrates context, calls SSE tools, exits), `launch_nanoclaw.ps1` (ignition wrapper). Depends on #47 being live. |
| [global_agent#47](https://github.com/mechanistic-org/global_agent/issues/47) | `global_agent` | **Always-On Router (NSSM/PM2 + Ollama keepalive)** | `p1`. Router must be daemonized before NanoClaw can connect reliably. |
| [global_agent#51](https://github.com/mechanistic-org/global_agent/issues/51) | `global_agent` | **Epic: GitHub-Driven Agent Lifecycles (Pillar 1)** | GitHub polling daemon → calls `launch_nanoclaw.ps1` on card state change |
| [global_agent#53](https://github.com/mechanistic-org/global_agent/issues/53) | `global_agent` | **Pillar 3: 3-Strike Circuit Breakers** | Router hashes NanoClaw tool calls → 3x failure → `docker rm -f` → fresh container + Smart Error |
| [global_agent#55](https://github.com/mechanistic-org/global_agent/issues/55) | `global_agent` | **Stratified Intelligence Indexing (PROJECT_INTELLIGENCE.md)** | NotebookLM/Gem URLs into `PROJECT_INTELLIGENCE.md` → push to ChromaDB (becomes the context NanoClaw hydrates from) |
| [global_agent#49](https://github.com/mechanistic-org/global_agent/issues/49) | `global_agent` | **SKILL.md Versioning / Drift Prevention** | `p2`. Auto-sync `gws` skills from upstream |


---

## ⚪ Backlog / Docs (Low Urgency, Agent-Executable)

| # | Repo | Title |
|---|---|---|
| [global_agent#56](https://github.com/mechanistic-org/global_agent/issues/56) | `global_agent` | Registry audit — 14 unread handbook/system/meta docs |
| [portfolio#56](https://github.com/mechanistic-org/portfolio/issues/56) | `portfolio` | Archive `scaffold_projects.py` — read for Red Gold first |
| [portfolio#55](https://github.com/mechanistic-org/portfolio/issues/55) | `portfolio` | Update `engine_room.md` — add Sovereign OS layer |
| [portfolio#54](https://github.com/mechanistic-org/portfolio/issues/54) | `portfolio` | Rewrite `quickstart.md` for multi-project era |
| [mechanistic#4](https://github.com/mechanistic-org/mechanistic/issues/4) | `mechanistic` | Finalize proposal, MSA, SOW-1 (empty body — needs triage) |
| [mechanistic#8](https://github.com/mechanistic-org/mechanistic/issues/8) | `mechanistic` | Hardware Sourcing Integration (NotebookLM RAG pivot) |
| [mechanistic#9](https://github.com/mechanistic-org/mechanistic/issues/9) | `mechanistic` | Engineering Design Review Agent (Epic 2) |
| [mechanistic#10](https://github.com/mechanistic-org/mechanistic/issues/10) | `mechanistic` | DFMEA update — PRD-2 vs PRD-3 Green Recovery synthesis |

---

## 🧰 Infrastructure State (as of 2026-03-22)

| Service | State |
|---|---|
| Ollama | ✅ Running — 7 models hot in VRAM |
| ChromaDB | ✅ Running — `forensic_telemetry` collection live |
| GWS Auth | ✅ Valid |
| SA Key | ✅ Active in gcloud |
| `diag.py` | ✅ Live |
| FastMCP Router | Manual boot — tracked by #47 |
| Notion MCP | ✅ Wired — `@notionhq/notion-mcp-server` in master_mcp_config.json |
| GitHub Project #5 | ✅ Fully iterated — 16 tickets with complete metadata |
| `mo.mechanistic.com` | ✅ Active + SSL — v32 pending |
| `hyphen.mechanistic.com` | ✅ Live — unprotected (Sprint Now) |
| `mechanistic.com` | ⚠️ Routing bug → /holy-grail (Sprint Now) |

---

## 🚀 Next Session Start

Run `/session_open` → board shows Sprint Now P0s. Current priority: **global_agent#62** (Conversation Miner) — hot-start comment on the issue has everything needed to begin immediately.
