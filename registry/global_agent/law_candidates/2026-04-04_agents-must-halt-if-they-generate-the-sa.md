# LAW CANDIDATE — 2026-04-04

**Rule:** Agents must halt if they generate the same output sequence three times consecutively, preventing infinite loops.

Agents must employ a `LoopDetector` to hash `response.text` from every model round. If the agent generates the exact same output sequence three times in a row, the circuit breaker must trip, halting the agent and flagging a human to prevent "whack-a-mole" loops and wasted budget.

**Tags:** agent rules, stability, loop detection, failsafe
