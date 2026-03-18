from typing import TypedDict
from langgraph.graph import StateGraph, END

# 1. State Definition (The "Memory" that passes through the swarm)
class PRDState(TypedDict):
    raw_document: str
    physicist_critique: str
    architect_zod_schema: str
    current_agent: str

# 2. Node Definitions (The Agent Cards)
def physicist_node(state: PRDState):
    print(f"\n[AGENT: Physicist] Waking up. Provisioning DeepSeek-R1-14B into VRAM...")
    print(f"[AGENT: Physicist] Querying Truth Engine MCP for math constraints...")
    
    # In live-fire, this queries localhost:8080 (where DeepSeek is loaded)
    critique = "Physics Violation Detected: Az91D cannot sustain 400C without active cooling."
    
    print(f"[AGENT: Physicist] Analysis complete. Unloading DeepSeek from VRAM.")
    return {"physicist_critique": critique, "current_agent": "Physicist"}

def architect_node(state: PRDState):
    print(f"\n[AGENT: Principal Architect] Waking up. Provisioning Llama-3-8B into VRAM...")
    print(f"[AGENT: Principal Architect] Synthesizing Physicist critique into strict Zod format...")
    
    # In live-fire, this queries localhost:8080 (where Llama-3 is loaded)
    schema = '{\n  "status": "CRITICAL",\n  "failure_mode": "Thermal Degradation (Az91D)"\n}'
    
    print(f"[AGENT: Principal Architect] Synthesis complete. Unloading Llama-3 from VRAM.")
    return {"architect_zod_schema": schema, "current_agent": "Principal Architect"}

# 3. Defining the Graph (The Architecture)
workflow = StateGraph(PRDState)

# Add our personas to the graph
workflow.add_node("Physicist", physicist_node)
workflow.add_node("PrincipalArchitect", architect_node)

# Define the logical flow (The Edges)
# _inbox -> Physicist -> Architect -> Output
workflow.set_entry_point("Physicist")
workflow.add_edge("Physicist", "PrincipalArchitect")
workflow.add_edge("PrincipalArchitect", END)

# Compile into an executable application
swarm_app = workflow.compile()

if __name__ == "__main__":
    print("==================================================")
    print("  INITIATING LANGGRAPH SWARM CASCADE (DRY RUN)")
    print("==================================================")
    
    # Simulate a raw file dropping into the _inbox
    initial_payload = {
        "raw_document": "PRD: High-mobility cycle using Az91D magnesium running at 400C continuous."
    }
    
    # Execute the Swarm
    for event in swarm_app.stream(initial_payload):
        # LangGraph automatically handles the state passing
        pass
        
    print("\n==================================================")
    print("  CASCADE COMPLETE. OUTPUT GENERATED.")
    print("==================================================")
