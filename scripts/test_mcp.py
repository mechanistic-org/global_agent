import sys
import json
import requests
import time
import threading

def test_sse():
    session = requests.Session()
    sse_response = session.get("http://127.0.0.1:8000/sse", stream=True)
    post_ep = None
    lines_received = []
    
    def read_stream():
        nonlocal post_ep
        for line in sse_response.iter_lines():
            if line:
                val = line.decode('utf-8')
                lines_received.append(val)
                if val.startswith("data: /messages/"):
                    post_ep = "http://127.0.0.1:8000" + val[6:]

    t = threading.Thread(target=read_stream, daemon=True)
    t.start()
    
    while post_ep is None:
        time.sleep(0.1)
        
    res1 = session.post(
        post_ep,
        json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}
    )
    time.sleep(0.5)
    
    res2 = session.post(
        post_ep,
        json={"jsonrpc": "2.0", "method": "notifications/initialized"}
    )
    time.sleep(0.5)
    
    res3 = session.post(
        post_ep,
        json={"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "router_health_check", "arguments": {}}}
    )
    time.sleep(1)
    
    with open("D:\\GitHub\\global_agent\\scripts\\out.json", "w", encoding="utf-8") as f:
        json.dump(lines_received, f, indent=2)

test_sse()
