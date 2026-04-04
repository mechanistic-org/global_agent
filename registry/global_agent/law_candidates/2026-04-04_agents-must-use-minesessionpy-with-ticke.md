# LAW CANDIDATE — 2026-04-04

**Rule:** Agents must use `mine_session.py` with `--ticket-id` for automated Forensic Flag extraction during session close.

Agents must update their session closing workflow to include the new requirement: `python scripts\mine_session.py --conversation-id <uuid> --ticket-id <ticket_id>`. This command ensures the automatic extraction and persistence of Forensic Flags, replacing the previous manual steps.

**Tags:** agent workflow, rule, command line, Forensic Flags
