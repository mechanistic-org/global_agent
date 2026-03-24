import os
import chromadb

REGISTRY_ROOT = os.path.abspath(r"D:\GitHub\global_agent\registry")
chroma_client = chromadb.PersistentClient(path=os.path.join(REGISTRY_ROOT, ".chroma_db"))
collection = chroma_client.get_or_create_collection(name="forensic_telemetry")

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
            print(f"Upserted {doc_id}")

print(f"Seeding complete. {indexed_count} documents indexed.")
