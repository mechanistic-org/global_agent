$PROJECT_ID = "PVT_kwDOEA3Ajc4BSLlf"

function WireIssue {
    param([string]$IssueUrl)
    Write-Host "Adding $IssueUrl to project..."
    $ITEM_JSON = gh project item-add 5 --owner mechanistic-org --url $IssueUrl --format json
    if (-not $ITEM_JSON) {
        Write-Host "Failed to add $IssueUrl"
        return
    }
    $ITEM_ID = ($ITEM_JSON | ConvertFrom-Json).id
    Write-Host "Item ID: $ITEM_ID"
    
    # Set to P0
    gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI --single-select-option-id "79628723"
    
    # Set to Backlog
    gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynrs --single-select-option-id "f75ad846"
}

WireIssue "https://github.com/mechanistic-org/global_agent/issues/99"
WireIssue "https://github.com/mechanistic-org/global_agent/issues/100"
WireIssue "https://github.com/mechanistic-org/global_agent/issues/101"
WireIssue "https://github.com/mechanistic-org/global_agent/issues/102"
