import os
import sys
from huggingface_hub import hf_hub_download

MODELS_DIR = r"D:\Local_Grok_Engine\models"
os.makedirs(MODELS_DIR, exist_ok=True)

models = [
    # DeepSeek-R1 (CTO / Physicist - 14B) - Approx 8.5 GB
    ("bartowski/DeepSeek-R1-Distill-Qwen-14B-GGUF", "DeepSeek-R1-Distill-Qwen-14B-Q4_K_M.gguf"),
    # Mistral NeMo 12B (CBDO / Strategy) - Approx 7.1 GB
    ("MaziyarPanahi/Mistral-Nemo-Instruct-2407-GGUF", "Mistral-Nemo-Instruct-2407.Q4_K_M.gguf"),
    # Qwen 2.5 Coder 14B (Software Dev) - Approx 8.5 GB
    ("bartowski/Qwen2.5-Coder-14B-Instruct-GGUF", "Qwen2.5-Coder-14B-Instruct-Q4_K_M.gguf"),
    # Microsoft Phi-3 Mini (Orchestrator / Router) - Approx 2.4 GB
    ("microsoft/Phi-3-mini-4k-instruct-gguf", "Phi-3-mini-4k-instruct-q4.gguf")
]

print(f"Starting background download to {MODELS_DIR}...")
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

print("\n--- ALL C-SUITE MODELS ACQUIRED ---")
