import os
import glob

dirs_to_scan = [
    r"D:\GitHub\global_agent\registry\linkedin\threads",
    r"D:\GitHub\global_agent\registry\linkedin\posted",
    r"D:\GitHub\global_agent\registry\linkedin\drafts"
]

output_path = r"D:\GitHub\global_agent\registry\linkedin\MASTER_LINKEDIN_CONTEXT.md"
base_dir = r"D:\GitHub\global_agent\registry\linkedin"

with open(output_path, "w", encoding="utf-8") as out:
    out.write("# Master LinkedIn Context Bundle\n\n")
    out.write("This document contains all active threads, posted content, and drafts for the EN-OS LinkedIn strategy.\n\n")
    
    for d in dirs_to_scan:
        # Use recursive globbing to catch anything in comments/ or archive/
        md_files = glob.glob(os.path.join(d, "**", "*.md"), recursive=True)
        for f in md_files:
            # Skip the output file
            if f == output_path:
                continue
                
            rel_path = os.path.relpath(f, start=base_dir)
            out.write(f"\n\n---\n## File: {rel_path}\n---\n\n")
            
            try:
                with open(f, "r", encoding="utf-8") as infile:
                    out.write(infile.read().strip() + "\n")
            except Exception as e:
                out.write(f"[Error reading file: {e}]\n")

print(f"Success! Bundle compiled to: {output_path}")
