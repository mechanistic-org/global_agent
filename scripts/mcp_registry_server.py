from mcp.server.fastmcp import FastMCP
import os
import sys
import yaml
import json
import urllib.request
import chromadb
import subprocess
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

mcp = FastMCP("sovereign-registry")

# ─── MICROCOMPACTION PIPELINE (EPIC A) ──────────────────────────────────────
def apply_microcompaction(payload: str) -> str:
    """Intercepts massive payloads and forcibly distills them to save Apex Tokens."""
    if len(payload) <= 8000:
        return payload
        
    print(f"[KAIROS] Triggering Microcompaction on {len(payload)} chars...", file=sys.stderr)
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=json.dumps({
        "model": "phi3",
        "prompt": (
            "You are KAIROS, a strict micro-compaction pipeline constraint.\n"
            "Pre-digest the following massive forensic data wall exactly as strict Markdown.\n"
            "Retain all structural schemas, constraints, and actionable code elements.\n"
            "DO NOT include conversational fluff.\n\n"
            f"--- RAW BOLUS ({len(payload)} chars) ---\n"
            f"{payload[:150000]}"
        ),
        "stream": False
    }).encode('utf-8'))
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=180.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            distilled = data.get('response', '')
            if distilled:
                return f"--- [NODE 0: MICROCOMPACTED BOLUS] ---\n{distilled}"
            return payload
    except Exception as e:
        print(f"[KAIROS] Microcompaction Failed: {e}", file=sys.stderr)
        return payload

# ─── Pydantic Frontmatter Schemas ───────────────────────────────────────────

class ColophonFrontmatter(BaseModel):
    """Schema for colophon/ and linkedin_drafts/ collection directories."""
    title: str = Field(min_length=5)
    pubDate: str                    # e.g. "2026-03-22"
    audio_url: Optional[str] = ""  # URL or empty string
    isDraft: bool = True
    tags: list[str] = []

class StandardRegistryFrontmatter(BaseModel):
    """Default schema for all other registry collection directories."""
    title: str
    date: str                       # e.g. "2026-03-22"
    context_node: str = ""

# Maps collection dir name → schema class. Falls back to StandardRegistryFrontmatter.
SCHEMA_ROUTING: dict = {
    "colophon": ColophonFrontmatter,
    "linkedin_drafts": ColophonFrontmatter,
}

# Constant constraint boundary
ENOS_ROOT = os.environ.get("ENOS_ROOT", r"D:\GitHub\global_agent")
REGISTRY_ROOT = os.path.abspath(os.path.join(ENOS_ROOT, "registry"))

# Initialize ChromaDB mapping locally inside the registry for offline execution
chroma_client = chromadb.PersistentClient(path=os.path.join(REGISTRY_ROOT, ".chroma_db"))

# Built-in embedding — no model download, no cold-start penalty.
# Switch to GeminiEmbeddingFunction if semantic quality becomes a concern.
collection = chroma_client.get_or_create_collection(name="forensic_telemetry")

@mcp.tool()
def search_registry(query: str, project_scope: str = None) -> list[str]:
    """Execute an absolute explicit layout search across the Markdown registry."""
    results = []
    search_path = REGISTRY_ROOT
    if project_scope:
        search_path = os.path.join(REGISTRY_ROOT, project_scope)
        if not os.path.exists(search_path):
            return [f"ERROR: Target project scope '{project_scope}' actively not found."]

    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            results.append(filepath)
                except Exception:
                    pass
    return results

@mcp.tool()
def semantic_search(query: str, project_scope: str = None, n_results: int = 3) -> str:
    """
    Execute a deep structural Cosine-Similarity extraction loop mapping ChromaDB vectors.
    Node 0 utilizes this native tool to retrieve topological documents natively escaping explicit LLM Hallucination loops.
    """
    try:
        kwargs = {
            "query_texts": [query],
            "n_results": n_results
        }
        if project_scope:
            kwargs["where"] = {"project": project_scope}
            
        results = collection.query(**kwargs)
        
        if not results['documents'] or not results['documents'][0]:
            return "No structurally embedded mapping found natively inside the Sovereign Vector Hub."
            
        payload = ""
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i] if results['metadatas'] else {}
            dist = results['distances'][0][i] if results['distances'] else 0.0
            comp = meta.get('component', 'UNKNOWN')
            payload += f"--- Result {i+1} [Geometry Vector Rank: {dist:.2f} | Execution Source: {comp}] ---\n{doc}\n\n"
            
        return apply_microcompaction(payload)
    except Exception as e:
        return f"CRITICAL: Structural geometric query loop violently failed. {str(e)}"

@mcp.tool()
def read_forensic_doc(filepath: str) -> str:
    """Retrieve exactly matched flat-file texts natively."""
    abs_filepath = os.path.abspath(filepath)
    if not abs_filepath.startswith(REGISTRY_ROOT):
        return "ERROR: FATAL BOUNDARY CROSSING. Structural execution attempted to breach internal limit loops."
        
    try:
        with open(abs_filepath, 'r', encoding='utf-8') as f:
            return apply_microcompaction(f.read())
    except Exception as e:
        return f"Structural File Read completely failed: {str(e)}"

