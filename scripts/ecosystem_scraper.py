import os
import shutil
import subprocess
from pathlib import Path

# The repositories to scrape (GitHub name -> Local directory name)
SPOKE_MAP = {
    "MO": "MO",
    "mechanistic": "mechanistic",
    "portfolio": "eriknorris"
}
HUB_DIR = r"D:\GitHub\global_agent\registry"

def git_pull_or_clone(repo_name: str, target_dir: str):
    """Ensures the repository is up to date locally before scraping."""
    if os.path.exists(target_dir):
        print(f"[{repo_name}] Directory exists. Pulling latest architecture...")
        subprocess.run(["git", "pull"], cwd=target_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print(f"[{repo_name}] Not found locally. Cloning via gh CLI...")
        subprocess.run(["gh", "repo", "clone", f"mechanistic-org/{repo_name}", target_dir])

def scrape_docs(repo_name: str, source_dir: str):
    """Scrapes all markdown files from the docs directory into the isolated mootmoat Hub."""
    docs_path = os.path.join(source_dir, "src", "content", "docs")
    if not os.path.exists(docs_path):
        print(f"[{repo_name}] No standard src/content/docs directory found. Skipping.")
        return
        
    hub_spoke_dir = os.path.join(HUB_DIR, repo_name)
    os.makedirs(hub_spoke_dir, exist_ok=True)
    
    count = 0
    for root, dirs, files in os.walk(docs_path):
        for file in files:
            if file.endswith(".md"):
                src_file = os.path.join(root, file)
                # Reconstruct relative path to maintain folder taxonomic structure
                rel_path = os.path.relpath(src_file, docs_path)
                dest_file = os.path.join(hub_spoke_dir, rel_path)
                
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(src_file, dest_file)
                count += 1
                
    print(f"[{repo_name}] Successfully scraped {count} forensic documents into the Hub.")

if __name__ == "__main__":
    print("==================================================")
    print("  ECOSYSTEM DAEMON: FORENSIC REGISTRY AGGREGATOR  ")
    print("==================================================")
    
    os.makedirs(HUB_DIR, exist_ok=True)
    
    for gh_name, local_dir in SPOKE_MAP.items():
        local_path = rf"D:\GitHub\{local_dir}"
        # We pass gh_name to gh clone, but local_path to the scraper
        git_pull_or_clone(gh_name, local_path)
        scrape_docs(gh_name, local_path)
        
    print("\nAggregation complete. Internal Registry is fresh.")
