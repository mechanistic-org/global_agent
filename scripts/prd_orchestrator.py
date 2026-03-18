import os
import asyncio
import gc
import sys

# --- CUDA DLL Injection ---
venv_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".venv", "Lib", "site-packages", "nvidia"))
cuda_rt = os.path.join(venv_base, "cuda_runtime", "bin")
cublas = os.path.join(venv_base, "cublas", "bin")

if os.path.exists(cuda_rt):
    os.add_dll_directory(cuda_rt)
if os.path.exists(cublas):
    os.add_dll_directory(cublas)

os.environ["PATH"] = cuda_rt + os.pathsep + cublas + os.pathsep + os.environ.get("PATH", "")
# --------------------------

from typing import TypedDict, List, Dict, Any, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from llama_cpp import Llama

# Import the massive system prompts
import prd_prompts

# ==========================================
# 0. MODEL CONFIGURATION (The Denzel Armory)
# ==========================================
MODELS_DIR = r"D:\Local_Grok_Engine\models"

# Map exactly to the downloaded GGUF files
MODEL_PATHS = {
    "saul": os.path.join(MODELS_DIR, "Saul-7B-Instruct-v1-Q4_K_M.gguf"),
    "qwen_math": os.path.join(MODELS_DIR, "Qwen2.5-Math-7B-Instruct-Q4_K_M.gguf"),
    "deepseek_r1": os.path.join(MODELS_DIR, "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf"),
    "llama3": os.path.join(MODELS_DIR, "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"),
    "mistral_nemo": os.path.join(MODELS_DIR, "Mistral-Nemo-Instruct-2407.Q4_K_M.gguf"),
    "qwen_coder": os.path.join(MODELS_DIR, "Qwen2.5-Coder-14B-Instruct-Q4_K_M.gguf")
}

def run_inference(model_key: str, system_prompt: str, user_prompt: str, max_tokens: int = 4000, pydantic_schema=None) -> str:
    """
    VRAM-Safe Local Inference.
    Dynamically loads the GGUF model into VRAM, executes the prompt, and forces garbage collection.
    If a Pydantic schema is passed, compiles a JSON Grammar to force strict compliance.
    """
    model_path = MODEL_PATHS.get(model_key)
    if not model_path or not os.path.exists(model_path):
        return f"[ERROR: Model {model_key} not found at {model_path}]"
        
    print(f"\n   [VRAM] Provisioning {model_key} ...")
    llm = Llama(model_path=model_path, n_gpu_layers=-1, n_ctx=32768, verbose=False)
    
    grammar = None
    if pydantic_schema:
        import json
        from llama_cpp.llama_grammar import LlamaGrammar
        schema_json = json.dumps(pydantic_schema.model_json_schema())
        grammar = LlamaGrammar.from_json_schema(schema_json)
        print(f"   [GRAMMAR] Synthesizing strict logic map for {pydantic_schema.__name__} ...")
    
    prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n"
    if model_key == "llama3" or model_key == "deepseek_r1":
        prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
    
    print(f"   [INFERENCE] Executing logic via {model_key} ...")
    if grammar:
        result = llm(prompt, max_tokens=max_tokens, temperature=0.1, stop=["<|im_end|>", "<|eot_id|>"], grammar=grammar)
    else:
        result = llm(prompt, max_tokens=max_tokens, temperature=0.1, stop=["<|im_end|>", "<|eot_id|>"])
        
    output = result['choices'][0]['text'].strip()
    
    print(f"   [VRAM] Unloading {model_key} ...")
    del llm
    gc.collect()
    
    return output

# ==========================================
# 1. DEFINE PIPELINE STATE
# ==========================================
class PRDPipelineState(TypedDict):
    raw_prd_input: str
    node_1_intelligence: Annotated[Dict[str, Any], operator.ior]
    node_2_critiques: Annotated[Dict[str, Any], operator.ior]
    node_3_architecture: Annotated[Dict[str, Any], operator.ior]
    node_4_risk_ops: Annotated[Dict[str, Any], operator.ior]
    node_5_commercial: Annotated[Dict[str, Any], operator.ior]
    node_6_frontend: Annotated[Dict[str, Any], operator.ior]

# ==========================================
# 2. DEFINE PIPELINE NODES
# ==========================================

async def node_1_research_discovery(state: PRDPipelineState):
    print("\n>>> [NODE 1] Research & Discovery")
    # Using Llama3 for basic text processing to simulate research
    finding = run_inference("llama3", prd_prompts.NODE_1_RESEARCHER, state["raw_prd_input"])
    return {"node_1_intelligence": {"dossier_json": finding}}

