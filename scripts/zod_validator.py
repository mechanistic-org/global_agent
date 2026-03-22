import json
from pydantic import BaseModel, Field
from typing import Dict

# The Python mapping of V32_MobileOutfittersSchema.ts
class NodeTelemetry(BaseModel):
    id: str = Field(pattern=r"^[0-9a-fA-F\-]{36}$")
    timestamp: str
    status: str = Field(pattern="^(NOMINAL|DEGRADED|FATAL)$")
    metrics: Dict[str, float]
    # Note: Using underscore mapping to reflect the JSON payload.
    forensicsSummary: str = Field(max_length=3000, alias="__forensicsSummary")

class V32DashboardPayload(BaseModel):
    accountId: str = Field(pattern=r"^[0-9a-fA-F\-]{36}$")
    activeNodes: list[NodeTelemetry]
    securityClearance: bool
    lastAudit: str

def validate_swarm_output(raw_json_str: str) -> dict:
    """Pre-Validates the local Swarm's raw hallucinated JSON against the strict V32 structural bounds."""
    try:
        data = json.loads(raw_json_str)
        validated = V32DashboardPayload(**data)
        return validated.model_dump(by_alias=True)
    except Exception as e:
        raise ValueError(f"CRITICAL: Zod Payload Constraint Breached. Local Swarm hallucinated invalid architecture: {str(e)}")
