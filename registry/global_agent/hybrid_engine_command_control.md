---
title: Hybrid Engine Command & Control Architecture
tags: ["architecture", "command-and-control", "sprint-board", "taxonomy"]
abstract: Documentation of the 5-Node Sovereign Pipeline, the 6-Node Custom Issue Type hierarchy, and Project #5 Automated Routing.
---

## Hybrid Engine Command & Control Architecture

The EN-OS Command & Control architecture relies on a strict **5-Node Sovereign Pipeline** and a **6-Node Custom Issue Type** hierarchy. `global_agent` serves as the operational center, aggregating work via **Project #5 (The Global Sprint Board)**.

### The 6-Node Custom Issue Types
The infrastructure uses 6 custom GitHub issue labels to deterministically tag and route work across all repositories:
1. **Epic:** Large, cross-repository architectural initiatives or mini-campaigns.
2. **Pivot:** Strategic shifts or fundamental refactors (e.g., changing from a multi-agent swarm model to a limit switch model).
3. **Task:** Standard engineering units of work.
4. **Bug:** Defect tracking requiring immediate resolution.
5. **Validation:** Checks or verification mechanisms, often attached to CI/CD loops.
6. **Enhancement:** Gradual improvements to existing stable systems.

### Automated Routing & The CEO Dashboard
The "Solopreneur Stack" (CEO Dashboard) utilizes GitHub **Project #5** as the single source of truth for the Sprint Board. 
It uses automated auto-add workflows via the `is:open label:"Epic"` filter (along with other project filters) to automatically ingest tickets from across all operational repositories (`global_agent`, `mechanistic`, `portfolio`, `mootmoat`, `hyphen`). Autonomous agents use the `sprint_board.py` tool to pull this unified view natively before acting.

### The "Ghost Ticket" Workaround
When cross-repo conceptual efforts, external vendor tasks, or pure design epics are created, they often lack a dedicated codebase. The workaround is the **Ghost Ticket**:
- These Epics are filed in the `global_agent` repository.
- They are tagged with specific **Node Affinity** tags to represent the external system or conceptual branch they apply to.
- This allows the global sprint board to track them as first-class items automatically, without cluttering client repositories or polluting the `mootmoat` identity protocol with operational detritus.
