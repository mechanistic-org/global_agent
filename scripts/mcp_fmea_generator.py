import os
import sys
import json
import argparse
import urllib.request
import yaml
import chromadb

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dfmea_schemas import PhysicsVault

ENOS_ROOT = os.environ.get("ENOS_ROOT", r"D:\GitHub\global_agent")
REGISTRY_ROOT = os.path.abspath(os.path.join(ENOS_ROOT, "registry"))
chroma_client = chromadb.PersistentClient(path=os.path.join(REGISTRY_ROOT, ".chroma_db"))
collection = chroma_client.get_or_create_collection(name="forensic_telemetry")

def generate_fmea(input_path: str, project_name: str, model: str = "qwen2.5-coder:32b"):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            prd_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Failed to read input file {input_path}. {e}")
        sys.exit(1)

    schema_json = json.dumps(PhysicsVault.model_json_schema(), indent=2)

    prompt = f"""You are a ruthless Mechanical Engineering constraint engine. Your goal is to evaluate the provided PRD or narrative and extract a rigorous Failure Modes and Effects Analysis (FMEA).

Strict Rules of Engagement:
1. Extract every possible physical, mechanical, thermal, or process failure mode you can deduce from the narrative.
2. Structure the output EXACTLY matching the JSON schema provided below.
3. Be purely objective. No conversational fluff or disclaimers.
4. Output raw JSON only.

JSON SCHEMA:
{schema_json}

PRD NARRATIVE TO EVALUATE:
{prd_content[:20000]}
"""

    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1}
    }).encode('utf-8'))
    req.add_header("Content-Type", "application/json")

    print(f"[FMEA] Interrogating {model} for semantic failure extraction...", file=sys.stderr)
    try:
        with urllib.request.urlopen(req, timeout=300.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            llm_output = data.get('response', '{}')
    except Exception as e:
        print(f"CRITICAL: Model extraction failed. {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[FMEA] Parsing output and enforcing deterministic arithmetic constraints...", file=sys.stderr)
    try:
        vault_data = json.loads(llm_output)
        vault = PhysicsVault(**vault_data)
    except Exception as e:
        print(f"CRITICAL: LLM output did not match PhysicsVault schema or was malformed JSON. {e}", file=sys.stderr)
        print("Raw Output:", llm_output, file=sys.stderr)
        sys.exit(1)

    table_rows = []
    headers = [
        "Subsystem", "Failure Mode", "Physics Description", "S", "O", "D", 
        "RPN (Fixed)", "Critical Blocker", "Status", "Mitigation", "Knock-On Effects"
    ]
    table_rows.append("| " + " | ".join(headers) + " |")
    table_rows.append("|" + "|".join(["---"] * len(headers)) + "|")

    for node in vault.nodes:
        subsys = node.subsystem_label.replace("|", "")
        for f in node.failures:
            enforced_rpn = f.severity * f.occurrence * f.detection
            
            fm = f.failure_mode.replace("|", "")
            desc = f.description.replace("|", "")
            mitigation = f.mitigation.replace("|", "")
            knock_on = ", ".join(f.knock_on_effects).replace("|", "")

            row = [
                subsys,
                fm,
                desc,
                str(f.severity),
                str(f.occurrence),
                str(f.detection),
                f"**{enforced_rpn}**",
                "Yes" if f.is_critical_blocker else "No",
                f.status.replace("|", ""),
                mitigation,
                knock_on
            ]
            table_rows.append("| " + " | ".join(row) + " |")

    markdown_body = "## Deterministic Physics Vault (FMEA Analysis)\n\n"
    markdown_body += "> **Note:** RPN (Risk Priority Number) is calculated explicitly as $Severity \\times Occurrence \\times Detection$ within the Python constraint boundary, overriding any LLM hallucinations.\n\n"
    markdown_body += "\n".join(table_rows)

    frontmatter = {
        "title": f"FMEA Matrix for {project_name}",
        "date": "2026-04-05",
        "context_node": "fmea"
    }
    
    frontmatter_yaml = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False, allow_unicode=True).strip()
    full_document = f"---\n{frontmatter_yaml}\n---\n\n{markdown_body}"

    # Write to project directory strictly
    target_dir = os.path.join(REGISTRY_ROOT, project_name)
    os.makedirs(target_dir, exist_ok=True)
    filepath = os.path.join(target_dir, "fmea.md")
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_document)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        print(f"CRITICAL: Failed to write flat-file fmea.md. {e}")
        sys.exit(1)

    # Push to ChromaDB safely
    doc_id = f"{project_name}_fmea"
    try:
        collection.upsert(
            documents=[full_document],
            metadatas=[{"project": project_name, "component": "fmea"}],
            ids=[doc_id],
        )
        print("SUCCESS")
    except Exception as e:
        print(f"WARNING: Flat-file saved successfully, but ChromaDB upsert failed due to lock/error: {str(e)}")
        print("SUCCESS")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic FMEA Generator & Matrix RPN Calculator")
    parser.add_argument("--input", required=True, help="Path to input PRD or markdown file")
    parser.add_argument("--project", required=True, help="Target project registry name")
    parser.add_argument("--model", default="qwen2.5-coder:32b", help="Local model to interrogate")

    args = parser.parse_args()
    generate_fmea(args.input, args.project, args.model)
