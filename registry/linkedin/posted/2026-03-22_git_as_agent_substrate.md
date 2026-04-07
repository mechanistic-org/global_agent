---
title: Git as Agent Memory Substrate
pubDate: 2026-03-22
status: posted
tags: [agent-memory, ai-engineering, Devops]
source: manual-draft
post_url: "https://www.linkedin.com/posts/eriknorris_one-day-soon-a-robot-will-make-you-a-salad-activity-6900148693434019840-lfqj"
thread_id: "trilogy_001"
arc_position: 1
---

I've spent months building an autonomous AI engineering OS.

The hardest problem wasn't the models. It wasn't the tooling. It was **memory** — how do you give an AI agent durable, reliable context that survives across sessions, machine restarts, and complete environment teardowns?

The answer I landed on: **GitHub.**

Not as a workaround. As the substrate.

Every property you need for persistent agentic context — durability, auditability, diffing, branching, multi-party write access, free API — git already has.

GitHub Issues with structured bodies IS a schema.
Project boards with iterations IS a task queue.
Commits ARE timestamped forensic logs.

The agents I'm building don't maintain conversation state. They boot cold, read a GitHub Issue, execute one task, post a comment, and die. The container burns. The commit survives.

I didn't build a workaround. I found the natural substrate.

Git was built for humans to track software work. It turns out that's identical to what an AI agent swarm needs to think.

The infrastructure was already there. We just weren't running agents on top of it yet.

---

*#AgenticAI #GitOps #SovereignOS #AIEngineering #DevOps*
