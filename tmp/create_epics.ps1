$ErrorActionPreference = "Stop"

function Create-Epic {
    param(
        [string]$Title,
        [string]$Body
    )
    Write-Host "Creating Epic: $Title"
    $ISSUE_URL = gh issue create --repo mechanistic-org/global_agent --title $Title --label "Epic" --body $Body
    Write-Host "Created Issue: $ISSUE_URL"
    
    $ITEM_JSON = gh project item-add 5 --owner mechanistic-org --url $ISSUE_URL --format json
    $ITEM_ID = ($ITEM_JSON | ConvertFrom-Json).id
    Write-Host "Item ID: $ITEM_ID"
    
    # Size = Epic
    gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvM --single-select-option-id fc09dfdb
    # Node = global_agent
    gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynvY --single-select-option-id 1604745d
    # Status = Backlog
    gh project item-edit --project-id PVT_kwDOEA3Ajc4BSLlf --id $ITEM_ID --field-id PVTSSF_lADOEA3Ajc4BSLlfzg_ynrs --single-select-option-id f75ad846
}

# 1. Intake Engine
$Body1 = @"
## Strategic Overview
Define the fundamental input and routing mechanisms for local unstructured data to feed the EN-OS.

## Objectives
- **Local Whisper Pipeline:** Automate NLM .mp4 audio transcription natively and MapReduce it into structured Markdown via `mine_session.py`.
- **Triage Router ("Brains in Boxes"):** An intake gateway that classifies input format (text vs x-section vs PDF) and statically hands it to specialized local agents.

## DoD
- [ ] Audio pipeline ingests an mp4 and outputs structured markdown into registry.
- [ ] Gating router successfully switches contexts between 2 different domains without manual intervention.
"@
Create-Epic -Title "[Epic] The Intake Engine: Brains in Boxes Routing" -Body $Body1

# 2. Mechanical Claws
$Body2 = @"
## Strategic Overview
Deep mechanical engineering workflows reliant on deterministic Python-driven math, acting upon LLM-extracted unstructured assumptions.

## Objectives
- **FMEA Generator:** Agent parses causes/effects; native Python (`dfmea_schemas.py`) scores the RPN; system outputs an aesthetic Markdown visualizing liability.
- **Tolerance & GD&T Vision:** A vision model processes inputted cross-sections, calculates the mechanical stack locally, and yields professional GD&T visualizations rooted in the Y14.5 Truth Engine.
- **Design of Experiments (DOE):** Takes fuzzy variables and outputs strict fractional factorial Python/JMP matrices and D3 visualization dashboards.

## DoD
- [ ] Stand up discrete FMEA Agent/Python boundary structure.
- [ ] Implement GD&T Vision stack with bounding constraint scripts.
- [ ] Generate one automated DOE D3 visualization locally.
"@
Create-Epic -Title "[Epic] The Mechanical Claws: Physics & Constraint Engines" -Body $Body2

# 3. Strategy & Deep Research Engines
$Body3 = @"
## Strategic Overview
Advanced analytical "forcing-function" visualizers and tightly constrained Deep Research workflows over local corporate data.

## Objectives
- **Constrained Deep Researcher:** A local, strictly bordered extraction claw querying local static/archival corporate assets.
- **Root-Cause Visualizations (SWOT, TOWS, Ishikawa):** Manual trigger workflows producing exponential visuals and metrics out of fuzzy market assumptions.
- **PRD Scaffolding Engine:** Standardized generation of agile epics.

## DoD
- [ ] A local agent performs deep research across a scoped selection of PDFs and yields a markdown summary.
- [ ] Single-shot matrix generator established.
"@
Create-Epic -Title "[Epic] Strategy & Deep Research Engines" -Body $Body3

# 4. Storyteller Claws
$Body4 = @"
## Strategic Overview
Converting raw EN-OS engineering history and screen captures into public-facing proof-of-work representations (Dark Hangar UX).

## Objectives
- **Sovereign Screenshot Time-Machine:** A vision claw chronologically tagging, storing, and assembling 2500+ screenshots into coherent story sets.
- **Portfolio Persona Agent:** A chatbot deeply trained on the EN-OS and Erik-centric artifacts, acting as the ultimate evaluate capability layer.
- **Dark Hangar Auto-Publisher:** Render structured stories to Markdown and seamlessly inject into Hyphen/Portfolio repos via AST patching to CF deployment.

## DoD
- [ ] Vision script parses 100 screenshots into structured chronological tags.
- [ ] Portfolio Agent answers 5 baseline technical questions accurately via CLI.
- [ ] Astro static injection successfully publishes to domains.
"@
Create-Epic -Title "[Epic] The Storyteller Claws: Portfolio & Vision" -Body $Body4
