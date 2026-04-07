# LAW CANDIDATE — 2026-04-07

**Rule:** MCP tools must return file paths, not content, to prevent JSON-RPC bloat and ensure agents use file-system reads.

Agents must not receive large file contents directly through the JSON-RPC pipeline. Instead, MCP tools that generate significant output, such as normalized Markdown files, must return a success string containing the absolute path to the generated file, compelling the agent to read the content via standard file-system tools.

**Tags:** agent-design, mcp-tool, json-rpc, performance, system-rule
