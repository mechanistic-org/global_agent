# LAW CANDIDATE — 2026-04-07

**Rule:** Agents must only trigger Python engines as standalone binaries via skill definitions, never directly executing risky bash commands.

Agents must trigger Python engines as standalone binaries via `.agent/skills/` definitions. This design completely protects the sovereign file loop from runtime code execution errors and prevents agents from running risky bash commands natively, ensuring system stability and security.

**Tags:** security, architecture, agent-design, system-stability, best-practice
