$ISSUE_BODY = @"
## Context
We need a coordinated strategic and tactical approach to deploy rich media assets (MP4 cinematic podcasts, infographics, mindmaps) alongside LinkedIn comments for the Arc 001 posts.
Due to LinkedIn edit constraints (text-only, no media insertion post-publication), all rich media must be attached natively to comments.
- **MP4s**: Lead asset for high-reach posts (e.g. Linus Torvalds post).
- **Infographics**: Clean, scroll-stopping visual summarization.

## DoD
- [ ] Asset media is generated, audited, and correctly sourced.
- [ ] Linus post self-comment is published with native MP4 attachment.
- [ ] Post #5 and Post #6 are published.
- [ ] Post #5 and Post #6 comments are deployed organically with relevant assets (e.g. infographics).
"@

$ISSUE_URL = gh issue create --repo mechanistic-org/portfolio --title "[Task] LinkedIn Asset & Comment Deployment Strategy" --body $ISSUE_BODY
Write-Output "URL: $ISSUE_URL"

$ITEM_JSON = gh project item-add 5 --owner mechanistic-org --url $ISSUE_URL --format json
$ITEM_ID = ($ITEM_JSON | ConvertFrom-Json).id
Write-Output "Item ID: $ITEM_ID"

gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTIF_lADOEA3Ajc4BSLlfzg_ynvU --iteration-id 381c7c80
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvI --single-select-option-id 0a877460
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM --single-select-option-id d761809f
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY --single-select-option-id e0bf719a
gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvc --single-select-option-id f6d8749f
