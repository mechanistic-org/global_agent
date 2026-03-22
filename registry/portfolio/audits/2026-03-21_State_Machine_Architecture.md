# Sovereign OS: State Machine Architecture

**Source:** 90-Minute Walk Transcripts (March 21, 2026)
**Core Concept:** *Stateless Agents, Stateful Swarm.*

The central paradox of local AI engineering is that while model weights are fixed, the Key-Value (KV) cache required for context grows linearly, and compute time grows quadratically. 

To run an autonomous, 8-core agent swarm locally without blowing out RTX VRAM or crashing into hallucination loops, **state must be ruthlessly externalized.** The LLM is purely a reasoning engine; it is not a hard drive.

Here is exactly how the state is "put into the machine."

---

## Pillar 1: The Macro State (GitHub as the Control Plane)
You do not maintain conversation histories. The Sovereign OS relies entirely on GitHub Projects and Issues as its persistent, universal memory layer.

1. **The Trigger Context:** The `mcp_router_node` polls the GitHub Project Board. When a card shifts to "Ready for Swarm", it grabs the Issue.
2. **Aggressive Context Compression:** Raw API payloads are toxic to token limits. The `read_issue_context` tool strips all HTML, drops the noisy middle of the thread, and returns only the Markdown body (the PRD) + the last 3 comments (the final human decisions).
3. **The Lock and Log:** The agent immediately calls `update_project_card_status` (a GraphQL facade) to move the card to "In Progress," locking out other agents. Upon completion or failure, it calls `append_issue_comment` to document its findings.
4. **Eviction:** When the ticket hits "Done" or "Blocked," the agent container is completely destroyed. Zero tokens remain in memory.

## Pillar 2: The Micro State (AST & Delta Payloads)
Agents are forbidden from reading raw source code or massive databases. They operate exclusively through "Data Compressors."

* **Code Manipulation (`patch_astro_component`):** Instead of rewriting a 600-line React file, the agent passes a tiny Zod-validated JSON payload (e.g., `{"partVolume": 45.2}`). A local `ts-morph` AST parser injects that variable directly into the component. The agent never sees the source code; it only sees the schema.
* **Database Updates (`update_dfmea_node`):** Instead of passing entire Risk Matrices into the context window, the agent requests point-updates. If it hallucinates an ID, it is blocked.

## Pillar 3: The Transient State (Smart Error Circuit Breakers)
Without a human driving the chat, an agent hitting an error will panic and enter an infinite loop. The Router Node must act as the unforgiving supervisor by maintaining a localized "Transient State."

1. **The 3-Strike Rule:** The Router Node hashes every tool call payload. If the agent repeats the exact same failed tool configuration 3 times, the Router trips the Circuit Breaker.
2. **Container Teardown:** The NanoClaw sandbox is violently terminated to clear the corrupted KV cache.
3. **Smart Checkpoints:** A fresh container is booted and handed the last known checkpoint along with a "Smart Error." 
4. **Smart Errors:** Errors map the physical state perfectly. If the agent asks for component `<HardwareSpecs />`, the error doesn't just crash; it returns: `"TARGET_NOT_FOUND. Actual State: ['Header', 'ProjectSpecs', 'Footer']"`. The agent learns the reality of the codebase through structured failure.

## Summary Execution Flow
1. **Router Node** wakes up → Reads GitHub Issue (Macro State)
2. **NanoClaw Container** spins up → Agent digests the compressed issue requirement.
3. Agent uses **AST/DB MCP Tools** to manipulate code/data (Micro State).
4. **Circuit Breaker** monitors for hallucination loops and manages container lifecycles (Transient State).
5. Agent updates the GitHub Board, leaves a comment, and **terminates**.
