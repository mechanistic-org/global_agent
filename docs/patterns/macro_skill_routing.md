# Pattern: Macro Skill Routing (The "Impeccable" Framework)

## Context
When an AI assistant (like Antigravity or Cursor) is tasked with generating code or resolving aesthetic issues, generic guardrails are often insufficient. While standard "Skills" (e.g., `SKILL.md` injection files) provide background rules, they lack the actionable vocabulary to enforce targeted, on-demand audits.

## The Solution
Inspired by the architecture of `pbakaus/impeccable`, we adopt a pattern of mapping specific **Macro Commands** (e.g., `/slash-commands`) to dedicated, context-heavy Skill directories.

Instead of writing one massive `prompt.txt`, we define atomic actions that trigger rigid schema validation or stylistic alignment, effectively creating a proprietary "design language" for the AI.

## Architecture

We emulate this structure in either `.agents/skills/` (for Antigravity) or `skills/` globally:

```
global_agent/
└── skills/
    ├── v31_audit/
    │   └── SKILL.md  (Triggered by /v31-audit)
    ├── solstice_align/
    │   └── SKILL.md  (Triggered by /solstice-align)
    └── distill/
        └── SKILL.md  (Triggered by /distill)
```

### Anatomy of a Macro Skill
Each command’s `SKILL.md` isn't just a list of tips. It contains:
1.  **The Trigger:** A clear instruction that the user invoked this specific directive.
2.  **The Anti-Patterns:** What the AI should explicitly *avoid* doing (e.g., "Do not use generic Tailwind utility wrappers for nested cards").
3.  **The Strict Schema:** A description or payload mapping to proprietary logic (e.g., the Holy Grail V31 interfaces).
4.  **The Resolution Step:** Specific code modifications required to clear the audit.

## Example Use Cases

### 1. The `/v31-audit` Command
Whenever a frontend component or JSON payload is suspiciously generic, invoking this macro does not just say "make it better." The skill forces the AI to:
- Compare all internal variable names to `vault_p_physics_v31.json`.
- Discard any DTO shape that violates the 4-layer taxonomy.

### 2. The `/solstice-align` Command
When a component looks like boilerplate UI, invoking this macro forces the AI to:
- Strip React/JSX generic structure.
- Apply strict Solstice Astro component definitions.
- Adhere to the "Air Gap" documentation aesthetic.

## Maintenance
When creating a new Macro, create the corresponding subfolder in `skills/` and provide explicit, uncompromising boundaries. The goal is predictable, localized intervention, not generalized improvement.
