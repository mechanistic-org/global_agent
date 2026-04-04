import sys
import subprocess
import codecs
import argparse
from pathlib import Path

# Ensure console output uses utf-8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

uid = "b8f893fe-234c-44ca-9d92-8fff6f82e53d"
cli = r"C:\Users\erik\AppData\Roaming\Python\Python314\Scripts\nlm.exe"

parser = argparse.ArgumentParser(description="Trigger NLM audio generation")
parser.add_argument("--prompt", type=str, help="Prompt text or path to a text file.")
args = parser.parse_args()

print("Triggering PODCAST_NLM-INPUT Audio Generation...")

# Check if prompt is a file path
if args.prompt and Path(args.prompt).is_file():
    with open(args.prompt, "r", encoding="utf-8") as f:
        podcast_prompt = f.read()
elif args.prompt:
    podcast_prompt = args.prompt
else:
    # Fallback to the legacy location if running in portfolio context
    legacy_path = Path("public/assets/prompts/PODCAST_NLM-INPUT.txt")
    if legacy_path.exists():
        with open(legacy_path, "r", encoding="utf-8") as f:
            podcast_prompt = f.read()
    else:
        print("❌ Error: No --prompt provided and fallback file not found.")
        sys.exit(1)

# Crucial: Use --length short and pass the exact prompt via --focus
audio_cmd = [
    cli, "audio", "create", uid, 
    "--length", "short", 
    "--focus", podcast_prompt, 
    "-y"
]
audio_result = subprocess.run(audio_cmd, capture_output=True, text=True, encoding="utf-8")
print(f"Audio Task Initiated:\n{audio_result.stdout}")
if audio_result.stderr:
    print(f"Audio Task Warnings/Errors:\n{audio_result.stderr}")
