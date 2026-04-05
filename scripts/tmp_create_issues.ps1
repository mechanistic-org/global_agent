$ProjectID = "PVT_kwDOEA3Ajc4BSLlf"
$NodeField = "PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY"
$PriorityField = "PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI"
$SizeField = "PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM"
$ImpactField = "PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc"
$StatusField = "PVTSSF_lADOEA3Ajc4BSLlfzg_ynrs"

$GlobalAgentNode = "1604745d"
$P2Priority = "da944a9c"
$TaskSize = "d761809f"
$EpicSize = "fc09dfdb"
$RnDImpact = "d0738fe8"
$SovImpact = "3bba799e"
$BacklogStatus = "f75ad846"

function Create-And-Wire {
    param (
        [string]$Title,
        [string]$BodyFile,
        [string]$Label,
        [string]$SizeId,
        [string]$ImpactId
    )
    Write-Host "Creating issue: $Title"
    $IssueUrl = gh issue create --repo mechanistic-org/global_agent --title $Title --label $Label --body-file $BodyFile
    Write-Host "Issue created: $IssueUrl"

    $ItemJson = gh project item-add 5 --owner mechanistic-org --url $IssueUrl --format json
    $ItemId = ($ItemJson | ConvertFrom-Json).id
    Write-Host "Project Item ID: $ItemId"

    # Set Node to global_agent
    gh project item-edit --project-id $ProjectID --id $ItemId --field-id $NodeField --single-select-option-id $GlobalAgentNode
    # Set Priority to P2
    gh project item-edit --project-id $ProjectID --id $ItemId --field-id $PriorityField --single-select-option-id $P2Priority
    # Set Size
    gh project item-edit --project-id $ProjectID --id $ItemId --field-id $SizeField --single-select-option-id $SizeId
    # Set Impact
    gh project item-edit --project-id $ProjectID --id $ItemId --field-id $ImpactField --single-select-option-id $ImpactId
    # Set Status to Backlog
    gh project item-edit --project-id $ProjectID --id $ItemId --field-id $StatusField --single-select-option-id $BacklogStatus
    
    Write-Host "Wired $Title successfully."
    Write-Host "---------------------------"
}

Create-And-Wire -Title "[Enhancement] Implement Singleton timeline.md Logging" -BodyFile "d:\GitHub\global_agent\tmp\ticket1.md" -Label "enhancement" -SizeId $TaskSize -ImpactId $RnDImpact
Create-And-Wire -Title "[Enhancement] Enforce index.md Structuration in Local Registry" -BodyFile "d:\GitHub\global_agent\tmp\ticket2.md" -Label "enhancement" -SizeId $TaskSize -ImpactId $SovImpact
Create-And-Wire -Title "[Enhancement] Enforce Strict Provenance Metrics in Markdown Schema" -BodyFile "d:\GitHub\global_agent\tmp\ticket3.md" -Label "enhancement" -SizeId $TaskSize -ImpactId $RnDImpact
Create-And-Wire -Title "[Research & Epic] Multi-Format Local Asset Ingestion & Normalization" -BodyFile "d:\GitHub\global_agent\tmp\ticket4.md" -Label "Epic" -SizeId $EpicSize -ImpactId $SovImpact

