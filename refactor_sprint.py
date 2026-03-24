import json
import re

json_path = "d:/GitHub/global_agent/project5.json"
old_plan_path = "d:/GitHub/global_agent/registry/portfolio/audits/2026-03-22_Sprint_Plan.md"
out_path = "d:/GitHub/global_agent/registry/portfolio/audits/2026-03-23_Sprint_Plan.md"

with open(json_path, 'r', encoding='utf-8-sig') as f:
    items = json.load(f).get("items", [])

with open(old_plan_path, 'r', encoding='utf-8') as f:
    old_plan = f.read()

# Build a fast lookup for all current items by title or issue number
issue_map = {}
for i in items:
    url = i.get('content', {}).get('url', '')
    title = i.get('title', '')
    issue_num = ""
    repo = "draft"
    if url:
        parts = url.split('/')
        if len(parts) >= 7:
            repo = parts[4]
            issue_num = parts[6]
    
    # Store item metadata
    issue_map[url] = {
        'repo': repo,
        'num': issue_num,
        'title': title,
        'url': url,
        'status': i.get('status', 'Todo'),
        'labels': [l.get('name') if isinstance(l, dict) else l for l in i.get('labels', [])]
    }
    
# Let's categorize known issues from the old plan to their waves
# A simple regex to find issue links like [repo#num](url)
# Actually, the old plan just had their numbers.
# I'll just put the newly migrated issues into a Triage wave, and keep the structure.

lines = []
lines.append("# Sprint Plan — 2026-03-23")
lines.append("> Generated: 2026-03-23 | Refactored with exact waves and issue links.")
lines.append("> Source: Live GitHub Project #5 pull (Consolidated with #4, #7, #8, #9)")
lines.append("")
lines.append("## ✅ Session Accomplishments (2026-03-23 — Session 4/5)")
lines.append("- **[global_agent#72](https://github.com/mechanistic-org/global_agent/issues/72) CLOSED** — Allan Evans Reply finalized and posted.")
lines.append("- **[global_agent#71](https://github.com/mechanistic-org/global_agent/issues/71) CLOSED** — Projects #4, #7, #8, #9 successfully migrated to #5 and deleted.")
lines.append("- **portfolio#53 IN PROGRESS** — Wave 1-3 archival cleanup complete. Deployed to production.")
lines.append("")

# Manual buckets based on old plan + status mapping
sprint_now = []
sprint_2 = []
sprint_3 = []
sprint_4 = []
backlog_docs = []
triage_new = []

# Hardcoded logic mapping from the old plan to ensure continuity
known_sprint_now = ["portfolio/issues/58", "mechanistic/issues/6", "MO/issues/8", "hyphen/issues/7", "global_agent/issues/72"]
known_sprint_2 = ["portfolio/issues/53", "global_agent/issues/47", "global_agent/issues/54", "portfolio/issues/57"]
known_sprint_3 = ["global_agent/issues/62", "portfolio/issues/47", "portfolio/issues/51", "portfolio/issues/44"]
known_sprint_4 = ["global_agent/issues/61", "global_agent/issues/51", "global_agent/issues/53", "global_agent/issues/55", "global_agent/issues/49"]
known_backlog = ["global_agent/issues/56", "portfolio/issues/56", "portfolio/issues/55", "portfolio/issues/54", "mechanistic/issues/4", "mechanistic/issues/8", "mechanistic/issues/9", "mechanistic/issues/10"]

for url, data in issue_map.items():
    if not url: 
        triage_new.append(data)
        continue
        
    if any(k in url for k in known_sprint_now):
        sprint_now.append(data)
    elif any(k in url for k in known_sprint_2):
        sprint_2.append(data)
    elif any(k in url for k in known_sprint_3):
        sprint_3.append(data)
    elif any(k in url for k in known_sprint_4):
        sprint_4.append(data)
    elif any(k in url for k in known_backlog):
        backlog_docs.append(data)
    else:
        # If it's closed in GitHub, skip or add to a closed list?
        # Actually, if it's new from the migration, drop it in Triage.
        triage_new.append(data)

def render_table(issues, title, description=""):
    out = [f"## {title}"]
    if description:
        out.append(f"> {description}")
        out.append("")
    out.append("| Issue | Title | Project Status |")
    out.append("|---|---|---|")
    for i in issues:
        link = f"[{i['repo']}#{i['num']}]({i['url']})" if i['url'] else "Draft"
        out.append(f"| {link} | **{i['title']}** | `{i['status']}` |")
    out.append("")
    return "\n".join(out)

lines.append(render_table(sprint_now, "🔴 Sprint Now — Execute First"))
lines.append(render_table(sprint_2, "🟡 Sprint 2 — Infrastructure & Platform Stability"))
lines.append(render_table(sprint_3, "🟠 Sprint 3 — Portfolio Product & Agent Infrastructure"))
lines.append(render_table(sprint_4, "🔵 Sprint 4 — Sovereign OS Agent Architecture", "The FastMCP Router (persistent) vs NanoClaw (ephemeral) pattern."))
lines.append(render_table(backlog_docs, "⚪ Backlog / Docs (Low Urgency, Agent-Executable)"))
lines.append(render_table(triage_new, "🟣 Newly Migrated / Triage (From Projects 4, 7, 8, 9)", "These items were just injected into Project 5. Review and slot into Sprints above."))

lines.append("---")
lines.append("## 🚀 Next Session Start")
lines.append("Run `/session_open` → board shows Sprint Now P0s. Triage the purple wave!")

with open(out_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

print("Successfully refactored sprint plan to 2026-03-23_Sprint_Plan.md")
