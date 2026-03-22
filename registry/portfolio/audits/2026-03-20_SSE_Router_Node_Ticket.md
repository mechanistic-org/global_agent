Our investigation into recent Antigravity UI crashes and MCP tool failures has surfaced three critical systemic vulnerabilities with relying on IDE-managed `stdio` for Swarm architecture:

### 1. Configuration Volatility
The `mcp_config.json` owned by the IDE extension is highly volatile. UI updates, crashes, or session resets silently overwrite our hardcoded configurations with blank templates (`{"mcpServers": {}}`), severing the entire tool bus. While we mitigated this by using `env-cmd` and natively loading `D:\Assets\.env.swarm` to keep actual API keys safe, the pipeline itself requires constant manual restoration.

### 2. Environment Stripping (The `uv` Path Bug)
Headless Node `child_process` environments spawned by the IDE extension strip out the interactive user `%PATH%`. They fail to locate globally installed binaries (such as `uv`), requiring unmaintainable absolute path hardcoding (`C:\Users\erik\.cargo\bin\uv.exe`).

### 3. Interactive Auth Blocking (The `gws` Bug)
MCP servers demanding interactive OAuth browser flows (e.g., Google Workspace) instantly crash with `EOF` errors. Background IDE processes cannot surface browser popups or terminal prompts gracefully, effectively blocking tools requiring user authentication flows.

## The Sovereign OS Solution: SSE Router Node Daemon
We must deprecate IDE-managed `stdio` orchestration and pivot to a standalone **SSE Router Node Daemon**.
* The daemon will execute natively in a dedicated terminal window (inheriting the full `%PATH%` and interactive shell capabilities for browser auth).
* It natively wraps `D:\Assets\.env.swarm`, routing secrets implicitly to the Node/Python servers without touching the IDE filesystem.
* The IDE extension becomes a "dumb" client, configured with a single, volatile-immune URL: `http://localhost:5000/sse`.

### Action Items:
- [ ] Scaffold the base FastMCP SSE server in `global_agent`.
- [ ] Wire the existing local MCP python scripts (`graph_bridge`, `grok_server`, and `registry_server`) to mount onto the SSE Router.
- [ ] Replace `C:\Users\erik\.gemini\antigravity\mcp_config.json` payload with the single SSE endpoint URL.
