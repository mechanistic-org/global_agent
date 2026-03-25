import sys, os
sys.path.insert(0, os.path.abspath('scripts'))
import mcp_registry_server

body = """## Decisions
- Mapped explicit dependencies across all open mechanistic-org tickets to triage into NOW, NEXT, and LATER.
- Executed GraphQL automated updates for Status, Priority, and Iteration fields across Project 5 for all active triage tickets, using 500-item pagination.
- Consolidated overlapping `[Epic] NanoClaw Containers` issues (57-60) into the canonical issue (#61).

## Blockers
- None. Project board is clean and prioritized.

## Next
- Execute P1 security block `hyphen#7` or begin work on the primary `global_agent#61` NanoClaw Epic."""

print(mcp_registry_server.push_forensic_doc(
    project_name="session_logs",
    component_name="2026-03-24_triage-sprint",
    markdown_body=body,
    frontmatter_dict={"title": "Session Triage Decisions", "date": "2026-03-24", "context_node": "session_close"}
))
