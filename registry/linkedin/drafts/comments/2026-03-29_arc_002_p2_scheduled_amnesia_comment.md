The first time I set this up, I put the agent on a 5-minute cron job.

It burned through API credits querying a quiet sprint board. Then it completely missed a race condition where two issues were linked and closed between intervals. The board looked clean. The agent committed against a state that no longer existed.

I'd already solved the stale cache problem in the memory layer. Then I rebuilt it one level up in the trigger layer without realizing it.

The hardest conceptual pivot of the whole architecture: stop thinking about time. Start thinking about events.

The question this raises immediately: if you rip out the cron job, how do you actually catch a GitHub webhook and physically wake a sleeping Python container on a local machine?

Next post: The Cloudflare Router.

Arc 002 so far: 
→ The Architecture Map + The Starter Motor: [link] 
→ Scheduled Amnesia: [this post]

Arc 001 (the full substrate build): [link]
