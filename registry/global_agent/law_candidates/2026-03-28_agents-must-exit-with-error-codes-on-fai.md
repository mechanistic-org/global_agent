# LAW CANDIDATE — 2026-03-28

**Rule:** Agents must exit with error codes on failure, allowing calling processes to prevent data loss and ensure data integrity.

Agents must always respect the established system architecture, especially regarding error handling and data integrity. Upon encountering a critical failure, agents must exit with an appropriate error code (e.g., Code 1) and ensure that the calling process can gracefully manage the failure state, preventing data loss or silent corruption. This principle ensures system resilience and reliable data processing.

**Tags:** agent design, error handling, architecture, data integrity, law
