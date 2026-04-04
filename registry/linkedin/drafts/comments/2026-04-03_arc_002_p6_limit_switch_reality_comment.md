For context, the exact specs representing the "12 Days of work" were dropped in the comments here:
https://www.linkedin.com/feed/update/urn:li:activity:7445540933250580480?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7445540933250580480%2C7445951198811238400%29

For those wondering what the execution of that spec actually looks like under the hood... here is the direct trace from our daemon logs when we tested the Dual-Mode routing logic.

When a human deliberately drops an `/execute` comment on that ticket, the Node upgrades the environment to `EXEC` mode, restoring the physical tool array:

`2026-04-03 20:19:25 | INFO | TRIGGER B: Item moved to 'In progress' [PLAN MODE]`
`2026-04-03 20:19:27 | INFO | TRIGGER A: /execute detected → mechanistic-org/global_agent#103 [EXEC MODE]`
`2026-04-03 20:19:27 | INFO | IGNITION: NanoClaw queued for mechanistic-org/global_agent#103`

Deterministic triggers, Zero "Whack-A-Mole" prompt tuning.
