import subprocess
import json
import sys
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

def run_graphql():
    query = """
    query {
      organization(login: "mechanistic-org") {
        projectV2(number: 5) {
          items(first: 100) {
            nodes {
              content {
                ... on Issue {
                  title
                  number
                  repository { name }
                }
              }
              fieldValues(first: 10) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field {
                      ... on ProjectV2SingleSelectField { name }
                    }
                  }
                  ... on ProjectV2ItemFieldIterationValue {
                    title
                    startDate
                    duration
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error calling GitHub API: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)

def main():
    data = run_graphql()
    items = data.get("data", {}).get("organization", {}).get("projectV2", {}).get("items", {}).get("nodes", [])
    
    parsed_items = []
    
    # We will compute the current date and map iterations
    today = datetime.now()
    
    for node in items:
        issue = node.get("content")
        if not issue or "title" not in issue: continue
        
        repo = issue.get("repository", {}).get("name", "unknown") if issue.get("repository") else "unknown"
        number = issue.get("number", "?")
        title = issue.get("title", "Untitled")
        
        fields = {}
        for fv in node.get("fieldValues", {}).get("nodes", []):
            if "startDate" in fv: # Iteration
                # Calculate if it's current or next
                start_date = datetime.strptime(fv["startDate"], "%Y-%m-%d")
                duration_days = fv["duration"]
                end_date = start_date + timedelta(days=duration_days)
                
                fields["IterationTitle"] = fv["title"]
                fields["StartDate"] = start_date
                fields["EndDate"] = end_date
                
                if start_date <= today < end_date:
                    fields["Bucket"] = "NOW"
                elif start_date >= end_date:
                    # Actually wait, if today < start_date, it's future
                    pass
                
                if today < start_date:
                    # It's a future iteration. We'll label the roughly "Next" one
                    fields["Bucket"] = "NEXT/LATER"
                elif today >= end_date:
                    # Past iteration, shouldn't really happen for active tickets unless carried over, we treat as NOW overdue
                    fields["Bucket"] = "NOW (Overdue)"
                    
            elif "name" in fv and "field" in fv:
                field_name = fv["field"]["name"]
                fields[field_name] = fv["name"]
        
        status = fields.get("Status", "Unknown")
        if status in ["Done", "Archived"]:
            continue
            
        bucket = fields.get("Bucket", "BACKLOG")
        if "IterationTitle" not in fields:
            bucket = "BACKLOG"
            fields["IterationTitle"] = "Unassigned"
            
        parsed_items.append({
            "repo": repo,
            "number": number,
            "title": title,
            "status": status,
            "priority": fields.get("Priority", "P99"), # P0, P1, P2, P3
            "iteration": fields.get("IterationTitle", "Unassigned"),
            "bucket": bucket,
            "start_date": fields.get("StartDate", datetime.max)
        })
    
    # Segment into buckets: NOW, NEXT, LATER
    now_items = [i for i in parsed_items if "NOW" in i["bucket"]]
    future_items = [i for i in parsed_items if i["bucket"] == "NEXT/LATER"]
    backlog_items = [i for i in parsed_items if i["bucket"] == "BACKLOG"]
    
    # Sort definitions
    def sort_prio(x):
        return (x["priority"], x["repo"], x["number"])

    now_items.sort(key=sort_prio)
    future_items.sort(key=lambda x: (x["start_date"], x["priority"]))
    backlog_items.sort(key=sort_prio)
    
    print("=" * 60)
    print("🚀 SESSION TRIAGE: NOW, NEXT, LATER")
    print("=" * 60)
    
    # ---------------- NOW ----------------
    print(f"\n# 🔴 NOW — Active Iteration & Overdue Blockers")
    if not now_items:
        print("  (No active items in the current iteration)")
    
    current_prio = None
    prio_headers = {
        "P0": "🔥 P0: BLOCKERS & PREREQUISITES (DO THIS FIRST)",
        "P1": "⚡ P1: HIGH PRIORITY",
        "P2": "🛠️ P2: STANDARD WORK",
        "P3": "🌅 P3: HORIZON / LOW PRIORITY",
        "P99": "❓ UNPRIORITIZED"
    }

    for item in now_items:
        p = item["priority"]
        if p != current_prio:
            current_prio = p
            header = prio_headers.get(p, prio_headers["P99"])
            print(f"\n  {header}")
        
        print(f"  - [{item['status']}] {item['repo']}#{item['number']} — {item['title']} ({item['iteration']})")
        
    # ---------------- NEXT ----------------
    print(f"\n\n# 🟡 NEXT — Upcoming Iterations")
    if not future_items:
        print("  (No upcoming items scheduled)")
    for item in future_items:
        print(f"  - [{item['iteration']}] {item['priority']} | {item['repo']}#{item['number']} — {item['title']}")
        
    # ---------------- LATER ----------------
    print(f"\n\n# 🔵 LATER — Backlog / Unassigned")
    if not backlog_items:
        print("  (Backlog is clear)")
    for item in backlog_items:
        print(f"  - [Backlog] {item['priority']} | {item['repo']}#{item['number']} — {item['title']}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
