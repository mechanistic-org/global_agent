import os
import sys
import json
import logging
import asyncio
import argparse
import datetime
import requests
import time
import chromadb
import google.generativeai as genai
from pathlib import Path
from mcp.client.streamable_http import streamablehttp_client  # SSE deprecated March 2025
from mcp.client.session import ClientSession
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── LOGGING ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | NanoClaw | %(levelname)s | %(message)s"
)
logger = logging.getLogger("NanoClaw")

FAILSAFES_LOG = Path(__file__).parent.parent / ".system_generated" / "logs" / "failsafes.log"
FAILSAFES_LOG.parent.mkdir(parents=True, exist_ok=True)

# ── ENV SETUP ───────────────────────────────────────────────────────────
TARGET_ISSUE = os.environ.get("TARGET_ISSUE")
TARGET_ASSET = os.environ.get("TARGET_ASSET")
TARGET_REPO = os.environ.get("TARGET_REPO", "mechanistic-org/global_agent")
AGENT_MODE = os.environ.get("AGENT_MODE", "plan").lower()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MAX_SESSION_TOKENS = int(os.environ.get("MAX_SESSION_TOKENS", "500000"))

missing_vars = []
if not GEMINI_API_KEY: missing_vars.append("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# ── CIRCUIT BREAKERS & STATE ────────────────────────────────────────────

def log_failsafe(repo: str, issue: str, reason: str, duration: float):
    dt = datetime.datetime.now().isoformat()
    msg = f"[{dt}] HALT | {repo}#{issue} | {reason} | Duration: {duration:.2f}s\n"
    logger.error(f"FAILSAFE TRIPPED: {msg.strip()}")
    with open(FAILSAFES_LOG, "a", encoding="utf-8") as f:
        f.write(msg)

async def call_tool_with_timeout(session: ClientSession, name: str, args: dict, timeout: float = 45.0):
    """Executes a FastMCP tool call with a hard wall-clock timeout."""
    try:
        return await asyncio.wait_for(session.call_tool(name, args), timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Tool {name} exceeded {timeout}s wall-clock limit.")

async def update_workflow_state(session: ClientSession, repo: str, issue: str, state: str):
    """Pushes an explicit state record to ChromaDB/Registry via FastMCP."""
    try:
        safe_repo = repo.replace('/', '_')
        await call_tool_with_timeout(
            session,
            "push_forensic_doc",
            {
                "project_name": "global_agent",
                "component_name": f"{safe_repo}_workflow_state_issue_{issue}",
                "markdown_body": f"Current Workflow State: {state.upper()}",
                "frontmatter_dict": {
                    "type": "workflow_state",
                    "repo": repo,
                    "issue": issue,
                    "state": state,
                    "updated_at": datetime.datetime.now().isoformat()
                }
            },
            timeout=15.0
        )
        logger.info(f"Epic D State Manifested: {state}")
    except Exception as e:
        logger.error(f"Failed to update workflow state to {state}. Ensure FastMCP is online. Error: {e}")

def track_token_telemetry(response) -> int:
    """Epic B: Unlocks historical baseline logic for the EN-OS dashboard."""
    try:
        if hasattr(response, 'usage_metadata'):
            u = response.usage_metadata
            logger.info(f"🪙 TELEMETRY | Tokens: IN:{u.prompt_token_count} | OUT:{u.candidates_token_count} | TOT:{u.total_token_count}")
            return u.total_token_count
    except Exception as e:
        pass
    return 0


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
    start_time = time.time()

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
                
                track_token_telemetry(response)
                
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
                
                # Epic B constraints wrapped around the FastMCP push natively
                res = await call_tool_with_timeout(session, "push_forensic_doc", tool_args, timeout=45.0)
                logger.info(f"Router response: {res.content}")
                
    except TimeoutError as e:
        log_failsafe("ingestion", source_filename, str(e), time.time() - start_time)
        sys.exit(1)
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
    
    # Epic B Local Hook for when script is executed outside docker container directly:
    if not os.path.exists(db_path):
        db_path = str(Path(__file__).parent.parent / "registry" / ".chroma_db")

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
async def run_agent_loop(issue_context: str, chroma_context: str, repo: str, issue_number: str) -> str:
    router_url = os.environ.get("ROUTER_URL", "http://host.docker.internal:8000/mcp")
    logger.info(f"Connecting to EN-OS Router (Streamable HTTP) at {router_url}...")

    # Epic B: Circuit Breaker Variables
    start_time = time.time()
    max_duration_seconds = 300  # 5 minutes wall-clock break
    strikes = 0
    max_strikes = 3
    iterations = 0
    max_iterations = 15

    try:
        async with streamablehttp_client(router_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools = await session.list_tools()
                
                # Epic C: Explicit Tool Allowlist (No Whack-A-Mole Blacklisting)
                if AGENT_MODE == "plan":
                    READ_ONLY_WHITELIST = {"search_registry", "semantic_search", "read_forensic_doc", "read_design_system"}
                    tools.tools = [t for t in tools.tools if t.name in READ_ONLY_WHITELIST]
                    logger.info(f"Connected (PLAN MODE). Restricted tools: {[t.name for t in tools.tools]}")
                else:
                    logger.info(f"Connected (EXEC MODE). All tools armed: {[t.name for t in tools.tools]}")
                
                # Epic D: Boot-Up State
                await update_workflow_state(session, repo, issue_number, "executing")

                model = genai.GenerativeModel("gemini-2.5-flash")
                
                # The execution loop bounded by hard Circuit Breakers
                final_output = ""
                total_tokens_used = 0
                soft_warning_issued = False

                while iterations < max_iterations:
                    runtime = time.time() - start_time
                    
                    # Circuit Breaker 1: Wall-clock Check
                    if runtime > max_duration_seconds:
                        halt_reason = f"Wall-clock max exceeded (>{max_duration_seconds}s)"
                        log_failsafe(repo, issue_number, halt_reason, runtime)
                        await update_workflow_state(session, repo, issue_number, "halted")
                        return f"[HALTED] {halt_reason}"
                        
                    # Circuit Breaker 2: Token Budget Accumulation (90% Hard Kill)
                    if total_tokens_used > (MAX_SESSION_TOKENS * 0.9):
                        halt_reason = f"Budget Exhausted: {total_tokens_used} tokens (>90% of {MAX_SESSION_TOKENS})"
                        log_failsafe(repo, issue_number, halt_reason, runtime)
                        await update_workflow_state(session, repo, issue_number, "halted")
                        return f"[HALTED] {halt_reason}"
                        
                    # Soft Warning: 50% Threshold
                    if not soft_warning_issued and total_tokens_used > (MAX_SESSION_TOKENS * 0.5):
                        logger.warning(f"⚠️ BUDGET WARNING: Token usage at {total_tokens_used} (>{MAX_SESSION_TOKENS * 0.5}). Approaching hard kill limit.")
                        soft_warning_issued = True
                    
                    try:
                        iterations += 1
                        logger.info(f"Model iteration {iterations}/{max_iterations}...")
                        
                        if AGENT_MODE == "plan":
                            prompt = (
                                "You are NanoClaw operating in STRICT PLAN MODE.\n"
                                "You are completely airgapped from code mutation or destruction vectors. Your sole tools are native registry searches.\n"
                                "Your objective is to read the active Git Issue and ChromaDB history, execute necessary searches to formulate a precise architectural plan, and output a markdown assessment.\n\n"
                                f"{chroma_context}\n\n"
                                "--- GITHUB ISSUE ---\n"
                                f"{issue_context}\n\n"
                                "If your plan requires execution logic, end your markdown strictly by indicating we are 'Awaiting the /execute command'."
                            )
                        else:
                            prompt = (
                                "You are NanoClaw operating in FULL EXECUTION MODE.\n"
                                "You have full write access to the filesystem and external endpoints via your tools.\n"
                                "Your objective is to review the following Git Issue context and ChromaDB context, execute the necessary changes natively, and output the final structural changes applied.\n\n"
                                f"{chroma_context}\n\n"
                                "--- GITHUB ISSUE ---\n"
                                f"{issue_context}\n\n"
                                "Ensure all changes adhere to strict Dark Hangar SCADA logic."
                            )
                        
                        response = model.generate_content(prompt)
                        used_tokens = track_token_telemetry(response)
                        total_tokens_used += used_tokens
                        
                        # In the future, this is where tool routing loops back into the while.
                        # For now, it's a structural 1-shot mapping but we exit cleanly.
                        final_output = response.text
                        await update_workflow_state(session, repo, issue_number, "closed")
                        break
                        
                    except Exception as e:
                        strikes += 1
                        logger.error(f"Strike {strikes}/{max_strikes} encountered: {e}")
                        if strikes >= max_strikes:
                            halt_reason = f"Fatal Execution Snag: {strikes} consecutive failures."
                            log_failsafe(repo, issue_number, halt_reason, time.time() - start_time)
                            await update_workflow_state(session, repo, issue_number, "halted")
                            return f"[HALTED] {halt_reason}"
                        
                        # Briefly sleep to allow API recovery
                        await asyncio.sleep(2)
                
                return final_output
                
    except Exception as e:
        logger.error(f"SSE connection or Agent loop Failed: {e}")
        return f"NanoClaw execution encountered an error: {e}"

def write_output(repo: str, issue_number: str, content: str):
    repo_name = repo.split("/")[-1]
    
    out_dir = Path("/output")
    if not os.path.exists("/output"):
        out_dir = Path(__file__).parent.parent / ".system_generated" / "logs"
    
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
        
        result = asyncio.run(run_agent_loop(issue_context, chroma_context, TARGET_REPO, TARGET_ISSUE))
        
        write_output(TARGET_REPO, TARGET_ISSUE, result)
        
        status_emoji = "🔴" if "[HALTED]" in result else "🟢"
        
        comment_body = (
            f"**NanoClaw Execution Log** {status_emoji}\n\n"
            "Ephemeral container sequence recorded.\n\n"
            "**Assessment Payload:**\n"
            f"```markdown\n{result[:60000]}\n```"
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
