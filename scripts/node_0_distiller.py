import os
import json
from pathlib import Path

# --- CONFIGURATION ---
MECHANISTIC_DOCS_DIR = Path("D:/GitHub/mechanistic/docs/projects/mobile_outfitters")
INDEX_FILE = MECHANISTIC_DOCS_DIR / "resource_index.md"
ORIGIN_STORY_FILE = Path("D:/GitHub/mechanistic/src/dfmea_core/data/origin_story.md")

OUTPUT_PAYLOAD = Path("D:/GitHub/global_agent/docs/v31_synthesis_baseline.md")

def compile_baseline():
    print(f"[NODE 0] Compiling Context Baseline for Epic V32...")
    
    baseline_content = [
        "# NODE 0 Context Baseline: Mobile Outfitters Holy Grail",
        "> This document is the verified distillation of 31 dashboard revisions and 2+ weeks of NLP tuning. It MUST be ingested by the Swarm before synthesizing new PRDs.",
        "---"
    ]

    # 1. Ingest the Resource Index
    if INDEX_FILE.exists():
        print(f"  -> Ingesting {INDEX_FILE.name}")
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            baseline_content.append("\n## Reference Architecture (The Resource Index)")
            baseline_content.append(f.read())
    else:
        print(f"  [!] Missing {INDEX_FILE}")

    # 2. Ingest the Origin Story (The Philosophical Core)
    if ORIGIN_STORY_FILE.exists():
        print(f"  -> Ingesting {ORIGIN_STORY_FILE.name}")
        with open(ORIGIN_STORY_FILE, 'r', encoding='utf-8') as f:
            baseline_content.append("\n## The Philosophical Core (Origin Story constraints)")
            baseline_content.append(f.read())
    else:
        print(f"  [!] Missing {ORIGIN_STORY_FILE}")
        
    # 3. Explicit Guardrails extracted from yesterday's failed run
    baseline_content.append("\n## STRICT NODE 1-6 SWARM GUARDRAILS")
    baseline_content.append("""
1. **NO UI HALLUCINATIONS:** Nodes 1-6 are forbidden from inventing UI components. You output pure mathematical/legal JSON.
2. **THE 15-INCH RULE:** The physical envelope constraint of 15 inches is NON-NEGOTIABLE. Any failure mode violating this must be scored as a CRITICAL BLOCKER.
3. **THE KINEMATIC ZERO DECREE:** You must assume workers will force mechanisms ("Human Unpredictability").
4. **THE DRAWBRIDGE PIVOT:** Every mechanical failure mathematically maps to a legal liability clause. You must supply ROI defense mechanisms for every physical risk.
5. **NO FLUFF:** The aesthetic is 'Hostile UI' SCADA presentation. Keep explanations brutally concise.
    """)

    # Write the compiled output to global_agent for the Swarm to ingest
    os.makedirs(OUTPUT_PAYLOAD.parent, exist_ok=True)
    with open(OUTPUT_PAYLOAD, 'w', encoding='utf-8') as f:
        f.write("\n".join(baseline_content))
        
    print(f"\n[+] Baseline successfully distilled to: {OUTPUT_PAYLOAD}")
    print(f"    Nodes 1-6 must read this file before querying PRD-2.")

if __name__ == "__main__":
    compile_baseline()
