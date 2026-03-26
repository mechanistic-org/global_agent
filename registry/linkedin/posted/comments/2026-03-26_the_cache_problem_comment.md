This was the hardest bug to track down because the machine wasn't hallucinating—it was executing perfectly against a reality that had already changed.

The fix was architectural: we stripped its ability to perform "lazy reads." The system now physically prevents an agent from acting unless it has queried the live GitHub state within the current boot cycle.

No cache. No stale state. Just the substrate.

Arc so far:
→ Git as substrate: https://link.eriknorris.com/egHwYwe
→ The loop closing: https://link.eriknorris.com/oz3KzKD
→ Jigs and amnesia: https://link.eriknorris.com/sYapFBd
→ The gatekeeper: https://link.eriknorris.com/fodmn3F
→ Mechanical FMEA: https://link.eriknorris.com/eJj1yz3

Next: the full architecture map — what EN-OS actually looks like as a system, and what it still can't do.
