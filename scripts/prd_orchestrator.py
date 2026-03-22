import os
import asyncio
import sys
import requests
import json
from typing import TypedDict, Dict, Any, Annotated
import operator
from langgraph.graph import StateGraph, START, END

# ==========================================
# 0. MODEL CONFIGURATION (Ollama Daemon)
# ==========================================
def run_inference(model_key: str, system_prompt: str, user_prompt: str, max_tokens: int = 4000) -> str:
    """
    Persistent VRAM Local Inference (Ollama).
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_key,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": max_tokens}
    }
    
    print(f"   [INFERENCE] Native Ollama REST ({model_key}) ...")
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"   [ERROR] Ollama connection failed: {e}")
        return "{}"

# ==========================================
# 1. STATELESS PIPELINE CONFIGURATION
# ==========================================
class StatelessGraphState(TypedDict):
    issue_id: int
    repo: str
    current_objective: str
    checkpoint_data: Annotated[Dict[str, Any], operator.ior]

# ==========================================
# 2. NANOCLAW EPHEMERAL SANDBOX (Simulated)
# ==========================================
async def invoke_sandbox_worker(agent_type: str, slm_model: str, objective: str, checkpoint: dict) -> dict:
    """
    Mimics booting a NanoClaw container, injecting the SLM, executing, and tearing down.
    The VRAM context window only survives for the duration of this function.
    """
    print(f"\n>>> [NANOCLAW SANDBOX] Spawning ephemeral container for [{agent_type}]")
    print(f"   [MEMORY] Container booting with Model: {slm_model}")
    
    # The prompt comes natively from the bounded container context, not an endless rolling string
    system_prompt = f"You are a sandboxed {agent_type} worker. Execute the objective strictly. Return a highly compressed JSON summary."
    user_prompt = f"OBJECTIVE: {objective}\nCHECKPOINT: {json.dumps(checkpoint)}"
    
    # The agent does its work 
    result = run_inference(slm_model, system_prompt, user_prompt, max_tokens=150)
    
    print(f"   [NANOCLAW SANDBOX] Tearing down container... VRAM flushed.")
    
    # Return a tiny tracked payload. Never the massive rolling context.
    summary_payload = {
        f"{agent_type}_status": "complete",
        "mock_tokens_used": 245,
        "action_summary": result[:100] + "..." # Physically truncate to prevent bloat
    }
    return summary_payload

# ==========================================
# 3. DISCRETE ROUTER NODES
# ==========================================
async def hardware_delta_node(state: StatelessGraphState):
    """Specialized Spoke: Hardware CAD Extractor"""
    objective = state.get("current_objective", "Analyze CAD delta.")
    result = await invoke_sandbox_worker("Hardware_Engineer", "deepseek-r1:8b", objective, state.get("checkpoint_data", {}))
    
    # Log the memory safety parameter
    state_size = sys.getsizeof(str(state))
    print(f"   [STATE METRICS] Graph State Context Size: {state_size} bytes")
    
    return {"checkpoint_data": result}

async def pcb_routing_node(state: StatelessGraphState):
    """Specialized Spoke: PCB Layout"""
    objective = "Route the schematic for the new encoder footprint based on the Hardware checkpoint."
    result = await invoke_sandbox_worker("PCB_Designer", "qwen2.5-coder:7b", objective, state.get("checkpoint_data", {}))
    
    state_size = sys.getsizeof(str(state))
    print(f"   [STATE METRICS] Graph State Context Size: {state_size} bytes")
    return {"checkpoint_data": result}

async def dfmea_update_node(state: StatelessGraphState):
    """Specialized Spoke: Database Mutator"""
    objective = "Use GraphQL facet tool to update Failure Mode records based on the PCB diffs."
    result = await invoke_sandbox_worker("QA_Reliability", "mistral-nemo", objective, state.get("checkpoint_data", {}))
    
    state_size = sys.getsizeof(str(state))
    print(f"   [STATE METRICS] Graph State Context Size: {state_size} bytes")
    return {"checkpoint_data": result}

# ==========================================
# 4. BUILD THE STATELESS GRAPH
# ==========================================
def build_stateless_pipeline():
    builder = StateGraph(StatelessGraphState)
    
    builder.add_node("hardware_delta", hardware_delta_node)
    builder.add_node("pcb_routing", pcb_routing_node)
    builder.add_node("dfmea_update", dfmea_update_node)
    
    # The routing logic goes strictly sequential for the mock, representing 
    # the Router Node dispatching sequential tasks from a single GitHub Issue
    builder.add_edge(START, "hardware_delta")
    builder.add_edge("hardware_delta", "pcb_routing")
    builder.add_edge("pcb_routing", "dfmea_update")
    builder.add_edge("dfmea_update", END)
    
    return builder.compile()

if __name__ == "__main__":
    async def run_pipeline():
        graph = build_stateless_pipeline()
        print("\n==================================================")
        print("  INITIATING STATELESS ROUTING PIPELINE (HYBRID)")
        print("==================================================")
        
        # The massive PRD has been entirely eradicated. The state is microscopic.
        initial_state = {
            "issue_id": 104,
            "repo": "c24-console",
            "current_objective": "Process GitHub Issue #104: Encoder Footprint Overhaul",
            "checkpoint_data": {}
        }
        
        async for output in graph.astream(initial_state):
            for node_name, state_update in output.items():
                print(f"[{node_name}] Checkpoint saved. Transitioning router.")
        
        print("\n==================================================")
        print("  STATELESS PIPELINE COMPLETED")
        print("==================================================")
        
    asyncio.run(run_pipeline())
