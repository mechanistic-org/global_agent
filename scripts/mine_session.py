#!/usr/bin/env python
"""
mine_session.py — Conversation Miner for EN-OS

Extracts structured "Gold" from Antigravity conversation artifacts and routes
each item by channel to the correct destination in the registry.

Usage:
    python scripts/mine_session.py                              # most recent brain dir
    python scripts/mine_session.py --conversation-id <uuid>    # specific conversation
    python scripts/mine_session.py --input-text "..."          # mine arbitrary text
    python scripts/mine_session.py --dry-run                   # print JSON, don't write
    python scripts/mine_session.py --backfill                  # mine portfolio-archive/

Channels:
    linkedin    → registry/global_agent/linkedin_drafts/YYYY-MM-DD_<slug>.md
    colophon    → registry/global_agent/colophon.md (append)
    internal    → push_forensic_doc → ChromaDB (via mcp_registry_server)
    testimonial → registry/portfolio/testimonials/<slug>.json
    law         → registry/global_agent/law_candidates/<slug>.md
    docs        → portfolio/src/content/docs/_inbox/YYYY-MM-DD_<slug>.md
    discard     → dropped silently
"""

import os
import sys
import json
import argparse
import re
import glob
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

# ─── Config ─────────────────────────────────────────────────────────────────

REPO_ROOT      = Path(r"D:\GitHub\global_agent")
BRAIN_DIR      = Path(r"C:\Users\erik\.gemini\antigravity\brain")
REGISTRY_ROOT  = REPO_ROOT / "registry"
ARCHIVE_ROOT   = Path(r"D:\GitHub\portfolio-archive")

LINKEDIN_DIR   = REGISTRY_ROOT / "global_agent" / "linkedin_drafts"
COLOPHON_FILE  = REGISTRY_ROOT / "global_agent" / "colophon.md"
TESTIMONIALS_DIR = REGISTRY_ROOT / "portfolio" / "testimonials"
LAW_CANDIDATES_DIR = REGISTRY_ROOT / "global_agent" / "law_candidates"
DOCS_INBOX_DIR = Path(r"D:\GitHub\portfolio\src\content\docs\_inbox")
VOICE_PRIMER_PATH = REGISTRY_ROOT / "linkedin" / "ERIK_VOICE_PRIMER.md"

load_dotenv(REPO_ROOT / ".env")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL   = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# ─── Voice primer ────────────────────────────────────────────────────────────

def _load_voice_primer() -> str:
    """Load ERIK_VOICE_PRIMER.md and return the content. Returns empty string on failure."""
    try:
        return VOICE_PRIMER_PATH.read_text(encoding="utf-8")
    except Exception as e:
        print(f"WARNING: Could not load voice primer at {VOICE_PRIMER_PATH}: {e}")
        return ""

VOICE_PRIMER_CONTENT = _load_voice_primer()

# Distilled constraint block injected into extraction prompt for linkedin items.
LINKEDIN_VOICE_CONSTRAINTS = """
LINKEDIN VOICE COMPLIANCE (mandatory for any item tagged channel: linkedin):

The following rules are absolute. Any linkedin item that violates them must be flagged
or reclassified. These come from ERIK_VOICE_PRIMER.md - the canonical voice constraint cage.

FORBIDDEN PATTERNS - do not generate linkedin content containing:
1. Em-dashes (—). Use space-dash-space ( - ) instead.
2. Sycophantic openers or filler: "I'm excited to share", "Thrilled to announce", "Humbled by..."
3. Scarcity whispers: "I probably shouldn't share this", "Most people don't know this",
   "I almost didn't post this"
4. Generic techno-schlock hooks: "The industry is panicking", "This changes everything",
   "game-changer", "revolutionary", "synergy"
5. Embedded commands: bolded imperatives disguised as casual observations
6. Forbidden terms: "delve", "chatbots", "AI companions", "Trigger/Intervention/Result" framing
7. Audience-oriented framing: rhetorical questions inviting engagement,
   "drop a comment if...", asking for reader approval
8. Identity installation: describing an aspirational archetype "just ahead" of the reader

REQUIRED VOICE (Controlled Stillness):
- Write from inside the build, not aimed at the audience
- Authority comes from mechanical specificity, not positioning
- Actuarial, deterministic language - like a tolerances document, not a pitch deck
- The ME Builder in Public persona: quiet, specific, reporting from within the work

DESTINATION RULE for linkedin items:
- Set destination to "draft" (not "registry" or "portfolio")
- linkedin items are seeds requiring editorial pass - NOT ready-to-post content
""".strip()

