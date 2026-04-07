import os
import sys
import argparse
import json
import urllib.request
import re
import yaml
from datetime import datetime

ENOS_ROOT = os.environ.get("ENOS_ROOT", r"D:\GitHub\global_agent")
REGISTRY_ROOT = os.path.abspath(os.path.join(ENOS_ROOT, "registry"))

def scaffold_prd(title: str, problem: str) -> str:
    prompt = (
        "You are the EN-OS PRD Scaffolding Engine. Convert the following target problem and title into a rigorous, agile Epic PRD.\n"
        "You must rigidly structure your response with these exact headers:\n"
        "## Strategic Overview\n"
        "## Core Constraints\n"
        "## System Interactions\n"
        "## Definition of Done (DoD)\n\n"
        "Do not include conversational filler. Do not use Em-Dashes (use ' - ' instead). Be concise, actuarial, and engineering-focused.\n\n"
        f"TITLE: {title}\n"
        f"PROBLEM STATEMENT: {problem}\n"
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
        print(f"[PrdScaffolder] LLM Request Failed: {e}", file=sys.stderr)
        return ""

def main():
    parser = argparse.ArgumentParser(description="EN-OS PRD Scaffolding Engine")
    parser.add_argument("--title", required=True, help="Short title of the Epic.")
    parser.add_argument("--problem", required=True, help="The fuzzy problem statement or goal.")
    parser.add_argument("--project", required=True, help="Target project namespace (e.g., 'portfolio').")
    args = parser.parse_args()

    print(f"[PrdScaffolder] Generating agile Epic PRD for '{args.title}' in namespace '{args.project}'...")
    
    markdown_output = scaffold_prd(args.title, args.problem)
    
    if not markdown_output:
        print("ERROR: LLM failed to return a valid PRD.", file=sys.stderr)
        sys.exit(1)

    # Sanitize title for filename
    safe_title = re.sub(r'[^a-z0-9_-]', '_', args.title.lower())
    
    # Write to target epic directory
    target_dir = os.path.join(REGISTRY_ROOT, args.project, "epics")
    os.makedirs(target_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_filepath = os.path.join(target_dir, f"{date_str}_{safe_title}.md")
    
    # Frontmatter
    frontmatter = {
        "title": args.title,
        "date": date_str,
        "status": "DRAFT",
        "project": args.project
    }
    frontmatter_yaml = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)
    
    final_doc = f"---\n{frontmatter_yaml}---\n\n{markdown_output}"
    
    with open(out_filepath, 'w', encoding='utf-8') as f:
        f.write(final_doc)
        
    print(f"[PrdScaffolder] PRD generated and saved to {out_filepath}")

if __name__ == "__main__":
    main()
