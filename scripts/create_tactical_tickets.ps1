$PROJECT_ID = "PVT_kwDOEA3Ajc4BSLlf"

function CreateAndWireIssue {
    param (
        [string]$Title,
        [string]$Body,
        [string]$Label,
        [string]$IterationId,
        [string]$PriorityId,
        [string]$SizeId,
        [string]$NodeId,
        [string]$ImpactId
    )
    
    Write-Host "`n>> Creating Issue: $Title"
    # Using a temporary file to safely pass complex markdown bodies
    $bodyFile = [System.IO.Path]::GetTempFileName()
    $Body | Out-File -FilePath $bodyFile -Encoding UTF8

    $ISSUE_URL = gh issue create --repo mechanistic-org/global_agent --title $Title --body-file $bodyFile --label $Label
    Remove-Item -Path $bodyFile -ErrorAction SilentlyContinue

    if (-not $ISSUE_URL) {
        Write-Error "Failed to create issue"
        return
    }
    Write-Host "Issue URL: $ISSUE_URL"
    
    $ITEM_JSON = gh project item-add 5 --owner mechanistic-org --url $ISSUE_URL --format json
    $ITEM_ID = ($ITEM_JSON | ConvertFrom-Json).id
    Write-Host "Project Item ID: $ITEM_ID"
    
    if ($IterationId) { gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID --field-id PVTIF_lADOEA3Ajc4BSLlfzg_ynvU --iteration-id $IterationId }
    if ($PriorityId) { gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI --single-select-option-id $PriorityId }
    if ($SizeId) { gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM --single-select-option-id $SizeId }
    if ($NodeId) { gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY --single-select-option-id $NodeId }
    if ($ImpactId) { gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc --single-select-option-id $ImpactId }
    Write-Host "Wired successfully."
}

# TICKET 1: Always-On Router
$body1 = @"
**BLUF:** Bridge the gap between GitHub events and autonomous NanoClaw containers without exposing the local network.

## Architecture
1. **Cloudflare Tunnel (`cloudflared`)**: Runs securely as a background service binding local machine to external webhook URL.
2. **FastAPI Daemon (`mcp_router_daemon.py`)**: A lightweight event receiver that listens on a local port. No inbound firewall rules required.
3. **Trigger**: Receives GitHub payload -> Validates HMAC signature -> Parses Issue ID -> Executes subprocess `docker run --rm nanoclaw:latest --issue <id>`.

## DoD
- [ ] Connect `cloudflared` tunnel and secure local endpoints.
- [ ] Built `mcp_router_daemon.py` with FastAPI and HMAC security.
- [ ] Define subprocess shell constraints for `docker run`.
- [ ] Successfully boot an ephemeral NanoClaw container via a GitHub webhook event.
"@

CreateAndWireIssue `
    -Title "Always-On Router: Cloudflare Tunnel + FastAPI Webhook Daemon" `
    -Body $body1 `
    -Label "Epic" `
    -IterationId "381c7c80" `
    -PriorityId "79628723" `
    -SizeId "0518a320" `
    -NodeId "1604745d" `
    -ImpactId "3bba799e"
    # sprint1, P0, Enhancement, global_agent, Sovereignty

# TICKET 2: PRD Linter
$body2 = @"
**BLUF:** Build a deterministic constraint cage to enforce structural schema parity and the Law of Narrative Impact on AI-drafted PRDs.

## Architecture
- **Tool:** `mcp_prd_linter`
- **Hook:** Agents must run PRDs through this gauge before saving/committing.
- **Rules:** Validates Keystatic configuration matching. Runs Regex/NLP passes to fail passive voice and enforce quantifiable metrics requirements.

## DoD
- [ ] Define the Keystatic TypeScript to Markdown validation ruleset.
- [ ] Implement the NLP Narrative constraint engine.
- [ ] Wire as an active MCP tool in the Sovereign Registry hub.
"@

CreateAndWireIssue `
    -Title "Skill: PRD Structural Generator & Linter (mcp_prd_linter)" `
    -Body $body2 `
    -Label "Epic" `
    -IterationId "" `
    -PriorityId "0a877460" `
    -SizeId "0518a320" `
    -NodeId "e0bf719a" `
    -ImpactId "f6d8749f"
    # Backlog, P1, Enhancement, portfolio, Aesthetic

# TICKET 3: FMEA Generator
$body3 = @"
**BLUF:** Hardware engineering requires deterministic Risk Priority Numbers (RPN) and auditable matrices. Generate this strictly using an MCP integration.

## Architecture
- **Tool:** `mcp_fmea_generator`
- **Hook:** Ingests PRD markdown, extracts mechanical/process failure modes via context flow, but natively calculates RPN values dynamically inside python logic constraint cage.
- **Persistence:** Creates a formatted Markdown matrix output, inherently saving locally to the registry and automatically embedding into ChromaDB via `push_forensic_doc`.

## DoD
- [ ] Write `mcp_fmea_generator` codebase.
- [ ] Establish Occurrence, Severity, Detection math models in code.
- [ ] Test the pipeline pushing specific hardware telemetry into ChromaDB for associative recall.
"@

CreateAndWireIssue `
    -Title "Skill: Deterministic FMEA Generator & Matrix RPN Calculator" `
    -Body $body3 `
    -Label "Epic" `
    -IterationId "" `
    -PriorityId "0a877460" `
    -SizeId "0518a320" `
    -NodeId "1af498ba" `
    -ImpactId "d0738fe8"
    # Backlog, P1, Enhancement, mechanistic, R&D

Write-Host "All tickets created and wired into Project #5."
