# EN-OS System Architecture

> [!WARNING]
> **CRITICAL ARCHITECTURAL DIRECTIVE FOR ALL AGENTS:**
> This engineering system employs a sovereign **Local ChromaDB** and a **FastMCP Router (`enos_router`)**. 
> You operate under the **"Two-Pillar" Rule**:
> 1. **Historical Context:** You must absolutely **NEVER** use brute-force filesystem loops (e.g., `ls -R`) to ingest contextual logic. Plundering massive historical blobs will burn tokens and crash memory. All historical telemetry must flow strictly through the localized `enos_router` MCP tools.
> 2. **Active Execution:** You have full permission to utilize standard IDE filesystem tools (`view_file`, `grep_search`) natively and surgically for the purpose of focused bug fixing, code reading, and targeted engineering inside active project directories.

## 1. Ideology & Perspective

EN-OS (Engineering Operating System) is a sovereign, highly compressed agentic infrastructure. It enforces strict context gating and relies on a local intelligence registry.

- **Sovereign Infrastructure:** The system relies on local ChromaDB and file-based state registries. There is no ambient cloud indexing. 
- **The "Dark Hangar" Aesthetic:** Premium, vibrant, deeply responsive dark-mode aesthetics. Minimum viable products, standard Bootstrap templates, or generic colors will be actively rejected.
- **Deterministic Compression over Brute Force:** Context must be maintained strictly using the "compression rule." External context must exclusively be fetched via the `enos_router` MCP tools, which return heavily compressed, schema-validated documents.

## 2. 5-Tier Architecture

EN-OS is structured around a finalized 5-Tier Architecture that enforces data sovereignty and decoupled execution.

| Tier | Component | Function |
| :--- | :--- | :--- |
| **Tier 1: IDE Surface** | Antigravity, Claude Desktop, Cursor, Continue.dev | The conversation and execution interfaces. Fully decoupled from direct filesystem reads where possible. |
| **Tier 2: Context Router** | `enos_router` (Port 8000), PM2, ChromaDB | The absolute bottleneck for context. Agents query FastMCP endpoints (Streamable HTTP `http://127.0.0.1:8000/mcp`). |
| **Tier 3: Ephemeral Tier** | `enos-webhook-daemon` (Port 8001), `NanoClaw` | GitHub webhook receiver -> ignites disposable `en-os:latest` Docker containers to handle background tasks autonomously. |
| **Tier 4: Swarm Tier** | `node_0_distiller.py`, `trigger_cascade_swarm.py` | Manual execution scripts utilizing LLM APIs for compounding, multi-persona synthesis. |
| **Tier 5: Model Runtime** | Local Ollama (`localhost:11434`) | Specialized local inference (e.g., `qwen2.5-coder:32b`, `deepseek-r1:32b`). |

## 3. System Topology & Repositories

The local workspace consists of discrete, highly decoupled domains operating concurrently:

1. **`d:\GitHub\global_agent` (The Core Brain)**
   - Houses the central registry, the FastMCP server (`mcp_enos_router`), and local Python orchestrators.
   - Contains the ephemeral containerization logic (`NanoClaw`) and webhook daemons.
2. **`d:\GitHub\mechanistic` (Protocol and History)**
   - The foundational truth engine. Stores the architectural history, correlation frameworks, and core constraints.
3. **`d:\GitHub\portfolio` (Public Facing Node)**
   - The visual proof-of-work. Encompasses the "Portrait API" (`projects.json`) and the Homepage Diagnostic Terminal. 
4. **`d:\GitHub\hyphen` (Client Staging)**
   - Sandbox and PRD delivery mechanism for live commercial client-facing iterations.

## 4. Operating Rituals & Execution Protocols

EN-OS functions on structured, explicitly defined mechanical pathways:

1. **Initialization (`/session_open`):** Every session begins by verifying system health (e.g., `diag.py`) and explicitly claiming a ticket with a strict Definition of Done (DoD).
2. **Workflows:** Complex tasks must align with the markdown definitions in `.agent/workflows/`. 
3. **Knowledge Persistence:** Ephemeral agent findings must be surgically pushed into the registry using `push_forensic_doc` so that future agent generations inherit them permanently.
4. **The Definition of Done (DoD):** Never start executing tasks until you have clearly stated a 1-sentence Definition of Done based on the GitHub Sprint Board.

## 5. Required Tooling & Protocols

Agents should strictly invoke the following tools natively rather than executing raw bash/PowerShell scripts for exploration:
- `mcp_enos_router_semantic_search`: Conceptual/thematic context gathering.
- `mcp_enos_router_search_registry`: Structural layouts and active documents.
- `mcp_enos_router_read_forensic_doc`: Exact matched flat-file texts in the registry.
- `mcp_enos_router_push_forensic_doc`: Dump structured intelligence into the registry mapping ChromaDB vector stores.

**Hazard Warning:** An uncompressed ~23MB `Node_0_Master_Context.txt` file exists historically near the global root. If this file or other massive generated outputs are read raw, it causes total API failure. Obey the Compression Rule outlined above.
