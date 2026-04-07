import os
import json
import time
import datetime
import urllib.request
import hashlib
from pathlib import Path

# Config
SCAN_INTERVAL_SECONDS = 3600  # 1 hour loop rhythm
ENOS_ROOT = Path(__file__).parent.parent
FAILSAFES_LOG = ENOS_ROOT / ".system_generated" / "logs" / "failsafes.log"
KAIROS_DIR = ENOS_ROOT / "registry" / "workflow_state"
KAIROS_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = KAIROS_DIR / "kairos_state.json"
LEDGER_FILE = KAIROS_DIR / "kairos_master_ledger.md"

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def dream_cycle():
    print(f"[{datetime.datetime.now().isoformat()}] [KAIROS] Waking for Dream Cycle...")
    
    if not FAILSAFES_LOG.exists():
        print(f"[KAIROS] No failsafes log found at {FAILSAFES_LOG}. Sleeping.")
        return
        
    current_hash = get_file_hash(FAILSAFES_LOG)
    
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            if state.get("last_failsafe_hash") == current_hash:
                print("[KAIROS] Log state unchanged. Hash matches. Sleeping.")
                return
                
    with open(FAILSAFES_LOG, "r", encoding="utf-8") as f:
        log_content = f.read()
        
    if not log_content.strip():
        print("[KAIROS] Failsafes log is empty. Sleeping.")
        return
        
    # Protect memory: keep at most the last 50,000 characters of logs
    log_content = log_content[-50000:]
    
    print("[KAIROS] Ingesting memory trails. Compressing structural truths using phi3...")
    
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=json.dumps({
        "model": "phi3",
        "prompt": (
            "You are KAIROS, the auto-dream daemon for the Sovereign Agent infrastructure.\n"
            "Analyze the following agent telemetry and failure logs.\n"
            "Distill the core architectural issues, recurring break-points, and overarching truths into a dense, hostile-SCADA style Markdown summary.\n"
            "Format the output strictly as Markdown without conversational filler.\n\n"
            f"--- RECENT FAILS AND TELEMETRY ---\n{log_content}"
        ),
        "stream": False
    }).encode('utf-8'))
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=300.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            distilled = data.get('response', '')
            
            if distilled:
                timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M")
                with open(LEDGER_FILE, "a", encoding="utf-8") as out:
                    out.write(f"---\ntype: kairos_dream\ntimestamp: {timestamp}\n---\n\n")
                    out.write(distilled + "\n\n")
                    # Strict Write Discipline
                    out.flush()
                    os.fsync(out.fileno())
                    
                with open(STATE_FILE, "w") as f:
                    json.dump({"last_failsafe_hash": current_hash, "last_run": timestamp}, f)
                    
                print(f"[KAIROS] Dream locked to {LEDGER_FILE.name}. Sleep sequence engaged.")
    except Exception as e:
        print(f"[KAIROS] REM Cycle violently awoken (Error): {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("KAIROS / AUTODREAM DAEMON ONLINE")
    print(f"Dream cycle interval: {SCAN_INTERVAL_SECONDS}s")
    print("=" * 50)
    
    # Run once on boot cleanly
    try:
        dream_cycle()
    except Exception as e:
        print(f"FATAL KAIROS BOOT ERROR: {e}")
        
    while True:
        time.sleep(SCAN_INTERVAL_SECONDS)
        try:
            dream_cycle()
        except Exception as e:
            print(f"FATAL KAIROS ERROR: {e}")
