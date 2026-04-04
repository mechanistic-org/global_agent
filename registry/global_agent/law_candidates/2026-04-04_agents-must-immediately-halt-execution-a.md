# LAW CANDIDATE — 2026-04-04

**Rule:** Agents must immediately halt execution and flag a human if the daily token budget is exceeded.

Agents must query the global `TokenLedger` before every model call. If the daily cost exceeds `MAX_DAILY_BUDGET_USD` (default $5.00), the agent must immediately trigger `log_failsafe()`, set the ticket to `halted` to flag a human, and gracefully exit, preventing further token burn.

**Tags:** agent rules, cost control, safety, failsafe
