---
title: "Applying Mechanical FMEA to Agentic Workflows"
pubDate: 
status: draft
post_url: ""
thread_id: "arc_001_architecture"
arc_position: 5
tags: ["mechanical-engineering", "FMEA", "software-3.0"]
---

The first time I watched an LLM calculate a Risk Priority Number, I felt the same thing I feel when I see a machinist eyeballing a tolerance.

Pure dread.

I've built disc changers that hold 700 DVDs. I've built wearable optics. In physical engineering, an RPN isn't a suggestion — it's the number that decides whether a failure mode gets a design review or gets shipped.

Severity × Occurrence × Detection.

That's the whole equation. No "approximately." No "based on my interpretation of the prompt."

This is what LLMs fundamentally are: volatile, highly entropic engines. You shouldn't trust them. You must strictly constrain them. And you should never, under any circumstances, let one touch your math.

**The Math Gap**

When I started running PRD automation through the EN-OS, the model was brilliant at the semantic work. Identifying failure modes. Describing downstream effects. Reasoning about root causes.

The moment I asked it to score and calculate, it drifted.

Change a word in the system prompt, get a different RPN. Run the same document twice, get two different risk matrices. One version flags a failure mode as Severity 8. The next run calls it a 6. Neither is wrong by the model's logic. Both are unacceptable by any engineering standard.

You can't version-control a vibe.

**The Split: `mcp_fmea_generator`**

You don't prompt an LLM to "be precise." You build a mechanical gauge — a structural constraint cage — that physically prevents it from committing slop before it ever touches the disk.

In this case, that means a clean architectural boundary.

1. The agent reads the PRD and extracts the semantic layer: Causes, Effects, failure language.
2. It passes raw text strings and base integer estimates to a FastMCP Python script.
3. Standard Python calculates the RPN. The math is the math.
4. A formatted Markdown matrix commits directly to the Git substrate.

The model reasons. Python calculates. Git records.

**The Audit Trail**

Because the FMEA lives as static Markdown in the repo, every risk change is perfectly diffable. If an RPN shifts next sprint, `git blame` shows exactly when and why — with zero model involvement in the record.

In mechanical engineering, you don't ask the machinist to remember the tolerance. You stamp it into the part.

Same rule. Different substrate.
