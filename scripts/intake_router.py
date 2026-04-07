"""
intake_router.py — The EN-OS Intake Engine (Brains in Boxes)
=============================================================
A static gateway that accepts unstructured local data dumps (.mp4, .pdf, .txt),
dynamically classifies their domain via Gemini, and statically dispatches them
to specific downstream agents or scripts (e.g., local Whisper parsing).

Usage:
    python scripts/intake_router.py
"""

import os
import shutil
import argparse
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# --- CONFIGURATION ---
REPO_ROOT = Path(r"D:\GitHub\global_agent")
INBOX_DIR = REPO_ROOT / "inbox"
ARCHIVE_DIR = INBOX_DIR / "archive"

# Supported static routes based on format
AUDIO_EXTENSIONS = (".wav", ".mp3", ".m4a", ".mp4", ".webm", ".mkv")
TEXT_EXTENSIONS = (".txt", ".md", ".json", ".csv")

load_dotenv(REPO_ROOT / ".env")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def setup_directories():
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def dispatch_audio(file_path: Path):
    """
    Subprocess dispatch to local whisper transcription.
    """
    script_path = REPO_ROOT / "scripts" / "transcribe_local.py"
    # The transcribe script processes a whole directory natively,
    # but since it's already coded to look at the inbox by default, we just invoke it.
    print(f"🎙️ AUDIO DETECTED: Dispatching '{file_path.name}' to transcribe_local.py")
    subprocess.run(["python", str(script_path), "--source", str(INBOX_DIR)])
    
    # transcribe_local.py handles the extraction internally now. We just move the files to archive.
    archive_path = ARCHIVE_DIR / file_path.name
    shutil.move(str(file_path), str(archive_path))
    
    # also move transcript and mining reports over if they are cleanly tied, 
    # but transcribe_local currently outputs to the target_dir (INBOX).
    # Since it outputs alongside the audio, we should clean up transcripts.
    transcript = Path(str(file_path) + ".transcript.txt")
    if transcript.exists():
        shutil.move(str(transcript), str(ARCHIVE_DIR / transcript.name))
    
    print(f"📦 Archived: {file_path.name}")

def dispatch_text(file_path: Path):
    """
    Uses LLM classification to decide if it's a generic knowledge dump 
    (goes to mine_session.py) or a structured physical constraints doc 
    (goes to mcp_prd_linter / fmea_generator).
    """
    # Read snippet
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"❌ Failed to read text file {file_path.name}: {e}")
        return
        
    snippet = content[:8000]
    domain = "generic_dump"
    
    if GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = (
                "You are an intake triage router. Read this snippet and classify the core domain.\n"
                "Respond strictly with one of these keywords:\n"
                "- 'HARDWARE_PRD' (if it details physical mechanical components, FMEA, NPI gates, or quantitative tolerances)\n"
                "- 'GENERIC_DUMP' (if it's a conversation dump, strategy log, notes, software planning, etc.)\n"
                "---\n"
                f"{snippet}\n"
            )
            response = model.generate_content(prompt)
            classification = response.text.strip().upper()
            
            if "HARDWARE" in classification:
                domain = "hardware_prd"
                
        except Exception as e:
            print(f"⚠️ Gemini Classification Failed, falling back to 'generic_dump': {e}")
    else:
        print("⚠️ No Gemini API Key found. Routing default to 'generic_dump'.")

    # Static dispatch based on domain
    if domain == "hardware_prd":
        print(f"⚙️ HARDWARE PRD DETECTED: Dispatching '{file_path.name}' to MCP Linter...")
        # Placeholder for dispatch: mcp_prd_linter is usually an MCP tool, but if we need a direct script we invoke it.
        # Right now we just archive it with a warning as the PRD linter runs on demand over MCP.
        print(f"   [Notice] PRD {file_path.name} recognized. Ready to be queried by enos_router.")
        archive_path = ARCHIVE_DIR / file_path.name
        shutil.move(str(file_path), str(archive_path))
        
    else:
        print(f"🧠 GENERIC DUMP DETECTED: Dispatching '{file_path.name}' to mine_session.py")
        script_path = REPO_ROOT / "scripts" / "mine_session.py"
        subprocess.run(["python", str(script_path), "--input-text", content])
        
        archive_path = ARCHIVE_DIR / file_path.name
        shutil.move(str(file_path), str(archive_path))

def main():
    parser = argparse.ArgumentParser(description="EN-OS Intake Engine Router")
    args = parser.parse_args()
    
    setup_directories()
    
    files = [f for f in INBOX_DIR.iterdir() if f.is_file()]
    if not files:
        print(f"📭 Inbox is empty: {INBOX_DIR}")
        return
        
    print(f"📥 Found {len(files)} files in inbox. Triaging...")
    
    for f in files:
        ext = f.suffix.lower()
        if ext in AUDIO_EXTENSIONS:
            dispatch_audio(f)
        elif ext in TEXT_EXTENSIONS:
            dispatch_text(f)
        else:
            print(f"⚠️ Unrecognized format '{ext}'. Skipping: {f.name}")
            
    print("✅ Triage complete.")

if __name__ == "__main__":
    main()
