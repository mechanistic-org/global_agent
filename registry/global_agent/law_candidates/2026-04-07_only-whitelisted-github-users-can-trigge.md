# LAW CANDIDATE — 2026-04-07

**Rule:** Only whitelisted GitHub users can trigger agent execution.

Agents must never execute commands without explicit authorization from a whitelisted GitHub user. The system enforces this by checking the `payload.get("comment", {}).get("user", {}).get("login")` against a predefined list of authorized users before any `/execute` transition.

**Tags:** security-policy, access-control, agent-security, rule
