import subprocess
import json
import time

p = subprocess.Popen(
    ["venv/Scripts/python.exe", "scripts/mcp_router_node.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(1) # wait for startup

init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}
p.stdin.write(json.dumps(init_req) + "\n")
p.stdin.flush()

out1 = p.stdout.readline()
print(f"Init resp: {repr(out1)}")

p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
p.stdin.flush()

tool_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "router_health_check", "arguments": {}}}
p.stdin.write(json.dumps(tool_req) + "\n")
p.stdin.flush()

out2 = p.stdout.readline()
print(f"Tool resp: {repr(out2)}")

p.terminate()
