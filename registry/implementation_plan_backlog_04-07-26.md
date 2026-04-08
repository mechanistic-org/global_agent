# Sovereign Backlog Consolidation Plan

We currently have ~46 open issues scattered across `portfolio` and `global_agent`. Many of these overlap, track the same historical debt, or reference stale architecture paradigms. The objective is to **synthesize and de-dupe** without destroying the underlying historical context, allowing us to pivot from an ambiguous backlog to a precise execution roadmap.

## Proposed Strategy: "The 6 Execution Vectors"

I have reviewed the list and propose compressing these ~46 issues into **6 core execution vectors**. We will select *one* tracking Epic per vector and move the redundant tickets into it as checklist items, subsequently closing the stragglers.

---

### Vector 1: The Dark Hangar UI Pivot (Diagnostic Terminal)
We have ~8 tickets discussing turning the portfolio into a diagnostic terminal, integrating agent chat, and headless API execution.
*   **portfolio#30**: [Epic 5] The Project OS UI Shell (Dark Hangar)
*   **portfolio#29**: Epic: Homepage Diagnostic Terminal Pivot
*   **portfolio#28**: Epic: Project-as-Dashboard (Diagnostic Terminal) Architecture Pivot
*   **portfolio#31**: [Epic 5] Headless Portfolio API (projects.json)
*   **portfolio#32**: [Epic 5] Portfolio Agent Chat Integration
*   **portfolio#65**: [Enhancement] Wire Pagefind Search UI into UniversalHUD
*   **global_agent#45**: Implement Persistent On-Demand Dashboards via Stitch
*   **global_agent#12**: [Epic 8] Holy Grail V31 UI Constraint Alignment
**Action:** Centralize under **portfolio#30 (Dark Hangar OS UI Shell)**. The rest are effectively features of the new Dark Hangar UI layer and should be closed as duplicates or converted to sub-tasks.

### Vector 2: The "Great Backport" (Data Hydration & Normalization)
There are 8 distinct Epics all trying to solve the same problem: getting the 30+ historical projects hydrated, mined by the Hack Pack, and compliant with the C24 schema.
*   **portfolio#13**: Epic: The "Great Backport"
*   **portfolio#14**: Epic: Pipeline the Remaining 20+ Deep Dives
*   **portfolio#8**: [Epic] Final Finishing Pass through all ~50 Deep Dives
*   **portfolio#7**: [Epic] Hydrate remaining ~20+ Deep Dive projects
*   **portfolio#9**: [Epic] Finish up the remainder of "Light" projects
*   **portfolio#10**: [Mining] Meta 1 (The First Loading) Analysis
*   **portfolio#19**: Resume NLM Hack Pack Mining & C24 Hydration
*   **global_agent#55**: Stratified Intelligence Indexing
**Action:** Centralize under **portfolio#13 (The Great Backport)**. We do not need 8 epics tracking historical markdown updates. We will bundle them into one master checklist representing the batch data correction.

### Vector 3: Sovereign Architecture & Tooling 
This tracks upgrades to our local agentic abilities (Python tools, schemas, physical constraints).
*   **global_agent#109**: [Epic] The Mechanical Claws: Physics & Constraint Engines
*   **global_agent#120**: GD&T Vision Stack & Bounding Constraints (Child of 109)
*   **global_agent#121**: Automated DOE D3 Visualization (Child of 109)
*   **global_agent#111**: [Epic] The Storyteller Claws: Portfolio & Vision
*   **portfolio#27**: Stitch Loop Development Pipeline & Figma Integration
*   **portfolio#47**: [Epic] Resume the C|24 Component Stitch Loop
*   **portfolio#51**: [Task] Document the 3 Stitch Workflow Paths
**Action:** Maintain **global_agent#109** and **global_agent#111** as primary capability bounds. Synthesize the Stitch tickets into a single `UI Agent` upgrade objective.

### Vector 4: Codebase Integrity & Tech Debt
Tickets addressing schema drift or literal ghost code cleanup.
*   **portfolio#61**: Schema Parity Check — Keystatic config ↔ content.config.ts drift detection
*   **portfolio#59**: [Task] Pre-commit Zod schema validator
*   **portfolio#53**: Legacy Portfolio Cleanup (Ghost Code & Import Paths)
*   **global_agent#56**: [Registry] Audit Unread Handbook & System Docs
**Action:** These are tactical strikes. **portfolio#53** should be executed first to clear the brush, moving unneeded templates to an `_archive` folder rather than nuking them completely, preserving safety.

### Vector 5: Identity Assets & Voids
Concept work for the CV, MootMoat, and data visualizations.
*   **portfolio#33**: Erik Norris Venn
*   **global_agent#91 / #90**: Biographic Synthesis / Venn Diagram Asset Generation
*   **portfolio#1**: [Keystone] The Neural Assembly (The Brain)
*   **portfolio#3**: Ouroboros & Hyde
*   **portfolio#4**: The Screenshot Colophon
*   **global_agent#89**: MootMoat V18 Architecture
**Action:** Centralize the Venn diagram tickets. The others (Brain, Colophon, Ouroboros) act as discrete feature tickets for the Dark Hangar terminal (Vector 1).

### Vector 6: Operational Rollout (LinkedIn Publishing)
*   **global_agent#104**, **#96**, **#95**: LinkedIn Arc 3, 4, 5 Rollouts
*   **global_agent#93**: Automate dub.co shortlink generation
*   **global_agent#87**: Generalize D2-to-Carousel Slicer Jig
**Action:** Group these under a single **Social Publishing Track**.

## User Review Required

> [!IMPORTANT]
> **Action Required to Proceed**
> 1. Do you agree with compressing the **8 Data Hydration** epics into a single `portfolio#13: The Great Backport` master checklist?
> 2. For the **Legacy Cleanup (portfolio#53)**, I propose we create an `_archive` folder inside the repo. Any template, component, or config we suspect is dead gets moved there instead of `git rm`. This satisfies your requirement of not blindly deleting months of work without safety logic.
> 3. Which of the 6 Vectors should we execute *first* to begin clearing the boards?
