import os
import sys
import json
import logging
import asyncio
import argparse
import datetime
import requests
import chromadb
import google.generativeai as genai
from pathlib import Path
from mcp.client.streamable_http import streamablehttp_client  # SSE deprecated March 2025
from mcp.client.session import ClientSession

# ── LOGGING ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | NanoClaw | %(levelname)s | %(message)s"
)
logger = logging.getLogger("NanoClaw")

# ── ENV SETUP ───────────────────────────────────────────────────────────
TARGET_ISSUE = os.environ.get("TARGET_ISSUE")
TARGET_ASSET = os.environ.get("TARGET_ASSET")
TARGET_REPO = os.environ.get("TARGET_REPO", "mechanistic-org/global_agent")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

missing_vars = []
if not GEMINI_API_KEY: missing_vars.append("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# ── ASSET INGESTION ──────────────────────────────────────────────────────
def extract_asset_text(asset_path: str) -> str:
    path = Path(asset_path)
    if not path.exists():
        logger.error(f"Asset not found: {asset_path}")
        sys.exit(1)
        
    if path.suffix.lower() == ".pdf":
        try:
            import pypdf
            text = ""
            with open(path, "rb") as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            logger.error("pypdf not installed. Cannot parse PDF.")
            sys.exit(1)
    else:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

async def run_ingest_loop(raw_text: str, source_filename: str):
    router_url = os.environ.get("ROUTER_URL", "http://host.docker.internal:8000/mcp")
    logger.info(f"Connecting to EN-OS Router (Streamable HTTP) at {router_url} for ingestion...")

    try:
        async with streamablehttp_client(router_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                prompt = (
                    "You are NanoClaw, an ephemeral ingestion processor for the EN-OS.\n"
                    "Extract the core facts from the following raw document dump and format them as a cohesive engineering forensic memory document.\n\n"
                    "--- RAW DUMP ---\n"
                    f"{raw_text[:30000]}\n\n" 
                    "Please respond with STRICT markdown only. No conversational pleasantries. Provide a concise summary and key bullet points."
                )
                
                model = genai.GenerativeModel("gemini-2.5-flash")
                logger.info("Calling Gemini for document extraction...")
                response = model.generate_content(prompt)
                structured_body = response.text
                
                dt_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                safe_name = Path(source_filename).stem.replace(" ", "_").lower()
                component_name = f"{dt_str}_{safe_name}"
                
                logger.info("Pushing via push_forensic_doc tool...")
                tool_args = {
                    "project_name": "global_agent",
                    "component_name": component_name,
                    "markdown_body": structured_body,
                    "frontmatter_dict": {
                        "type": "forensic_inbox",
                        "source": str(source_filename),
                        "ingested_at": dt_str
                    }
                }
                res = await session.call_tool("push_forensic_doc", tool_args)
                logger.info(f"Router response: {res.content}")
                
    except Exception as e:
        logger.error(f"Ingestion Loop Failed: {e}")
        sys.exit(1)

# ── GITHUB FETCH ─────────────────────────────────────────────────────────
def fetch_issue_context(repo: str, issue_number: str) -> str:
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    logger.info(f"Fetching {repo}#{issue_number}...")
    
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    issue_data = resp.json()
    
    comments_url = f"{url}/comments"
    comments_resp = requests.get(comments_url, headers=headers)
    comments_resp.raise_for_status()
    comments_data = comments_resp.json()
    
    context = f"TITLE: {issue_data.get('title')}\nBODY:\n{issue_data.get('body')}\n\nCOMMENTS:\n"
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

# ── STREAMABLE HTTP ROUTER AGENT ────────────────────────────────────────────
async def run_agent_loop(issue_context: str, chroma_context: str) -> str:
    router_url = os.environ.get("ROUTER_URL", "http://host.docker.internal:8000/mcp")
    logger.info(f"Connecting to EN-OS Router (Streamable HTTP) at {router_url}...")

    try:
        async with streamablehttp_client(router_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools = await session.list_tools()
                logger.info(f"Connected. Available tools: {[t.name for t in tools.tools]}")
                
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="issue", choices=["issue", "ingest"])
    args, unknown = parser.parse_known_args()
    
    if args.mode == "issue":
        if not TARGET_ISSUE: missing_vars.append("TARGET_ISSUE")
        if not GITHUB_TOKEN: missing_vars.append("GITHUB_TOKEN")
        if missing_vars:
            logger.error(f"Missing env vars for issue tracking: {', '.join(missing_vars)}")
            sys.exit(1)
            
        logger.info(f"=== NANOCLAW IGNITION: {TARGET_REPO}#{TARGET_ISSUE} ===")
        issue_context = fetch_issue_context(TARGET_REPO, TARGET_ISSUE)
        chroma_context = hydrate_chroma_context(issue_context[:500])
        result = asyncio.run(run_agent_loop(issue_context, chroma_context))
        write_output(TARGET_REPO, TARGET_ISSUE, result)
        
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
        
    elif args.mode == "ingest":
        if not TARGET_ASSET: missing_vars.append("TARGET_ASSET")
        if missing_vars:
            logger.error(f"Missing env vars for ingestion: {', '.join(missing_vars)}")
            sys.exit(1)
            
        logger.info(f"=== NANOCLAW IGNITION [INGEST]: {TARGET_ASSET} ===")
        raw_text = extract_asset_text(TARGET_ASSET)
        asyncio.run(run_ingest_loop(raw_text, TARGET_ASSET))
        logger.info("=== NANOCLAW TERMINATING CLEANLY ===")
        sys.exit(0)
