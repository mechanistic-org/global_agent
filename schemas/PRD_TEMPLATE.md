---
project_id: "HW-001"
npi_stage: "EVT"
bom_health_flags: "Active, Second-Source Confirmed, Placeholder $1000 for bespoke chassis"
---

# Physical Hardware Product Requirements Document (PRD)

## BLUF
This product is a highly durable, precision-machined sensory chassis for extreme environments. It ensures accurate data acquisition under structural loads by isolating internal electronics from external mechanical resonance.

## Use Cases and Product Overview
[Define the exact deployment environment and pain point. No subjective fluff.]

## Categorized Dimensions
1. **Critical Dimensions:**
   - [e.g., Distance between alignment pins: 45.00 ± 0.05 mm]
   - [e.g., Mating surface flatness: ≤ 0.02 mm over 100 mm]
2. **Controlled Dimensions:**
   - [e.g., Mounting hole diameter: 4.5 ± 0.1 mm]
3. **Reference Dimensions:**
   - [e.g., Overall bounding box length: 120 mm]

## Quantified Stack-Up Analysis
*Mandatory worst-case stack-up modeling covering all tolerances from mating components.*

- **Surface Finishes & Coatings:** All mechanical interfaces have been tolerance-stacked accounting for Anodize Type II (adds 10-15 µm per surface). 
- **Tolerance Loop [Example]:** Component A (±0.1 mm) + Coating (±0.015 mm) + Component B (±0.15 mm) = ±0.265 mm total possible gap variance.

## Testing Limits (HALT / HASS / MTBF)
1. **HALT Requirements (Destruct Limits):**
   - The device will be subjected to thermal step-stress and multi-axis vibration until mechanical failure is induced (e.g., destruct point modeling).
2. **HASS Requirements (Production Screen):**
   - 100% of EVT units will be subjected to random vibration screening safely *below destruct* limits to catch manufacturing latent defects without inducing fatigue.
3. **MTBF Baseline (Life Cycle Testing):**
   - A sub-population will undergo simulated actual service loads for true *life cycle* benchmarking to establish the baseline MTBF standard.

## FMEA Consideration
- FMEA analysis mapping single-point failure modes (e.g., fastener back-out under vibration, compromised environmental seals) is provided in the separate DFMEA log.

## Regulatory & Environmental
- **Certifications:** Must be FCC Part 15 / CE compliant prior to DVT exit.
- **Environmental:** IP67 sealed rating required.

