---
title: "Docker Sandboxes and NanoClaw"
pubDate: 2026-04-01
status: posted
post_url: https://www.linkedin.com/posts/eriknorris_i-spent-the-last-few-weeks-duct-taping-together-activity-7445136219661033472-SNPk?utm_source=share&utm_medium=member_desktop&rcm=ACoAAABdXVoBKKhtjiCX7nis-4b57W2tJQIdL2I
thread_id: 
arc_position: 
tags: []
---

I spent the last few weeks duct-taping together a solution to a problem I didn't fully understand - building the plane while flying it - and then Docker shipped a product that told me I'd been solving the right problem all along.

I'm not a developer. I'm a mechanical engineer who got obsessed with building my own local AI stack. And the further I pushed my setup from "chat assistant" to something that could actually do things autonomously, the more I ran into the same terrifying edge case: what happens when it hallucinates and takes a wrong turn on your live filesystem?

I didn't know the elegant solution. So I did what any non-coder does — I followed the logic of the problem until something worked.

If the agent can't be trusted with the real machine, give it a fake one. Spin up a disposable container, let it run loose in there, and when it's done — or when it breaks something — just throw the whole thing away. I wired this together with a lot of googling, a lot of Claude, and a probably embarrassing amount of pm2 configuration.

It worked. It was ugly. And I was mid-patch trying to make it less ugly when I checked my feeds.
Docker had just shipped "Docker Sandboxes" — sub-second microVMs built specifically so AI agents can run with full autonomy, fully isolated from the host. And a funded startup called NanoClaw had just announced a formal partnership with Docker built around the exact same premise.

Three completely independent parties. A $5B infrastructure company, a funded agent startup, and a non-coder bumbling around at home. All arrived at the same architecture.

I'm not claiming I figured something out. I'm saying the problem has a shape, and if you follow it honestly — regardless of your background — it leads you somewhere. And apparently that somewhere is now a product category.

The duct tape worked. Time to throw it away and build the next layer.
