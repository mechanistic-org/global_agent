---
description: How to start a new LinkedIn post ticket and scaffold draft files
---
# /draft_linkedin_post

Run this workflow when beginning a new LinkedIn post to ensure it is properly tracked and scaffolded according to EN-OS standards.

## Steps

1. State the **topic or working title** of the new LinkedIn post.

2. Create a tracking issue in GitHub bridging to the project board using the `/create_issue` workflow implicitly, or manually via MCP:
```json
{
  "title": "Draft LinkedIn Post: [Topic]",
  "body": "**Topic:** [Topic]\n**Objective:** Complete draft and prepare for publishing.\n\n- [ ] Draft written in `registry/linkedin/drafts/`\n- [ ] Self-comment written in `registry/linkedin/drafts/comments/`\n- [ ] Validated against Law 004 (LinkedIn Persona)",
  "labels": ["content"]
}
```

// turbo-all
3. Scaffold the canonical draft file in the local registry with strict Keystatic frontmatter.
```powershell
New-Item -Path "registry\linkedin\drafts\$(Get-Date -Format 'yyyy-MM-dd')_$($args[0].ToLower().Replace(' ', '-')).md" -ItemType File -Value @"
---
title: "[Topic]"
pubDate: 
status: draft
post_url: 
thread_id: 
arc_position: 
tags: []
---

[Draft content goes here]
"@
```

// turbo-all
4. Scaffold the corresponding cross-comment file.
```powershell
New-Item -Path "registry\linkedin\drafts\comments\$(Get-Date -Format 'yyyy-MM-dd')_$($args[0].ToLower().Replace(' ', '-'))_comment.md" -ItemType File -Value @"
[Self-comment linking back to earlier threads or dropping receipts]
"@
```

5. Hand over control to the operator to begin drafting, reminding them to review `laws/law_004_linkedin_persona.md`.
