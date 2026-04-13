---
title: En-OS Constraints & Security Topology (Follow-up)
pubDate: 2026-04-13
status: draft
post_url: ""
thread_id: standalone
tags: ["AgenticAI", "CyberSecurity", "SovereignOS", "AIEngineering"]
---

Last week I asked for help. Here's what I've committed to actually doing.

1. Every agent gets a manifest before it touches anything.

A written list of which tools it can call, which environment variables it can read, which network destinations it's allowed to reach. If it's not on the manifest, it doesn't exist in the agent's environment. One manifest per agent - not a shared policy, not inherited defaults. This isn't a security layer. It's a precondition for knowing what you're auditing.

2. API keys are not passwords. Treat them like capabilities.

One key, one capability, one agent. No shared keys across agents. Every key is scoped to the minimum surface area that makes the workflow functional - not convenient, functional. Broad keys get rotated down. If scoping breaks the workflow, that's signal the workflow was poorly designed, not that the key needs more permissions.

3. You can't catch logic errors you don't know you're making - so you change the question.

The right question isn't "did my agent do something wrong?" It's "did my agent do anything I didn't explicitly anticipate?" Those are different. The first requires knowing the error space in advance. The second just requires logging every action and reviewing the diff between expected behavior and actual behavior after each run. Boring, but tractable.

4. Auth flows get a BROKER - a dedicated chokepoint between agents and secrets.

Auth material never touches the reasoning layer. The agent requests a credential via an internal broker. The broker issues a short-lived token scoped to the immediate task. The agent never sees the underlying secret. One node in the trust graph owns all credential issuance. That concentration is intentional: a single chokepoint is auditable in a way that distributed key access is not. If the broker is compromised, you know exactly where to look. If keys are scattered across agents, you don't.

5. The attack surface isn't the problem. The attack topology is.

Every new component doesn't just add exposure - it adds a trust relationship, and each trust relationship has its own failure mode and its own owner. microVM ↔ host. ChromaDB ↔ agent. Agent ↔ broker. I now map these as a directed graph before building, not after. The manifest (point 1) and the broker (point 4) are both outputs of that mapping - you can only define them once you know which relationships exist.

6. The Security Claw is real now, and it's simple on purpose.

A background watchdog that ingests router telemetry and runs three deterministic checks: did any agent initiate an outbound connection to an unregistered destination; did any agent call a tool more than N times in a window without a human checkpoint; did any agent spawn a subprocess outside its manifest. Fail any check → agent suspended, human reviews before resumption. No AI in the watchdog. Deterministic rules only. The manifest from point 1 is what makes check three possible - the Claw can only flag manifest violations if the manifest exists.

7. The minimal viable constraint stack, in order.

Tool allowlist via manifest. Scoped API keys. Short-lived tokens via broker. Deterministic Security Claw watchdog. Human checkpoint on any novel action class. Each layer is independently auditable - when something breaks, you know which layer failed. That property matters more than coverage. A perfect security layer you can't reason about is worse than a partial one you can.

The meta-lesson from the ransomware operators: they're cautious not because AI is weak, but because the cost of an unrecoverable error is existential to them. That constraint is clarifying. Build as if every mistake is unrecoverable. Design for reversibility first, capability second.

Still learning. Still building. What did I get wrong?

---

## Carousel Info

5 slides, ready to upload directly to LinkedIn.

**Structure:**
- **Slide 1 — Cover:** hook from the ransomware operators framing, teal accent rule, subtext sets the premise
- **Slide 2 — Constraints 01 & 02:** Manifest per agent / One key, one capability
- **Slide 3 — Constraint 03:** BROKER chokepoint (anchor slide) - AGENT → BROKER → TOKEN trust flow diagram, amber accent throughout, the two punchy closing lines in italic
- **Slide 4 — Constraints 04 & 05:** Security Claw (red) / Topology map (teal)
- **Slide 5 — Stack summary:** all 5 rows with color-coded left strips, meta-lesson quote, "What did I get wrong?" CTA

**Color coding meaning:**
- Teal = environment controls
- Amber = credential architecture
- Red = watchdog
Slide 5 makes that logic visible as a recap.

**Links to draft viz:**
- https://docs.google.com/presentation/d/13KnWu_8Ut5YIqKysx59NoQtKFEzbxoM3nmHJE4Z9ZOk/edit?usp=drive_link
- "D:\GitHub\global_agent\registry\linkedin\drafts\assets\en_os_trust_graph.png"
- "D:\GitHub\global_agent\registry\linkedin\drafts\assets\en-os-carousel.pptx"

**Links to chats-in-progress:**
- https://www.perplexity.ai/computer/a/en-os-carousel-JVvJ9l5jQSOlXHSEc36qVQ
- https://claude.ai/claude-code-desktop/local_094467c7-465a-4c85-881c-8dcea216b450

