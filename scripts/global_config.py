import os
from pathlib import Path
from dotenv import load_dotenv

# Use Path(__file__) to dynamically walk up the directory tree
GLOBAL_AGENT_ROOT = Path(__file__).resolve().parent.parent
GITHUB_ROOT = GLOBAL_AGENT_ROOT.parent

# Sibling repositories
MECHANISTIC_ROOT = GITHUB_ROOT / "mechanistic"
MOOTMOAT_ROOT = GITHUB_ROOT / "mootmoat"
# Handle portfolio differently since it's typically D:/portfolio based on user environments
PORTFOLIO_ROOT = Path("D:/portfolio") if Path("D:/portfolio").exists() else GITHUB_ROOT / "portfolio"

# Load local .env
local_env = GLOBAL_AGENT_ROOT / ".env"
if local_env.exists():
    load_dotenv(dotenv_path=local_env)
else:
    print(f"⚠️ Warning: Global .env file not found at {local_env}")

# Master Swarm Environment Override
master_fallback = Path("D:/Assets/.env.swarm")
master_env_path = Path(os.getenv("SWARM_ENV_PATH", master_fallback))

if master_env_path.exists():
    load_dotenv(dotenv_path=master_env_path)
    # print(f"✅ Loaded Master Swarm Environment Cache from {master_env_path}")

def get_repo_root(repo_name: str) -> Path:
    repos = {
        'global_agent': GLOBAL_AGENT_ROOT,
        'mechanistic': MECHANISTIC_ROOT,
        'mootmoat': MOOTMOAT_ROOT,
        'portfolio': PORTFOLIO_ROOT
    }
    
    path = repos.get(repo_name)
    if not path:
        path = GITHUB_ROOT / repo_name
        
    if not path.exists():
        raise FileNotFoundError(f"❌ Critical Error: Could not locate sibling repository '{repo_name}' at {path}")
        
    return path

# Grok Engine & Vault configuration
LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", r"D:\Local_Grok_Engine\models\Meta-Llama-3-8B-Instruct.Q4_K_M.gguf")
GROK_VAULT_DIR = os.getenv("GROK_VAULT_DIR", r"H:\Grok_Vector_Vault")
