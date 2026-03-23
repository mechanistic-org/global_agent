# LAW CANDIDATE — 2026-03-22

**Rule:** Agents must not hand-format YAML frontmatter; structured data must be passed for programmatic serialization and validation.

Agents must never hand-format YAML frontmatter directly within markdown content. Instead, structured data should be passed as a dictionary to a dedicated function, which will handle serialization and Pydantic validation to prevent hallucinations and ensure data integrity.

**Tags:** agent-behavior, rule, yaml, validation, hallucination-prevention
