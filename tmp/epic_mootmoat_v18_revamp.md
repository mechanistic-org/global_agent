# Epic: MootMoat V18 Architecture & Aesthetic Revamp

**Status:** Backlog
**Labels:** `epic`, `mootmoat`, `astro`, `frontend`, `automation`
**Assignee:** @erik

### The Problem
MootMoat (the Sovereign Identity Protocol and the primary documentation/portfolio hub for the EN-OS) is currently decaying on an ancient V17 baseline. The live site (`mootmoat.com`) is riddled with boilerplate templates, the aesthetic is severely lacking ("superlame"), and the underlying pipeline is entirely manual. As the EN-OS infrastructure matures (Hyphen-LID, Arc 002, Swarm operations), the core documentation repository cannot remain a piece of legacy technical debt. 

### The Objective
This Epic serves as the coordination hub to orchestrate a ~30+ ticket teardown and rebuild of the `mootmoat` repository. The goal is to elevate MootMoat to a "V18" standard: fully automated, visually aligned with the Dark Hangar aesthetic, and systematically refactored by the NanoClaw agent swarm.

### Core Objectives (The 30-Ticket Baseline)

**1. Aesthetic Teardown & Rebuild**
- [ ] Eradicate all V17 boilerplate code and default Astro/Starlight templates.
- [ ] Implement the dark-mode / Dark Hangar design system across all topography.
- [ ] Overhaul typographic hierarchy and landing page routing.

**2. Automation & Data Pipelines**
- [ ] Finalize the "Spoke Scraper Daemon" to automatically sync `.md` exhaust from `mechanistic` and `MO` into the MootMoat hub without manual intervention.
- [ ] Ensure the local Vector DB (ChromaDB) ingestion loop is stable and automated.

**3. Agentic Task Delegation**
- [ ] Break down the frontend refactor into 30 atomic, discrete tickets.
- [ ] Spin up NanoClaw agents to systematically execute the component rewrites, treating the UI overhaul as a native OS engineering task.

### Notes
*This is the parent coordination ticket. Execution requires slicing the 30 individual tasks into the sprint board and assigning them out to either human or claw.*
