---
title: Jigs, Amnesia, and the Old Testament of Project Management
pubDate: 2026-03-23
status: draft-v2
tags: [ai-engineering, StateMachines, mental-models, tooling]
source: hired-gun-synthesis
---

I've written about the substrate (git) and the loop (self-review). Today the question is: what keeps the machine from wandering?

The more things change, the more they stay exactly the same.

In the pursuit of building a futuristic AI engineering OS — coordinating swarms, orchestrating model handoffs, managing autonomous loops — I realized the entire system still lives or dies by one thing:

Old-school, Old Testament project management rigor. A persistent vision. A rigid architecture. And the tooling to enforce it.

For months, I tried building with "agents" by talking to them. I kept tweaking system prompts, building more elaborate systems of files and folders, hoping to make the model maintain context and follow instructions.

Then the context window would shift. And the machine would forget everything.

Not metaphorically. Literally. Hours of established architecture, decisions made, patterns agreed upon — gone. The agent would pick up mid-session and treat the whole thing as a clean slate. You'd find yourself re-explaining the same constraints to the same system, watching it confidently rebuild something you already built together and already broke.

That's the amnesia. That's the real problem nobody warns you about.

So I stopped treating this as a software problem and started treating it as a physical engineering problem.

**I am building a Cognitive Manufacturing Line.**

In a machine shop, if you want a drill to hit dead-center on ten thousand parts, you don't give the motor a 10-page instruction manual. You build a jig. You fabricate a rigid metal frame that physically prevents the bit from wandering.

For now — and the irony is not lost on me — we still need to build the exact same tooling for LLMs. The most sophisticated autonomous stack in your lab is, at this moment, being held together by the cognitive equivalent of Post-It notes and physical jigs. Not because it's elegant. Because the machine still forgets.

They are volatile, highly entropic engines. You shouldn't trust them to format a PRD or calculate an FMEA matrix. You don't ask for precision. You build constraint cages.

My OS doesn't ask the agent to "be precise." The agent is forced to run its output through a strict validation gate. If it hallucinates a field, misses a metric, or uses passive voice, the runtime physically rejects the payload and returns the structural error.

The machine is forced to iterate mechanically until its output fits the exact physical tolerance of the schema.

It's just a motor inside a frame. GitHub is the factory floor. The MCP scripts are the jigs.

I'm trying to stop having a conversation with my command line, and focus on building the machine.

Stop talking to the machine. Start building the frames.
