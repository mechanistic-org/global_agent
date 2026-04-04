$epics = @(
    @{
        title = "[Epic] Circuit Breakers & Runaway Execution Halts"
        priority = "79628723"  # P0
        body = "## Context`nWe must implement failsafes to stop API and compute burn loops.`n`n## DoD`n- [ ] Fail Loop Break: 3 consecutive failures triggers a hard halt.`n- [ ] Wall-clock Break: Max 45s per tool call, 5min total per job.`n- [ ] Cost Accumulation: Soft warning at 50% API budget, hard kill at 90%.`n- [ ] Telemetry: Log halt reasons explicitly to \.system_generated\logs for future parsing."
    },
    @{
        title = "[Epic] The 5-Layer Context Compaction Pipeline"
        priority = "79628723"  # P0
        body = "## Context`nImplement Claude's tiered pointer memory and compression structure to resolve context limits.`n`n## DoD`n- [ ] Ingestion Microcompaction: Compress extreme payloads before returning to main agent using local qwen2.5-coder:32b or phi3.`n- [ ] Strict Write Discipline: Update index only after confirmed OS writes.`n- [ ] KAIROS / AutoDream Daemon: Run background summarization over logs during idle time with hash-checks and append-only mode."
    },
    @{
        title = "[Epic] Dual-Mode Exec: Plan vs Execute (Agent Type System)"
        priority = "0a877460"  # P1
        body = "## Context`nSeparate the Intent layer from the Action layer.`n`n## DoD`n- [ ] NanoClaw Profiles: 'plan' mode (read-only, no outbound) vs 'exec' mode (full permissions).`n- [ ] Secondary Classifier Gating: Acts as a gate between plan and exec mode, blocks 50-Subcommand vulnerability.`n- [ ] Container Metadata: Encode agent type strictly into NanoClaw container labels."
    },
    @{
        title = "[Epic] Explicit Workflow State Management"
        priority = "da944a9c"  # P2
        body = "## Context`nShift away from relying purely on the conversation text as the state representation.`n`n## DoD`n- [ ] Typed Workflow Registry: Track states (planning, awaiting_approval, executing, closed, halted) in the markdown registry.`n- [ ] Crash Resurrection: Use checkpoints to safely resume jobs in case of drops.`n- [ ] Timeout Hooking: Tie into Circuit Breakers so any job stuck in executing automatically drops to halted."
    }
)

foreach ($epic in $epics) {
    Write-Host "Creating $($epic.title)..."
    $ISSUE_URL = gh issue create --repo mechanistic-org/global_agent --title $epic.title --label "Epic" --body $epic.body
    Write-Host "Issue created: $ISSUE_URL"
    
    $ITEM_JSON = gh project item-add 5 --owner mechanistic-org --url $ISSUE_URL --format json
    $ITEM_ID = ($ITEM_JSON | ConvertFrom-Json).id
    Write-Host "Added to project board Item ID: $ITEM_ID"
    
    gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTIF_lADOEA3Ajc4BSLlfzg_ynvU --iteration-id b6a8f1bb
    gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI --single-select-option-id $epic.priority
    gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM --single-select-option-id fc09dfdb
    gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY --single-select-option-id 1604745d
    gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc --single-select-option-id 3bba799e
}
