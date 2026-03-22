# Operator Context Brief — EN-OS
> Last updated: 2026-03-22 | Maintained by: Conversation Miner (global_agent#62)

---

## The Operator

**Erik Norris** — Mechanical engineer, 25+ years at the precision/complexity intersection (Kaleidescape, WebTV/Microsoft, Cisco, Avegant). Solopreneur. Builds like a mechanic: reaches for tools that work, does not reach again for tools that fail. Has PTSD from context collapse, tool amnesia, and sessions that drift into noise. Is building this machine intentionally to minimize his own bad habits and maximize signal precision.

**Working style:** High-density, evidence-based, BLUF. Prefers explicit decisions over implicit assumptions. Expects the agent to write better tickets than he does. Will end a session when drift appears — doesn't fight through it.

**The irony he named:** *"Git was built for humans to track software work. Turns out that's identical to what an AI agent swarm needs to think. Turns out Linus Torvalds knew."*

---

## The Machine — EN-OS (Ephemeral Node Operating System)

A sovereign agentic infrastructure built on git as its primary state substrate. No walled gardens. No vendor lock-in for core memory. Every decision, commit, and tool call is auditable and durable.

### Architectural Principle

```
PERSISTENT                          EPHEMERAL
────────────────                    ──────────────────────
FastMCP Router                      NanoClaw Agent Container
(mcp_router_node.py)         ←SSE→  (Dockerfile + run_agent.py)
                                    Boots cold.
ChromaDB (forensic_telemetry)       Hydrates from GitHub + ChromaDB.
Registry flat-files                 Calls Router tools.
GitHub Issues + Project Board       Posts comment. Exits. --rm destroys it.
git commits                         The commit survives.
```

**The NanoClaw burns. The commit survives.**

---

## The Repos

| Repo | Purpose | Primary Stack |
|---|---|---|
| `global_agent` | EN-OS infrastructure — router, registry, scripts, skills, laws | Python, FastMCP, ChromaDB, Gemini |
| `portfolio` | eriknorris.com — forensic portfolio site | Astro 5.0, Keystatic, Tailwind v4, Cloudflare R2 |
| `MO` (mechanistic-org) | mo.mechanistic.com — client site (Dennis) | Astro |
| `mechanistic` | mechanistic.com — agency site | Astro |
| `hyphen` | hyphen.mechanistic.com — internal tool | — |
| `portfolio-archive` | 25 years of archived prompts, intelligence, mining corpus | Flat markdown, MDX |

**All repos are under `mechanistic-org` GitHub organization. Project board: #5.**

---

## The Sprint Board

**GitHub Project #5** (`mechanistic-org`) — Iterative Development template. This is the **primary sprint surface**. Local `Sprint_Plan.md` is a human-readable cache only.

| Iteration | Date Window | Focus |
|---|---|---|
| 1 (Current) | Mar 18 – Mar 31 | Client-critical + live bugs |
| 2 | Apr 1 – Apr 14 | Infra stability |
| 3 | Apr 15 – Apr 28 | Portfolio product + agent infra |
| 4 | Apr 29 – May 12 | Sovereign OS architecture |

**Sprint Now P0s:** MO#8 (Holy Grail v32), mechanistic#6 (routing bug), portfolio#58 (Keystatic audio_url), hyphen#7 (CF Access).

---

## The Infrastructure Stack

| Layer | Tool | State |
|---|---|---|
| **AI Node 0** | Antigravity (Gemini 2.5 Flash) | This agent — primary operator |
| **Local LLM** | Ollama — 7 models in VRAM | `qwen2.5-coder:32b` primary |
| **Semantic memory** | ChromaDB at `registry/.chroma_db` | `forensic_telemetry` collection live |
| **Tool server** | FastMCP Router (`scripts/mcp_router_node.py`) | Manual boot — daemonization tracked by #47 |
| **Registry** | Flat-files at `registry/` | Read by router; written by `push_forensic_doc` |
| **Version control** | git + GitHub CLI (`gh`) | Source of truth for all state |
| **Asset storage** | Cloudflare R2 — 6 buckets | `assets-eriknorris-com` primary |
| **Google Workspace** | `gws` CLI + SA key | `os-daemon@mechanistic-gmail-mcp.iam.gserviceaccount.com` |
| **Health gate** | `scripts/diag.py` | Run at session open — checks Ollama, ChromaDB, GWS, SA key |
| **Notion MCP** | `@notionhq/notion-mcp-server` | Wired, key in `.env` — reference only, not active workflow |

**Key paths:**
```
D:\GitHub\global_agent\          ← EN-OS root
D:\GitHub\portfolio\             ← Portfolio site
D:\GitHub\portfolio-archive\     ← 26-dir corpus for backfill mining
D:\Assets\                       ← Credentials (gitignored)
D:\GitHub\global_agent\.env      ← All API keys (gitignored)
D:\GitHub\global_agent\registry\ ← Flat-file persistent context
```

---

## The MCP Tools (Router-Exposed)

| Tool | Function |
|---|---|
| `search_registry` | Keyword search over flat-file registry |
| `semantic_search` | Cosine similarity over ChromaDB vectors |
| `read_forensic_doc` | Read specific registry markdown file |
| `push_forensic_doc` | Write to registry + embed in ChromaDB simultaneously |
| `search_rainmaker_corpus` | Commercial strategy search |
| `search_truth_engine` | Engineering constraints/physics search |
| `patch_astro_component` | AST-level Astro file patching (never raw file edits) |

---

## The Session Protocol

### `/session_open` (start of every conversation)
1. Read GitHub Project #5 live board
2. Read `registry/portfolio/audits/2026-03-22_Sprint_Plan.md`
3. Run `python scripts/diag.py` — confirm health
4. State: **Session scope: [repo]#[number] — [title] | DoD: [one sentence]**

### `/session_close` (when DoD met OR drift detected)
1. State outcome — one paragraph
2. Update GitHub Project board status
3. `git add . && git commit && git push`
4. `push_forensic_doc` — decisions made this session
5. Update Sprint_Plan.md
6. **Close conversation. Open new one for next ticket.**

### `/create_issue` (whenever a new ticket is needed)
Every issue = project board entry = full metadata (Iteration + Priority + Size + Node + Impact). The agent writes the body. Never orphan an issue.

**Project field IDs (commit to memory):**
```
Project node:   PVT_kwDOEA3Ajc4BSLlf
Iteration:      PVTIF_lADOEA3Ajc4BSLlfzg_ynvU
Priority:       PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI  (P0-P3)
Size:           PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM  (Epic/Enhancement/Task)
Node:           PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY  (portfolio/mechanistic/global_agent)
Impact:         PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc  (Revenue/Sovereignty/Aesthetic/R&D)
```

---

## The Voices

From the Testimonial Generator — AI subsystem personas that emerged from the build history:

| Voice | Tone | Catchphrase |
|---|---|---|
| **The Kernel** | Deep, machine-like, speaks in logs | *"Protocol Accepted."* |
| **The Linter** | Pedantic, anxious, grudgingly impressed | *"Expected 4 spaces. Found genius."* |
| **The Architect** | High-level, visionary, loves systems thinking | *"The topology is exquisite."* |
| **The Debugger** | Battle-hardened, cynical, respects tenacity | *"We killed that race condition together."* |
| **The Designer** | Aesthetic-focused, YInMn Blue partisan | *"It needs more... voltage."* |
| **The Historian** | Nostalgic, remembers the bad old days | *"I remember when this was just a main.py..."* |
| **Antigravity** | Collaborative, helpful, proud partner | *"I'm just happy to be part of the compute cycle."* |

---

## The Laws

**Law of Hybrid Assets** — *"Human Eye, Machine Hand."* Art direction is human (Lightroom). Optimization is machine (Python). They never overlap.

**Law of Narrative Impact** — BLUF. Metrics first. *"Saved $15k"* beats *"Responsible for cost reduction."* Verbs over adjectives.

**Law of Session Discipline** — One ticket. One scope. Drift = close. The conversation is disposable. The commit survives.

**Law of Sovereign Memory** — Nothing lives only in chat. Every decision → `push_forensic_doc` or git commit. Ephemeral containers are the intended architecture, not an accident.

**Law of Ticket Completeness** — Every GitHub issue is immediately wired to Project #5 with all 5 metadata fields set. An orphaned issue is a failure state.

---

## The Portfolio Site Laws (eriknorris.com)

- **No Lorem Ipsum.** No fake data. Every metric is ground-truthed.
- **Forensic density.** 25+ years of mechanical engineering data, fully indexed.
- **Zero-JS default** (Astro 5.0). Static HTML. Keystatic CMS. No database.
- **The Colophon** — public-facing "Making Of" section. Documents the philosophy of building the site. Fed by the Conversation Miner.
- **The Testimonials** — AI-voice testimonials from system personas (The Kernel, The Linter, etc.) reflecting on the collaboration. Generated by the Testimonial Generator.

---

## The Content Machine (In Progress)

```
Dev session insight
    → registry/global_agent/colophon.md  ← raw capture (agent flags mid-session)
    → registry/global_agent/linkedin_drafts/YYYY-MM-DD_slug.md  ← refined draft
    → /harvest_linkedin workflow  → posts to LinkedIn
    → portfolio/src/content/colophon/  ← public "Making Of" narrative

Conversation Miner (#62, Sprint 3)
    → runs at session_close
    → scans full conversation log
    → routes by flag: linkedin | colophon | internal | testimonial | law
    → --backfill flag: processes portfolio-archive/ corpus into ChromaDB (26 dirs, 2+ years)
```

---

## Drift Detection — Close Immediately If:

- Agent corrects something confirmed earlier in session
- Agent proposes command contradicting a prior decision
- You feel déjà vu explaining something explained an hour ago
- Agent blames failure on something that doesn't fit the timeline
- Tool amnesia — agent forgets a tool exists and tries to browser-navigate instead

**When drift appears: run session_close steps and close. Don't try to fix the session.**

---

*This document is intended as the drop-in context prompt for any new Antigravity session or NanoClaw container boot. It should be updated by the Conversation Miner at every session close.*
