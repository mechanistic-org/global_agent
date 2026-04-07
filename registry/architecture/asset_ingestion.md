# Local Asset Ingestion Architecture

## Sovereign Constraint
All asset parsing (`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.eml`) must occur entirely locally. We strictly forbid the use of external cloud APIs or data leakage vectors when ingesting external office artifacts.

## The Normalization Pipeline
The EN-OS pipeline processes arbitrary non-markdown objects and normalizes them into pure, RAG-and-Agent-ready markdown.

### Target Formats & Modalities

| Extension | Library / Parser | Rationale |
|-----------|------------------|-----------|
| `.pdf` | `docling` | Native layout-aware parsing, chunk preservation, embedded element OCR (local PyTorch models). |
| `.docx`| `docling` | Robust heading mapping, table reconstruction mapped uniformly with PDF logic. |
| `.pptx`| `docling` | Slide-by-slide layout extraction natively integrated. |
| `.xlsx`, `.csv` | `pandas` | Truncated dataset ingestion (Top 1000 rows mapped to markdown tables) to prevent agent token overflow. |
| `.eml` | python `email` | Native binary unrolling of headers, subject, and MIME decoded body parts. |

## The Output Protocol
**Target Distributed Write Locations**
The pipeline leverages a discrete `scripts/normalize_asset.py` acting natively inside the agent's MCP domain. It supports an optional `--output` flag to map assets into explicit persistent registry domains (e.g., specific `portfolio` case ingestions).
If no `--output` flag is passed, the tool forces ephemeral behavior:
`registry/.tmp/normalized/[filename].md`. Agents must retrieve from this path explicitly.
