---
commenter: Dmitry Fink
title: Software Engineer at Oculus VR / Facebook
date: 2026-03-27
post: 2026-03-22_git_as_agent_substrate
status: responded
---

# Interaction Log: Dmitry Fink (The "Lynus" Comment)

## The Comment
> "What did Lynus knew? This is quite click baity. Any source control would work here, nothing special about how git stores things internally , e.x CVS would work as well :) Tasks has nothing to do with git or Lynus. Neither have proper semantic search capabilities"

## The Strategy
**The Public Square Defense:** The commenter was combative, dismissive ("click baity"), missed the entire point of the architecture, and repeatedly misspelled Linus. Instead of arguing, we adopted the "Adult in the Room" correction—passive spelling correction, refusing the bait, and delivering an overwhelmingly stronger architectural reason for Git (LLM training weights, not file storage).

We also took his insult about missing semantic search and turned it into proof that the architecture was two steps ahead of him (ChromaDB layer).

This interaction ultimately led to the formalization of **Law 005: LinkedIn Engagement Defense**.

## The Response
> "Dmitry, crediting Linus is not clickbait—it's attribution.
> 
> Part of my engineering process is diligence: looking at a structural problem and asking, 'has this already been solved?' By explicitly framing the LLM memory problem against what Torvalds built decades ago, I'm giving credit where credit is due rather than pretending I invented the wheel.
> 
> To your technical point: CVS or SVN could theoretically store text, sure. But the reason Git is the substrate for my specific OS isn't about internal file storage—it's about LLM training weights. Foundation models are natively fluent in Git commands, branching, and diffs out of the box. They don't natively understand CVS. Giving an autonomous agent Git is just handing it a tool it already knows how to use.
> 
> And you're spot-on regarding semantic search! That's exactly why Git is solely the storage layer here. The actual semantic routing is handled by a separate ChromaDB instance sitting on top of the markdown, which I cover exactly how to build later in the arc.
> 
> Thanks for stopping by!"
