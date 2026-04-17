# Registry Topography Map

This file acts as the determinisitic structural map for the `registry/` directory. Agents must consult this index to establish spatial awareness and avoid hallucinations before executing context retrieval or `semantic_search`.

## Core Domains & Topology

- `global_agent/` - Documentation, system laws, and artifacts specific to the EN-OS orchestration layer. Key governance doc: `global_agent/board_governance.md` (milestone structure, triage protocol, label taxonomy, issue lifecycle).
- `infrastructure/` - Artifacts and constraints representing the underlying server and networking deployments.
- `linkedin/` - The staging ground for social publishing flows (interactions, drafts, and posted artifacts).
- `portfolio/` - Backing content and logs for the front-facing engineering portfolio OS.
- `session_logs/` - Historical system transcripts, traces, and artifacts from sovereign agentic sessions.
- `test_desk_hardware/` - Physical constraint data, mechanical PRDs, and hardware configuration logs.
- `workflow_state/` - Persisted data structures representing ongoing task pipelines and operational state.
- `master_mcp_config.json` - Global routing configuration for the Model Context Protocol DAEMON.

## Rules of Structuration
1. **Consult First:** Never guess the directory structure. Find the appropriate domain here before interacting with files.
2. **Map Updates Unconditional:** If you create a new structural node or sub-directory (e.g., `registry/new_domain/`), you must update this file immediately to reflect the new geometry.
