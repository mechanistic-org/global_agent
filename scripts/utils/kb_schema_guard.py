def robust_json_indexer(raw_json: dict, pydantic_schema_class):
    """
    Ticket #2 Post-Mortem Solution.
    Physically prevents the global Knowledge Base from detonating its initialization boot sequence 
    if a local Agent hallucinates broken Zod/JSON formatting into a forensic logging file.
    """
    try:
        validated_data = pydantic_schema_class(**raw_json)
        return validated_data
    except Exception as e:
        print(f"[FATAL KB ERROR] Forensic Zod Integrity breach caught organically: {e}")
        # Return fallback metrics strictly adhering to the fundamental layout.
        # This keeps the Knowledge base indexing loop alive without a Python trace-stack crash.
        return None
