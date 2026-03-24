---
title: "Walk Notes — Architectural Review (NanoClaw, State Machine, Cognitive Manufacturing Line)"
date: 2026-03-23
source: walk-notes_architectural-review (Google Drive)
source_folder_id: 18Eqidta-f5gL7jWAImiH2U7pFbwQSEhj
status: processed
tags: [nanoclaw, fastapi, state-machine, prd-linter, fmea, architecture, cognitive-manufacturing]
linked_tickets: ["#73", "#74", "#75", "#61", "#47"]
---

# Walk Notes — Architectural Review
> Source: 6 Google Docs from Drive folder `walk-notes_architectural-review`. Session saved during walk 2026-03-23 evening.

## 1. EN-OS Architecture Review (doc1)

**Triumphs:**
- "The NanoClaw burns. The commit survives." — right philosophy. Durable state in git/GitHub, not the LLM context window.
- Decoupled memory via FastMCP + ChromaDB — context window stays clean; retrieve only what's needed.
- Strict Session Protocols (DoD + bail-out triggers) prevent sunk-cost hallucination loops.

**Blindspots flagged:**
- **Tool Coverage Gap:** No generic file patcher for Python/YAML/config files — agent falls back to prose, violating Machine Hand law. Needs a generic `patch_file` tool alongside `patch_astro_component`.
- **Drift Detection is biological** — relies on operator fatigue. Needs mechanistic circuit breaker: token depth monitor or strict turn/time limit before forced `/session_close`.
- **operator_context_brief.md bloat risk** — as Sprint Board and Content Machine sections grow, agent will begin ignoring laws at bottom. Hard token limit required.

---

## 2. Hired Gun Context v2 — Tactical Priorities (doc2)

### Priority: GitHub Webhook → Local Docker Boot (Pillar 1, #73)
- **Solution:** `cloudflared` tunnel (no local firewall exposure) + lightweight FastAPI daemon
- Daemon validates HMAC, parses issue ID, fires: `subprocess.run(["docker","run","--rm","nanoclaw:latest","--issue",issue_id])`
- Aligns with Always-On Router (#47)

### Problem Space A: PRD Linter (#74)
- `mcp_prd_linter` tool — agent cannot commit a PRD without passing it through the linter first
- Linter checks: frontmatter vs `keystatic.config.tsx`, passive voice, quantifiable metrics, zero-JS compliance
- Hard validation failure returned to agent → iterates until fit

### Problem Space B: FMEA Generator (#75)
- `mcp_fmea_generator` — statically generated markdown FMEA matrix, deterministic RPN math
- Agent handles failure mode ideation (the entropy), tool handles RPN calculation (the constraint)
- Output auto-embedded in ChromaDB via `push_forensic_doc`

### Problem Space C: Colophon Map-Reduce
- **LATER RETRACTED** (see doc3) — the mine_session.py + flat-file colophon.md is already the correct solution

---

## 3. Architectural Correction — Colophon (doc3)
> The Map-Reduce proposal was hallucination of complexity. Violated "Law of Sovereign Memory."

- `mine_session.py` runs at `/session_close`, appends to `registry/global_agent/colophon.md` while context is hot
- Astro renders the living ledger — no additional pipeline needed
- **The constraint cages (PRD Linter + FMEA) are correct** — push constraints to tooling/compilation layer, not prompt layer

---

## 4. Cognitive Manufacturing Line Framework (doc4)

> Stop thinking about this as a software project. Treat EN-OS as a **cognitive manufacturing line**.

### EN-OS as a State Machine
- GitHub Project Board (#5) is the **Control Plane**, not just a tracker
- NanoClaw should never boot without a Git state or Webhook trigger
- NanoClaw should never die without a defined exit code dictating next mechanical action

### Three Pillars of Rigor
**A. The Constraint Cage (Boundary Layer)**
- All constraints pushed to compilation/tooling layer, not prompt layer
- Every FastMCP tool must have Pydantic/Zod input schema
- Hard validation error = tool rejects call, agent forced to retry

**B. Memory Stratification (Memory Bus)**
- Hot: current ticket + Sprint_Plan.md + operator_context_brief.md
- Warm: ChromaDB vector retrieval limited to active project namespace
- Cold: broad commercial strategy corpus — only if explicitly invoked

**C. Automated Circuit Breaker (Drift Detection)**
- NanoClaw needs TTL or token budget
- 3 consecutive linter failures → fatal exception → `/session_close` → registry write → container die
- Do not let the machine spin its wheels

### Engine vs. Spokes
- **Engine (global_agent):** Router, Daemon, Chroma, MCP tools — factory floor only
- **Spokes (portfolio, MO, hyphen):** Source code + Keystatic schemas + Markdown — zero orchestration logic

---

## 5. State Machine Blueprint (doc5)

| State | Name | Trigger | Action | Transitions |
|-------|------|---------|--------|-------------|
| 0 | IDLE_LISTEN | System boot | CF tunnel + FastAPI daemon running | Wait for POST |
| 1 | AUTH_GATE | Incoming payload | HMAC signature verify | PASS→2, FAIL→401→0 |
| 2 | PAYLOAD_PARSE | Payload verified | Parse event type, extract issue# | MATCH→3, IGNORE→200→0 |
| 3 | NANOCLAW_IGNITION | Actionable issue ID | `subprocess.Popen(docker run...)` + 202 return | SPAWNED→4 |
| 4 | COMPUTE_AND_CONSTRAINT | Container running | Agent loop with constraint cages | VALID→5, CIRCUIT_BREAKER→6 |
| 5 | SOVEREIGN_COMMIT | Artifact passes | git commit + push + push_forensic_doc | PERSISTED→6 |
| 6 | CONTAINER_BURN | Done or failure | Exit 0: success comment / Exit 1: failure comment. Docker --rm destroys. | Back to 0 |

**Engineering Rule:** Daemon must never wait for the Docker container. FastAPI returns 202 immediately. NanoClaw is fully detached.

---

## 6. daemon.py Implementation (doc6)

See: `scripts/daemon.py` — Full FastAPI webhook handler with:
- `verify_signature()` — HMAC SHA256 with `hmac.compare_digest()` (prevents timing attacks)
- `ignite_nanoclaw()` — `subprocess.Popen` with `DEVNULL` stdout/stderr (detached, non-blocking)
- Trigger A: manual `/execute` comment on issue
- Trigger B: `projects_v2_item` move to "Sprint Now" status

> **Note:** Project V2 webhooks are GraphQL-backed and complex. The exact JSON traversal to extract issue number from `projects_v2_item` payload may need adjustment after inspecting a raw payload.

---

## Action Items (Linked to Open Tickets)

| Ticket | Action |
|--------|--------|
| [#73](https://github.com/mechanistic-org/global_agent/issues/73) | Wire daemon.py + cloudflared tunnel — the code exists in doc6 |
| [#74](https://github.com/mechanistic-org/global_agent/issues/74) | Build `mcp_prd_linter` — architecture is fully spec'd |
| [#75](https://github.com/mechanistic-org/global_agent/issues/75) | Build `mcp_fmea_generator` — architecture is fully spec'd |
| [#61](https://github.com/mechanistic-org/global_agent/issues/61) | NanoClaw Dockerfile + `run_agent.py` — state machine blueprint is locked |
| [#47](https://github.com/mechanistic-org/global_agent/issues/47) | Always-On Router — daemon.py is Stage 1 of this |
