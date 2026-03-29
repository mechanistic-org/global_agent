---
status: posted
post_url: "https://www.linkedin.com/feed/update/urn:li:activity:7443811239484624896?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7443811239484624896%2C7443811920656199680%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287443811920656199680%2Curn%3Ali%3Aactivity%3A7443811239484624896%29"
---

The first time I set this up, I put the agent on a 5-minute cron job.

It completely missed a race condition where two issues were linked and closed between intervals. The board looked clean. The agent committed against a state that no longer existed.

I'd already solved the stale cache problem in the memory layer. Then I rebuilt it one level up in the trigger layer without realizing it.

The hardest conceptual pivot of the whole architecture: stop thinking about time. Start thinking about events.

The question this raises immediately: if you rip out the cron job, how do you actually catch a GitHub webhook and physically wake a sleeping Python container on a local machine?

Next post: The Cloudflare Router.

Arc 002 so far: 
→ The Architecture Map + The Starter Motor: https://link.eriknorris.com/OasiFcx
→ Scheduled Amnesia: [this post]

Arc 001 (the full substrate build):
→ Git as substrate: https://link.eriknorris.com/oz3KzKD
→ The loop closing: https://link.eriknorris.com/sYapFBd
→ Jigs and amnesia: https://link.eriknorris.com/fodmn3F
→ The gatekeeper: https://link.eriknorris.com/egHwYwe
→ Mechanical FMEA: https://link.eriknorris.com/ejJ1yz3
→ The cache problem: https://link.eriknorris.com/lsR2UB9
