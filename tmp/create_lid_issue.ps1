$ISSUE_URL = gh issue create `
  --repo mechanistic-org/portfolio `
  --title "[Task] Draft Hyphen LID Case Study (Pending Permission)" `
  --label "task" `
  --body "## Context`nDrafting the LID case study for the EN-OS generated portfolio. Currently waiting on Danny (Hyphen) for permission to use parts of the project.`n`n## DoD`n- [ ] Permission received from Danny`n- [ ] Content structured`n- [ ] Draft completed"
Write-Output "Issue created: $ISSUE_URL"

$ITEM_JSON = gh project item-add 5 --owner mechanistic-org --url $ISSUE_URL --format json
$ITEM_ID = ($ITEM_JSON | ConvertFrom-Json).id
Write-Output "Item ID: $ITEM_ID"

# Set metadata (Pipeline Node: portfolio, Priority: P3, Size: Task, Impact: Aesthetic, Status handled natively by project)
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY --single-select-option-id e0bf719a
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI --single-select-option-id 2c4f4751
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM --single-select-option-id d761809f
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc --single-select-option-id f6d8749f
Write-Output "Ticket fully wired to board."
