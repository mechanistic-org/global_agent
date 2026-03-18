from pydantic import BaseModel, Field
from typing import List

# ==========================================
# 1. THE PHYSICS VAULT (DFMEA)
# ==========================================
class FailureMode(BaseModel):
    failure_mode: str = Field(..., description="The specific physical, thermal, or kinematic failure mode.")
    description: str = Field(..., description="Deep forensic engineering description of WHY it fails based on physics.")
    severity: int = Field(..., ge=1, le=10, description="AIAG Severity score 1-10")
    occurrence: int = Field(..., ge=1, le=10, description="AIAG Occurrence score 1-10")
    detection: int = Field(..., ge=1, le=10, description="AIAG Detection score 1-10")
    rpn: int = Field(..., description="Risk Priority Number (Severity * Occurrence * Detection)")
    is_critical_blocker: bool = Field(..., description="Does this prevent the system from functioning entirely?")
    status: str = Field(..., description="Must be 'CRITICAL', 'MARGINAL', or 'HOLD'")
    mitigation: str = Field(..., description="Strict engineering modification or SOW gate required to prevent failure")
    knock_on_effects: List[str] = Field(..., description="Downstream cascading catastrophic effects if unmitigated")

class DFMEANode(BaseModel):
    subsystem_label: str = Field(..., description="Name of the subsystem layer")
    dependency_blocked: bool = Field(..., description="Is this blocked by an upstream failure?")
    failures: List[FailureMode] = Field(..., description="List of rigorous failure modes for this subsystem")

class PhysicsVault(BaseModel):
    nodes: List[DFMEANode] = Field(..., description="Array of all subsystem nodes and their physics failures")

# ==========================================
# 2. THE FINANCE VAULT (COMMERCIAL VALUE)
# ==========================================
class CostEscalation(BaseModel):
    stage_name: str = Field(..., description="e.g. 'Prototype Scrap', 'Tooling Failure'")
    cost_usd: int = Field(..., description="The estimated financial cost if this risk occurs")
    justification: str = Field(..., description="Actuarial justification for this cost")

class AvoidedCatastrophicCost(BaseModel):
    failure_mode_reference: str = Field(..., description="Reference to the exact physics failure mode")
    amount: int = Field(..., description="Base liability amount")
    escalation_stages: List[CostEscalation] = Field(..., description="The escalating cost stages if this fails")

class ROIJustification(BaseModel):
    avoided_catastrophic_costs: List[AvoidedCatastrophicCost]
    total_prevented_liability: int = Field(..., description="Sum of all catastrophic costs avoided")
    quarterly_retainer_usd: int = Field(..., description="The cost of our retainer")

class FinanceVault(BaseModel):
    roi_justification: ROIJustification

# ==========================================
# 3. THE LEGAL VAULT (MSA/SOW CONSTRAINTS)
# ==========================================
class DFMEALiabilityClause(BaseModel):
    failure_mode_reference: str = Field(..., description="Reference to the exact physics failure mode")
    mitigation: str = Field(..., description="The exact legal/MSA clause bounding our liability")

class EngagementTerms(BaseModel):
    limitation_of_liability: str = Field(..., description="Global limitation of liability boundaries")
    unified_architecture_mandate: str = Field(..., description="Client cannot arbitrarily swap components")
    objective: str = Field(..., description="The core legal objective of the SOW")

class LegalVault(BaseModel):
    org_dfmea: List[DFMEALiabilityClause] = Field(..., description="Specific liability clauses tied to DFMEA risks")
    engagement_terms: EngagementTerms

# ==========================================
# 4. CRUCIBLE EVALUATOR 
# ==========================================
class CrucibleEvaluation(BaseModel):
    passed: bool = Field(..., description="Does the payload meet rigorous threshold standards?")
    critique: str = Field(..., description="If failed, providing punishing critique of what was lacking.")
