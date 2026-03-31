module.exports = {
  apps: [
    {
      name: "enos-router",
      script: "scripts/mcp_router_node.py",
      interpreter: "venv/Scripts/python.exe",
      cwd: "D:/GitHub/global_agent",
      watch: false,
      autorestart: true,
      max_restarts: 10,
      env: {
        PYTHONUNBUFFERED: "1",
        // SSE deprecated March 2025 — Streamable HTTP is the MCP standard
        MCP_TRANSPORT: "http"
      }
    },
    {
      // GitHub Webhook → NanoClaw ignition bridge (port 8001)
      // Requires GITHUB_WEBHOOK_SECRET in .env
      // Set NANOCLAW_ENABLED=true in .env once en-os:latest image is built (Epic #61)
      name: "enos-webhook-daemon",
      script: "scripts/webhook_daemon.py",
      interpreter: "venv/Scripts/python.exe",
      cwd: "D:/GitHub/global_agent",
      watch: false,
      autorestart: true,
      max_restarts: 10,
      env: {
        PYTHONUNBUFFERED: "1"
        // Reads GITHUB_WEBHOOK_SECRET and NANOCLAW_ENABLED from .env via dotenv
      }
    },
    {
      name: "ollama-reasoning-keepalive",
      script: "ollama",
      args: "run deepseek-r1:32b --keepalive -1",
      cwd: "D:/GitHub/global_agent",
      autorestart: false, // Run once on boot to load reasoning model into VRAM
      watch: false
    },
    {
      name: "ollama-coder-keepalive",
      script: "ollama",
      args: "run qwen2.5-coder:32b --keepalive -1",
      cwd: "D:/GitHub/global_agent",
      autorestart: false, // Run once on boot to load daily coding model into VRAM
      watch: false
    }
  ]
};
