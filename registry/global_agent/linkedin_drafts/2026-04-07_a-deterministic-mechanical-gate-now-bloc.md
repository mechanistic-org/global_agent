---
title: A deterministic mechanical gate now blocks the '50-Subcommand bypass' prompt injection.
pubDate: 2026-04-07
audio_url: ''
isDraft: true
tags: ["security", "prompt-injection", "llm-security", "vulnerability-fix", "nanoclaw"]
---

A critical prompt injection vulnerability, the '50-Subcommand bypass,' was addressed by implementing a deterministic mechanical gate. This gate strictly counts subcommands (like `&&`, `||`, `;`, `|`, `&`) in `/execute` payloads via regex, rejecting execution instantly if more than five are detected, effectively blocking complex bash logic attacks before LLM interaction.