Five posts in. Here's what the arc has actually been about.

I started with the substrate question — where does an autonomous agent put its memory? The answer was already built. Git has durability, auditability, diffing, branching, and a free API. The agents boot cold, read a GitHub Issue, execute one task, post a comment, and die. The container burns. The commit survives.

That solved durability. It didn't solve coherence.

The loop closing showed what happens when you hand the machine its own documentation and tell it to find the bugs. It filed six tickets before I got back from a walk. The machine reviewed the system that runs the machine. That was the proof of concept.

Then the harder problems appeared.

The amnesia is real — context windows shift, and hours of established architecture become a clean slate. The solution isn't better prompts. It's jigs: rigid structural frames that physically prevent the agent from wandering the same way a drill press prevents the bit from drifting.

The gatekeeper was the first concrete jig: a FastMCP Python linter that intercepts every agent commit and checks it against the exact Keystatic schema before it touches the substrate. If it hallucinates a field, the payload is rejected. The agent reads the error and rewrites. No exceptions.

The FMEA post extended the same logic to math: LLMs reason brilliantly. They calculate unreliably. So the architectural split is clean — the agent extracts semantic content, passes raw estimates to Python, Python runs the RPN, Git records the result. The model never touches the math.

The through-line across all five posts is the same:

**You don't prompt for precision. You build the constraint.**

The LLM is the spindle. Python is the quality control inspector. Git is the factory floor.

Full arc:
→ Git as substrate: https://www.linkedin.com/feed/update/urn:li:activity:7441577236518006784
→ The loop closing: https://link.eriknorris.com/oz3KzKD
→ Jigs and amnesia: https://link.eriknorris.com/sYapFBd
→ The gatekeeper: https://link.eriknorris.com/fodmn3F
→ Mechanical FMEA: https://www.linkedin.com/posts/eriknorris_theres-a-specific-feeling-i-get-when-i-first-share-7442663494254010369-B4Fv

Post 6 is the cache problem — why the machine has to be taught to aggressively forget. Coming shortly.
