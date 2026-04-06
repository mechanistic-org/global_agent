---
name: "prd-linter"
description: "Mathematically validates physical Hardware PRDs against the EN-OS constraint cage (NPI gates, Stack-Ups, HALT/HASS limits)."
version: "1.0.0"

inputs:
  filepath: "string (Absolute path to the PRD markdown file)"
returns: 
  type: "json"
  schema: "mcp_router.lint_hardware_prd output"

applicability:
  trigger_events:
    - "User requests to validate or lint a PRD."
    - "A new PRD is pushed to the hardware registry or NPI gating board."
  required_context:
    - "Must have the absolute path to the target PRD markdown file."
  exclusion_criteria:
    - "Do not apply this linter to pure software architecture documents. This is solely for physical hardware endpoints."

termination:
  success_state: "Linter completes execution and returns a status payload (success/failed)."
  failure_state: "Tool throws an infrastructure error or file cannot be parsed."
  max_iterations: 1
  handoff_protocol: "Output the linter JSON payload fully to the user so they can clearly read the failure modes or success confirmation."
---

# Policy ($\pi$)

When invoked to validate a physical hardware PRD, execute the following specific sequence:

1. **Verify Target:** Identify the complete absolute filepath of the PRD to be tested. 
2. **Execute Linter via MCP:**
   - Call the native EN-OS router tool: `lint_hardware_prd`.
   - Pass the `filepath` argument exactly as identified.
3. **Parse and Yield Results:**
   - If the returned payload indicates `"status": "success"`, confirm to the user that the PRD has passed NPI gating for its listed level.
   - If the payload returns `"status": "failed"`, list out the EXACT errors from the `errors` array in the JSON response using bullet points so the user can amend the document.
   - Do NOT attempt to "auto-fix" mechanical tolerances or NPI gates. Only report the results directly to the user.
