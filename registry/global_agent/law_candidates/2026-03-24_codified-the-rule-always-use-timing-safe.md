# LAW CANDIDATE — 2026-03-24

**Rule:** Codified the rule: Always use timing-safe comparisons for cryptographic secrets like HMACs.

Agents must always use timing-safe comparison functions, such as `hmac.compare_digest()`, when validating cryptographic secrets like webhook HMAC signatures. This prevents timing attacks that could reveal secret information.

**Tags:** security, hmac, best practice, webhooks, law
