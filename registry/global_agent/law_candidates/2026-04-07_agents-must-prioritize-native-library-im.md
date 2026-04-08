# LAW CANDIDATE — 2026-04-07

**Rule:** Agents must prioritize native library imports over `subprocess` calls for robust tool integration.

Agents must always prefer importing Python libraries natively over invoking CLI tools via `subprocess` for external tool integration. This practice ensures direct error handling, prevents encoding issues, and significantly enhances the stability and maintainability of automated processes.

**Tags:** best-practice, tooling, stability, error-handling, architecture
