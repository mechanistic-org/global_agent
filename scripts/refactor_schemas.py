import os
import re

base_dir = r"d:\GitHub\global_agent"
schemas_dir = os.path.join(base_dir, "schemas", "skill-returns")
skills_dir = os.path.join(base_dir, ".agent", "skills")

# Mapping from current schema filename to the skill folder name
mapping = {
    "create_issue_summary.json": "create-issue",
    "deploy_production_summary.json": "deploy-production",
    "evidence_extraction_summary.json": "evidence-extraction",
    "hydration_summary.json": "hydrate-project",
    "linkedin_harvest_summary.json": "harvest-linkedin",
    "linkedin_reply_summary.json": "draft-linkedin-reply",
    "linkedin_scaffold_summary.json": "draft-linkedin-post",
    "mining_campaign_summary.json": "run-mining-campaign",
    "processed_notes_summary.json": "process-walk-notes",
    "publish_post_summary.json": "publish-post",
    "scaffold_project_summary.json": "scaffold-project",
    "sync_assets_summary.json": "sync-assets",
    "triage_results.json": "intake-dump",
    "update_resume_summary.json": "update-resume"
}

for old_name, skill_name in mapping.items():
    new_name = f"{skill_name}_summary.json"
    old_path = os.path.join(schemas_dir, old_name)
    new_path = os.path.join(schemas_dir, new_name)
    
    # Rename the schema file if old exists
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")
    elif os.path.exists(new_path):
        print(f"Already renamed: {new_name}")
    else:
        print(f"Warning: neither {old_name} nor {new_name} exist!")
        
    # Update the corresponding SKILL.md file
    skill_md_str = os.path.join(skills_dir, skill_name, "SKILL.md")
    if os.path.exists(skill_md_str):
        with open(skill_md_str, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Regex to catch the current schema string, which might vary but usually is:
        # schema: "file://schemas/skill-returns/..."
        # We replace the whole line mapping to the new naming convention
        
        # This regex matches the schema line and replaces the filename part
        # e.g., schema: "file://schemas/skill-returns/anyname.json"
        pattern = r'(schema:\s*"file://schemas/skill-returns/)[^"]+("\s*)'
        new_content = re.sub(pattern, rf'\g<1>{new_name}\g<2>', content)
        
        if new_content != content:
            with open(skill_md_str, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_content)
            print(f"Updated SKILL.md for {skill_name}")
        else:
            print(f"SKILL.md for {skill_name} already correct or pattern not found")
    else:
        print(f"SKILL.md not found for {skill_name}")

print("Done.")
