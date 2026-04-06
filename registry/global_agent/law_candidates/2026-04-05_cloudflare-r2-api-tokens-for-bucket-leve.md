# LAW CANDIDATE — 2026-04-05

**Rule:** Cloudflare R2 API tokens for bucket-level configurations require "Admin Read & Write" permissions.

Cloudflare R2 API tokens used for modifying bucket-level configurations, such as CORS policies via the S3 API, must be scoped with "Admin Read & Write" permissions. Tokens with only "Object Read & Write" permissions will result in `Access Denied` errors for these operations, preventing successful configuration updates.

**Tags:** cloudflare, r2, api, permissions, cors, access control