# ─── Extraction prompt ───────────────────────────────────────────────────────

EXTRACTION_PROMPT_PREFIX = """
You are the EN-OS Conversation Miner. Your job is to extract "Gold" from engineering conversation artifacts.

Gold = decisions made, problems solved, architecture patterns established, memorable one-liners,
client/team wins, code breakthroughs, lessons about tools/systems, and moments worth LinkedIn posts.

Read the provided text and return a JSON array of extracted items. Each item MUST have this exact schema:

{
  "channel": "linkedin | colophon | internal | testimonial | law | docs | discard",
  "confidence": "captured | inferred",
  "destination": "registry | portfolio | draft | discard",
  "content": "full extracted content, 2-5 sentences",
  "one_liner": "single punchy sentence summarizing the Gold",
  "source_context": "brief quote or reference to where this came from",
  "tags": ["tag1", "tag2"],
  "voice_compliant": true
}

Channel definitions:
- linkedin: Raw seed material - a compelling insight or technical win that MAY become a LinkedIn
  post after operator editorial review. NOT ready-to-post content. Set destination to "draft".
  Content must comply with LinkedIn voice constraints below - if it cannot, classify as internal.
- colophon: A design decision, architectural choice, or 'how we built this' moment for the portfolio
- internal: Technical decision, constraint, or fact worth embedding in ChromaDB for future agent context
- testimonial: Client praise, user feedback, or external validation
- law: A rule or principle that should be codified (e.g. 'agents never hand-format YAML')
- docs: A systemic update, architecture decision, or new protocol that should be codified in the master portfolio documentation
- discard: Not useful, routine status updates, noise

Confidence:
- captured: The item was explicitly flagged or documented in the source
- inferred: You extracted it from context - it's implicit Gold

""" + LINKEDIN_VOICE_CONSTRAINTS + """

CRITICAL RULES:
1. Return ONLY a valid JSON array. No markdown, no explanation, no preamble.
2. Be selective - quality over quantity. 3-8 items per conversation is typical.
3. discard items should still appear in the array (so we can audit what was dropped).
4. For "law" items, content should be phrased as an imperative rule: "Agents must never X"
5. For "linkedin" items: set destination to "draft". Set voice_compliant to true only if the
   content strictly obeys the LINKEDIN VOICE COMPLIANCE rules above. If it cannot be written
   compliantly, classify as "internal" instead.
6. For all other channels: voice_compliant defaults to true.

TEXT TO MINE:
---
"""

# ─── Routing functions ───────────────────────────────────────────────────────

def _slug(text: str, max_len: int = 40) -> str:
    """Convert text to a safe filename slug."""
    s = re.sub(r"[^a-z0-9\s-]", "", text.lower())
    s = re.sub(r"[\s-]+", "-", s).strip("-")
    return s[:max_len]


