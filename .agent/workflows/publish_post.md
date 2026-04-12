---
description: The official ritual for moving a drafted LinkedIn post to published status, syncing OS file states with the public feed.
---

# /publish_post

> **This workflow is a routing shim.** The canonical policy, applicability conditions, and termination contract live in:
> `.agent/skills/publish-post/SKILL.md` (v2.0.0)
>
> Read and execute that skill. Do not execute logic from this file directly.

## Invocation

```
/publish_post [draft filename without extension]
```

Example: `/publish_post 2026-04-10_vibe_coding_vulnerability`

## Pre-flight Check

Before invoking the skill, confirm:
- Exactly one canonical draft file exists for this post in `registry/linkedin/drafts/`
- No `_v2`, `_revised`, or duplicate variants exist alongside it — Git history is the iteration record
- Draft frontmatter `status` is not already `posted`

If any of these fail, halt and surface to the operator before proceeding.

## Delegates to

`.agent/skills/publish-post/SKILL.md` — execute its `Policy ($\pi$)` block in full.

## Claude Code users

Use `.claude/commands/publish_post.md` — it is the environment-native shim with Bash-compatible commands.
