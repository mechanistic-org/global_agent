## Context
Currently, session logs are highly siloed. Inspired by Karpathy's LLM-Wiki, we need a single `timeline.md` at the root of `registry/` that acts as an append-only chronological ledger of all OS activity.

## DoD
- [ ] Modify `.agent/workflows/session_close.md` and/or `enos_router` to append a strictly formatted one-liner to `registry/timeline.md` on every teardown.
- [ ] Ensure the format is easily `grep`-able (e.g., `## [YYYY-MM-DD] action: X | agent: Y | docs: Z`).