async def node_2_pre_mortem_red_team(state: PRDPipelineState):
    print("\n>>> [NODE 2] Pre-Mortem Red Team (Fan-Out requirement implementation)")
    prd = state["raw_prd_input"]
    dossier = state.get("node_1_intelligence", {}).get("dossier_json", "")
    
    context = f"Original PRD:\n{prd}\n\nNode 1 Research Dossier:\n{dossier}"
    
    # 1. The Physicist (Qwen-Math)
    phys_output = run_inference("qwen_math", prd_prompts.NODE_2_PHYSICIST, context)
    
    # 2. The Mechanical Engineer (DeepSeek-R1)
    me_output = run_inference("deepseek_r1", prd_prompts.NODE_2_ME, context)
    
    # 3. Risk & Compliance (Llama-3)
    risk_output = run_inference("llama3", prd_prompts.NODE_2_COMPLIANCE, context)
    
    res = {
        "physicist": phys_output,
        "mechanical": me_output,
        "compliance": risk_output
    }
    return {"node_2_critiques": res}

async def node_3_architecture_decomposition(state: PRDPipelineState):
    print("\n>>> [NODE 3] Architecture Breakdown")
    prd = state["raw_prd_input"]
    critiques = str(state.get("node_2_critiques", {}))
    
    context = f"Original PRD:\n{prd}\n\nNode 2 Validated Constraints:\n{critiques}"
    
    # 1. Systems Architect (Qwen-Coder)
    arch_output = run_inference("qwen_coder", prd_prompts.NODE_3_ARCHITECT, context)
    
    # 2. Test & Validation (DeepSeek-R1)
    test_output = run_inference("deepseek_r1", prd_prompts.NODE_3_TESTING, context)
    
    # 3. Human Factors (Llama-3)
    hf_output = run_inference("llama3", prd_prompts.NODE_3_HUMAN, context)
    
    res = {"architect": arch_output, "testing": test_output, "human_factors": hf_output}
    return {"node_3_architecture": res}

async def node_4_risk_operations(state: PRDPipelineState):
    print("\n>>> [NODE 4] Risk & Operations Cell")
    prd = state["raw_prd_input"]
    arch = str(state.get("node_3_architecture", {}))
    
    import dfmea_schemas
    
    context = f"Original PRD:\n{prd}\n\nNode 3 Architecture:\n{arch}"
    
    # 1. Reliability Engineer (DeepSeek-R1) with Crucible Evaluator Loop
    rel_output = ""
    for attempt in range(1, 4):
        print(f"\n   [CRUCIBLE] Generating DFMEA (Attempt {attempt}/3)")
        rel_output = run_inference("deepseek_r1", prd_prompts.NODE_4_RELIABILITY, context, pydantic_schema=dfmea_schemas.PhysicsVault)
        
        print("\n   [CRUCIBLE] Evaluating physics constraints with Cheerful Mentor (Llama-3)...")
        eval_context = f"Attempt {attempt} DFMEA Payload:\n{rel_output}"
        eval_output = run_inference("llama3", prd_prompts.EVALUATOR_PROMPT, eval_context, pydantic_schema=dfmea_schemas.CrucibleEvaluation)
        
        try:
            import json
            eval_data = json.loads(eval_output)
            if eval_data.get("passed"):
                print("   [CRUCIBLE] >> PASSED << DFMEA met forensic V31 threshold.")
                break
            else:
                critique = eval_data.get("critique", "Generic failure.")
                print(f"   [CRUCIBLE] >> FAILED << Critique: {critique}")
                if attempt < 3:
                    context += f"\n\n[CRUCIBLE REJECTION - You must rewrite your FMEA matrix addressing this critique]:\n{critique}"
        except Exception as e:
            print(f"   [CRUCIBLE] Error parsing evaluation json: {e}")
            break
            
    # 2. Supply Chain (Llama-3)
    sc_output = run_inference("llama3", prd_prompts.NODE_4_SUPPLY_CHAIN, context)
    
    # 3. IP Strategist (Mistral-Nemo)
    ip_output = run_inference("mistral_nemo", prd_prompts.NODE_4_IP, context)
    
    res = {"reliability": rel_output, "supply_chain": sc_output, "ip_strategy": ip_output}
    return {"node_4_risk_ops": res}

