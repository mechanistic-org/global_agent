---
description: Create a new GitHub issue AND wire it fully to the global project board in one operation.
---

# /create_issue

The agent ALWAYS uses this pattern when creating any ticket. Never orphan an issue.

## Field Reference

| Field | ID | Options |
|---|---|---|
| Iteration | `PVTIF_lADOEA3Ajc4BSLlfzg_ynvU` | sprint1=`381c7c80` · sprint2=`54cf5c95` · sprint3=`d2c335bc` · sprint4=`b6a8f1bb` |
| Priority | `PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI` | P0=`79628723` · P1=`0a877460` · P2=`da944a9c` · P3=`2c4f4751` |
| Size | `PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM` | Epic=`fc09dfdb` · Enhancement=`0518a320` · Task=`d761809f` |
| Node | `PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY` | portfolio=`e0bf719a` · mechanistic=`1af498ba` · global_agent=`1604745d` |
| Impact | `PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc` | Revenue=`bdc0922b` · Sovereignty=`3bba799e` · Aesthetic=`f6d8749f` · R&D=`d0738fe8` |
| Status | `PVTSSF_lADOEA3Ajc4BSLlfzg_ynrs` | Backlog=`f75ad846` · Ready=`e18bf179` · In progress=`47fc9ee4` · Done=`98236657` |

Project node ID: `PVT_kwDOEA3Ajc4BSLlf`

## Steps

// turbo
1. Create the issue — agent writes full structured body:
```powershell
$ISSUE_URL = gh issue create `
  --repo mechanistic-org/REPO `
  --title "[Type] Short title" `
  --label "Epic" `
  --body "## Context\n...\n## DoD\n- [ ] ..."
Write-Output $ISSUE_URL
```

// turbo
2. Add to project board and capture item ID:
```powershell
$ITEM_JSON = gh project item-add 5 --owner mechanistic-org --url $ISSUE_URL --format json
$ITEM_ID = ($ITEM_JSON | ConvertFrom-Json).id
Write-Output "Item ID: $ITEM_ID"
```

// turbo
3. Set Iteration:
```powershell
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID `
  --field-id PVTIF_lADOEA3Ajc4BSLlfzg_ynvU --iteration-id ITER_ID_HERE
```

// turbo
4. Set Priority, Size, Node, Impact:
```powershell
# Priority
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID `
  --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI --single-select-option-id PRIORITY_ID

# Size
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID `
  --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM --single-select-option-id SIZE_ID

# Node
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID `
  --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY --single-select-option-id NODE_ID

# Impact
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID `
  --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc --single-select-option-id IMPACT_ID
```

## Notes

- Steps 3 and 4 are safe to auto-run (`// turbo`) once item ID is confirmed
- Never skip metadata — title + body alone is noise. Iteration + Priority + Node = signal.
- The agent writes the issue body. The human approves it at the `gh issue create` step.
