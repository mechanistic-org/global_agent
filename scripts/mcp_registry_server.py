from mcp.server.fastmcp import FastMCP
import os
import chromadb
from chromadb.utils import embedding_functions

mcp = FastMCP("sovereign-registry")

# Constant constraint boundary
REGISTRY_ROOT = os.path.abspath(r"D:\GitHub\global_agent\registry")

# Initialize ChromaDB mapping locally inside the registry for offline execution
chroma_client = chromadb.PersistentClient(path=os.path.join(REGISTRY_ROOT, ".chroma_db"))

# Using lightweight local embedding geometric loops
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="forensic_telemetry", embedding_function=sentence_transformer_ef)

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
def semantic_search(query: str, n_results: int = 3) -> str:
    """
    Execute a deep structural Cosine-Similarity extraction loop mapping ChromaDB vectors.
    Node 0 utilizes this native tool to retrieve topological documents natively escaping explicit LLM Hallucination loops.
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if not results['documents'] or not results['documents'][0]:
            return "No structurally embedded mapping found natively inside the Sovereign Vector Hub."
            
        payload = ""
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i] if results['metadatas'] else {}
            dist = results['distances'][0][i] if results['distances'] else 0.0
            comp = meta.get('component', 'UNKNOWN')
            payload += f"--- Result {i+1} [Geometry Vector Rank: {dist:.2f} | Execution Source: {comp}] ---\n{doc}\n\n"
            
        return payload
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
            return f.read()
    except Exception as e:
        return f"Structural File Read completely failed: {str(e)}"

@mcp.tool()
def push_forensic_doc(project_name: str, component_name: str, markdown_content: str) -> str:
    """
    The Active Core Engine Constraint loop. Forces a Swarm to dump structural intelligence 
    into the flat-file registry AND mechanically embeds the string matrix directly into local ChromaDB memory stores.
    """
    # Mathematical token compression bounds limits
    if len(markdown_content) > 3000:
        return "ERROR: Executing Documentation is natively too massive. Context Window limits breached. Compress output to under 3000 indices."
        
    target_dir = os.path.join(REGISTRY_ROOT, project_name)
    os.makedirs(target_dir, exist_ok=True)
    
    filename = component_name if component_name.endswith('.md') else f"{component_name}.md"
    filepath = os.path.join(target_dir, filename)
    
    doc_id = f"{project_name}_{component_name}"
    
    try:
        # Write flat-file text bound
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        # Inject structural multi-dimension geometry into the Hub layer
        collection.upsert(
            documents=[markdown_content],
            metadatas=[{"project": project_name, "component": component_name}],
            ids=[doc_id]
        )
            
        return f"SUCCESS: Formal physical timestamp generated AND dynamically embedded into Matrix local registry layer for {component_name}."
    except Exception as e:
        return f"CRITICAL: FastMCP Context ingestion violently rejected. {str(e)}"

@mcp.tool()
def read_design_system() -> str:
    design_path = os.path.abspath(r"D:\GitHub\global_agent\laws\law_002_design_system.md")
    try:
        with open(design_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR: FastMCP Hub violently failed to aggregate tokens: {str(e)}"

if __name__ == "__main__":
    mcp.run()
