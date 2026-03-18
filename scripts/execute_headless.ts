const { GoogleGenAI } = require("@google/genai");
const Anthropic = require("@anthropic-ai/sdk");
const fs = require("fs");
const path = require("path");

// Native MCP Integration scaffolding
// require("@modelcontextprotocol/sdk/client/index.js")
const { Client } = require("@modelcontextprotocol/sdk/client/index.js");
const { StdioClientTransport } = require("@modelcontextprotocol/sdk/client/stdio.js");

// Load global config (handles .env hydration dynamically)
require("./global_config");

// Execute Headless Swarm
async function executeHeadlessAction() {
  const args = process.argv.slice(2);
  const promptFile = args[0] || "prompt.txt";
  const logFile = path.resolve(__dirname, "output.log");

  if (!fs.existsSync(promptFile)) {
    console.error(`[!] Fatal: Prompt file not found at ${promptFile}`);
    process.exit(1);
  }

  const promptContent = fs.readFileSync(promptFile, "utf-8");
  
  // -- 1. Configure Hardcoded MCP Transports --
  // Hardcoding ensures the cron job never crashes due to flaky external wrapper resolution
  
  const githubTransport = new StdioClientTransport({
      command: "npx",
      args: ["-y", "@modelcontextprotocol/server-github"],
      env: {
          ...process.env,
          GITHUB_PERSONAL_ACCESS_TOKEN: process.env.GITHUB_PERSONAL_ACCESS_TOKEN || process.env.GITHUB_FALLBACK_TOKEN
      }
  });

  const notionTransport = new StdioClientTransport({
      command: "npx",
      args: ["-y", "@notionhq/notion-mcp-server"],
      env: {
          ...process.env,
          // The Notion server natively expects this exact variable pattern
          OPENAPI_MCP_HEADERS: process.env.NOTION_FALLBACK_HEADER
      }
  });

  // Extract API key from local/master environment configuration
  let extractedKey = process.env.GEMINI_API_KEY || "";

  if (!extractedKey) {
      console.error("[FATAL] Required GEMINI_API_KEY missing.");
      process.exit(1);
  }
  
  const anthropicApiKey = process.env.ANTHROPIC_API_KEY || "";
  if (promptContent.includes("[WORKER]") && !anthropicApiKey) {
      console.error("[FATAL] Required ANTHROPIC_API_KEY missing for Worker/Coding routing. Please add it to .env.swarm or export it.");
      process.exit(1);
  }

  const ai = new GoogleGenAI({ apiKey: extractedKey, httpOptions: { baseUrl: "https://generativelanguage.googleapis.com" } });
  
  console.log(`[+] Initializing Headless Gemini CLI execution...`);
  console.log(`[+] Instruction: ${promptContent}`);

  try {
      // Initialize MCP Clients
      console.log(`[+] Connecting hardcoded MCP Clients...`);
      const githubClient = new Client({ name: "headless-github-client", version: "1.0.0" }, { capabilities: {} });
      const notionClient = new Client({ name: "headless-notion-client", version: "1.0.0" }, { capabilities: {} });

      await githubClient.connect(githubTransport);
      console.log(`[+] GitHub MCP Connected!`);
      
      await notionClient.connect(notionTransport);
      console.log(`[+] Notion MCP Connected!`);

      // Extract tools just to prove they are loaded
      const ghTools = await githubClient.listTools();
      console.log(`[+] Found ${ghTools.tools?.length} GitHub tools.`);
      
      const nocTools = await notionClient.listTools();
      console.log(`[+] Found ${nocTools.tools?.length} Notion tools.`);
      
      const isWorkerTask = promptContent.includes("[WORKER]") || promptContent.includes("[CODING]");
      
      let resultText = "";
      
      if (isWorkerTask) {
          console.log(`[+] Task routed to WORKER tier (Claude 3.7 Sonnet)...`);
          const anthropic = new Anthropic({ apiKey: anthropicApiKey });
          
          // Map MCP tools to Anthropic tool schema
          const allMcpTools = [...(ghTools.tools || []), ...(nocTools.tools || [])];
          const anthropicTools = allMcpTools.map(t => ({
              name: t.name,
              description: t.description,
              input_schema: t.inputSchema
          }));

          const response = await anthropic.messages.create({
              model: "claude-3-7-sonnet-20250219",
              max_tokens: 4096,
              system: "You are the Worker Subagent. You have access to GitHub and Notion via MCP tools.",
              messages: [{ role: "user", content: promptContent }],
              tools: anthropicTools.length > 0 ? anthropicTools : undefined
          });
          
          resultText = response.content[0].text || "No response generated.";
      } else {
          console.log(`[+] Task routed to ORCHESTRATOR tier (Gemini 2.5 Pro)...`);
          const response = await ai.models.generateContent({
              model: "gemini-2.5-pro",
              contents: [{ role: "user", parts: [{ text: promptContent }] }],
              config: {
                  systemInstruction: "You are the Headless Chief of Staff running an asynchronous cron job. Return structural execution logs.",
                  temperature: 0.1
              }
          });
          resultText = response.text || "No response generated.";
      }
      
      const logEntry = `\n--- RUN AT ${new Date().toISOString()} ---\nPROMPT:\n${promptContent}\n\nROUTER: ${isWorkerTask ? 'Claude-3.5-Sonnet (Worker)' : 'Gemini-2.5-Pro (Chief of Staff)'}\n\nOUTPUT:\n${resultText}\n`;
      fs.appendFileSync(logFile, logEntry);
      
      console.log(`[+] Headless run completed successfully. Log updated.`);
      
  } catch (error) {
      console.error(`[-] Fatal Error during execution:`, error);
      process.exit(1);
  }
}

executeHeadlessAction();

// Export to make this file an isolated module, fixing TypeScript redeclaration lints
export {};
