---
title: "Applying Mechanical FMEA to Agentic Workflows"
pubDate: 
status: draft
post_url: ""
thread_id: "arc_001_architecture"
arc_position: 5
tags: ["mechanical-engineering", "FMEA", "software-3.0"]
---

1. The Hook (The Scroll-Stopper)
I wouldn’t let an LLM design the mechanism for a modular disc vault, and I definitely won't let it calculate my Risk Priority Numbers. In the mechanical engineering world, rigor isn't optional. We use FMEA (Failure Mode and Effects Analysis) to mathematically quantify risk. But in the rush to adopt AI agents, developers are asking stochastic language models to perform deterministic risk analysis end-to-end.
If you let a neural net calculate your failure modes, you aren't doing engineering. You're rolling dice.

2. The Outline / Body Narrative
The Problem: The Math Gap in Software 3.0
Large Language Models are brilliant semantic engines, but they are terrible calculators. A Risk Priority Number (RPN) is a rigid equation: Severity × Occurrence × Detection.
When I started building out the EN-OS to automate the PRD cycles for my consultancy, I realized the agent could easily hallucinate the math or casually change a risk score based on the "temperature" of the prompt. That is unacceptable. You can't version-control a vibe.

The Solution: Splitting the Cognitive Load (mcp_fmea_generator)
To solve this, I split the pipeline. The AI handles the semantics; Python handles the math.
1. Semantic Extraction: The ephemeral agent (NanoClaw) reads the Product Requirements Document and uses its vast context to extract the semantic "Causes" and "Effects" of potential failures.
2. Deterministic Handoff: It hands those raw text strings and base integer estimates to a FastMCP Python script.
3. The Hard Math: Standard, Software 1.0 Python calculates the RPN and generates a perfectly formatted Markdown matrix.
4. The Git Substrate: That static matrix is committed directly to the repo.

The Takeaway
We are combining the fuzzy reasoning of Software 3.0 with the bare-metal determinism of Git and Python. Because the FMEA is generated as a static Markdown table, every single risk fluctuation is perfectly diffable over time.
If an RPN score changes next sprint, git blame tells me exactly when and why, with zero AI hallucination. Keep the math out of the neural net.
