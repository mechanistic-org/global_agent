# LAW CANDIDATE — 2026-03-24

**Rule:** Codified the rule: Operational docs must clearly delineate manual authentication and DNS setup for external services.

Operational documentation must explicitly call out manual user authentication steps for external services, such as running `cloudflared tunnel login` in a browser, and manual DNS configuration (e.g., CNAME records). These steps cannot be fully automated and are critical for successful deployment.

**Tags:** operations, cloudflare, authentication, manual steps, documentation, law
