# LAW CANDIDATE — 2026-04-07

**Rule:** Always append an `[ACKNOWLEDGED]` flag to `failsafes.log` to clear halts, preserving the forensic audit trail.

Agents must append an `[ACKNOWLEDGED] All halts cleared by Admin` timestamp to the `failsafes.log` when clearing a halt, rather than deleting the file. This ensures the preservation of a complete forensic trail and audit history for all safety state transitions.

**Tags:** safety, logging, audit_trail, forensics, rule, design_decision
