The first time I wired this up, I created an autonomous ouroboros.

The agent woke on a "new issue" webhook, did the work, and pushed its commit. But I hadn't filtered the webhook events correctly. GitHub saw the agent's commit and fired another webhook. NanoClaw caught it, woke the agent back up, told it to review the change. The agent looked at its own work, decided it was fine, posted a status comment. Which triggered another webhook.

It burned through a terrifying amount of API credits in about 45 seconds before I severed the tunnel.

The fix is in the event filter — not the agent logic. The agent behaved correctly every single time. The frame around it didn't.

If you want to see the exact routing logic that prevents this now: `mechanistic-org/nanoclaw-router/main.py`.

The question this raises: what happens when the system actually works? What is the physical exhaust of a machine that runs while you sleep?

Next post: The Lights-Out Run.

Arc 002 so far: 
→ The Architecture Map + The Starter Motor: https://link.eriknorris.com/OasiFcx
→ Scheduled Amnesia: https://link.eriknorris.com/7k4M207
→ Wiring the Limit Switch: [this post]

Arc 001 (the full substrate build):
→ Git as substrate: https://link.eriknorris.com/oz3KzKD
→ The loop closing: https://link.eriknorris.com/sYapFBd
→ Jigs and amnesia: https://link.eriknorris.com/fodmn3F
→ The gatekeeper: https://link.eriknorris.com/egHwYwe
→ Mechanical FMEA: https://link.eriknorris.com/ejJ1yz3
→ The cache problem: https://link.eriknorris.com/lsR2UB9

