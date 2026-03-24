---
title: "AI Architecture Determinism & The Ephemeral Shift"
date: "2026-03-24"
source: "Walk Notes / Voice Session"
source_folder_id: "1T1R3T1mmlv3wZ4Lh7qR6uZt_wjkWO85-"
status: "processed"
tags: ["architecture", "determinism", "FMEA", "LLM-constraints", "content-strategy", "map-reduce"]
linked_tickets: ["#74", "#75"]
---

# 📡 EN-OS ARCHITECTURAL DISPATCH: SOULULAR ALIGNMENT

*Synthesized from Frontier Node (Session #4/5 - March 24, 2026).*

## The Ephemeral Shift — Transitioning from Prompt to Engine Block

We have fundamentally redefined the agent's existence within EN-OS. The system is moving away from the "Good Boy" prompt (relying on polite instructions hoping for strict schema adherence) to deterministic constraints.

1. **The Constraint Cage:** Neural nets are stochastic and sloppy. They will no longer be trusted to output valid PRDs or calculate FMEA matrices independently. We must build physical Go/No-Go gauges (like `mcp_prd_linter`). If the agent generates out-of-spec JSON, the Python runtime will aggressively reject the tool call.
2. **The Deterministic Wake Cycle:** Moving to a strict State Machine. Tied to the Pillar 1 Event Bridge (Cloudflare Tunnel → FastAPI local daemon). Agents should not idle. When a ticket moves to "Sprint Now", the daemon spawns a NanoClaw container to execute and exit.
3. **Hot Sovereign Memory:** Memory should avoid expensive, retrospective AI summaries. The `mine_session.py` architecture is reaffirmed. The "Making Of" history is extracted in the moment, appended to the flat-file registry at `/session_close`, and pushed to ChromaDB. 

## Architectural Review: State Substrate & Automation

Git is the absolute state substrate. ChromaDB is merely a high-speed, lossy index generated from that record. 

* **The Lock Issue (Wave 0 diagnostics):** The 10-30 minute hang during `session_close` and 80MB git pushes are symptoms of treating a binary DB as plain-text state.
  * **Fix:** Untrack `.chroma_db/` from Git.
  * **Fix:** Explicitly terminate the ChromaDB SQLite WAL locks using `gc.collect()` and explicit client deletions before zipping/moving the registry.
* **The Colophon Loop (Problem Space C):** Map-Reduce Summarization. To avoid context exhaustion, `mine_session.py` generates a highly compressed "Forensic Flag" per ticket. The Sprint Distillation only reads these dense flags when composing the final Colophon.
* **Pinned Models:** `qwen2.5-coder:32b` should be pinned into VRAM on the host OS via NSSM. NanoClaw Ephemeral Containers hit the host's Ollama port (`host.docker.internal:11434`), rather than spinning up models inside themselves.

## Applying Mechanical FMEA to Agentic Workflows

We must isolate semantic processing from mathematical and structural formatting. The LLM (pinned to `qwen2.5-coder:32b`) handles reading text and identifying failure modes (assigning S-O-D scores based on a rigid 1-10 rubric). Python exclusively handles RPN calculation, Action Priority evaluation, and Markdown compilation.

**AIAG-VDA Action Priority Evaluator (Python Logic):**
We are adopting the AIAG & VDA FMEA Handbook (1st Edition, 2019) standards. Instead of an arbitrary RPN >= 100 threshold, Action Priority (AP - High/Medium/Low) determines critical issues.

```python
def get_action_priority(s: int, o: int, d: int) -> str:
    if s == 1: return 'L'
    if s >= 9:
        if o >= 6: return 'H'
        if o >= 4: return 'H' if d >= 2 else 'M'
        if o >= 2: return 'H' if d >= 7 else ('M' if d >= 5 else 'L')
        return 'L'
    if s >= 7:
        if o >= 8: return 'H'
        if o >= 6: return 'H' if d >= 5 else 'M'
        if o >= 2: return 'M' if d >= 5 else 'L'
        return 'L'
    if s >= 4:
        if o >= 8: return 'H' if d >= 5 else 'M'
        if o >= 6: return 'M' if d >= 2 else 'L'
        if o >= 4: return 'M' if d >= 5 else 'L'
        if o >= 2: return 'L'
        return 'L'
    if s >= 2:
        if o >= 8: return 'M' if d >= 5 else 'L'
        return 'L'
    return 'L'
```

Any item evaluated as `AP: High` immediately triggers the NanoClaw agent to create a GitHub Issue.

## LinkedIn Architecture Dispatch

Upcoming content sequence crafted to establish systemic rigor ("Software 3.0 requires Software 1.0 logic"):

* **Post 4 (The Gatekeeper):** The machine needs a micrometer. The `mcp_prd_linter` enforces Keystatic schemas strictly via Python, bouncing LLM drift back for fixing.
* **Post 5 (Mechanical FMEA):** The Neural Net cannot do math. The split pipeline: ephemeral agent extracts semantics, Python calculates FMEA matrix and Action Priority. Keep the math out of the neural net.
* **Post 6 (Surviving Context Collapse):** The `session_close` MapReduce pattern. The machine needs to forget in order to remember. Compress raw logs into "Forensic Flags".

---

## Action Items

- [ ] Implement `teardown_chroma_connection(chroma_client)` with `gc.collect()` inside `mine_session.py` / `session_close` to prevent OS locking on SQLite.
- [ ] Add `registry/.chroma_db/` to the root `.gitignore`.
- [ ] Implement `mcp_prd_linter` (Epic #74) to bounce non-compliant payload structures.
- [ ] Provide AIAG-VDA SOD 1-10 mapping directly into the PRD prompt injection payload for the `mcp_fmea_generator` (Epic #75), and use the `get_action_priority` Python evaluator in place of RPN > 100 flags.
- [ ] Create Map-Reduce context summarizations inside `mine_session.py` to draft "Forensic Flags" into `registry/flags/`.
