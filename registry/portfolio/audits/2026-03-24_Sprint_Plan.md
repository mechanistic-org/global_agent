# Sprint Plan — 2026-03-24
> Generated: 2026-03-24T11:06 PDT | Source: Live GitHub API + board audit
> Focus: Infrastructure prereqs, fix recurring DX pain, mandatory order-of-operations to unlock subsequent work.

---

## ✅ Session Accomplishments (2026-03-24 — Session 7)
- **`[global_agent#81](https://github.com/mechanistic-org/global_agent/issues/81) CLOSED`** — Untracked `.chroma_db` from git to fix hanging pushes; enforced sequential execution in `session_close` workflow to prevent SQLite lock.
- **`[global_agent#63](https://github.com/mechanistic-org/global_agent/issues/63) CLOSED`** — Reseeded ChromaDB natively from registry docs (30 items).
- **`[global_agent#70](https://github.com/mechanistic-org/global_agent/issues/70) CLOSED`** — Added auto-refresh to `diag.py` to prevent stale GWS OAuth tokens blocking sessions.
- **`[global_agent#64](https://github.com/mechanistic-org/global_agent/issues/64) CLOSED`** — Replaced hardcoded paths with `$ENOS_ROOT` in `mcp_registry_server.py`.
- **Board Triage** — Bumped MO#8 and hyphen#7 to `Ready` via GraphQL mutations to bypass missing `gh` functionality.

---

## 🧠 Situational Awareness

### What shipped last session (Session 6 — #73)
- `webhook_daemon.py` (FastAPI + HMAC) — live at `hooks.mechanistic.com`
- Cloudflare Tunnel wired. GitHub webhook registered. E2E test: `/execute` comment → HMAC validated → SIMULATION: `docker run nanoclaw:latest` ✅
- `registry/.chroma_db/` was committed to git (problem — see Wave 0 below)
- `SentenceTransformerEmbeddingFunction` cold-start removed from `mcp_registry_server.py`

### Board Status Audit
The live board (`gh project item-list 5`) is stale — it only surfaced 3 Backlog items, missing most of the sprint cache. **MO#8 and hyphen#7 need manual status bumps to `Ready`.**

---

## 🔥 WAVE 0 — Structural Fixes (No New Features Until These Are Done)

> These are blocking mistakes that cost 10–30+ minutes per session and corrupt the git history. Execute in strict order.

