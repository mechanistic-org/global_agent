import os
import sys
from huggingface_hub import hf_hub_download

MODELS_DIR = r"D:\Local_Grok_Engine\models"
os.makedirs(MODELS_DIR, exist_ok=True)

models = [
    # The Legal Counsel (Node 5)
    ("tensorblock/Saul-7B-Instruct-v1-GGUF", "Saul-7B-Instruct-v1-Q4_K_M.gguf"),
    
    # The Physicist & Actuary (Nodes 2 & 5)
    ("bartowski/Qwen2.5-Math-7B-Instruct-GGUF", "Qwen2.5-Math-7B-Instruct-Q4_K_M.gguf"),
    
    # The Engineers & FMEA (Nodes 2, 3, 4)
    ("unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF", "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf"),
    
    # The Technical Writer / Compliance Officer (Nodes 2, 6)
    ("bartowski/Meta-Llama-3-8B-Instruct-GGUF", "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"),
]

print(f"Starting background download of the Denzel Armory to {MODELS_DIR}...")
for repo, filename in models:
    dest_path = os.path.join(MODELS_DIR, filename)
    if os.path.exists(dest_path):
        print(f"[SKIP] {filename} already exists at {dest_path}.")
        continue
    
    print(f"=====================================")
    print(f"[DOWNLOADING] {filename} from {repo}")
    print(f"=====================================")
    
    try:
        hf_hub_download(
            repo_id=repo,
            filename=filename,
            local_dir=MODELS_DIR,
            local_dir_use_symlinks=False
        )
        print(f"[SUCCESS] Downloaded {filename}\n")
    except Exception as e:
        print(f"[ERROR] Failed to download {filename}: {e}", file=sys.stderr)

print("\n--- DENZEL ARMORY MODELS ACQUIRED ---")