@mcp.tool()
def push_forensic_doc(
    project_name: str,
    component_name: str,
    markdown_body: str,
    frontmatter_dict: dict,
) -> str:
    """
    The Active Core Engine Constraint loop. Forces a Swarm to dump structural intelligence
    into the flat-file registry AND mechanically embeds the string matrix directly into local ChromaDB memory stores.

    Args:
        project_name:    Registry collection directory (e.g. 'colophon', 'linkedin_drafts', 'global_agent').
        component_name:  Filename stem — .md extension added automatically.
        markdown_body:   Prose body content ONLY. Do NOT include frontmatter here.
        frontmatter_dict: Structured dict of frontmatter fields. Python serializes this — never hand-format YAML.

    Returns a ValidationError description string on bad input (agent must self-correct and retry).
    Returns SUCCESS string on successful disk write + ChromaDB embed.
    """
    # ── Pydantic validation ──────────────────────────────────────────────────
    schema_class = SCHEMA_ROUTING.get(project_name, StandardRegistryFrontmatter)
    try:
        validated = schema_class(**frontmatter_dict)
    except ValidationError as e:
        # Return structured error so agent can self-correct without human intervention.
        errors = e.errors(include_url=False)
        error_lines = []
        for err in errors:
            loc = " -> ".join(str(x) for x in err["loc"])
            error_lines.append(f"  - Field '{loc}': {err['msg']} (type={err['type']})'")
        return (
            f"ValidationError: frontmatter_dict failed schema '{schema_class.__name__}' for "
            f"collection '{project_name}'.\n"
            "Fix the following fields and retry:\n" + "\n".join(error_lines) +
            f"\nExpected fields: {list(schema_class.model_fields.keys())}"
        )

    # ── Token size guard ────────────────────────────────────────────────────
    if len(markdown_body) > 3000:
        return "ERROR: markdown_body is too large. Compress to under 3000 characters."

    # ── Compose final document (Python owns all YAML) ────────────────────────
    frontmatter_yaml = yaml.safe_dump(
        validated.model_dump(), default_flow_style=False, sort_keys=False, allow_unicode=True
    ).strip()
    full_document = f"---\n{frontmatter_yaml}\n---\n\n{markdown_body}"

    # ── Write to disk ────────────────────────────────────────────────────────
    target_dir = os.path.join(REGISTRY_ROOT, project_name)
    os.makedirs(target_dir, exist_ok=True)

    filename = component_name if component_name.endswith(".md") else f"{component_name}.md"
    filepath = os.path.join(target_dir, filename)
    doc_id = f"{project_name}_{component_name}"

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_document)
            f.flush()
            os.fsync(f.fileno())

        try:
            # ── Embed into ChromaDB ──────────────────────────────────────────────
            collection.upsert(
                documents=[full_document],
                metadatas=[{"project": project_name, "component": component_name}],
                ids=[doc_id],
            )
            return f"SUCCESS: '{component_name}' written to '{project_name}/' and embedded in ChromaDB."
        except Exception as e:
            return f"WARNING: Flat-file saved successfully, but ChromaDB upsert failed due to lock/error: {str(e)}"
            
    except Exception as e:
        return f"CRITICAL: Registry disk write failed. {str(e)}"

@mcp.tool()
def read_design_system() -> str:
    ENOS_ROOT = os.environ.get("ENOS_ROOT", r"D:\GitHub\global_agent")
    design_path = os.path.abspath(os.path.join(ENOS_ROOT, "laws", "law_002_design_system.md"))
    try:
        with open(design_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR: FastMCP Hub violently failed to aggregate tokens: {str(e)}"

@mcp.tool()
def normalize_local_asset(filepath: str, target_path: Optional[str] = None) -> str:
    """
    Ingest and normalize a local Office artifact (.pdf, .docx, .pptx, .xlsx, .csv, .eml) into Markdown.
    Provides the agent with access to non-markdown payloads by translating them strictly locally using Docling, Pandas, or Email parsers.
    
    Args:
        filepath: Absolute path to the original target asset.
        target_path: Optional absolute path indicating where the Markdown equivalent should be deposited.
                     If missing, the system forces ephemeral write to registry/.tmp/normalized/ and returns that path.
    """
    script_path = os.path.abspath(os.path.join(ENOS_ROOT, "scripts", "normalize_asset.py"))
    
    cmd = ["python", script_path, "--input", filepath]
    if target_path:
        cmd.extend(["--output", target_path])
        
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            return f"SUCCESS: Asset normalized successfully.\\nExecution Log:\\n{result.stdout.strip()}"
        else:
            return f"ERROR: Normalization failed.\\nStdout: {result.stdout.strip()}\\nStderr: {result.stderr.strip()}"
    except Exception as e:
        return f"CRITICAL: Failed to execute normalization script: {str(e)}"

if __name__ == "__main__":
    mcp.run()
