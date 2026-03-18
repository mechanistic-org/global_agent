import os
import sys
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Global Paths
VAULT_DIR = r"H:\Grok_Vector_Vault"
TRUTH_ENGINE_SOURCE = r"\\morespace\projects\__ME__"
COLLECTION_NAME = "truth_engine"

print(f"Initializing Sovereign Memory Vault at: {VAULT_DIR}")

# 2. Initialize ChromaDB (Persistent Local Storage)
client = chromadb.PersistentClient(path=VAULT_DIR)

# 3. Get or Create the Isolated Collection
# We use cosine similarity which is standard for dense text retrieval
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine", "domain": "physics/law"}
)

print(f"Collection '{COLLECTION_NAME}' active. Current vector count: {collection.count()}")

# 4. Load the Embedding Model
# all-MiniLM-L6-v2 is extremely fast, runs on CPU/GPU, and produces high-quality 384-dimensional embeddings.
print("Loading embedding model (all-MiniLM-L6-v2)...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text(file_path: Path) -> str:
    """Basic extraction. For a full production run, we'd add PyPDF2 or python-docx."""
    try:
        if file_path.suffix.lower() in ['.txt', '.md', '.json', '.csv']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    except Exception as e:
        print(f"  [!] Skipped {file_path.name}: {e}")
    return ""

def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    """Extremely basic character chunking for the MVP."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# 5. Ingestion Loop
print(f"\nScanning {TRUTH_ENGINE_SOURCE} for physics and constraints mapping...")
if not os.path.exists(TRUTH_ENGINE_SOURCE):
    print(f"ERROR: Cannot reach {TRUTH_ENGINE_SOURCE}. Ensure the network drive is mounted.")
    sys.exit(1)

files_processed = 0
chunks_embedded = 0

for root, dirs, files in os.walk(TRUTH_ENGINE_SOURCE):
    # Optional: Skip heavy binary folders like 'CAD' or 'Renderings'
    if any(skip in root.lower() for skip in ['cad', 'renderings', 'images', 'archive_old']):
        continue
        
    for file in files:
        if file.endswith(('.txt', '.md', '.json', '.csv')):
            file_path = Path(root) / file
            print(f"Ingesting: {file_path.relative_to(TRUTH_ENGINE_SOURCE)}")
            
            raw_text = extract_text(file_path)
            if not raw_text.strip():
                continue
                
            chunks = chunk_text(raw_text)
            
            # Prepare batch for ChromaDB
            ids = [f"{file_path.stem}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{"source": str(file_path), "filename": file, "domain": "physics/law"} for _ in chunks]
            
            # We embed using SentenceTransformers explicitly because it doesn't require an API key
            embeddings = embedder.encode(chunks).tolist()
            
            # Upsert into the local H: drive database
            collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            
            files_processed += 1
            chunks_embedded += len(chunks)

print(f"\n==========================================")
print(f"INGESTION COMPLETE")
print(f"==========================================")
print(f"Files Processed: {files_processed}")
print(f"Knowledge Vectors Secured: {chunks_embedded}")
print(f"Total Database Size: {collection.count()} vectors.")
print(f"Vault Location: {VAULT_DIR}")
