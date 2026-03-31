import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Optional
from mcp.server.fastmcp import FastMCP

# Modulize the raw Python scripts natively without duplicating their logic
import mcp_registry_server
import mcp_grok_server

# ---------------------------------------------------------------------------
# SOVEREIGN EN-OS ROUTER NODE
# ---------------------------------------------------------------------------
# Unifies all disparate Python MCP tools into a single daemonized SSE endpoint.
# ---------------------------------------------------------------------------

router_node = FastMCP("enos-router")

# --- REGISTRY SECTOR MOUNTS ---
# We use .add_tool() to harvest the functions from the original files so you 
# can still manage your domain logic independently if you want.
router_node.add_tool(mcp_registry_server.search_registry)
router_node.add_tool(mcp_registry_server.semantic_search)
router_node.add_tool(mcp_registry_server.read_forensic_doc)
router_node.add_tool(mcp_registry_server.push_forensic_doc)
router_node.add_tool(mcp_registry_server.read_design_system)

# --- GROK VAULT MOUNTS ---
router_node.add_tool(mcp_grok_server.search_truth_engine)
router_node.add_tool(mcp_grok_server.search_rainmaker_corpus)

@router_node.tool()
def router_health_check() -> str:
    """Diagnostic loop to ensure the SSE Daemon is actively listening."""
    return "SUCCESS: EN-OS Sovereign Router Node is online and routing beautifully."

@router_node.tool()
def patch_astro_component(
    filepath: str,
    target_selector: str,
    zone: str = "template",
    set_attributes: Optional[dict] = None,
    add_class: Optional[str] = None,
    add_import: Optional[dict] = None,
    set_variable: Optional[dict] = None,
) -> str:
    """
    Pillar 2 Data Compressor: Surgically patches a single Astro component using
    an AST delta payload. Agents NEVER read the raw file — they submit a JSON
    payload and receive a structured success/error response.

    Args:
        filepath: Absolute path to the .astro file.
        target_selector: Element tag name or CSS class to locate in the template.
        zone: 'template' (default) for HTML body; 'frontmatter' for TS block.
        set_attributes: Dict of {attr_name: attr_value} to inject on the target.
        add_class: A CSS class string to append to the target element.
        add_import: {'moduleSpecifier': str, 'namedImport': str} for frontmatter.
        set_variable: {'name': str, 'value': any} for frontmatter variable.
    """
    # ── PATH SECURITY BOUNDARY ─────────────────────────────────────────────
    abs_path = os.path.abspath(filepath)
    allowed = os.path.abspath(r"D:\GitHub")
    if not abs_path.startswith(allowed):
        return json.dumps({
            "status": "error",
            "reason": "PATH_VIOLATION",
            "detail": f"Target '{abs_path}' is outside D:\\GitHub\\"
        })

    # ── BUILD PAYLOAD ──────────────────────────────────────────────────────
    payload: dict[str, Any] = {"zone": zone}
    if set_attributes:
        payload["setAttributes"] = set_attributes
    if add_class:
        payload["addClass"] = add_class
    if add_import:
        payload["addImport"] = add_import
    if set_variable:
        payload["setVariable"] = set_variable

    # ── INVOKE NODE SUBPROCESS ─────────────────────────────────────────────
    patcher_path = str(Path(__file__).parent.parent / ".agent" / "skills" / "ast_patcher" / "patcher.js")

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", dir=str(Path(__file__).parent / ".tmp"),
            delete=False, encoding="utf-8"
        ) as tmp:
            tmp_path = tmp.name
            json.dump(payload, tmp)

        result = subprocess.run(
            ["node", patcher_path, abs_path, target_selector, tmp_path],
            capture_output=True, text=True, timeout=15
        )

        if result.returncode != 0:
            return json.dumps({
                "status": "error",
                "reason": "NODE_EXCEPTION",
                "detail": result.stderr.strip()
            })

        # stdout is guaranteed JSON from patcher.js
        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return json.dumps({"status": "error", "reason": "TIMEOUT", "detail": "patcher.js exceeded 15s"})
    except Exception as e:
        return json.dumps({"status": "error", "reason": "INTERNAL_ERROR", "detail": str(e)})
    finally:
        # Always clean up the temp payload — never leave artifacts on disk
        try:
            if 'tmp_path' in dir():
                os.unlink(tmp_path)
        except Exception:
            pass

if __name__ == "__main__":
    print("-------------------------------------------------------")
    print("BOOTING SOVEREIGN EN-OS ROUTER NODE (STREAMABLE HTTP)")
    print("Mounting to: http://127.0.0.1:8000/mcp")
    print("NOTE: SSE transport deprecated (MCP spec, March 2025).")
    print("-------------------------------------------------------")

    # FastMCP Streamable HTTP transport — the current MCP standard.
    # SSE (http://127.0.0.1:8000/sse) is deprecated and removed.
    # All clients (Claude Desktop, Claude Code, Continue.dev, VS Code)
    # must connect to: http://127.0.0.1:8000/mcp
    #
    # PM2 env: MCP_TRANSPORT=http
    # Fallback: stdio (for subprocess / test use)
    try:
        transport_mode = os.environ.get("MCP_TRANSPORT", "stdio")
        if transport_mode == "sse":
            # Legacy guard: auto-upgrade to http if someone sets old value
            print("WARNING: MCP_TRANSPORT=sse is deprecated. Upgrading to http.")
            transport_mode = "http"
        if transport_mode == "http":
            print("Booting as Streamable HTTP Server on Port 8000 (/mcp)")
        router_node.run(transport=transport_mode)
    except Exception as e:
        print(f"CRITICAL BOOT FAILURE: {e}")