| # | Issue | What | Why It Hurts |
|---|---|---|---|
| 1 | [global_agent#81](https://github.com/mechanistic-org/global_agent/issues/81) | ~~**Fix `.gitignore` — exclude `registry/.chroma_db/`**~~ | Git is tracking a SQLite binary. Every push/pull includes 80MB+ of ChromaDB state. Kills push time, corrupts history. |
| 2 | [global_agent#81](https://github.com/mechanistic-org/global_agent/issues/81) | ~~**ChromaDB SQLite lock fix — sequential session_close steps**~~ | `mine_session.py` + `push_forensic_doc` race on the same SQLite WAL → session_close hangs 10–30 min. Option 1: run sequentially. |
| 3 | [global_agent#63](https://github.com/mechanistic-org/global_agent/issues/63) | ~~**Seed ChromaDB from scratch after gitignore fix**~~ | After untracking `.chroma_db/`, reseed from `forensic_telemetry` registry docs. Document the init command. |
| 4 | [global_agent#70](https://github.com/mechanistic-org/global_agent/issues/70) | ~~**GWS OAuth auto-refresh in `diag.py`**~~ | Every session open requires manual `gws auth login`. Blocks GWS MCP tools 100% of the time at session start if token is stale. |
| 5 | [global_agent#64](https://github.com/mechanistic-org/global_agent/issues/64) | ~~**Define `$ENOS_ROOT` — replace hardcoded `D:\GitHub\global_agent` paths**~~ | Scripts break on any other machine / path. Portability prereq for Docker/NanoClaw. |

### Wave 0 Execution Order
```
1. git rm -r --cached registry/.chroma_db/
2. Add registry/.chroma_db/ to .gitignore
3. git commit "fix: untrack chroma_db from git — gitignore + cache clear"
4. Fix session_close: make mine_session.py run BEFORE push_forensic_doc (sequential)
5. Add $ENOS_ROOT to system env + patch scripts/diag.py, mcp_registry_server.py
6. Patch diag.py: call `gws auth refresh` before reporting ❌ on GWS OAuth
7. Reseed ChromaDB: run mcp_registry_server.py seed command
```

---

## 🟠 WAVE 1 — Model Efficiency & Cold Start (Fix The 10-Minute Tax)

> Ollama re-downloads and model cold starts are burning 10+ minutes per session. Fix the keepalive and pin the models.

| # | Issue | What | Cost |
|---|---|---|---|
| 1 | *(new)* | **Pin Ollama model keepalive in NSSM/startup** | `ollama run qwen2.5-coder:32b --keepalive -1` is run manually every session. Wire it to NSSM as an always-on service alongside the daemon. |
| 2 | *(new)* | **Ollama model manifest — document pinned model set** | No canonical list of what models should be resident in VRAM. Agents spin up random models then the right one isn't loaded. Document: `qwen_coder`, `deepseek_r1_14b`, `phi3` → `laws/law_005_model_roster.md` |
| 3 | [global_agent#55](https://github.com/mechanistic-org/global_agent/issues/55) | **Stratified Intelligence Indexing — PROJECT_INTELLIGENCE.md per project** | Without per-project context files, every agent session requires a full ChromaDB query cold start. Static `PROJECT_INTELLIGENCE.md` files give instant context without model warm-up. |

### Wave 1 Execution Order
```
1. Add `ollama run qwen2.5-coder:32b --keepalive -1` to NSSM service config (alongside daemon)
2. Document pinned model roster → laws/law_005_model_roster.md
3. Scaffold PROJECT_INTELLIGENCE.md for global_agent + portfolio (high-value first)
```

---

## 🟡 WAVE 2 — Sprint Board Fix (Make `session_open` Actually Work)

> The board is surfacing 3 items when there are 30+. The `query_sprint_board` MCP tool is the permanent fix. Until then, manual bumps.

| # | Issue | What |
|---|---|---|
| 1 | **Manual: Bump MO#8 → `Ready`** | `[Deploy] Holy Grail v32 → mo.mechanistic.com Migration + CF Access Update` |
| 2 | **Manual: Bump hyphen#7 → `Ready`** | `[Security] Add CF Access to hyphen.mechanistic.com` |
| 3 | [global_agent#65](https://github.com/mechanistic-org/global_agent/issues/65) | **`query_sprint_board` MCP tool** — GraphQL-backed live board read → auto-generates Sprint_Plan.md. Eliminates manual plan caching forever. |

### Wave 2 Execution Order
```
1. gh project item-edit ... --status "Ready" for MO#8 and hyphen#7
2. Implement global_agent#65: query_sprint_board MCP tool
3. Wire to session_open workflow step 1
```

---

## 🔵 WAVE 3 — Platform Stability P0s (Deploy-Blocked Items)

> These are blocking real deployments. MO and hyphen are prod items that need to ship.

| # | Issue | Title | Repo |
|---|---|---|---|
| P0 | [MO#8](https://github.com/mechanistic-org/MO/issues/8) | **[Deploy] Holy Grail v32 → mo.mechanistic.com Migration + CF Access** | MO |
| P0 | [hyphen#7](https://github.com/mechanistic-org/hyphen/issues/7) | **[Security] Add CF Access Protection to hyphen.mechanistic.com** | hyphen |
| P1 | [global_agent#54](https://github.com/mechanistic-org/global_agent/issues/54) | **R2 Endpoint Standardization — Custom Domains, CORS, Public URL Audit** | global_agent |

---

## 🟢 WAVE 4 — Core Agent Infrastructure (Mandatory Before NanoClaw)

> These unlock async/ephemeral container work. Must be done in order.

| # | Issue | Title | Prereq For |
|---|---|---|---|
| 1 | [global_agent#47](https://github.com/mechanistic-org/global_agent/issues/47) | **Persistence & Auto-Boot Architecture ("Always On" Router)** | NanoClaw, webhook_daemon as NSSM service |
| 2 | [global_agent#61](https://github.com/mechanistic-org/global_agent/issues/61) | **NanoClaw Ephemeral Container Layer — Dockerfile + run_agent.py** | ingest_watchdog, R2 events |
| 3 | [global_agent#67](https://github.com/mechanistic-org/global_agent/issues/67) | **ingest_watchdog.py — local inbox auto-routes to ChromaDB via NanoClaw** | Depends on #61 |
| 4 | [global_agent#68](https://github.com/mechanistic-org/global_agent/issues/68) | **R2 Event Notification → CF Worker → asset ledger auto-update** | Depends on #61 + CF tunnel |
| 5 | [global_agent#51](https://github.com/mechanistic-org/global_agent/issues/51) | **[Epic] Pillar 1: GitHub-Driven Agent Lifecycles** | Full autonomous loop |

### Wave 4 Dependency Graph
```
Wave 0 (gitignore + env) 
  └─► Wave 1 (model keepalive)
       └─► global_agent#47 (NSSM auto-boot)
            └─► global_agent#61 (NanoClaw Dockerfile)
                 ├─► global_agent#67 (ingest_watchdog)
                 └─► global_agent#68 (R2 events)
                      └─► global_agent#51 (GitHub-Driven Lifecycles — full loop)
```

---

## 🟣 WAVE 5 — LinkedIn & Content OS

> Lower urgency than infrastructure, but high ROI. Do these during low-energy sessions or in parallel with waiting on deploys.

| # | Issue | Title |
|---|---|---|
| 1 | [global_agent#80](https://github.com/mechanistic-org/global_agent/issues/80) | **`/publish_post` Ritual — Registry Schema Enforcement** |
| 2 | [global_agent#79](https://github.com/mechanistic-org/global_agent/issues/79) | **LinkedIn Thread Orchestration — Arc, Persona, Cross-Link Strategy** |
| 3 | [global_agent#74](https://github.com/mechanistic-org/global_agent/issues/74) | **PRD Structural Generator & Linter (`mcp_prd_linter`)** |
| 4 | [global_agent#75](https://github.com/mechanistic-org/global_agent/issues/75) | **Deterministic FMEA Generator & Matrix RPN Calculator** |

---

## ⚪ BACKLOG — High Value, No Immediate Blocker

| Issue | Title | Repo |
|---|---|---|
| [portfolio#53](https://github.com/mechanistic-org/portfolio/issues/53) | Legacy Portfolio Cleanup | portfolio |
| [portfolio#59](https://github.com/mechanistic-org/portfolio/issues/59) | Pre-commit Zod schema validator | portfolio |
| [portfolio#60](https://github.com/mechanistic-org/portfolio/issues/60) | Pagefind static search | portfolio |
| [global_agent#49](https://github.com/mechanistic-org/global_agent/issues/49) | SKILL.md Drift — Agent Tool Submodule Versioning | global_agent |
| [global_agent#69](https://github.com/mechanistic-org/global_agent/issues/69) | Client-facing deliverable sanitizer → PDF → GWS SA email | global_agent |
| [portfolio#47](https://github.com/mechanistic-org/portfolio/issues/47) | [Epic] Resume the C\|24 Component Stitch Loop | portfolio |
| [MO#1](https://github.com/mechanistic-org/MO/issues/1) | [Epic] Mobile Outfitters Clone-and-Purge Extraction | MO |

---

## 🚀 Session Start Protocol

```
/session_open → diag.py → pick ONE ticket from Wave 0 or Wave 3
```

**Current recommended pick:** Wave 0 Step 1 — fix `.gitignore` + untrack `.chroma_db/`.
This unblocks git, stops the push timeout, and takes < 15 minutes.
