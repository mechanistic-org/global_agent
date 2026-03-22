import os
import re
import argparse

def extract_component_data(file_context: str) -> dict:
    """Extracts Component bounds and TypeScript Props via native AST/regex."""
    comp_match = re.search(r"export\s+(?:const|function|default\s+function)\s+([A-Z]\w+)", file_context)
    component_name = comp_match.group(1) if comp_match else "UnknownComponent"
    
    prop_match = re.search(r"(?:interface|type)\s+Props\s*=?\s*{(.*?)}", file_context, re.DOTALL)
    props = prop_match.group(1).strip() if prop_match else "None (Static Geometry)"
    props = re.sub(r"\s+", " ", props)
    return {"name": component_name, "props": props}

def execute_global_recon(target_dir: str, spoke_name: str):
    print("==================================================")
    print(f"  NODE 0: ALGORITHMIC RECON CRAWLER ({spoke_name.upper()})")
    print("==================================================")
    
    # Dynamically inject into the correct Spoke isolated registry bucket
    registry_output = os.path.join(r"d:\GitHub\global_agent\registry", spoke_name.lower(), "ARCHITECTURE_INDEX.md")
    os.makedirs(os.path.dirname(registry_output), exist_ok=True)
    
    results = []
    print(f"-> Sweeping architecture boundaries at: {target_dir}")
    if not os.path.exists(target_dir):
        print(f"[FATAL] Target framework {target_dir} is physically missing.")
        return
        
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith((".tsx", ".astro")) and not file.endswith(".test.tsx"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, target_dir)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = extract_component_data(f.read())
                        if data["name"] != "UnknownComponent":
                            out_path = rel_path.replace(os.sep, '/')
                            results.append(f"### `{data['name']}`\n- **Import:** `import {data['name']} from '@components/{out_path}'`\n- **TS Props:** `{data['props']}`\n")
                except Exception as e:
                    print(f"[RECON ERROR] Failed to parse AST on {rel_path}: {e}")
                    
    print(f"-> Global Extraction complete. {len(results)} exact nodes mathematically trapped.")
    
    with open(registry_output, "w", encoding="utf-8") as out:
        out.write(f"# {spoke_name.upper()} Architecture Map (Node 0 Hub Registry)\n\n")
        out.write("This explicit mapping defines the exact geometric constraints required for Spoke UI generative loops. "
                  "Swarms MUST organically extract Prop arrays from this layout BEFORE hallucinating `<Component>` bindings.\n\n")
        out.write("---\n\n".join(results))
        
    print(f"-> SUCCESS: Telemetry mapped. FastMCP Context Registry updated at: {registry_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Global Node 0 UI Reconnaissance Crawler")
    parser.add_argument("--spoke", type=str, required=True, help="Name of the target spoke (e.g., 'portfolio', 'mo')")
    parser.add_argument("--target", type=str, required=True, help="Absolute path to the target component directory")
    
    args = parser.parse_args()
    execute_global_recon(args.target, args.spoke)
