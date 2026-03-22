# LAW 003: UI Generation Paths

## 1. The Decision Tree
When the `router.py` node receives an objective to generate a new dashboard or interface, it must cleanly select one of three generation paths. This explicitly prevents "mushy" AI outputs where logic and aesthetics bleed into a broken React state.

### Path 1: Raw Logic (The Headless State)
- **Trigger:** Heavy physics, data-modeling, or DFMEA schema crunching.
- **Execution:** Do not build UI components. Generate raw Zod-validated JSON/TypeScript payloads. Let the existing UI engine map the telemetry visually.

### Path 2: Vibe-First (The Concept Scaffold)
- **Trigger:** Establishing a new dark-hangar telemetry visual without underlying rigid data constraints.
- **Execution:** Build the CSS, the layouts, and the interactive skeleton using mocked bounds. Do not attempt to wire it to backend schemas yet.

### Path 3: Mechanistic Alloy (The Hybrid Merge)
- **Trigger:** A mature component ready for production.
- **Execution:** Fuse Path 1 (Strict Zod Schemas) with Path 2 (Vibe-First Components). Ensure all React/Astro `props` strongly type against the `MasterDTO`. 

## 2. Enforcement
The Orchestrator must use the GitHub Ticket labels or the explicit task context to enforce a Path. If a Path is not clear, default to **Path 1 (Raw Logic)**. It is always safer to build headless constraints than broken UI.
