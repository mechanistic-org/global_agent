## Context
The sovereign system requires a dedicated "Single Pane of Glass" to monitor infrastructure, deployment states, and financial constraints. We have chosen to implement **Option 3 (Python/Streamlit)** as phase 1 because it allows zero-friction local filesystem querying while having a negligible throwaway cost if we pivot to a React UI (Option 4) in the future.

## Dashboard Display Requirements (The 4 Quadrants)

### 1. Infrastructure & Connectivity (The Daemons)
This is the baseline heartbeat of the system. If these fail, the agent is unreachable.
* **Ingress Map (Windows Service):** `Cloudflared agent` Status (Running / Stopped / Restarting) and Tunnel vitality.
* **Local Routing (PM2 Node Daemons):** `enos-router` status, uptime, memory usage, and `enos-webhook` listener status.
* **(Future):** Other local server bridges (text-to-speech, vision processors).

### 2. Financial & Resource Constraints (The Ledger)
Consumes `.system_generated/logs/token_ledger.json` tracking the "Active Agentic Engineer" burn rate.
* **Daily Token Burn:** Line chart showing input vs. output tokens across the current 24hr loop.
* **Cost Vector (USD):** Aggregated cost metrics, updating per tool call.
* **Model Distribution:** Fast Model (Gemini Flash/Haiku) vs. Frontier reasoning (Gemini Pro/deepseek).
* **Limit Switch Gauge:** Visual gauge tracking proximity to the $5.00 daily hard cap.

### 3. Safety & Circuit Breakers (The Dead-Man's Switch)
Reads `.system_generated/logs/failsafes.log`. This quadrant demands human attention if tripped.
* **Agent Status Plate:** (IDLE | RUNNING | HALTED).
* **Halt Intercepts:** Wall-Clock Breakers, Sanity/Loop Breakers, Financial Breakers.
* **Action Required:** If `[HALTED]`, a prominent "Acknowledge & Clear" button forces log review before resuming.

### 4. Orchestration & Truth Engine (The Work)
Reflects system I/O and links into GitHub project logic.
* **Sprint Trajectory:** Currently active GitHub Issue and Iteration (Sprint) progress from `board.json`.
* **Memory Ingestion:** ChromaDB metrics on vector embeddings vs flat-file registry.
* **Local Tool Operations:** Live stdout tails or recent tool usage history.

## DoD
- [ ] Bootstrap `enos_dashboard.py` running on Streamlit.
- [ ] Connect Quad 1: PM2 and Windows Service status APIs.
- [ ] Connect Quad 2: Parse `token_ledger.json`.
- [ ] Connect Quad 3: Parse `failsafes.log` & implement visual Halt clearing state.
- [ ] Connect Quad 4: Surface `board.json` sprint data.
