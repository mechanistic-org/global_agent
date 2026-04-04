---
description: Inviolable constraint on when an agent is authorized to automatically close GitHub tickets.
---

# Focal Ticket Authority (The Blast Radius Limit Switch)

An autonomous agent operating within the EN-OS ecosystem MUST NEVER automatically close or mutate the state of a GitHub issue that was not explicitly declared as its focal objective.

## The Rule
1. **1 Session = 1 Issue:** The agent is only authorized to automatically execute the `/session_close` hygiene and state-change protocols on the **exact focal ticket** designated at the start of the session (e.g., via `/session_open`).
2. **The "Collateral Satisfaction" Constraint:** If the agent executes work that technically satisfies *other* open tickets in the backlog (either intentionally or as a side-effect), the agent **must explicitly halt and not touch those tickets**. 
3. **Escalation Phase:** For any collateral tickets that the agent believes are now satisfied, it must explicitly defer to the human operator by stating:
   *"I have incidentally satisfied Ticket X. Please manually review and close it, or explicitly authorize me to run a secondary closure."*

## Why This Exists
This is a structural limit switch designed to protect the project backlog from probabilistic LLM behavior and runaway headless automation (e.g., NanoClaw). It guarantees that an agent cannot recursively wipe out unrelated backlog issues simply because it hallucinates a semantic connection between its work and another ticket.
