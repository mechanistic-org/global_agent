# LAW CANDIDATE — 2026-04-04

**Rule:** Agents must only auto-close the focal ticket of a session, escalating collateral ticket closures to humans.

Agents must strictly adhere to the 'Focal Ticket Constraint' rule. This means an agent is only authorized to automatically execute closure hygiene and state-change on the exact ticket number declared during `/session_open`. If work incidentally satisfies other 'collateral' tickets, the agent must not close them automatically, but instead escalate by asking the human for secondary closure execution.

**Tags:** AI behavior, ticket management, rule, focal ticket, collateral tickets
