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
        MCP_TRANSPORT: "sse"
      }
    },
    {
      name: "ollama-keepalive",
      script: "ollama",
      args: "run deepseek_r1:latest \"\" --keepalive -1m",
      cwd: "D:/GitHub/global_agent",
      autorestart: false, // Run once on boot to load model into VRAM
      watch: false
    }
  ]
};
