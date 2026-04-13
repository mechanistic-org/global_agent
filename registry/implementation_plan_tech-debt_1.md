# EN-OS AI Technical Debt & Security Audit Strategy

This plan expands on your initial 3-Phase classification framework for AI Technical Debt. It develops specific, actionable "Security Postures" and "Debt Payment Plans" tailored directly to the EN-OS architecture (including your recent insights from the vibe coding analysis).

## Phase 1: Security & Architecture Postures

A "Posture" is a default stance or systemic constraint that inherently prevents Reckless Debt from accumulating. These postures align with the structural constraints of EN-OS.

### 1. The "Least-Privilege" Context Boundary (Data & Prompt Audit)
*   **The Posture:** Agents do not get "full access" to the system. Tools and context must be explicitly granted based on the specific Task ID or phase. 
*   **Application:** We enforce the "Two-Pillar Compression Law" (Router for history, IDE for active code). Agents cannot run generic, untethered recursive shell commands (`ls -R`). They must use surgical tools (`view_file`, `semantic_search`) to prevent context poisoning and reduce prompt vulnerability.

### 2. The "Security Claw" Telemetry Watchdog (Model & Data Audit)
*   **The Posture:** Trust nothing implicitly. Localize and monitor agent activity.
*   **Application:** (Referencing the Vibe Coding draft) Deploying a background daemon that monitors the MCP router's telemetry limits. If an agent initiates an out-of-scope CLI command or attempts a destructive action without the `// turbo-all` explicit user flag, the action is intercepted.

### 3. Structural Persistance & Ephemeral Death (Organizational Audit)
*   **The Posture:** If it isn't persisted in the Registry or ChromaDB, it does not exist. 
*   **Application:** Stop allowing implicit architectural assumptions to float in chat history. We enforce the use of `push_forensic_doc` to cement "Strategic Technical Debt" decisions. This provides a paper trail for *why* a shortcut was taken, moving it from "Reckless" to "Strategic."

## Phase 2: Debt Payment Plans

These are the operational schedules for how we actually burn down the debt in your personal stack before it compounds.

### Plan A: The "Just-In-Time" (JIT) Toll
*   **Mechanism:** The Boy Scout Rule mandated for AI agents.
*   **Action:** When a new ticket requires touching an existing module (e.g., the `sprint_board.py` or `.astro` components), the agent is *required* to run a localized audit of that file. It must add type safety, improve error handling, or document an assumption *before* laying down the new feature code.

### Plan B: The "Strategic Freeze" Sprint
*   **Mechanism:** Dedicated Iterations for structural integrity.
*   **Action:** Every 4th iteration, feature development is locked. The entire sprint is dedicated to:
    1. Upgrading/pinning local models and MCP dependencies (Model Audit).
    2. Rewriting "Reckless Debt" components into "Strategic" ones with the "Ready, Aim, Fire" approach.
    3. Pruning dead code and untethered registry documents (e.g., global_agent#56).

### Plan C: The Penetration & Drift Day 
*   **Mechanism:** Scheduled Red Teaming operations.
*   **Action:** Once a month, we aggressively try to break the EN-OS. Can we prompt-inject the agent to delete a local file? Does the Astro frontend crash under specific data loads? Finding these edges turns unknown security exposures into known, trackable tasks.

---

## Next Steps for Execution (User Review Required)

> [!IMPORTANT]
> Please review the proposed Postures and Payment Plans above. 

Once approved, I propose we execute the following steps to ground this strategy in the system:

1.  **Registry Embodiment:** Formally synthesize your prompt's "Audit Plan" and these new Postures/Payment Plans into a new doctrine document: `registry/system/doctrine_technical_debt.md` (via `push_forensic_doc`).
2.  **SOP Integration:** Update the Agent Orientation Laws (`AGENTS.md`) and session rituals to actively enforce the JIT Toll (Plan A).
3.  **Ticket Generation:** Create immediate GitHub/Sprint tickets for the "Security Claw" watchdog and the first "Strategic Freeze" system audit. 

**Does this align with how you want to manage the physical mechanisms of the audit?**
