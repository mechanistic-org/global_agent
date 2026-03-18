import { z } from "zod";

// ---------------------------------------------------------------------------
// THE MODEL CONTEXT PROTOCOL (MCP) TOOL CAGE
// ---------------------------------------------------------------------------
// These schemas mathematically enforce the data shape for MCP communication.
// The local Llama engine will act as the Client, calling these tools 
// from your local MCP Servers (File System, GitHub, Vector DB).

// 1. General JSON RPC 2.0 Base Schemas
export const McpRequestSchema = z.object({
  jsonrpc: z.literal("2.0"),
  id: z.union([z.string(), z.number()]),
  method: z.string(),
  params: z.record(z.any()).optional(),
});

export const McpResponseSchema = z.object({
  jsonrpc: z.literal("2.0"),
  id: z.union([z.string(), z.number()]),
  result: z.any().optional(),
  error: z.object({
    code: z.number(),
    message: z.string(),
    data: z.any().optional(),
  }).optional(),
}).refine(data => data.result !== undefined || data.error !== undefined, {
  message: "Response must contain either 'result' or 'error'",
});

// ---------------------------------------------------------------------------
// 2. Specific Tool: Read Inbox File (Filesystem MCP)
// ---------------------------------------------------------------------------
export const McpReadInboxFileParamsSchema = z.object({
  filename: z.string().describe("The name of the file to read from the _inbox directory. E.g., 'holy_grail_raw.txt'"),
});

export const McpReadInboxFileResultSchema = z.object({
  content: z.string().describe("The raw text content of the file."),
  metadata: z.record(z.string()).optional(),
});

// ---------------------------------------------------------------------------
// 3. Specific Tool: Search Grok Vector DB (RAG MCP)
// ---------------------------------------------------------------------------
export const McpSearchVectorDbParamsSchema = z.object({
  query: z.string().describe("The natural language or keyword query to search your history (e.g., 'AZ91D magnesium constraints')."),
  top_k: z.number().int().min(1).max(20).default(5).describe("Number of relevant historic chunks to return."),
  domain_filter: z.array(z.string()).optional().describe("Optional filters (e.g., ['GD&T', 'Material Science', 'Avegant'])."),
});

export const McpSearchVectorDbResultSchema = z.object({
  results: z.array(z.object({
    content: z.string().describe("The relevant historic text chunk."),
    source_document: z.string().describe("The origin file, e.g., '2016_avegant_thermal_study.md'"),
    similarity_score: z.number().describe("Vector distance score for relevance."),
  }))
});

// ---------------------------------------------------------------------------
// 4. Specific Tool: Draft SOW Proposal (Operational Action)
// ---------------------------------------------------------------------------
export const McpDraftSowParamsSchema = z.object({
  client_name: z.string(),
  liability_decoupled: z.boolean().describe("Must be true to ensure Erik is not liable for client design flaws."),
  sow_content: z.string().describe("The markdown draft of the SOW."),
});

// Type Exports
export type McpRequest = z.infer<typeof McpRequestSchema>;
export type McpResponse = z.infer<typeof McpResponseSchema>;
export type McpSearchVectorDbParams = z.infer<typeof McpSearchVectorDbParamsSchema>;
export type McpReadInboxFileParams = z.infer<typeof McpReadInboxFileParamsSchema>;
