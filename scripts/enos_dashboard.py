import streamlit as st
import pandas as pd
import json
import subprocess
import os
from pathlib import Path
import datetime
import chromadb

# Paths
ROOT_DIR = Path(__file__).parent.parent
LOGS_DIR = ROOT_DIR / ".system_generated" / "logs"
TOKEN_LEDGER_PATH = LOGS_DIR / "token_ledger.json"
FAILSAFES_PATH = LOGS_DIR / "failsafes.log"
BOARD_PATH = ROOT_DIR / "board.json"
CHROMA_PATH = ROOT_DIR / "registry" / ".chroma_db"

st.set_page_config(page_title="EN-OS Dashboard", layout="wide", page_icon="🎛️")

st.title("EN-OS Supervisory Dashboard")
st.markdown("Actuarial-grade Single Pane of Glass observability.")

col1, col2 = st.columns(2)

def run_cmd(cmd_list):
    try:
        if cmd_list[0].lower() == 'powershell':
            result = subprocess.run(cmd_list, capture_output=True, text=True, check=True)
            return result.stdout
        else:
            cmd_str = " ".join(cmd_list)
            if os.name == 'nt' and cmd_list[0] == 'pm2':
                cmd_str = "pm2.cmd " + " ".join(cmd_list[1:])
            
            result = subprocess.run(cmd_str, capture_output=True, text=True, check=True, shell=True)
            return result.stdout
    except Exception as e:
        return f"Error: {e}"

# ==== QUADRANT 1: INFRASTRUCTURE ====
with col1:
    st.header("1. Infrastructure & Connectivity")
    
    st.subheader("Local Routing (PM2)")
    pm2_out = run_cmd(["pm2", "jlist"])
    try:
        if "Error:" not in pm2_out:
            pm2_data = json.loads(pm2_out)
            if pm2_data:
                df_pm2 = []
                for p in pm2_data:
                    df_pm2.append({
                        "Name": p.get("name"),
                        "Status": p.get("pm2_env", {}).get("status"),
                        "Memory (MB)": round(p.get("monit", {}).get("memory", 0) / 1024 / 1024, 2)
                    })
                st.dataframe(pd.DataFrame(df_pm2), hide_index=True)
            else:
                st.info("No PM2 processes running.")
        else:
            st.error("Failed to query PM2.")
    except Exception:
        st.error("Could not parse PM2 jlist output.")
            
    st.subheader("Ingress (Cloudflared)")
    cf_out = run_cmd(["powershell", "-Command", "Get-Service cloudflared | Select-Object Status, Name, DisplayName | ConvertTo-Json"])
    try:
        if "Error:" not in cf_out:
            cf_data = json.loads(cf_out)
            status_code = cf_data.get("Status") if isinstance(cf_data, dict) else (cf_data[0].get("Status") if isinstance(cf_data, list) else 0)
            status_text = "Running (4)" if status_code == 4 else f"Status Code: {status_code}"
            st.metric("cloudflared tunnel", status_text)
        else:
            st.error("Cloudflared service status not found in services.")
    except Exception:
        st.error("Could not parse cloudflared service status.")

# ==== QUADRANT 2: FINANCIAL ====
with col2:
    st.header("2. Financial Constraints")
    
    MAX_DAILY_BUDGET_USD = 5.00
    st.subheader("Token Ledger Burn (Daily)")
    
    if TOKEN_LEDGER_PATH.exists():
        try:
            with open(TOKEN_LEDGER_PATH, 'r') as f:
                ledger = json.load(f)
                
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            today_data = ledger.get(today, {})
            
            total_cost = sum(m.get("cost_usd", 0.0) for m in today_data.values())
            
            st.metric("Today's Spend", f"${total_cost:.4f}", f"${MAX_DAILY_BUDGET_USD - total_cost:.4f} remaining", delta_color="inverse")
            st.progress(min(total_cost / MAX_DAILY_BUDGET_USD, 1.0))
            
            if today_data:
                chart_data = []
                for mod, ops in today_data.items():
                    chart_data.append({"Model": mod, "Cost": ops.get("cost_usd", 0.0)})
                if chart_data:
                    st.bar_chart(pd.DataFrame(chart_data).set_index("Model"))
            else:
                st.info("No token operations recorded today.")
        except Exception as e:
            st.error(f"Error parsing ledger: {e}")
    else:
        st.warning("No token_ledger.json found.")

st.divider()

col3, col4 = st.columns(2)

