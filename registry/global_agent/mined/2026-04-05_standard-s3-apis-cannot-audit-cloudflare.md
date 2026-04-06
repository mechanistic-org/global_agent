---
title: Standard S3 APIs cannot audit Cloudflare R2 custom domains or `.r2.dev` URLs, requiring Cloudflare-specific access.
date: 2026-04-05
context_node: conversation_miner
---

Auditing Cloudflare R2 custom domains and randomly generated `.r2.dev` public URLs cannot be performed solely via the standard S3 (`boto3`) API. Comprehensive data collection for these endpoints requires direct access to the Cloudflare Dashboard or specific Cloudflare API keys, highlighting a limitation of the standard S3 interface for Cloudflare-specific features.