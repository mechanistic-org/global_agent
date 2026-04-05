from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys

class RequestLogger(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"GET {self.path}", file=sys.stderr)
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        self.wfile.write(b"event: endpoint\ndata: /messages\n\n")

        with open("proxy_req.log", "a") as f:
            f.write(f"GET {self.path}\nHeaders: {self.headers}\n\n")

    def do_POST(self):
        print(f"POST {self.path}", file=sys.stderr)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        print(f"Body: {body.decode()}", file=sys.stderr)
        
        with open("proxy_req.log", "a") as f:
            f.write(f"POST {self.path}\nHeaders: {self.headers}\nBody: {body.decode()}\n\n")
            
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"jsonrpc":"2.0", "id": 1, "result": "dummy"}')

if __name__ == "__main__":
    print("Starting diagnostic HTTP server on 8000...")
    server = HTTPServer(('127.0.0.1', 8000), RequestLogger)
    server.serve_forever()
