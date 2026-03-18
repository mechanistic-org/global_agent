import time
import os
import shutil
import subprocess
from pathlib import Path

# Import paths from the new global config
from global_config import GLOBAL_INBOX_DIR, get_repo_root

def isolate_file(file_path: Path) -> Path:
    """Moves the file to the processed directory to prevent double-processing."""
    processed_dir = GLOBAL_INBOX_DIR / "processed"
    target_path = processed_dir / file_path.name
    try:
        if target_path.exists():
            os.remove(target_path)
        shutil.move(str(file_path), str(target_path))
        return target_path
    except Exception as e:
        print(f"[DAEMON] ⚠️ Could not isolate file (might be locked): {e}")
        return None

def process_file(file_path: Path):
    """Routes the file to the correct ecosystem pipeline based on filename."""
    filename = file_path.name.lower()
    
    # --- 1. Routing Logic based on Filename Heuristics ---
    task_type = None
    if "prd" in filename:
        task_type = "PRD"
    elif "dfmea" in filename:
        task_type = "DFMEA"
    
    if not task_type:
        print(f"[DAEMON] ❌ Unrecognized file type '{filename}'. Must contain 'PRD' or 'DFMEA'. Archiving.")
        return

    print(f"\n[DAEMON] ⚙️ Routing '{filename}' to Mechanistic Node as type: {task_type}")

    # --- 2. Execute target sequence ---
    try:
        mechanistic_root = get_repo_root('mechanistic')
        script_target = mechanistic_root / 'scripts' / 'generate_structured_docs.ts'
        
        print(f"[DAEMON] 🚀 Firing Sequence: npx tsx {script_target.name} {task_type} {file_path}")
        
        # Use shell=True for npx resolution on Windows
        result = subprocess.run(
            ["npx", "tsx", "scripts/generate_structured_docs.ts", task_type, str(file_path)],
            cwd=str(mechanistic_root), 
            capture_output=True,
            text=True,
            shell=True
        )

        if result.stdout:
            print(result.stdout)
            
        if result.returncode == 0:
            print(f"[DAEMON] ✅ Successfully synthesized {task_type} payload.")
        else:
            print(f"[DAEMON] ❌ Generation Failed (Exit {result.returncode})")
            print(f"Error Log:\n{result.stderr}")

    except Exception as e:
        print(f"[DAEMON] 💥 Fatal routing error: {e}")

def start_watcher():
    print(f"\n======================================")
    print(f"⚡ SOLOPRENEUR STACK OS-POLLING DAEMON ONLINE ⚡")
    print(f"======================================")
    print(f"👁️‍🗨️  Watching Inbox: {GLOBAL_INBOX_DIR}")
    print(f"Press CTRL+C to stop the daemon.\n")
    
    try:
        while True:
            # Poll the directory for all files
            for filename in os.listdir(GLOBAL_INBOX_DIR):
                file_path = GLOBAL_INBOX_DIR / filename
                
                # We only want files directly in the inbox, not directories like 'processed'
                if file_path.is_file():
                    # Only process text files
                    if filename.lower().endswith(".txt") or filename.lower().endswith(".md") or filename.lower().endswith(".docx"):
                        print(f"\n[DAEMON] 🚨 Detected payload drop: {filename}")
                        # Immediately isolate
                        isolated_path = isolate_file(file_path)
                        if isolated_path:
                            # Process it
                            process_file(isolated_path)
            
            # Sleep 3 seconds before polling again to reduce CPU spin
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n[DAEMON] 🛑 Stopping Watcher...")

if __name__ == "__main__":
    start_watcher()