def route_item(item: dict, today: str, dry_run: bool = False) -> str:
    """Route a single Gold item to its destination. Returns a status string."""
    channel = item.get("channel", "discard")
    one_liner = item.get("one_liner", "untitled")
    content = item.get("content", "")
    tags = item.get("tags", [])

    if channel == "discard":
        return f"  DISCARD: {one_liner[:60]}"

    if dry_run:
        return f"  DRY-RUN [{channel.upper()}]: {one_liner[:70]}"

    if channel == "linkedin":
        LINKEDIN_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"{today}_{_slug(one_liner)}.md"
        filepath = LINKEDIN_DIR / filename
        voice_compliant = item.get("voice_compliant", True)
        violations = item.get("violations", [])
        violations_note = "\n# VOICE VIOLATIONS FLAGGED:\n" + "\n".join(f"# - {v}" for v in violations) if violations else ""
        frontmatter = (
            f"---\ntitle: {one_liner}\npubDate: {today}\naudio_url: ''\n"
            f"status: seed\nisDraft: true\nvoice_compliant: {str(voice_compliant).lower()}\n"
            f"tags: {json.dumps(tags)}\n---\n"
            f"# EDITORIAL PASS REQUIRED - this is miner seed content, not ready-to-post\n"
            f"{violations_note}\n\n"
        )
        filepath.write_text(frontmatter + content, encoding="utf-8")
        return f"  LINKEDIN (seed): {filepath.name}"

    elif channel == "colophon":
        COLOPHON_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = f"\n\n## {today} — {one_liner}\n\n{content}\n"
        with open(COLOPHON_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
        return f"  COLOPHON: appended — {one_liner[:60]}"

    elif channel == "internal":
        # Write to ChromaDB via enos-router FastMCP SSE bridge
        try:
            import asyncio
            from mcp.client.sse import sse_client
            from mcp.client.session import ClientSession

            slug = _slug(one_liner)
            
            async def _push_via_mcp():
                async with sse_client("http://127.0.0.1:8000/sse") as (read_stream, write_stream):
                    async with ClientSession(read_stream, write_stream) as session:
                        await session.initialize()
                        call_result = await session.call_tool("push_forensic_doc", arguments={
                            "project_name": "global_agent",
                            "component_name": f"mined_{today}_{slug}",
                            "markdown_body": content,
                            "frontmatter_dict": {"title": one_liner, "date": today, "context_node": "conversation_miner"}
                        })
                        # Extract the string response correctly from TextContent
                        return call_result.content[0].text if call_result.content else "SUCCESS"
            
            result = asyncio.run(_push_via_mcp())
            return f"  INTERNAL (SSE): {result[:80]}"
        except Exception as e:
            # Fallback: write to registry flat file
            fallback_dir = REGISTRY_ROOT / "global_agent" / "mined"
            fallback_dir.mkdir(parents=True, exist_ok=True)
            slug = _slug(one_liner)
            fp = fallback_dir / f"{today}_{slug}.md"
            fp.write_text(f"---\ntitle: {one_liner}\ndate: {today}\ncontext_node: conversation_miner\n---\n\n{content}", encoding="utf-8")
            return f"  INTERNAL (fallback): {fp.name} (ChromaDB err: {e})"

    elif channel == "testimonial":
        TESTIMONIALS_DIR.mkdir(parents=True, exist_ok=True)
        slug = _slug(one_liner)
        filepath = TESTIMONIALS_DIR / f"{today}_{slug}.json"
        payload = {"date": today, "one_liner": one_liner, "content": content, "tags": tags}
        filepath.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return f"  TESTIMONIAL: {filepath.name}"

    elif channel == "law":
        LAW_CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
        slug = _slug(one_liner)
        filepath = LAW_CANDIDATES_DIR / f"{today}_{slug}.md"
        filepath.write_text(f"# LAW CANDIDATE — {today}\n\n**Rule:** {one_liner}\n\n{content}\n\n**Tags:** {', '.join(tags)}\n", encoding="utf-8")
        return f"  LAW: {filepath.name}"

    elif channel == "docs":
        DOCS_INBOX_DIR.mkdir(parents=True, exist_ok=True)
        slug = _slug(one_liner)
        filepath = DOCS_INBOX_DIR / f"{today}_{slug}.md"
        # Astro Starlight requires title and description in frontmatter
        description = (content[:97] + '...') if len(content) > 100 else content
        frontmatter = f"---\ntitle: \"{one_liner}\"\ndescription: \"{description}\"\n---\n\n"
        filepath.write_text(frontmatter + content + f"\n\n**Tags:** {', '.join(tags)}\n", encoding="utf-8")
        return f"  DOCS: {filepath.name} (Quarantined in _inbox)"

    return f"  UNKNOWN channel '{channel}': {one_liner[:60]}"


# ─── Gemini extraction ───────────────────────────────────────────────────────

def extract_gold(text: str) -> list[dict]:
    """Call Gemini API and return list of Gold items."""
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        print("ERROR: google-genai not installed. Run: pip install google-genai")
        sys.exit(1)

    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY not found in .env")
        sys.exit(1)

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Build prompt by concatenation to avoid .format() conflict with JSON braces
    prompt = EXTRACTION_PROMPT_PREFIX + text[:20000] + "\n---\n"

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        raw = response.text.strip()
        # Strip any accidental markdown fences
        raw = re.sub(r"^```json\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()

        # Use json_repair to handle invalid escape sequences / minor JSON malformation
        # that Gemini occasionally emits (backslashes in content strings, trailing commas etc.)
        from json_repair import repair_json
        repaired = repair_json(raw, return_objects=True)
        if isinstance(repaired, list):
            return repaired
        # repair_json may return a dict if only one object — wrap it
        if isinstance(repaired, dict):
            return [repaired]
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Gemini returned non-JSON response: {e}")
        print("Raw response:", response.text[:500])
        return []
    except Exception as e:
        print(f"ERROR: Gemini API call failed: {e}")
        return []


# ─── LinkedIn voice validation ──────────────────────────────────────────────

LINKEDIN_VALIDATION_PROMPT = """
You are a voice compliance auditor for EN-OS. You are given a list of LinkedIn seed items
extracted from an engineering session. Your job is to audit each item against the voice primer
rules and return a compliance verdict.

Voice primer rules (absolute constraints):
""" + LINKEDIN_VOICE_CONSTRAINTS + """

For each item in the input array, return a JSON object with:
{
  "index": <original array index>,
  "voice_compliant": true | false,
  "violations": ["list of specific rule violations found, empty if compliant"],
  "revised_content": "revised content with violations corrected, or null if compliant"
}

Return ONLY a valid JSON array of these verdict objects. No markdown, no explanation.

ITEMS TO AUDIT:
---
{items_json}
---
"""


def validate_linkedin_voice(items: list[dict]) -> list[dict]:
    """Second-pass: audit linkedin items for voice compliance via Gemini.

    Returns the input items list with voice_compliant and violations fields updated.
    Non-linkedin items are passed through unchanged.
    """
    linkedin_indices = [i for i, item in enumerate(items) if item.get("channel") == "linkedin"]
    if not linkedin_indices:
        return items

    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        print("WARNING: google-genai not installed - skipping voice validation")
        return items

    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY not set - skipping voice validation")
        return items

    linkedin_items = [{"index": i, **items[i]} for i in linkedin_indices]
    items_json = json.dumps(linkedin_items, indent=2)
    prompt = LINKEDIN_VALIDATION_PROMPT.replace("{items_json}", items_json)

    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )
        raw = response.text.strip()
        raw = re.sub(r"^```json\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()

        from json_repair import repair_json
        verdicts = repair_json(raw, return_objects=True)
        if not isinstance(verdicts, list):
            verdicts = [verdicts] if isinstance(verdicts, dict) else []

        # Apply verdicts back to items
        verdict_map = {v["index"]: v for v in verdicts if "index" in v}
        for i in linkedin_indices:
            verdict = verdict_map.get(i, {})
            items[i]["voice_compliant"] = verdict.get("voice_compliant", True)
            violations = verdict.get("violations", [])
            if violations:
                items[i]["violations"] = violations
                print(f"  VOICE FAIL [{i}]: {items[i].get('one_liner', '')[:60]}")
                for v in violations:
                    print(f"    - {v}")
                revised = verdict.get("revised_content")
                if revised:
                    items[i]["content"] = revised
                    print(f"    -> Content revised by validator")
            else:
                print(f"  VOICE OK  [{i}]: {items[i].get('one_liner', '')[:60]}")

        return items

    except Exception as e:
        print(f"WARNING: LinkedIn voice validation failed: {e}")
        return items


# ─── Input collection ────────────────────────────────────────────────────────

def collect_brain_text(conv_id: str) -> str:
    """Read all readable artifacts from a brain/<conv-id>/ directory."""
    brain_path = BRAIN_DIR / conv_id
    if not brain_path.exists():
        print(f"ERROR: Brain dir not found: {brain_path}")
        sys.exit(1)

    texts = []
    for md_file in brain_path.glob("*.md"):
        if ".metadata" not in md_file.name and ".resolved" not in md_file.name:
            try:
                texts.append(f"=== {md_file.name} ===\n{md_file.read_text(encoding='utf-8')}")
            except Exception:
                pass

    if not texts:
        return f"[No readable artifacts found in conversation {conv_id}]"

    return "\n\n".join(texts)


def collect_most_recent_brain() -> tuple[str, str]:
    """Return (conv_id, text) for the most recently modified brain dir."""
    dirs = sorted(
        [d for d in BRAIN_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")],
        key=lambda d: d.stat().st_mtime,
        reverse=True
    )
    if not dirs:
        print("ERROR: No conversation dirs found in brain.")
        sys.exit(1)

    conv_id = dirs[0].name
    return conv_id, collect_brain_text(conv_id)


def collect_backfill_text() -> str:
    """Read key files from portfolio-archive/ for backfill run."""
    if not ARCHIVE_ROOT.exists():
        print(f"ERROR: portfolio-archive not found at {ARCHIVE_ROOT}")
        sys.exit(1)

    target_files = [
        "context_lifecycle/MINING_LOG.md",
        "context_lifecycle/HISTORICAL_LEDGER.md",
        "context_lifecycle/ROADMAP_ACTIVE.md",
        "prompts_quarantine/AGENCY_MEMORY.md",
        "prompts_quarantine/LINKEDIN_IDENTITY_KIT.md",
        "prompts_quarantine/LINKEDIN_STRATEGY_LOG.md",
        "archive_2025_rescue_dump/meta/GOLDEN_DIALOGUE_CORPUS.md",
        "archive_2025_rescue_dump/meta/MANIFESTO.md",
        "archive_2025_rescue_dump/meta/PERSONAL_USER_MANUAL.md",
    ]

    texts = []
    for rel in target_files:
        fp = ARCHIVE_ROOT / rel
        if fp.exists():
            try:
                contents = fp.read_text(encoding="utf-8", errors="replace")
                texts.append(f"=== {rel} ===\n{contents[:5000]}")  # cap per file
                print(f"  READ: {rel} ({len(contents)} chars)")
            except Exception as e:
                print(f"  SKIP: {rel} — {e}")
        else:
            print(f"  MISSING: {rel}")

    return "\n\n".join(texts)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="EN-OS Conversation Miner")
    parser.add_argument("--conversation-id", help="Specific conversation UUID to mine")
    parser.add_argument("--input-text", help="Mine arbitrary text string directly")
    parser.add_argument("--dry-run", action="store_true", help="Print routing plan without writing files")
    parser.add_argument("--backfill", action="store_true", help="Mine portfolio-archive/ corpus (one-time enrichment)")
    args = parser.parse_args()

    today = date.today().isoformat()

    # ── Collect input text ───────────────────────────────────────────────────
    if args.backfill:
        print("=== BACKFILL MODE: mining portfolio-archive/ ===\n")
        source_label = "backfill"
        text = collect_backfill_text()
    elif args.input_text:
        source_label = "stdin"
        text = args.input_text
    elif args.conversation_id:
        source_label = args.conversation_id
        text = collect_brain_text(args.conversation_id)
        print(f"Mining conversation: {source_label}")
        print(f"Text collected: {len(text)} chars\n")
    else:
        conv_id, text = collect_most_recent_brain()
        source_label = conv_id
        print(f"Mining most recent conversation: {source_label}")
        print(f"Text collected: {len(text)} chars\n")

    if not text.strip():
        print("ERROR: No text to mine.")
        sys.exit(1)

    # ── Extract Gold ─────────────────────────────────────────────────────────
    print("Calling Gemini extraction...\n")
    items = extract_gold(text)

    if not items:
        print("No Gold extracted.")
        sys.exit(0)

    print(f"Extracted {len(items)} items:\n")
    for i, item in enumerate(items, 1):
        ch = item.get("channel", "?")
        ol = item.get("one_liner", "no one-liner")
        print(f"  [{i}] {ch.upper():12s} - {ol}")

    # ── LinkedIn voice validation (second pass) ──────────────────────────────
    linkedin_count = sum(1 for item in items if item.get("channel") == "linkedin")
    if linkedin_count > 0:
        print(f"\nRunning voice compliance audit on {linkedin_count} LinkedIn item(s)...\n")
        items = validate_linkedin_voice(items)

    print()

    # ── Write JSON dump ──────────────────────────────────────────────────────
    dump_path = REPO_ROOT / "registry" / "global_agent" / f"mine_dump_{today}_{source_label[:8]}.json"
    if not args.dry_run:
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        dump_path.write_text(json.dumps(items, indent=2), encoding="utf-8")
        print(f"Raw dump: {dump_path}\n")

    # ── Route items ──────────────────────────────────────────────────────────
    print("Routing Gold:\n")
    for item in items:
        status = route_item(item, today=today, dry_run=args.dry_run)
        print(status)

    print(f"\n{'DRY-RUN COMPLETE' if args.dry_run else 'MINING COMPLETE'} — {len([i for i in items if i.get('channel') != 'discard'])} items routed.")


if __name__ == "__main__":
    main()
