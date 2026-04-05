import os
import sys

from mcp.server.fastmcp import FastMCP

router_node = FastMCP("test")
@router_node.tool()
def hello():
    return "hello"

print("Starting FastMCP custom router...")
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
import uvicorn

sse = SseServerTransport("/mcp/messages/")

async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await router_node.server.run(
            streams[0], streams[1], router_node.server.create_initialization_options()
        )

async def handle_messages(request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

app = Starlette(
    debug=True,
    routes=[
        Route("/mcp", endpoint=handle_sse),
        Route("/mcp/messages/", endpoint=handle_messages, methods=["POST"]),
    ],
)
uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
