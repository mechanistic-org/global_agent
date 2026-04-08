import os
import sys
import json
import asyncio
import argparse
from pathlib import Path

# Try to import the NotebookLM wrapper
try:
    from notebooklm import NotebookLMClient
except ImportError:
    print('{"status": "ERROR", "message": "notebooklm-py not installed.", "auth_state": "MISSING"}')
    sys.exit(1)

async def _run_campaign_async(notebook_id=None, query=None):
    try:
        # The library uses asynchronous execution Native to Google's RPC payloads.
        client = await NotebookLMClient.from_storage()
        
        # Scenario 1: Interactive / Discovery mode (No arguments)
        if not notebook_id:
            notebooks = await client.notebooks.list()
            if not notebooks:
                 print('{"status": "SUCCESS", "message": "Auth valid, but no notebooks found.", "auth_state": "ACTIVE"}')
                 return
                 
            print("=== AVAILABLE NOTEBOOKS ===")
            for nb in notebooks:
                print(f"ID: {nb.id} | Title: {nb.title}")
            return

        # Scenario 2: Headless Extraction mode (Arguments provided)
        if notebook_id and query:
            print(f"Extracting payload for Notebook: {notebook_id}...")
            # Query the notebook specifically
            result = await client.chat.ask(notebook_id, query)
            
            payload = {
                "status": "SUCCESS", 
                "auth_state": "ACTIVE",
                "notebook_id": notebook_id,
                "response": result.text if hasattr(result, 'text') else str(result)
            }
            # Output pure JSON for the Make-Checker pipeline to consume
            print(json.dumps(payload, indent=2))
            return
            
    except Exception as e:
        err_msg = str(e)
        print(json.dumps({
            "status": "FATAL",
            "auth_state": "EXPIRED",
            "message": "The NotebookLM authentication cookie has expired or was rejected.",
            "raw_error": err_msg,
            "action_required": "Please authenticate via the browser pop-up. Try running `notebooklm login` CLI to cache cookies."
        }))
        sys.exit(1)

def run_campaign():
    parser = argparse.ArgumentParser(description="Headless NotebookLM Extraction script")
    parser.add_argument("--notebook-id", type=str, help="The UUID of the target notebook", default=None)
    parser.add_argument("--query", type=str, help="The prompt to execute", default="Provide a structural summary of the files in this notebook.")
    args = parser.parse_args()
    
    # Silence asyncio warnings for clean stdout
    import warnings
    warnings.simplefilter('ignore', RuntimeWarning)
    
    asyncio.run(_run_campaign_async(notebook_id=args.notebook_id, query=args.query))

if __name__ == "__main__":
    run_campaign()
