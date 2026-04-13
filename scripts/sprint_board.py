#!/usr/bin/env python3
"""
sprint_board.py - EN-OS Session Triage Board

Queries GitHub Projects V2 across all repos in mechanistic-org.
Used by the session_open ritual to declare focal ticket.

Usage:
  python sprint_board.py                      # NOW + NEXT + BACKLOG
  python sprint_board.py --current-iteration  # NOW bucket only (session_open default)
  python sprint_board.py --repo global_agent  # Filter to single repo
  python sprint_board.py --status "In Progress"
  python sprint_board.py --compact            # One line per item, fast scan
  python sprint_board.py --all                # Include Done / Archived
"""

import subprocess
import json
import sys
import argparse
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding="utf-8")

ORG = "mechanistic-org"
PROJECT_NUMBER = 5

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
PRIORITY_LABELS = {
    "P0": "P0  BLOCKER",
    "P1": "P1  HIGH",
    "P2": "P2  STANDARD",
    "P3": "P3  HORIZON",
    None: "UNPRIORITIZED",
}

# Mutable so --all can clear it at runtime
SKIP_STATUSES = {"Done", "Archived"}


# ─────────────────────────────────────────────
# GitHub API
# ─────────────────────────────────────────────

def run_graphql(query: str) -> dict:
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"GitHub API error:\n{result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(result.stdout)
    if "errors" in data:
        for e in data["errors"]:
            print(f"GraphQL error: {e.get('message', e)}", file=sys.stderr)
        sys.exit(1)
    return data


def fetch_project_items() -> list:
    query = """
    query {
      organization(login: "%s") {
        projectV2(number: %d) {
          items(first: 100) {
            nodes {
              content {
                ... on Issue {
                  title
                  number
                  state
                  url
                  repository { name }
                }
              }
              fieldValues(first: 15) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field { ... on ProjectV2SingleSelectField { name } }
                  }
                  ... on ProjectV2ItemFieldIterationValue {
                    title
                    startDate
                    duration
                    field { ... on ProjectV2IterationField { name } }
                  }
                }
              }
            }
          }
        }
      }
    }
    """ % (ORG, PROJECT_NUMBER)

    data = run_graphql(query)
    return (
        data
        .get("data", {})
        .get("organization", {})
        .get("projectV2", {})
        .get("items", {})
        .get("nodes", [])
    )


# ─────────────────────────────────────────────
# Parsing
# ─────────────────────────────────────────────

def parse_item(node: dict, today: datetime) -> dict | None:
    """
    Convert a raw project item node into a clean dict.
    Returns None for: drafts, closed issues, done/archived status.
    """
    issue = node.get("content")
    if not issue or "title" not in issue:
        return None  # Draft item - no linked issue

    if issue.get("state") == "CLOSED":
        return None

    repo   = (issue.get("repository") or {}).get("name", "unknown")
    number = issue.get("number", 0)
    title  = issue.get("title", "Untitled")
    url    = issue.get("url", "")

    fields = {}

    for fv in (node.get("fieldValues") or {}).get("nodes", []):
        if not fv:
            continue

        # Iteration field - determine NOW / NEXT bucket
        if "startDate" in fv:
            start    = datetime.strptime(fv["startDate"], "%Y-%m-%d")
            duration = fv.get("duration") or 14
            end      = start + timedelta(days=duration)
            label    = fv.get("title", "")

            fields["IterationTitle"] = label
            fields["StartDate"]      = start
            fields["EndDate"]        = end

            if today < start:
                fields["Bucket"] = "NEXT"
            elif start <= today < end:
                fields["Bucket"] = "NOW"
            else:
                # Past iteration end — issue was not closed. Treat as overdue.
                fields["Bucket"]        = "NOW"
                fields["IterationTitle"] = f"{label} (overdue)"

        # Single-select fields: Status, Priority, Size, Node, Impact
        elif "name" in fv and fv.get("field"):
            field_name = (fv["field"] or {}).get("name", "")
            if field_name:
                fields[field_name] = fv["name"]

    status = fields.get("Status", "Backlog")
    if status in SKIP_STATUSES:
        return None

    bucket = fields.get("Bucket", "BACKLOG")
    if "IterationTitle" not in fields:
        bucket = "BACKLOG"

    return {
        "repo":       repo,
        "number":     number,
        "title":      title,
        "url":        url,
        "status":     status,
        "priority":   fields.get("Priority"),
        "size":       fields.get("Size"),
        "node":       fields.get("Node"),
        "impact":     fields.get("Impact"),
        "iteration":  fields.get("IterationTitle", "Unscheduled"),
        "bucket":     bucket,
        "start_date": fields.get("StartDate", datetime.max),
    }


