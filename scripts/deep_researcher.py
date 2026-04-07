import os
import sys
import argparse
import json
import urllib.request
import pypdf
import chromadb
import uuid
import yaml

ENOS_ROOT = os.environ.get("ENOS_ROOT", r"D:\GitHub\global_agent")
REGISTRY_ROOT = os.path.abspath(os.path.join(ENOS_ROOT, "registry"))

def summarize_with_llm(text_chunk: str, query: str = None) -> str:
    """Send text to local LLM for summary extraction."""
    q_str = f"Focus strictly on extracting relevant facts answering: '{query}'" if query else "Extract a comprehensive structural summary of key metrics, constraints, and architecture."
    prompt = (
        "You are an analytical deep research extraction engine.\n"
        f"Analyze the following PDF text segment. {q_str}\n"
        "Format your output strictly as Markdown without conversational filler.\n"
        "Do not include Em-Dashes. Use Space-Dash-Space (' - ') instead.\n\n"
        f"--- RAW PDF TEXT ---\n{text_chunk}\n"
    )
    
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=json.dumps({
        "model": "qwen_coder:latest",
        "prompt": prompt,
        "stream": False
    }).encode('utf-8'))
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=300.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('response', '')
    except Exception as e:
        print(f"[DeepResearcher] LLM Request Failed: {e}", file=sys.stderr)
        return ""

def main():
    parser = argparse.ArgumentParser(description="EN-OS Deep Research Engine")
    parser.add_argument("--pdf-path", required=True, help="Absolute path to target PDF")
    parser.add_argument("--project", required=True, help="Target project namespace (e.g., 'portfolio', 'active_projects\\hyphen_lid')")
    parser.add_argument("--query", required=False, default=None, help="Specific intelligence constraints to extract")
    args = parser.parse_args()

    pdf_path = os.path.abspath(args.pdf_path)
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF path not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[DeepResearcher] Ingesting {pdf_path} into namespace '{args.project}'...")
    
    try:
        reader = pypdf.PdfReader(pdf_path)
        full_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n--- Page {i+1} ---\n{text}"
    except Exception as e:
        print(f"ERROR: Failed to read PDF {pdf_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Simplified windowing: If text is massive, we should technically chunk it. 
    # For now, Qwen 32k limits usually handle ~20-30k words easily. 
    # Truncate to a safe bolus limit for now (e.g. 50k chars).
    safe_text = full_text[:50000]
    
    print("[DeepResearcher] Analyzing text...")
    summary_markdown = summarize_with_llm(safe_text, args.query)
    
    if not summary_markdown:
        print("ERROR: LLM failed to return a string array.", file=sys.stderr)
        sys.exit(1)

    # Compose output file
    filename = os.path.basename(pdf_path).replace('.pdf', '')
    target_dir = os.path.join(REGISTRY_ROOT, args.project, "assets")
    os.makedirs(target_dir, exist_ok=True)
    
    out_filepath = os.path.join(target_dir, f"{filename}_research.md")
    
    # Generate metadata frontmatter
    frontmatter = {
        "title": f"Deep Research: {filename}",
        "date": "2026",
        "sources": [pdf_path],
        "project": args.project
    }
    frontmatter_yaml = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)
    
    final_doc = f"---\n{frontmatter_yaml}---\n\n{summary_markdown}"
    
    with open(out_filepath, 'w', encoding='utf-8') as f:
        f.write(final_doc)

    print(f"[DeepResearcher] Markdown retained at {out_filepath}")
        
    # ChromaDB insertion
    try:
        chroma_client = chromadb.PersistentClient(path=os.path.join(REGISTRY_ROOT, ".chroma_db"))
        collection = chroma_client.get_or_create_collection(name="forensic_telemetry")
        
        doc_id = f"{args.project}_asset_{filename}"
        
        collection.upsert(
            documents=[final_doc],
            metadatas=[{"project": args.project, "component": f"asset_{filename}"}],
            ids=[doc_id]
        )
        print(f"[DeepResearcher] Successfully embedded into ChromaDB with metadata project: '{args.project}'.")
    except Exception as e:
        print(f"WARNING: Database lock or failure on upsert: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
