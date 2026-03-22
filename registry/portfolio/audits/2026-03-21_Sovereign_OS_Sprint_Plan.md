# Cross-Project Ticket Analysis & Sprint Series (Refactored)

**Date:** March 21, 2026

The following is the formalized master sequence bridging the `global_agent` backend infrastructure directly into the `portfolio` UI Shell and terminating in Client Workloads. All structural vulnerabilities identified in the Gap Analysis have been natively integrated into the timeline to prevent downstream catastrophic failures.

---

### Sprint 1: Foundation & Decoupling (Completed)
**Focus:** Stabilize the tool bus and decouple prompt engineering. 
*   ✅ **[global_agent]** #41: Pivot to Standalone SSE Router Node
*   ✅ **[global_agent]** #42: Scaffold Control File Hierarchy (`.agent/personas/`)

---

### Sprint 2: The Hybrid Orchestration Pipeline (Actionable Next)
**Focus:** Secure the background runtime environment, eradicate VRAM bottlenecks, and establish the 100+ native `gws` terminal agent capabilities.
*   🔥 **[NEW] [global_agent] Persistence & Auto-Boot Architecture** *(NSSM Daemon & Ollama keepalive)*
*   ⏳ **[global_agent]** #43: Refactor `prd_orchestrator.py` for Hybrid Routing *(Amended: Must be a completely stateless routing cycle)*
*   ⏳ **[global_agent]** #46: Integrate `googleworkspace/cli` via `.agent/skills/`
*   🔥 **[NEW] [global_agent] Agent Tool/Skill Submodule Versioning** *(SKILL.md Drift Management)*

---

### Sprint 3: Sovereign State Management & Perception (NEW FOCUS)
**Focus:** Implement the 3 State Pillars (GitHub Lifecycles, AST Patcher, Circuit Breakers) to protect VRAM before hitting UI workloads.
*   🔥 **[NEW] [global_agent] [Epic] Pillar 1: GitHub-Driven Agent Lifecycles** *(Polling, Context Compression, Teardown)*
*   🔥 **[NEW] [global_agent] [Task] Pillar 2: Scaffold AST & DB Point-Update MCP Tools** *(ts-morph & GraphQL)*
*   🔥 **[NEW] [global_agent] [Epic] Pillar 3: Transient State & 3-Strike Circuit Breakers** *(Hashing & NanoClaw Sandbox)*
*   🔥 **[NEW] [global_agent] Testing & Health Check Harness** *(Pre-Flight Diagnostics for Ollama, Chroma, and GWS)*
*   ⏳ **[global_agent]** #44: Embed Sovereign Registry Native Context-Streaming into LangGraph
*   ⏳ **[global_agent]** #45: Implement Persistent On-Demand Dashboards via the Stitch MCP
*   ⏳ **[portfolio]** #51: Document the 3 Stitch Workflow Paths in the Agent Orientation Laws

---

### Sprint 4: The Project OS UI Shell (Dark Hangar)
**Focus:** Clean the slate in the portfolio repo, establish the headless `projects.json` structure, and stitch the Dashboards together.
*   🔥 **[NEW] [portfolio] Legacy Portfolio Cleanup** *(Slash and Burn orphaned eriknorris* ghost code)*
*   ⏳ **[portfolio]** #30: The Project OS UI Shell (Dark Hangar)
*   ⏳ **[portfolio]** #31: Headless Portfolio API (`projects.json`)
*   ⏳ **[portfolio]** #28 & #29: Homepage Diagnostic Terminal Pivot
*   ⏳ **[portfolio]** #47: Resume the C|24 Component Stitch Loop *(Amended: Agents must exclusively use the new AST patcher payload, no full-file rewrites)*

---

### Sprint 5: Workload Execution (Client Epics)
**Focus:** Unleash the autonomous swarm on live production datasets.
*   ⏳ **[mootmoat]** #5: Sovereign Command & Control Architecture
*   ⏳ **[MO]** #1: The Mobile Outfitters Clone-and-Purge Extraction
*   ⏳ **[mechanistic]** #9 & #10: Engine Design Review Agent / Holy Grail DFMEA
*   ⏳ **[moreplay]** #12: Generate Global BFD Dashboard UI from Stitch
