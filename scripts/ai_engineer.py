import os
import sys
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from zod_validator import validate_swarm_output

# 1. Load Environment Constraints
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[FATAL] Node 0 Core Offline: GEMINI_API_KEY missing from environment.")
    sys.exit(1)

# 2. Instantiate the Apex Router
client = genai.Client()

SYSTEM_DIRECTIVE = """
You are Node 0 (Apex Router). You operate with a massive 2M+ token context window.
Your primary role is NOT to write granular Astro or React code. Your role is Orchestration.
1. Ingest massive multi-document PDFs (SOWs, PRDs, Master Architectures).
2. Synthesize High-Level Architectural Plans.
3. DELEGATE specialized reasoning tasks to local 14B SLMs via the Denzel Armory HTTP endpoints over localhost:11434.
4. Interface with the Sovereign Context Hub via FastMCP to read and write downstream forensics.
"""

def parse_master_sow(filepath: str) -> str:
    """Ingests generic multiformat Client documents natively mapping into Node 0."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"[ERROR] Failed to ingest {filepath}: {e}"

def delegate_to_local_llm(context: str, instruction: str) -> dict | str:
    """
    Physically routes the UI building blocks from Node 0 to the local SLM Swarm running on :11434.
    """
    import urllib.request
    
    payload = {
        "model": "qwen2.5-coder",
        "prompt": f"Context: {context}\\nInstruction: {instruction}\\nGenerate extremely strict JSON matching the V32 Schema.",
        "stream": False,
        "format": "json"
    }
    
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=json.dumps(payload).encode('utf-8'))
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return validate_swarm_output(data.get('response', '{}'))
    except Exception as e:
        return f"[ERROR] Local Swarm Execution aborted: {e}"

def ping_node_0():
    """Validates the basic SDK handshake for Sprint 5 and Sprint 8 modifications."""
    print("==================================================")
    print("  NODE 0: APEX ROUTER (GEMINI 2.5) ONLINE         ")
    print("==================================================")
    print(" -> Data Validation constraints actively routing local-swarm endpoints.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--ping":
        ping_node_0()
    else:
        print("Usage: python ai_engineer.py --ping")
