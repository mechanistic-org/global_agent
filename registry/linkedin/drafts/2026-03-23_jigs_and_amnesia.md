---
title: Jigs, PTSD, and the Old Testament of Project Management
pubDate: 2026-03-23
status: draft
tags: [ai-engineering, StateMachines, mental-models, tooling]
source: hired-gun-synthesis
---

The more things change, the more they stay exactly the same.

In the pursuit of building a futuristic AI engineering OS - coordinating swarms, orchestrating model handoffs, and managing autonomous loops - I realized the entire system still lives or dies by one thing:

Old-school, Old Testament project management rigor. You must, as ever, define and maintain a persistent vision and architecture, and then build the tooling to enforce it.

For months, I tried building with "agents" by talking to them. I kept tweaking system prompts, using more and more complex systems of files and folders, hoping to make the model maintain context and follow instructions.

Hit the wrong zone of the context window, and you will find yourself repeating yourself endlessly to an ephemeral machine.

So I stopped treating this as an academic software problem and started treating it as a physical engineering problem.

I am building a Cognitive Manufacturing Line.

In a machine shop, if you want a drill to hit dead-center on ten thousand parts, you don't give the motor a 10-page instruction manual. You build a jig. You fabricate a rigid metal frame that physically prevents the bit from wandering.

Right now, it seems like we need to build the exact same tooling for LLMs.

They are volatile, highly entropic engines. You shouldn't trust them to format a PRD or calculate an FMEA matrix. Instead, you build constraint cages.

My OS doesn't ask the agent to "be precise." The agent is forced to run its output through a strict Pydantic validation tool. If it hallucinates a field, misses a metric, or uses passive voice, the Python runtime physically rejects the payload and returns the structural error.

The machine is forced to iterate mechanically until its output fits the exact physical tolerance of the schema.

It’s just a motor inside a frame. GitHub is the factory floor. The MCP scripts are the jigs.

I'm trying to stop having a conversation with my command line, and focus on building the machine.

Stop talking to the machine. Start building the frames.
