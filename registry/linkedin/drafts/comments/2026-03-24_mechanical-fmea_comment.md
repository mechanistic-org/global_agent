Breadcrumb: This is the same architectural pattern as the gatekeeper [link to Post #4] — just applied one layer deeper. The linter enforces the schema. The FMEA generator enforces the math. In both cases the constraint is identical: the LLM is not allowed to touch the deterministic layer.

Having built hardware where tolerances are unforgiving, watching a model guess an RPN wasn't just architecturally wrong. It was viscerally wrong.

The agent code lives in mechanistic-org/global_agent if you want to see the split in practice.
