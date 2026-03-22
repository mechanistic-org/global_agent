---
name: ast-patcher
description: Surgically patches Astro component files using point-update JSON payloads. Prevents agents from reading or overwriting raw .astro files. Invoked by the Python FastMCP Router via subprocess.
---

# AST Patcher Skill

## Purpose
This skill is the implementation of **Pillar 2: Data Compressor** from the Sovereign OS State Machine Architecture.

Agents NEVER read raw `.astro` files. They submit a structured JSON delta payload to `patch_astro_component` on the FastMCP router, which invokes this script in an ephemeral subprocess.

## CLI Interface
```bash
node patcher.js <filepath> <target_selector> <json_payload_path>
```

## Parser Strategy
| Zone | Tool | Scope |
|---|---|---|
| Frontmatter (`---` block) | `ts-morph` | Import injection, variable manipulation |
| Template (HTML body) | `@astrojs/compiler` | Component prop changes, class injection |

## Output Contract (stdout only, always valid JSON)
```json
// Success
{"status": "success", "file": "SovereignNode.astro", "modified_lines": 1}

// Target not found (agent guessed wrong selector)
{"status": "error", "reason": "TARGET_NOT_FOUND", "available_components": ["article", "header", "footer"]}

// Path violation (rogue agent targeting OS files)
{"status": "error", "reason": "PATH_VIOLATION", "detail": "Target path is outside D:\\GitHub\\"}

// Node runtime exception
{"status": "error", "reason": "NODE_EXCEPTION", "detail": "<stderr stack trace>"}
```

## Dependencies
Install in this directory only — never in the portfolio repo:
```bash
npm install
```
