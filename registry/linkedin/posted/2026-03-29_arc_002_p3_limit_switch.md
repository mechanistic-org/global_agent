---
title: "\"Wiring the Limit Switch: Cloudflare and the NanoClaw\""
pubDate: 2026-03-29
status: posted
post_url: "https://www.linkedin.com/posts/eriknorris_we-killed-the-cron-job-we-established-that-share-7444100105600692224-fiH6?utm_source=share&utm_medium=member_desktop&rcm=ACoAAABdXVoBKKhtjiCX7nis-4b57W2tJQIdL2I"
dub_link: "https://link.eriknorris.com/HQQeu0Z"
tags: ["AgenticAI", "SovereignOS", "EventDriven", "FastAPI", "Software30"]
---

We killed the cron job. We established that an autonomous system can't poll for changes — it has to be shocked awake by the environment.

In a physical factory, you wire a limit switch to the conveyor belt. In the EN-OS, the limit switch is a webhook. The wire is a Cloudflare Tunnel.

**The Signal**: A human — or another system — opens a GitHub Issue, adds a label, or pushes a specific branch. The Git substrate fires a JSON webhook payload into the ether.

**The Synapse**: A persistent Cloudflare Tunnel catches it and routes it securely through the firewall directly to local hardware. No open ports. No exposed surface. The outside world can push. The host stays sealed.

**The Motor Starter**: The webhook doesn't hit the LLM directly. It hits NanoClaw — a lightweight, deterministic FastAPI router sitting on the machine. NanoClaw parses the JSON, identifies the event type, and spools up the correct agent profile.

The brain wakes up inside its container. Blind to everything except the task it was handed.

**The Danger of the Live Wire**
Connecting a stochastic LLM to a live internet trigger is terrifying. 

The first time I wired this up, I didn't have adequate circuit breakers. A webhook fired and woke Node 0 (the global agent). Node 0 read the repository and autonomously decided to trigger the UI generative framework. It booted up 17 localized sub-agents in a serial cascade, all trying to read and write to the same Astro components at once. 

It instantly locked up 128GB of RAM, brought a 24-core i9 to its knees, and burned through an entire daily allocation of API tokens in about 45 seconds before executing a single successful merge. The RTX 4000 Ada in the same box sat completely idle. The inference was running on the CPU.

This is exactly why Arc 001 (The Constraint Cages) had to happen first.

I can only let the machine wake itself up because I already built the micrometer. When NanoClaw wakes the agent, the agent is immediately locked inside the constraint cages built weeks ago. It reads the live substrate — no cache. It does the work. It attempts to commit. If the output is slop, the mcp_prd_linter physically rejects it before it touches the disk.

The agent iterates until it passes mechanical tolerance. Then it commits.
Then the container burns. The agent dies.

It doesn't stay awake waiting for the next job. It shuts down completely, leaving only the validated commit on the substrate.

We took our hands off the spindle. The line is live.

---
_Next: The first real part off the line. We take the always-on OS and feed it a real, high-stakes hardware project: The Hyphen Universal Dispenser Lid._

#AgenticAI #SovereignOS #EventDriven #FastAPI #Software30