# ==== QUADRANT 3: SAFETY & BREAKERS ====
with col3:
    st.header("3. Safety & Circuit Breakers")
    
    global_status = "IDLE"
    unacknowledged_halts = []
    
    if FAILSAFES_PATH.exists():
        try:
            with open(FAILSAFES_PATH, 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                if "HALT" in line:
                    unacknowledged_halts.append(line.strip())
                elif "[ACKNOWLEDGED]" in line:
                    unacknowledged_halts = []  # Clear slate up to this point
                    
            if unacknowledged_halts:
                global_status = "HALTED"
        except Exception as e:
            st.error(f"Error reading failsafes: {e}")
            
    if global_status == "HALTED":
        st.error(f"🚨 SYSTEM HALTED! 🚨")
        for halt in unacknowledged_halts:
            st.write(f"`{halt}`")
            
        st.warning("Action required. Review the logs above to understand the halt constraints.")
        
        if st.button("Acknowledge & Clear Halts"):
            with open(FAILSAFES_PATH, 'a') as f:
                f.write(f"[{datetime.datetime.now().isoformat()}] [ACKNOWLEDGED] All halts cleared by Admin via Dashboard.\n")
                
            # Best effort workflow state reset in Registry
            for h in unacknowledged_halts:
                try:
                    parts = h.split(" | ")
                    if len(parts) > 1:
                        target = parts[1] # e.g. mechanistic-org/global_agent#105
                        repo_issue = target.split("#")
                        if len(repo_issue) == 2:
                            repo, issue = repo_issue[0], repo_issue[1]
                            safe_repo = repo.replace('/', '_')
                            wf_file = ROOT_DIR / "registry" / "global_agent" / f"{safe_repo}_workflow_state_issue_{issue}.md"
                            if wf_file.exists():
                                content = wf_file.read_text("utf-8")
                                content = content.replace("state: halted", "state: closed")
                                content = content.replace("Current Workflow State: HALTED", "Current Workflow State: CLOSED (Ack'd via Dash)")
                                wf_file.write_text(content, "utf-8")
                except Exception:
                    pass 
            st.rerun()
            
        st.subheader("Resurrection Bay")
        st.info("You may optionally respawn an explicitly killed execution task.")
        target_restarts = set()
        for h in unacknowledged_halts:
             parts = h.split(" | ")
             if len(parts) > 1: target_restarts.add(parts[1])
             
        for target in target_restarts:
            if st.button(f"Respawn Agent for {target}"):
                repo_issue = target.split("#")
                if len(repo_issue) == 2:
                    repo, issue = repo_issue[0], repo_issue[1]
                    agent_path = ROOT_DIR / "scripts" / "run_agent.py"
                    cmd = f'python "{agent_path}" --mode issue'
                    env = os.environ.copy()
                    env["TARGET_REPO"] = repo
                    env["TARGET_ISSUE"] = issue
                    env["AGENT_MODE"] = "exec"
                    # Span asynchronous process
                    subprocess.Popen(cmd, env=env, cwd=ROOT_DIR, shell=True)
                    st.success(f"Spawned native background process for {repo}#{issue}!")
    else:
        st.success("🟢 IDLE / NOMINAL")
        st.caption("Failsafe circuit breakers are active and monitoring.")

# ==== QUADRANT 4: ORCHESTRATION ====
with col4:
    st.header("4. Orchestration Engine")
    
    st.subheader("Current Sprint Operations")
    if BOARD_PATH.exists():
        try:
            with open(BOARD_PATH, 'r') as f:
                board = json.load(f)
            
            # Simple recursive search for items array
            def find_items(d):
                if isinstance(d, dict):
                    if "items" in d and "nodes" in d["items"]: return d["items"]["nodes"]
                    for v in d.values():
                        res = find_items(v)
                        if res is not None: return res
                elif isinstance(d, list):
                    for idx in d:
                        res = find_items(idx)
                        if res is not None: return res
                return None
                
            items = find_items(board) or []
                
            active_items = []
            for item in items:
                status = "Unknown"
                title = "Unknown"
                repo_issue = "Unknown"
                
                if "content" in item:
                    title = item["content"].get("title", "")
                    repo_issue = f"{item['content'].get('repository', {}).get('name', 'repo')}#{item['content'].get('number', '0')}"
                
                for fv in item.get("fieldValues", {}).get("nodes", []):
                    if fv.get("field", {}).get("name") == "Status":
                        status = fv.get("name", "")
                
                if status.lower() in ["in progress", "todo", "done"]: # Filter broadly active states
                    active_items.append({"Ticket": repo_issue, "Title": title, "Status": status})
                    
            if active_items:
                st.dataframe(pd.DataFrame(active_items), hide_index=True)
            else:
                st.info("Parsed logical board payload but found 0 explicitly 'In Progress/Todo' active items.")
        except Exception as e:
            st.error(f"Error parsing board.json: {e}")
    else:
        st.warning("No board.json found. Ensure `sprint_board.py` was executed.")
        
    st.subheader("Memory Intake (ChromaDB)")
    if CHROMA_PATH.exists():
        try:
            client = chromadb.PersistentClient(path=str(CHROMA_PATH))
            # Wrap in try-catch in case 'forensic_telemetry' does not exist yet
            try:
                col = client.get_collection("forensic_telemetry")
                count = col.count()
                st.metric("Indexed Forensic Documents", count)
            except Exception:
                st.metric("Indexed Forensic Documents", 0)
        except Exception as e:
            st.error(f"ChromaDB Load Error: {e}")
    else:
        st.warning("No local ChromaDB registry found.")
