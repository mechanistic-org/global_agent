import os
import sys
import gc
import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
import fitz  # PyMuPDF
from llama_cpp import Llama

# Configure dynamic paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from global_config import LLAMA_MODEL_PATH, GLOBAL_AGENT_ROOT, PORTFOLIO_ROOT

LLAMA_3_PATH = str(LLAMA_MODEL_PATH)

# 1. State Definition
class PRDState(TypedDict):
    raw_document: str
    physicist_critique: str
    architect_zod_schema: str

# 2. Extract Text from PDF
def extract_pdf_text(pdf_path: str) -> str:
    print(f"\n[SYSTEM] Ingesting PRD PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 3. Agent Nodes (with explicit VRAM provision / deprovision)
def physicist_node(state: PRDState):
    print("\n---------------------------------------------------------")
    print("[AGENT: Physicist] Waking up.")
    print(f"[AGENT: Physicist] Provisioning {os.path.basename(LLAMA_3_PATH)} into VRAM...")
    
    # Load model into VRAM
    llm = Llama(model_path=LLAMA_3_PATH, n_gpu_layers=-1, n_ctx=4096, verbose=False)
    
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are the Virtual Physicist. You find mechanical, logical, and physical flaws in Product Requirements Documents. Be highly critical, concise, and direct.<|eot_id|><|start_header_id|>user<|end_header_id|>
Analyze this PRD excerpt and output ONLY your core critique of physical/engineering viability. Do not be polite.
PRD: {state['raw_document'][:3000]}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

    print("[AGENT: Physicist] Running inference on PRD constraints...")
    result = llm(prompt, max_tokens=600, temperature=0.1, stop=["<|eot_id|>"])
    critique = result['choices'][0]['text'].strip()
    
    print(f"\n[PHYSICIST OUTPUT]:\n{critique}")
    
    # Free VRAM explicitly
    print("\n[AGENT: Physicist] Analysis complete. Unloading model from memory...")
    del llm
    gc.collect() 
    
    return {"physicist_critique": critique}

def architect_node(state: PRDState):
    print("\n---------------------------------------------------------")
    print("[AGENT: Principal Architect] Waking up.")
    print(f"[AGENT: Principal Architect] Provisioning {os.path.basename(LLAMA_3_PATH)} into VRAM...")
    
    # Load model into VRAM
    llm = Llama(model_path=LLAMA_3_PATH, n_gpu_layers=-1, n_ctx=4096, verbose=False)
    
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are the Principal Architect. You map raw technical critiques into a strict Zod-compliant JSON schema. Do not output anything but JSON object.<|eot_id|><|start_header_id|>user<|end_header_id|>
Convert this critique into a valid JSON object with keys "status" (CRITICAL, MODERATE, PASS), "failure_mode" (string summary), and "rationale" (string).
Critique: {state['physicist_critique']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

    print("[AGENT: Principal Architect] Synthesizing into strict Zod JSON...")
    result = llm(prompt, max_tokens=500, temperature=0.1, stop=["<|eot_id|>"])
    schema = result['choices'][0]['text'].strip()
    
    # Strip markdown if present
    if schema.startswith("```json"):
        schema = schema[7:-3].strip()
    elif schema.startswith("```"):
        schema = schema[3:-3].strip()
        
    print(f"\n[ARCHITECT OUTPUT]:\n{schema}")
    
    # Free VRAM explicitly
    print("\n[AGENT: Principal Architect] Synthesis complete. Unloading model from memory...")
    del llm
    gc.collect()
    
    return {"architect_zod_schema": schema}

def build_and_run_swarm(pdf_path: str):
    if not os.path.exists(pdf_path):
        print(f"ERROR: Cannot find PRD at {pdf_path}")
        return

    # Extract Text
    raw_text = extract_pdf_text(pdf_path)
    
    # 4. Build LangGraph
    print("\n[SYSTEM] Compiling LangGraph State Machine...")
    workflow = StateGraph(PRDState)
    
    workflow.add_node("Physicist", physicist_node)
    workflow.add_node("PrincipalArchitect", architect_node)
    
    workflow.set_entry_point("Physicist")
    workflow.add_edge("Physicist", "PrincipalArchitect")
    workflow.add_edge("PrincipalArchitect", END)
    
    app = workflow.compile()
    
    # 5. Execute Swarm
    print("==================================================")
    print("  INITIATING LIVE-FIRE SWARM CASCADE")
    print("==================================================")
    
    initial_payload = {"raw_document": raw_text}
    
    for event in app.stream(initial_payload):
        pass

    print("\n==================================================")
    print("  CASCADE COMPLETE. LOCAL GROK ENGINE VALIDATED.")
    print("==================================================")

def get_swarm_payload(swarm_id: str = "mobile_outfitters"):
    matrix_path = GLOBAL_AGENT_ROOT / "swarms" / "payload_matrix.json"
    if not matrix_path.exists():
        raise FileNotFoundError(f"Missing payload matrix at {matrix_path}")
    
    with open(matrix_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    payload = data.get(swarm_id, data.get("default_swarm"))
    # Assume prd_target is relative to the PORTFOLIO_ROOT/.. or just absolute
    # The user stored it originally in D:\projects\... so we'll fallback to resolving from D:/ if PORTFOLIO_ROOT is D:/portfolio
    target_rel = payload["prd_target"]
    
    # Heuristic for resolving if PORTFOLIO_ROOT is D:/portfolio
    target_prd = PORTFOLIO_ROOT / ".." / target_rel if PORTFOLIO_ROOT.name == "portfolio" else PORTFOLIO_ROOT / target_rel
    
    # If the file doesn't exist, try just GITHUB_ROOT.parent / target_rel
    if not target_prd.exists() and (PORTFOLIO_ROOT.parent / target_rel).exists():
        target_prd = PORTFOLIO_ROOT.parent / target_rel
        
    return str(target_prd.resolve())

if __name__ == "__main__":
    target_prd = get_swarm_payload("mobile_outfitters")
    build_and_run_swarm(target_prd)
