---
description: Process an unstructured external AI output dump (Google Docs, voice notes, analysis files) into triaged GitHub tickets
---

# /intake_dump — External Content Ingestion Workflow

Use this when you have a batch of external AI-generated docs, voice note transcripts, or analysis files that need to be decomposed and triaged into the sprint board.

**Canonical trigger:** Files in `Antigravity_Shared_Bus` Google Drive folder, or local files in `D:\GitHub\global_agent\inbox\`.

---

## Step 1 — Move files to Shared Bus

If files are in Google Docs or Drive:
- Ensure they are shared to `Antigravity_Shared_Bus` folder (ID: `1GG-z8rLTugURJ-vbUD-PxZT7WhfSqBtv`)
- Service account `os-daemon@mechanistic-gmail-mcp.iam.gserviceaccount.com` has read access

If files are local PDFs or text:
- Drop into `D:\GitHub\global_agent\inbox\` (future: picked up by `ingest_watchdog.py` / global_agent#67)

---

## Step 2 — Read all files via service account

```python
# Run: python C:\tmp\read_intake_docs.py
# The read_walk_docs.py pattern — reads all doc IDs via Google Docs API
# Saves combined output to C:\tmp\intake_combined.txt
```

For Google Docs, use the service account script pattern:
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SA_FILE = r"D:\Assets\mechanistic-gmail-mcp-5e0f2d2d80eb.json"
SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]
# ... extract_text() and iterate doc IDs
```

---

## Step 3 — Deep analysis and triage

Read all content. For each document, classify:

| Category | Action |
|---|---|
| **Already ticketed** | Skip — note the overlap |
| **Net-new infrastructure** | Create ticket → global_agent repo |
| **Net-new portfolio feature** | Create ticket → portfolio repo |
| **Strategic framing only** | Capture to `registry/global_agent/colophon.md` if colophon-worthy |
| **Code already written** | Note in ticket body as "Implementation provided" |
| **Duplicate of existing ticket** | Add comment to existing ticket |

---

## Step 4 — Create tickets via batch script

Use the standard pattern from `C:\tmp\create_walk_tickets.py`:

```python
# Per ticket:
# 1. gh issue create --repo mechanistic-org/{repo} --title ... --label ... --body ...
# 2. gh project item-add 5 --owner mechanistic-org --url {URL} --format json
# 3. gh project item-edit (set Iteration, Priority, Size, Node, Impact, Status)
```

**Field IDs (memorize):**
```
Project:   PVT_kwDOEA3Ajc4BSLlf
Iteration: PVTIF_lADOEA3Ajc4BSLlfzg_ynvU
Priority:  PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI
Size:      PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM
Node:      PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY
Impact:    PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc
```

**Iteration IDs:**
```
Sprint 2: 54cf5c95
Sprint 3: d2c335bc
```

---

## Step 5 — Capture colophon-worthy insights

After triage, scan content for insights worth capturing:
```
push_forensic_doc(
  project_name="global_agent",
  component_name="intake_dump_YYYY-MM-DD",
  markdown_content="## Key insights from [session description]..."
)
```

Flag any LinkedIn-worthy nuggets to `registry/global_agent/colophon.md`.

---

## Step 6 — Commit

```bash
git add .
git commit -m "chore: intake dump triage YYYY-MM-DD — N tickets created"
git push
```

---

## Notes

- **This workflow IS the `/intake_dump` pattern.** Documents 1–10 from the 2026-03-22 walk session were the first execution of it.
- **Common input sources:** External AI sessions seeded with `operator_context_brief.md`, voice-to-doc walks, NotebookLM outputs, client constraint dumps.
- **What goes to tickets vs. colophon:** Tickets = actionable, buildable, bounded. Colophon = insight, narrative, wisdom.
- **Do not create tickets for strategic framing alone** — capture framing to the registry instead.
