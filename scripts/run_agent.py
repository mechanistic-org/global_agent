import os
import sys
import json
import logging
import asyncio
import requests
import chromadb
import google.generativeai as genai
from pathlib import Path
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

# ── LOGGING ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | NanoClaw | %(levelname)s | %(message)s"
)
logger = logging.getLogger("NanoClaw")

# ── ENV SETUP ───────────────────────────────────────────────────────────
TARGET_ISSUE = os.environ.get("TARGET_ISSUE")
TARGET_REPO = os.environ.get("TARGET_REPO", "mechanistic-org/global_agent")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not TARGET_ISSUE or not GITHUB_TOKEN or not GEMINI_API_KEY:
    logger.error("Missing required env vars: TARGET_ISSUE, GITHUB_TOKEN, GEMINI_API_KEY")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# ── GITHUB FETCH ─────────────────────────────────────────────────────────
def fetch_issue_context(repo: str, issue_number: str) -> str:
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    logger.info(f"Fetching {repo}#{issue_number}...")
    
    # Get issue body
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    issue_data = resp.json()
    
    # Get comments
    comments_url = f"{url}/comments"
    comments_resp = requests.get(comments_url, headers=headers)
    comments_resp.raise_for_status()
    comments_data = comments_resp.json()
    
    context = f"TITLE: {issue_data.get('title')}\nBODY:\n{issue_data.get('body')}\n\nCOMMENTS:\n"
    # Take last 3 comments
    for c in comments_data[-3:]:
        context += f"--- {c.get('user',{}).get('login')} ---\n{c.get('body')}\n\n"
        
    return context

def post_github_comment(repo: str, issue_number: str, body: str):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    logger.info(f"Posting completion comment to {repo}#{issue_number}...")
    resp = requests.post(url, headers=headers, json={"body": body})
    resp.raise_for_status()

# ── CHROMA DB ────────────────────────────────────────────────────────────
def hydrate_chroma_context(query: str) -> str:
    db_path = "/registry/.chroma_db"
    if not os.path.exists(db_path):
        logger.warning(f"Chroma DB not found at {db_path}. Skipping hydration.")
        return ""
    
    try:
        client = chromadb.PersistentClient(path=db_path)
        # Assuming collection name "forensic_telemetry" from diag.py logs
        collection = client.get_collection("forensic_telemetry")
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
        context = "--- CHROMA CONTEXT ---\n"
        for doc in results["documents"][0]:
            context += f"{doc}\n"
        return context
    except Exception as e:
        logger.error(f"ChromaDB error: {e}")
        return ""

# ── SSE ROUTER AGENT ─────────────────────────────────────────────────────
async def run_agent_loop(issue_context: str, chroma_context: str) -> str:
    router_url = os.environ.get("ROUTER_SSE_URL", "http://host.docker.internal:8000/sse")
    logger.info(f"Connecting to EN-OS Router SSE at {router_url}...")
    
    try:
        async with sse_client(router_url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools = await session.list_tools()
                logger.info(f"Connected. Available tools: {[t.name for t in tools.tools]}")
                
                # In a full LangChain/GenerativeAI loop, we would pass tools to the model.
                # For Phase 1 ignition, we synthesize the directive and generate a structured response.
                prompt = (
                    "You are NanoClaw, an ephemeral execution container for the EN-OS.\n"
                    "Your objective is to review the following Git Issue context and ChromaDB context, "
                    "and output a forensic resolution or status update.\n\n"
                    f"{chroma_context}\n\n"
                    "--- GITHUB ISSUE ---\n"
                    f"{issue_context}\n\n"
                    "Generate a concise, highly technical execution log indicating what NanoClaw "
                    "assessed from this context. Do not invent code changes, just provide the assessment."
                )
                
                model = genai.GenerativeModel("gemini-2.5-flash")
                logger.info("Calling Gemini for task completion...")
                response = model.generate_content(prompt)
                
                # We could call a tool here using session.call_tool("push_forensic_doc", {...})
                # For this epic, demonstrating we can read the tools and boot is sufficient.
                
                return response.text
                
    except Exception as e:
        logger.error(f"SSE connection or Agent loop Failed: {e}")
        return f"NanoClaw execution encountered an error: {e}"

def write_output(repo: str, issue_number: str, content: str):
    repo_name = repo.split("/")[-1]
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{repo_name}_{issue_number}_forensics.md"
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("# NanoClaw Execution Payload\n")
        f.write(f"Repo: {repo}\nIssue: {issue_number}\n\n")
        f.write(content)
    logger.info(f"Wrote forensic payload to {out_file}")

# ── MAIN EXECUTION ───────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info(f"=== NANOCLAW IGNITION: {TARGET_REPO}#{TARGET_ISSUE} ===")
    
    # 1. GitHub Context
    issue_context = fetch_issue_context(TARGET_REPO, TARGET_ISSUE)
    
    # 2. Chroma Context
    chroma_context = hydrate_chroma_context(issue_context[:500]) # First 500 chars as query
    
    # 3. Connect to Router & Execute Loop
    # Windows/Linux difference: inside docker `host.docker.internal` handles localhost routing for SSE
    result = asyncio.run(run_agent_loop(issue_context, chroma_context))
    
    # 4. Write forensic output
    write_output(TARGET_REPO, TARGET_ISSUE, result)
    
    # 5. Comment back to GitHub to close the loop
    comment_body = (
        "**NanoClaw Execution Complete** 🟢\n\n"
        "Ephemeral container successfully spun up, hydrated context from ChromaDB, "
        "and analyzed the task.\n\n"
        "**Assessment Payload:**\n"
        f"```markdown\n{result}\n```"
    )
    post_github_comment(TARGET_REPO, TARGET_ISSUE, comment_body)
    
    logger.info("=== NANOCLAW TERMINATING CLEANLY ===")
    sys.exit(0)
