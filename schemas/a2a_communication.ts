import { z } from "zod";

// ---------------------------------------------------------------------------
// THE VIRTUAL C-SUITE (A2A) CONSTRAINT CAGE
// ---------------------------------------------------------------------------
// These schemas mathematically enforce the data shape when the local Llama models 
// act as Persona Agents. They cannot hallucinate risk assessments; they must 
// output exact JSON matching this specification.

// The ECU Taxonomy definitions for Risk Grading
export const EcuTaxonomySchema = z.enum(["NOMINAL", "MARGINAL", "CRITICAL", "HOLD_LOCK"]);

// The 8-Persona Identification
export const PersonaSchema = z.enum([
  "CTO",
  "CBDO",
  "CFO",
  "PHYSICIST",
  "COO",
  "LEGAL_COUNSEL",
  "HCI_VISIONARY",
  "PRINCIPAL_ARCHITECT"
]);

// A single finding from a persona auditing a PRD/SOW
export const PersonaFindingSchema = z.object({
  persona: PersonaSchema,
  domain: z.string().describe("The specific area of concern (e.g., Thermodynamics, IP Strategy, Supply Chain)"),
  severity: EcuTaxonomySchema,
  finding: z.string().describe("Detailed description of the risk, liability, or baseline observation."),
  mitigation_strategy: z.string().optional().describe("Proposed solution or constraint to enforce to mitigate the finding."),
  historical_reference: z.string().optional().describe("Citation of a past Erik Norris project or GD&T rule that justifies this finding.")
});

// The final ECU Synthesis report compiled by the Principal Architect
export const EcuSynthesisSchema = z.object({
  project_id: z.string(),
  client_name: z.string(),
  baseline_viability: z.boolean().describe("True if the project baseline is viable, False if the core physics/logic fails."),
  overall_risk_grade: EcuTaxonomySchema,
  critical_liabilities: z.array(z.string()).describe("List of exact constraints the client must accept to proceed and decouple liability."),
  persona_findings: z.array(PersonaFindingSchema),
  architect_summary: z.string().describe("Final deterministic recommendation (e.g., 'Proceed with modifications', 'Decline engagement').")
});

export type EcuTaxonomy = z.infer<typeof EcuTaxonomySchema>;
export type Persona = z.infer<typeof PersonaSchema>;
export type PersonaFinding = z.infer<typeof PersonaFindingSchema>;
export type EcuSynthesis = z.infer<typeof EcuSynthesisSchema>;