# ─────────────────────────────────────────────
# Rendering
# ─────────────────────────────────────────────

def priority_sort_key(item: dict) -> tuple:
    return (PRIORITY_ORDER.get(item.get("priority"), 99), item["repo"], item["number"])


def print_bucket(label: str, items: list, compact: bool = False) -> None:
    print(f"\n{'─' * 62}")
    print(f"  {label}  ({len(items)})")
    print(f"{'─' * 62}")

    if not items:
        print("  (empty)")
        return

    if compact:
        for item in items:
            p = item["priority"] or "--"
            print(f"  {p:<4}  {item['repo']}#{item['number']:<5}  {item['title']}")
        return

    # Full view — group by priority within bucket
    current_priority = object()  # sentinel - intentionally never matches a real value
    for item in items:
        p = item.get("priority")
        if p != current_priority:
            current_priority = p
            print(f"\n  ── {PRIORITY_LABELS.get(p, 'UNPRIORITIZED')}")

        status_col = f"[{item['status']}]"
        iter_col   = f"  ({item['iteration']})" if item["bucket"] != "BACKLOG" else ""
        print(f"    {status_col:<18} {item['repo']}#{item['number']} — {item['title']}{iter_col}")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="EN-OS Sprint Triage Board",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--current-iteration", action="store_true",
        help="Show NOW bucket only — for session_open ritual"
    )
    parser.add_argument(
        "--repo", type=str, default=None,
        help="Filter to a single repo name (e.g. global_agent)"
    )
    parser.add_argument(
        "--status", type=str, default=None,
        help="Filter by status value (e.g. 'In Progress')"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Include Done and Archived items"
    )
    parser.add_argument(
        "--compact", action="store_true",
        help="One-line output per item — fast triage scan"
    )
    args = parser.parse_args()

    if args.all:
        SKIP_STATUSES.clear()

    today    = datetime.now()
    raw      = fetch_project_items()

    items = []
    for node in raw:
        parsed = parse_item(node, today)
        if parsed is None:
            continue
        if args.repo   and parsed["repo"]   != args.repo:
            continue
        if args.status and parsed["status"].lower() != args.status.lower():
            continue
        items.append(parsed)

    now_items  = sorted([i for i in items if i["bucket"] == "NOW"],     key=priority_sort_key)
    next_items = sorted([i for i in items if i["bucket"] == "NEXT"],    key=lambda x: (x["start_date"], priority_sort_key(x)))
    bl_items   = sorted([i for i in items if i["bucket"] == "BACKLOG"], key=priority_sort_key)

    # ── Header
    scope = f"repo:{args.repo}" if args.repo else f"org:{ORG}  ·  project:{PROJECT_NUMBER}"
    mode  = "CURRENT ITERATION" if args.current_iteration else "NOW / NEXT / BACKLOG"

    print(f"\n{'═' * 62}")
    print(f"  SESSION TRIAGE  ·  {mode}")
    print(f"  {today.strftime('%Y-%m-%d %H:%M')}  ·  {scope}")
    print(f"{'═' * 62}")

    if args.current_iteration:
        print_bucket("NOW — Active iteration", now_items, compact=args.compact)
    else:
        print_bucket("NOW — Active & overdue",    now_items,  compact=args.compact)
        print_bucket("NEXT — Upcoming iterations", next_items, compact=args.compact)
        print_bucket("BACKLOG — Unscheduled",      bl_items,   compact=args.compact)

    total = len(now_items) + len(next_items) + len(bl_items)
    print(f"\n  {total} open items")
    print(f"{'═' * 62}\n")


if __name__ == "__main__":
    main()
