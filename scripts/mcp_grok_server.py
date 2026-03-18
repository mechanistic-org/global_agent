import os
import sys
import chromadb
from sentence_transformers import SentenceTransformer
from mcp.server.fastmcp import FastMCP

# Dynamic imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from global_config import GROK_VAULT_DIR

# Initialize FastMCP Server
mcp = FastMCP("GrokVault")

# Constraints mapped across the "Hardware Moat" Architecture
VAULT_DIR = str(GROK_VAULT_DIR)
TRUTH_ENGINE_COLLECTION = "truth_engine"
RAINMAKER_COLLECTION = "rainmaker"

# Write diagnostic logs to standard error to keep the stdio buffer clean for MCP RPC communication
print("Initializing ChromaDB connection...", file=sys.stderr)
client = chromadb.PersistentClient(path=VAULT_DIR)

print("Loading embedding model (all-MiniLM-L6-v2) for RAG Queries...", file=sys.stderr)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

@mcp.tool()
def search_truth_engine(query: str, n_results: int = 5) -> str:
    """
    Search the local Truth Engine (Physics/Law/Constraints) vector database for relevant engineering history.
    
    Args:
        query: The engineering constraints or physical laws to search for (e.g., 'maximum thermal load of Az91D')
        n_results: Number of results to return (default 5)
    """
    print(f"Executing Truth Engine Query: {query}", file=sys.stderr)
    try:
        # We explicitly retrieve the collection so it errors cleanly if the collection hasn't been ingested yet 
        collection = client.get_collection(name=TRUTH_ENGINE_COLLECTION)
    except Exception as e:
        return f"Error: Truth Engine collection not found or uninitialized. Run ingest script first. Details: {e}"

    query_embedding = embedder.encode(query).tolist()
    
    # Query ChromaDB (Cosine Similarity)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    if not results['documents'] or not results['documents'][0]:
        return "No relevant engineering data found in the Truth Engine."
        
    formatted = "--- TRUTH ENGINE FORENSIC RESULTS ---\n\n"
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        source = metadata.get('filename', 'Unknown Source')
        domain = metadata.get('domain', 'UNKNOWN')
        formatted += f"[{i+1}] Source: {source} (Domain: {domain})\n{doc}\n\n"
        
    return formatted

@mcp.tool()
def search_rainmaker_corpus(query: str, n_results: int = 5) -> str:
    """
    Search the commercial Rainmaker Corpus for past brand wins, UI/UX solutions, and successful client pitches.
    
    Args:
        query: The commercial strategy or correlation to search for (e.g., 'wearable thermal solution for Avegant')
        n_results: Number of results to return (default 5)
    """
    print(f"Executing Rainmaker Query: {query}", file=sys.stderr)
    try:
        collection = client.get_collection(name=RAINMAKER_COLLECTION)
    except Exception as e:
        return f"Error: Rainmaker collection not found or uninitialized. Run ingest script first. Details: {e}"

    query_embedding = embedder.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    if not results['documents'] or not results['documents'][0]:
        return "No relevant commercial data found in the Rainmaker Corpus."
        
    formatted = "--- RAINMAKER CORPUS RESULTS ---\n\n"
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        source = metadata.get('filename', 'Unknown Source')
        formatted += f"[{i+1}] Source: {source}\n{doc}\n\n"
        
    return formatted

if __name__ == "__main__":
    # Start the FastMCP stdio server
    print("Sovereign Grok Vault MCP Server is LIVE on stdio.", file=sys.stderr)
    mcp.run()
