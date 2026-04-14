import os
import re
import chromadb

REGISTRY_ROOT = os.path.abspath(r"D:\GitHub\global_agent\registry")
PORTFOLIO_PROJECTS_ROOT = os.path.abspath(r"D:\GitHub\portfolio\src\content\projects")

chroma_client = chromadb.PersistentClient(path=os.path.join(REGISTRY_ROOT, ".chroma_db"))
collection = chroma_client.get_or_create_collection(name="forensic_telemetry")

# ── Pillar 1: global_agent registry ──────────────────────────────────────────
dirs_to_index = [
    "session_logs",
    "global_agent/mined",
    "global_agent/intelligence",
    "global_agent/law_candidates"
]

indexed_count = 0
for d in dirs_to_index:
    target_dir = os.path.join(REGISTRY_ROOT, os.path.normpath(d))
    if not os.path.exists(target_dir):
        continue
    for f in os.listdir(target_dir):
        if f.endswith(".md"):
            filepath = os.path.join(target_dir, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            project_name = d.replace('/', '\\').split('\\')[0]
            component_name = f.replace('.md', '')
            doc_id = f"{project_name}_{component_name}"

            collection.upsert(
                documents=[content],
                metadatas=[{"project": project_name, "component": component_name}],
                ids=[doc_id]
            )
            indexed_count += 1
            print(f"  Upserted {doc_id}")

# ── Pillar 2: portfolio project deep-dives ───────────────────────────────────
def extract_mdx_body(content: str) -> str:
    """Strip YAML frontmatter (between opening and closing ---) and return body."""
    parts = content.split('---', 2)
    if len(parts) >= 3:
        return parts[2].strip()
    return content.strip()

def extract_frontmatter_field(content: str, field: str) -> str:
    """Pull a single scalar field from frontmatter."""
    match = re.search(rf'^{field}:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    return match.group(1).strip() if match else ''

# Max chars per portfolio doc — keeps payload under the 8000-char microcompaction
# threshold in mcp_registry_server.py, and within MiniLM's 512-token embed window.
PORTFOLIO_DOC_MAX_CHARS = 5000

def distill_project_content(slug: str, raw: str, source_file: str) -> str:
    """
    Extract a dense, high-signal summary from a project document.
    Prefers explicit section headers (PROJECT SUMMARY, QUANTIFIED IMPACT, etc.)
    then falls back to the first N chars of the body.
    """
    if source_file == "_intelligence.md":
        body = raw
    else:
        body = extract_mdx_body(raw)

    title = extract_frontmatter_field(raw, 'title') if source_file != "_intelligence.md" else slug

    # Try to extract high-signal sections by header
    sections_to_pull = [
        r'PROJECT SUMMARY',
        r'QUANTIFIED IMPACT',
        r'LINKEDIN ARTIFACTS',
        r'THE NUMBERS',
        r'ANATOMY OF FAIL',
    ]
    extracted_sections = []
    for section_name in sections_to_pull:
        pattern = rf'(?:^|\n)#{1,3}\s+(?:[IVX]+\.\s+)?{section_name}.*?\n(.*?)(?=\n#{1,3}\s|\Z)'
        match = re.search(pattern, body, re.IGNORECASE | re.DOTALL)
        if match:
            extracted_sections.append(match.group(0).strip())

    if extracted_sections:
        distilled = f"# {title} ({slug})\n\n" + "\n\n".join(extracted_sections)
    else:
        # Fallback: first chunk of body
        distilled = f"# {title} ({slug})\n\n" + body

    return distilled[:PORTFOLIO_DOC_MAX_CHARS]

if os.path.exists(PORTFOLIO_PROJECTS_ROOT):
    project_count = 0
    for slug in os.listdir(PORTFOLIO_PROJECTS_ROOT):
        project_dir = os.path.join(PORTFOLIO_PROJECTS_ROOT, slug)
        if not os.path.isdir(project_dir):
            continue

        # Prefer _intelligence.md (distilled forensic report) if it exists
        intelligence_path = os.path.join(project_dir, "_intelligence.md")
        mdx_path = os.path.join(project_dir, "index.mdx")

        if os.path.exists(intelligence_path):
            with open(intelligence_path, 'r', encoding='utf-8', errors='replace') as f:
                raw = f.read()
            source_file = "_intelligence.md"
        elif os.path.exists(mdx_path):
            with open(mdx_path, 'r', encoding='utf-8', errors='replace') as f:
                raw = f.read()
            source_file = "index.mdx"
        else:
            continue

        content = distill_project_content(slug, raw, source_file)

        # Skip stubs
        if len(content.strip()) < 100:
            print(f"  Skipped {slug} (insufficient content)")
            continue

        doc_id = f"portfolio_{slug}"
        collection.upsert(
            documents=[content],
            metadatas=[{"project": "portfolio", "component": slug, "source": source_file}],
            ids=[doc_id]
        )
        indexed_count += 1
        project_count += 1
        print(f"  Upserted portfolio/{slug} ({source_file}, {len(content)} chars)")

    print(f"\nPortfolio projects indexed: {project_count}")
else:
    print(f"WARNING: Portfolio projects root not found: {PORTFOLIO_PROJECTS_ROOT}")

print(f"\nSeeding complete. {indexed_count} total documents indexed.")
