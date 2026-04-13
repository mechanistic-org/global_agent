module.exports = {
  apps: [
    {
      name: "enos-router",
      script: "scripts/mcp_router_node.py",
      interpreter: "D:/GitHub/global_agent/venv/Scripts/python.exe",
      cwd: "D:/GitHub/global_agent",
      watch: false,
      windowsHide: true,      // CRITICAL on Windows: prevents forrtl error 200 (console-CLOSE kill)
      autorestart: true,
      max_restarts: 5,        // Hard stop after 5 consecutive crashes
      min_uptime: "10s",      // Must stay alive 10s to count as a clean start
      restart_delay: 5000,    // 5s cooldown between restarts — prevents terminal storm
      env: {
        PYTHONUNBUFFERED: "1",
        // SSE deprecated March 2025 — Streamable HTTP is the MCP standard
        MCP_TRANSPORT: "http",
        FOR_DISABLE_CONSOLE_CTRL_HANDLER: "1"
      }
    },
    {
      // GitHub Webhook → NanoClaw ignition bridge (port 8001)
      // Requires GITHUB_WEBHOOK_SECRET in .env
      // Set NANOCLAW_ENABLED=true in .env once en-os:latest image is built (Epic #61)
      name: "enos-webhook-daemon",
      script: "scripts/webhook_daemon.py",
      interpreter: "D:/GitHub/global_agent/venv/Scripts/python.exe",
      cwd: "D:/GitHub/global_agent",
      watch: false,
      windowsHide: true,      // CRITICAL on Windows: prevents forrtl error 200 (console-CLOSE kill)
      autorestart: true,
      max_restarts: 5,        // Hard stop after 5 consecutive crashes
      min_uptime: "10s",      // Must stay alive 10s to count as a clean start
      restart_delay: 5000,    // 5s cooldown between restarts
      env: {
        PYTHONUNBUFFERED: "1"
        // Reads GITHUB_WEBHOOK_SECRET and NANOCLAW_ENABLED from .env via dotenv
      }
    },

/*
    {
      name: "enos-ingress-tunnel",
      script: "cloudflared",
      args: "tunnel --config .cloudflared/config.yml run enos-webhook",
      cwd: "D:/GitHub/global_agent",
      watch: false,
      windowsHide: true,
      autorestart: true,
      max_restarts: 5
    },*/
    {
      name: "enos-autodream-daemon",
      script: "scripts/autodream_daemon.py",
      interpreter: "D:/GitHub/global_agent/venv/Scripts/python.exe",
      cwd: "D:/GitHub/global_agent",
      watch: false,
      windowsHide: true,      // CRITICAL on Windows: prevents forrtl error 200 (console-CLOSE kill)
      autorestart: true,
      max_restarts: 5,        // Hard stop after 5 consecutive crashes
      min_uptime: "10s",      // Must stay alive 10s to count as a clean start
      restart_delay: 5000,    // 5s cooldown between restarts
      env: {
        PYTHONUNBUFFERED: "1"
      }
    }
  ]
};
