import os
import sys
import argparse
import json
import urllib.request
import uuid
import yaml

ENOS_ROOT = os.environ.get("ENOS_ROOT", r"D:\GitHub\global_agent")
REGISTRY_ROOT = os.path.abspath(os.path.join(ENOS_ROOT, "registry"))

PROMPTS = {
    "swot": "Generate a rigorous 2x2 SWOT (Strengths, Weaknesses, Opportunities, Threats) matrix as a Markdown table. Apply critical actuarial metrics.",
    "tows": "Generate a TOWS matrix (Threats, Opportunities, Weaknesses, Strengths) focusing on strategic alignment. Output as a Markdown table.",
    "ishikawa": "Generate an Ishikawa (Fishbone) Root-Cause Diagram. Since Mermaid does not natively support fishbones, output a heavily structured Mermaid Mindmap block (` ```mermaid \\n mindmap `). Expand into Methods, Machines, Materials, Measurements, Mother Nature, and Manpower."
}

def generate_matrix(topic: str, matrix_type: str) -> str:
    # If "all", combine prompts
    if matrix_type == "all":
        p_str = (
            "You are the EN-OS matrix generation engine. Based on the following fuzzy market assumption or problem statement, you must output three sequentially rigid visualizations:\n"
            "1. " + PROMPTS["swot"] + "\n"
            "2. " + PROMPTS["tows"] + "\n"
            "3. " + PROMPTS["ishikawa"] + "\n"
        )
    else:
        p_str = (
            "You are the EN-OS matrix generation engine. Based on the following fuzzy market assumption or problem statement, you must output:\n"
            + PROMPTS[matrix_type] + "\n"
        )

    prompt = (
        f"{p_str}\n"
        "Format your output strictly as Markdown without conversational filler. Do NOT use Em-Dashes. Use Space-Dash-Space (' - ') instead.\n\n"
        f"--- TARGET PROBLEM / ASSUMPTION ---\n{topic}\n"
    )

    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=json.dumps({
        "model": "qwen_coder:latest",
        "prompt": prompt,
        "stream": False
    }).encode('utf-8'))
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=300.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('response', '')
    except Exception as e:
        print(f"[MatrixGenerator] LLM Request Failed: {e}", file=sys.stderr)
        return ""

def main():
    parser = argparse.ArgumentParser(description="EN-OS Root-Cause Matrix Generator")
    parser.add_argument("--input-string", required=True, help="The fuzzy problem statement or market assumption.")
    parser.add_argument("--matrix-type", choices=["swot", "tows", "ishikawa", "all"], default="all", help="Visualization type.")
    parser.add_argument("--project", required=True, help="Target project namespace (e.g., 'portfolio').")
    parser.add_argument("--output-mode", choices=["standalone", "raw"], default="raw", help="How to deliver the structural markdown.")
    args = parser.parse_args()

    print(f"[MatrixGenerator] Generating {args.matrix_type.upper()} matrix for project '{args.project}'...")
    
    markdown_output = generate_matrix(args.input_string, args.matrix_type)
    
    if not markdown_output:
        print("ERROR: LLM failed to return a string.", file=sys.stderr)
        sys.exit(1)

    if args.output_mode == "raw":
        # Dump to stdout for the agent to trivially read and inject into current buffers.
        print("\n--- MATRIX OUTPUT RAW ---\n")
        print(markdown_output)
        print("\n-------------------------\n")
    else:
        # Standalone mode: push directly to OS flat-file registry via push_forensic_doc equivalent
        target_dir = os.path.join(REGISTRY_ROOT, args.project, "assets")
        os.makedirs(target_dir, exist_ok=True)
        
        file_id = f"matrix_{args.matrix_type}_{uuid.uuid4().hex[:6]}"
        out_filepath = os.path.join(target_dir, f"{file_id}.md")
        
        frontmatter = {
            "title": f"Root Cause Matrix: {args.matrix_type.upper()}",
            "date": "2026",
            "project": args.project
        }
        frontmatter_yaml = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)
        final_doc = f"---\n{frontmatter_yaml}---\n\n{args.input_string}\n\n{markdown_output}"
        
        with open(out_filepath, 'w', encoding='utf-8') as f:
            f.write(final_doc)
            
        print(f"[MatrixGenerator] Markdown cleanly mapped and saved as standalone at {out_filepath}")

if __name__ == "__main__":
    main()
