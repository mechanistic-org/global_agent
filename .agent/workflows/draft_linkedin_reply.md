---
description: Scaffolds a structured interaction log for significant LinkedIn replies to permanently capture architectural stances in the global registry.
---

# /draft_linkedin_reply

Use this workflow to ingest a meaningful inbound LinkedIn comment and draft a response. This is NOT about saving typing time; it is about keeping the "Second Brain" synchronized. By logging the interaction, the OS permanently remembers the architectural stance you took, allowing future agents to reference it.

## Steps

// turbo-all
1. Create the `interactions` directory if it doesn't exist, and scaffold the interaction file in the local registry with strict frontmatter.
```powershell
New-Item -Path "registry\linkedin\interactions" -ItemType Directory -Force | Out-Null
New-Item -Path "registry\linkedin\interactions\$(Get-Date -Format 'yyyy-MM-dd')_$($args[0].ToLower().Replace(' ', '_')).md" -ItemType File -Value @"
---
interlocutor: "[Name]"
topic: "[Core Subject]"
project_node: "[e.g., global_agent, portfolio]"
stance_taken: "[1-sentence summary of the architectural position taken in the reply]"
status: draft
---

## Inbound Context
[Paste the raw inbound comment]

## OS Analysis & Alignment
[Analyze the comment against EN-OS Laws. Is this a pitch? A challenge? Does it violate Sovereignty?]

## Drafted Response
[The actual text to copy-paste into LinkedIn]
"@
```

2. The agent automatically fills out the Markdown structure, synthesizing the OS Analysis and generating the Drafted Response in alignment with the Hired Gun persona.
