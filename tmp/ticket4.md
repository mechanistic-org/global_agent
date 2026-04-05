## Context
While EN-OS is flawless with code and markdown, we lack a robust, local pipeline for handling organizational "Office" assets (`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.eml`). We need a formalized suite of local tools handling ON-THE-FLY (OTF) conversion of these modalities into our standard markdown formats without breaking sovereignty (no cloud APIs).

## Objective
Identify, evaluate, install, and formalize the toolchain required for local asset-to-markdown alignment. This will culminate in a new MCP Tool (e.g., `normalize_asset`) that agents can execute against inbound files.

## Research Scope & Candidates
1. **PDFs (`.pdf`)**: 
   - *Candidates:* `pymupdf4llm` (natively outputs RAG-ready markdown), `docling`, or `Marker` by Suraj. 
   - *Requirement:* Handle layouts, tables, and optional local OCR.
2. **Word/Presentations (`.docx`, `.pptx`)**: 
   - *Candidates:* `pandoc` (industry standard for format translation) or python-native `python-docx` / `python-pptx` bridging.
3. **Spreadsheets (`.xlsx`, `.csv`)**: 
   - *Candidates:* `pandas` dataframe-to-markdown table conversion.
   - *Requirement:* Handle size limits intelligently (truncating massive datasets vs. full conversion).
4. **Email/Comms (`.eml`)**: 
   - *Candidates:* Python's `email` module.
   - *Requirement:* Extract headers and body into EN-OS `.md` schema.

## DoD
- [ ] Finalize research and select the definitive local libraries for each format.
- [ ] Document the pipeline in `registry/architecture/asset_ingestion.md`.
- [ ] Scaffold the Python normalization orchestrator (`scripts/normalize_asset.py`) capable of OTF conversion.
- [ ] Wire the orchestrator into the `enos_router` MCP server for agent invocation.
