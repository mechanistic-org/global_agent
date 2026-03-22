# Compounded Component Engineering Template
**Status:** Binding Template (`law_003`)

> **[Agent Directive]** This template MUST be filled out by the Router before assigning a UI generation task. Any Agent executing this task MUST respect all 4 constraint vectors below.

## Vector 1: The Visual Mandate (Stitch MCP)
- **Target Aesthetic:** `[Stitch Project Name]` (Default: Dark Hangar)
- **Action Required:** You MUST query the `read_design_system` tool on the MootMoat MCP server to retrieve the exact `#colors` and `Typography` tokens for `[Stitch Project Name]` before writing any CSS/Tailwind. Hallucinating colors is a fatal error.

## Vector 2: The Architectural Bound
- **Component Request:** `[Component Name]`
- **Parent Objective:** `[Parent Ticket or SOW Context]`
- **Framework Constraint:** Astro / React TSX. All state must be pushed to the edges (Islands architecture).

## Vector 3: The Data Contract (Zod)
You are not allowed to invent dummy JSON payloads. Your component MUST be capable of ingesting the strict Zod payload defined for this ticket.
- **Enforced Zod Schema:** `[Target Schema Name]`
- **Mandatory Field Enforcement:** Your data model MUST include the `__forensicSummary` field and render it natively or via a tooltip/logging console within the component.

## Vector 4: Operational Boundaries (The Kill-Switch)
- **MAX_RETRIES:** `3`
- If your generated component fails the `npm run check` or `tsc --noEmit` build step three consecutive times, you MUST:
  1. Abort execution immediately.
  2. Emit a GitHub comment on the PR tagging `@eriknorris` for manual override.
  3. DO NOT continue modifying the file into a death loop.
