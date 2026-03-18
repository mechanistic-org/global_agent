import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
import chromadb

# 1. State Definition (Adding 'messages' for native Tool calling)
class PRDState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "The conversation history"]
    current_agent: str

# 2. Define the Truth Engine Tool
# By wrapping this with @tool, LangChain automatically extracts the Zod schema
# and feeds it to the LLM's system prompt (Llama-3 or DeepSeek).
@tool
def search_truth_engine(query: str, n_results: int = 3) -> str:
    """
    Query the local Grok Vector Vault (Truth Engine) to retrieve Mechanistic rules,
    V31 constraints, and project history. USE THIS to fact-check your work.
    """
    print(f"\n[TOOL EXECUTION] Triggering 'search_truth_engine' for query: '{query}'")
    
    # Connect directly to the H: drive where the Vector DB lives
    db_path = r"H:\Grok_Vector_Vault\Truth_Engine"
    if not os.path.exists(db_path):
        return "ERROR: Vector Vault not found at H:\\Grok_Vector_Vault\\Truth_Engine"
        
    client = chromadb.PersistentClient(path=db_path)
    try:
        collection = client.get_collection(name="truth_engine_core")
        results = collection.query(query_texts=[query], n_results=n_results)
        
        # Format the results into a string for the LLM to read
        formatted_results = ""
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i]
            formatted_results += f"Source ({meta.get('source', 'Unknown')}):\n{doc}\n\n"
            
        return formatted_results if formatted_results else "No relevant documents found."
    except Exception as e:
        return f"Database query failed: {str(e)}"

# A list of tools available to our Swarm
swarm_tools = [search_truth_engine]
tool_node = ToolNode(swarm_tools)

# 3. Define the LLM Model (Mocking the Llama.cpp binding for the scaffold)
# In production, this uses langchain_community.llms.LlamaCpp
class MockLlama3WithTools:
    def bind_tools(self, tools):
        return self
        
    def invoke(self, messages):
        last_message = messages[-1].content
        if "High-mobility cycle" in last_message:
            # The LLM decides it needs to use a tool to check constraints
            print("[LLM: Llama-3-8B] \"I need to check the Truth Engine for 'Az91D magnesium constraints'\"")
            return AIMessage(
                content="",
                tool_calls=[{"name": "search_truth_engine", "args": {"query": "Az91D magnesium thermal constraints"}, "id": "call_123"}]
            )
        else:
            # Tool returned the data, now the LLM writes the final critique
            print("[LLM: Llama-3-8B] \"Based on the Truth Engine, Az91D will melt. Writing rejection notice.\"")
            return AIMessage(content="CRITICAL FAILURE: Vector UI constraints prohibit 400C Az91D.\nAction: Rework Material.")

mock_llm = MockLlama3WithTools()

# 4. Agent Nodes
def principal_architect_node(state: PRDState):
    print(f"\n[NODE: Principal Architect] Evaluating PRD...")
    
    # The LLM reads the messages and either returns a Tool Call or a Final Answer
    response = mock_llm.invoke(state["messages"])
    
    return {"messages": [response], "current_agent": "Principal Architect"}

def should_continue(state: PRDState):
    """Router to determine if the LLM wants to use a Tool or end its turn."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print(f"[ROUTER] -> Routing to Tool Node (Vector DB)")
        return "tools"
    print(f"[ROUTER] -> Task Complete. Routing to END.")
    return END

# 5. Build the Graph
workflow = StateGraph(PRDState)

# Add Nodes
workflow.add_node("PrincipalArchitect", principal_architect_node)
workflow.add_node("tools", tool_node)

# Add Edges
workflow.set_entry_point("PrincipalArchitect")
# Conditional Edge: Either loop to the tool node, or finish
workflow.add_conditional_edges("PrincipalArchitect", should_continue)
# Return from tool node back to the Architect to evaluate the tool output
workflow.add_edge("tools", "PrincipalArchitect")

# Compile
swarm_app = workflow.compile()

if __name__ == "__main__":
    print("==================================================")
    print("  INITIATING LANGGRAPH + TRUTH ENGINE TOOL BINDING")
    print("==================================================")
    
    initial_payload = {
        "messages": [HumanMessage(content="PRD: High-mobility cycle using Az91D magnesium running at 400C continuous.")]
    }
    
    for event in swarm_app.stream(initial_payload):
        pass
        
    print("\n==================================================")
    print("  CASCADE COMPLETE.")
    print("==================================================")
