This is the same architectural pattern as the gatekeeper — applied one layer deeper. The linter enforces the schema. The FMEA generator enforces the math. In both cases: the LLM is not allowed to touch the deterministic layer.

Having built hardware where tolerances are non-negotiable, watching a model guess an RPN wasn't just architecturally wrong. It was viscerally wrong.

The agent code is in mechanistic-org/global_agent if you want to see the split in practice.

Arc so far:
→ Git as substrate: https://link.eriknorris.com/oz3KzKD
→ The loop closing: https://link.eriknorris.com/sYapFBd
→ Jigs and amnesia: https://link.eriknorris.com/fodmn3F
→ The gatekeeper: https://link.eriknorris.com/eJj1yz3

Next: the cache problem — why the machine has to be taught to aggressively forget.
