import os
import sys
import urllib.request
import json
import zipfile
import shutil
from pathlib import Path

GROK_DIR = r"D:\Local_Grok_Engine"
BIN_DIR = os.path.join(GROK_DIR, "bin")
MODELS_DIR = os.path.join(GROK_DIR, "models")

print(f"Creating Grok Engine directories at {GROK_DIR}...")
os.makedirs(BIN_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# 1. Download Llama.cpp
llama_exe = os.path.join(BIN_DIR, "llama-server.exe")
if not os.path.exists(llama_exe):
    print("Fetching latest Llama.cpp release info for Windows CUDA...")
    req = urllib.request.Request("https://api.github.com/repos/ggerganov/llama.cpp/releases/latest")
    with urllib.request.urlopen(req) as response:
        release_data = json.loads(response.read())

    asset_url = None
    for asset in release_data['assets']:
        name = asset['name'].lower()
        # Find the CUDA Windows build, explicitly avoiding the cudart-only zip
        if "win" in name and ("cu12" in name or "cuda" in name) and name.endswith(".zip") and "cudart" not in name:
            asset_url = asset['browser_download_url']
            break

    if not asset_url:
        print("Could not find a matching Windows CUDA 12 asset on GitHub.")
        sys.exit(1)

    zip_path = os.path.join(GROK_DIR, "llama_cpp.zip")
    print(f"Downloading Llama.cpp from {asset_url}...")
    urllib.request.urlretrieve(asset_url, zip_path)
    
    print("Extracting Llama.cpp...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(BIN_DIR)
    os.remove(zip_path)
    print("Llama.cpp extracted successfully.")
else:
    print("Llama.cpp is already installed.")

# 2. Download Model using Hugging Face Hub
try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("huggingface_hub is not installed. Please install it first.")
    sys.exit(1)

REPO_ID = "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF"
FILENAME = "Meta-Llama-3-8B-Instruct.Q4_K_M.gguf"

print(f"\nDownloading/Verifying Model: {FILENAME} from {REPO_ID}...")
print("This may take several minutes if downloading for the first time (~4.9GB)...")

model_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME, local_dir=MODELS_DIR)
print(f"Model successfully located at: {model_path}")

# 3. Create the Start Script
bat_path = os.path.join(GROK_DIR, "start_grok_engine.bat")
with open(bat_path, "w") as f:
    f.write("@echo off\n")
    f.write("title Sovereign Grok Engine (Llama.cpp)\n")
    f.write(f'cd /d "{BIN_DIR}"\n')
    f.write("echo Starting Llama.cpp Server on port 8080 with 8192 context window...\n")
    # -ngl 99 offloads all layers to the RTX 4000 GPU VRAM.
    f.write(f'llama-server.exe -m "{model_path}" -c 8192 -ngl 99 --port 8080\n')
    f.write("pause\n")

print(f"\nSetup Complete! The Sovereign Grok Engine is ready.")
print(f"To launch the server, run: {bat_path}")
