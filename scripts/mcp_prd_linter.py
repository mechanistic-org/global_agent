import os
import re
import yaml
import json

def lint_hardware_prd(filepath: str) -> str:
    """
    Validates a physical Hardware PRD against the strict EN-OS constraint cage.
    Ensures that NPI gates, HALT/HASS testing, stack-up models, and BOM health are rigidly defined.
    """
    if not os.path.exists(filepath):
        return json.dumps({"status": "error", "detail": f"File not found: {filepath}"})

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return json.dumps({
            "status": "error", 
            "detail": "Invalid PRD format. Must contain YAML frontmatter surrounded by ---."
        })

    frontmatter_str = parts[1]
    body_str = parts[2]

    try:
        frontmatter = yaml.safe_load(frontmatter_str) or {}
    except Exception as e:
        return json.dumps({"status": "error", "detail": f"YAML Parse error: {e}"})

    errors = []

    # 1. Frontend Constraints
    project_id = frontmatter.get('project_id')
    npi_stage = str(frontmatter.get('npi_stage', '')).upper()
    bom_health = str(frontmatter.get('bom_health_flags', '')).lower()

    if not project_id:
        errors.append("Missing Keystatic property: 'project_id'")
        
    valid_npi = ['POC', 'EVT', 'DVT', 'PVT', 'MP']
    if npi_stage not in valid_npi:
        errors.append(f"Invalid 'npi_stage'. Must be one of {valid_npi}")

    if not bom_health:
        errors.append("Missing Keystatic property: 'bom_health_flags'. We must track BOM risk (Active/NRND/EOL).")

    # BOM Locking Rule based on NPI stage
    if npi_stage in ['DVT', 'PVT', 'MP']:
        if 'locked' not in bom_health:
            errors.append(f"NPI Stage '{npi_stage}' triggered a BOM failure: The BOM must be explicitly 'locked' prior to DVT entry.")
    
    # 2. Narrative Constraints (Regex checks over the body)
    body_lower = body_str.lower()

    # Dimensions
    if not all(term in body_lower for term in ['critical', 'controlled', 'reference']):
        errors.append("Dimensions un-categorized. You must explicitly separate Critical, Controlled, and Reference dimensions.")
        
    # Stack-up Analysis
    if 'stack-up' not in body_lower and 'stackup' not in body_lower:
        errors.append("Missing 'worst-case stack-up analysis'. (Must account for surface finishes/coatings).")
    elif 'finish' not in body_lower and 'coating' not in body_lower:
        errors.append("Stack-up analysis identified, but it must explicitly account for surface 'finishes' and 'coatings'.")

    # HALT / HASS / MTBF
    if 'halt' not in body_lower or 'destruct' not in body_lower:
        errors.append("HALT phase missing or fails to define discovery of fundamental 'destruct limits'.")
    if 'hass' not in body_lower:
        errors.append("HASS screening limits missing. Must be set below destruct boundaries.")
    if 'mtbf' not in body_lower and 'life cycle' not in body_lower and 'lifecycle' not in body_lower:
        errors.append("MTBF baseline missing. You must define in-service 'life cycle' testing.")

    # FMEA Soft Requirement
    if 'fmea' not in body_lower:
        errors.append("FMEA Soft Requirement Failed: You must provide FMEA inputs up front or explicitly explain their absence.")

    # Fluff check
    fluff_words = ['lightweight', 'seamless', 'blazing fast', 'magic', 'just works']
    found_fluff = [w for w in fluff_words if w in body_lower]
    if found_fluff:
        errors.append(f"Subjective fluff detected. A hardware PRD uses physical bounds. Remove: {', '.join(found_fluff)}")

    if errors:
        return json.dumps({
            "status": "failed",
            "errors": errors,
            "message": "PRD failed hardware NPI validation constraints."
        }, indent=2)

    return json.dumps({
        "status": "success",
        "message": f"Hardware PRD successfully validated for gated stage {npi_stage}."
    })
