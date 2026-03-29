import urllib.parse
import sys
import os

sys.path.append(r"D:\GitHub\global_agent\scripts")
from mcp_registry_server import push_forensic_doc

push_forensic_doc(
    project_name="session_logs",
    component_name="2026-03-28_epic_61_92_nanoclaw",
    markdown_body=(
        "## Decisions\n"
        "- Authored the complete NanoClaw Ephemeral Container layer architecture (Dockerfile, run_agent.py, launch_nanoclaw.ps1).\n"
        "- Opted to use winget for silently installing Docker Desktop instead of complex external host orchestration.\n\n"
        "## Blockers\n"
        "- Awaiting required OS reboot / Docker daemon UI acceptance sequence for PATH variables to register.\n\n"
        "## Next\n"
        "- Next session picks up verification of nanoclaw:latest build and End-to-End webhook lifecycle."
    ),
    frontmatter_dict={"title": "Session Epic #61 + #92 Decisions", "date": "2026-03-28", "context_node": "session_close"}
)
print("Forensic doc pushed successfully.")
