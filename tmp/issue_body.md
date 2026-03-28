## Context
Arc 001 and Arc 002 established the memory substrate and the event-driven "Nervous System" of the EN-OS. Currently, observing the system's state requires reading raw terminal logging or checking GitHub commits. To fully mature the OS, we need a native frontend to serve as the live telemetry dashboard.

## Work Completed
We prototyped the initial UI via the Stitch MCP.
- **Project Name:** EN-OS Mission Control
- **Stitch Project ID:** 12529546519156084703
- **Prompt Stack Executed:**
> A premium, dark-mode technical dashboard for an autonomous AI operating system (EN-OS) serving as the system's Mission Control. Vibe: Elite, highly technical, deep space blues (#0d1117 background) with neon green and purple accents. Layout: Left Sidebar (The Nervous System), Center Panel (The Spindle & Jigs), Right Panel (Substrate & Sensor).

## Problem
The system operates blindly in the background. Generating architectural diagrams to explain the system's behavior is inefficient. The system must natively render its own live state visually for both the engineer and for generating "X-Ray View" content.

## DoD
- [ ] Export Stitch UI React components into a local Astro/Next.js repository.
- [ ] Wire the frontend to the NanoClaw FastMCP server to receive live webhook telemetry.
- [ ] Implement live rendering of the FastMCP `mcp_prd_linter` constraint check logs in the UI terminal pane.
- [ ] Implement visualization of the active Spindle sleep/wake state.