async def node_5_commercial_legal(state: PRDPipelineState):
    print("\n>>> [NODE 5] Commercial & Legal Cell")
    prd = state["raw_prd_input"]
    risk = str(state.get("node_4_risk_ops", {}))
    
    import dfmea_schemas
    
    context = f"Original PRD:\n{prd}\n\nNode 4 Risk Profile:\n{risk}"
    
    # 1. Legal Counsel (Saul-7B) explicitly bound to LegalVault schema
    leg_output = run_inference("saul", prd_prompts.NODE_5_LEGAL, context, pydantic_schema=dfmea_schemas.LegalVault)
    
    # 2. Pricing Actuary (Qwen-Math) explicitly bound to FinanceVault schema
    act_output = run_inference("qwen_math", prd_prompts.NODE_5_ACTUARY, context, pydantic_schema=dfmea_schemas.FinanceVault)
    
    # 3. Proposal Strategist (Mistral-Nemo)
    prop_output = run_inference("mistral_nemo", prd_prompts.NODE_5_PROPOSAL, context)
    
    res = {"legal": leg_output, "pricing": act_output, "proposal": prop_output}
    return {"node_5_commercial": res}

async def node_6_comms_frontend(state: PRDPipelineState):
    print("\n>>> [NODE 6] Communications & Frontend Cell")
    
    # Pass all accumulated data
    data_payload = f"Architecture:\n{state.get('node_3_architecture', {})}\n\nRisk:\n{state.get('node_4_risk_ops', {})}\n\nCommercial:\n{state.get('node_5_commercial', {})}"
    
    # 1. Tech Writer (Llama-3)
    tw_output = run_inference("llama3", prd_prompts.NODE_6_WRITER, data_payload)
    
    # 2. UI Developer (Qwen-Coder)
    ui_output = run_inference("qwen_coder", prd_prompts.NODE_6_UI, data_payload)
    
    # 3. Data Viz (Qwen-Coder)
    viz_output = run_inference("qwen_coder", prd_prompts.NODE_6_VIZ, data_payload)
    
    res = {"tech_writing": tw_output, "ui_dev": ui_output, "data_viz": viz_output}
    return {"node_6_frontend": res}

# ==========================================
# 3. BUILD THE LANGGRAPH
# ==========================================

def build_prd_pipeline():
    """Compiles the StateGraph for the PRD Pipeline."""
    builder = StateGraph(PRDPipelineState)
    
    # Register Nodes
    builder.add_node("node_1", node_1_research_discovery)
    builder.add_node("node_2", node_2_pre_mortem_red_team)
    builder.add_node("node_3", node_3_architecture_decomposition)
    builder.add_node("node_4", node_4_risk_operations)
    builder.add_node("node_5", node_5_commercial_legal)
    builder.add_node("node_6", node_6_comms_frontend)
    
    # Build Edges (Linear sequential flow, with inner parallel execution defined inside nodes)
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2", "node_3")
    builder.add_edge("node_3", "node_4")
    builder.add_edge("node_4", "node_5")
    builder.add_edge("node_5", "node_6")
    builder.add_edge("node_6", END)
    
    graph = builder.compile()
    return graph

# ==========================================
# 4. EXECUTE SCRIPT
# ==========================================
def read_prd_file(filepath: str) -> str:
    """Utility to read the PRD content into memory."""
    try:
        if filepath.lower().endswith(".pdf"):
            import pypdf
            with open(filepath, 'rb') as file:
                reader = pypdf.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        else:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
    except Exception as e:
        print(f"[ERROR] Reading PRD file failed. Generating mock PRD. Error: {e}")
        return "Client requests a high-mobility bicycle utility vehicle capable of hauling 500lbs over uneven terrain."

if __name__ == "__main__":
    
    async def run_pipeline():
        graph = build_prd_pipeline()
        print("\n==================================================")
        print("  INITIATING LOCAL PRD PIPELINE (DENZEL ARMORY)")
        print("==================================================")
        
        # Note: We can load the physical PRD here. Using a mocked file path for robustness, falling back to string if missing.
        actual_prd_path = r"D:\projects\mobile_outfitters\Holy Grail PRD-2.pdf"
        prd_content = read_prd_file(actual_prd_path)
        
        initial_state = {
            "raw_prd_input": prd_content,
            "node_1_intelligence": {},
            "node_2_critiques": {},
            "node_3_architecture": {},
            "node_4_risk_ops": {},
            "node_5_commercial": {},
            "node_6_frontend": {}
        }
        
        # Stream the graph execution
        async for output in graph.astream(initial_state):
            for node_name, state_update in output.items():
                print(f"[{node_name}] Completed Output Injection.")
        
        # Save the final state to disk for review
        import json
        with open("pipeline_output.json", "w", encoding='utf-8') as f:
            # Note: We need to print safely for any weird json artifacts
            safe_output = str(output)
            f.write(safe_output)
            
        print("\n==================================================")
        print("  PRD PIPELINE COMPLETED")
        print("==================================================")
        
    asyncio.run(run_pipeline())
