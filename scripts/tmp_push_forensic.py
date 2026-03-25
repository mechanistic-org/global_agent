import sys, os
sys.path.insert(0, os.path.abspath('scripts'))
import mcp_registry_server

body = """## Decisions
- Executed `/publish_post` for `2026-03-24_the-gatekeeper.md`, updating the metadata, thread ledger, and moving to the `posted/` pipeline.
- Scrubber: Removed "mootmoat.com/moreplay.com production" hallucination from the pre-drafted comment.
- Formatting: De-indented the numbered list paragraphs to align flush-left, respecting LinkedIn's native mobile-wrap limitations.

## Blockers
- None.

## Next
- The next session picks up `hyphen#7` (CF Access Block) or `global_agent#61` (NanoClaw)."""

print(mcp_registry_server.push_forensic_doc(
    project_name="session_logs",
    component_name="2026-03-24_linkedin-post-promoted",
    markdown_body=body,
    frontmatter_dict={"title": "Session LinkedIn Gatekeeper Decisions", "date": "2026-03-24", "context_node": "session_close"}
))
