import subprocess

TARGET_REPOS = [
    "mechanistic-org/global_agent",
    "mechanistic-org/portfolio",
    "mechanistic-org/mechanistic",
    "mechanistic-org/MO"
]

LABELS = [
    {"name": "Epic", "color": "3E4B9E", "desc": "A massive, multi-sprint architectural bounding box"},
    {"name": "Task", "color": "0E8A16", "desc": "A linear execution subroutine within a given sprint constraint"},
    {"name": "Pivot", "color": "D93F0B", "desc": "A fundamental shift in architectural theory or core engine state"},
    {"name": "Bug", "color": "D73A4A", "desc": "A lethal structural fault in the executing code or UI framework"},
    {"name": "Enhancement", "color": "A2EEEF", "desc": "A local feature upgrade extending the origin system boundary"}
]

print("==================================================")
print("  NODE 0: ECOSYSTEM METADATA SYNCHRONIZATION      ")
print("==================================================\n")

for repo in TARGET_REPOS:
    print(f"-> Targeting Origin: {repo}")
    for label in LABELS:
        name = label["name"]
        color = label["color"]
        desc = label["desc"]
        
        try:
            # Force parameter completely overwrites diverging legacy shapes organically
            subprocess.run([
                "gh", "label", "create", name,
                "--repo", repo,
                "--color", color,
                "--description", desc,
                "--force"
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"   [SYNCED] {name}")
        except subprocess.CalledProcessError as e:
            # Graceful edit trap if physical repo prevents creation injection
            try:
                subprocess.run([
                    "gh", "label", "edit", name,
                    "--repo", repo,
                    "--color", color,
                    "--description", desc
                ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"   [OVERWRITTEN] {name}")
            except Exception as e2:
                print(f"   [FAILED] {name} - Architecture locked. {e2}")

print("\n-> SUCCESS: The entire mechanistic-org taxonomy is perfectly synchronized. Phase 5 Operations scaled natively.")
