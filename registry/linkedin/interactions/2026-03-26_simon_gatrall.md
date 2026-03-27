---
interlocutor: "Simon Gatrall"
topic: "GitHub as native LLM environment (FeatureScript/Onshape)"
project_node: "global_agent"
stance_taken: "Validate that LLMs natively understand Git structures, bridging his FeatureScript experience to the broader concept of agentic memory."
status: draft
---

## Inbound Context
If you just ask ChatGPT (or likely Claude etc) what's the best way to set up a development system to work with it, it will tell you to use GitHub. At least that was my experience with FeatureScript coding for Onshape. It makes it easier to also have local repo clones of other projects or standard libraries for reference. For web applications it hasn't been so specific.

## OS Analysis & Alignment
This is not a question or a challenge; it's validation from a highly relevant peer (an Onshape developer/mechanical-adjacent engineer). He is observing that when you ask an LLM to organize a complex workspace (like FeatureScript standard libraries), it naturally hallucinates or requests Git infrastructure. This perfectly aligns with the OS premise that Git is the natural substrate for agents. Since he is an Onshape dev, connecting this to hardware/CAD engineering contexts is valuable.

## Drafted Response
Perfect validation of the 'made in our image' aspect - It’s fascinating that when you give these models a complex structural problem (like managing FeatureScript libraries), they organically steer you toward a Git-like architecture just to keep themselves grounded.

They intrinsically understand repositories, cloning, and branching as ways to separate 'standard reference' from 'active work.' What I’ve found is that if you take that instinct and actually wire the agents directly into the Git APIs, they stop treating GitHub as just version control and start using it as their actual short-term and long-term memory.

Have you been using Claude/ChatGPT to write custom FeatureScript? Would love to hear how that's working out for you in Onshape.