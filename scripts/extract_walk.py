import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import sys

try:
    print("Loading credentials...")
    creds_path = r"d:\GitHub\global_agent\.gdrive_tokens.json"
    if not os.path.exists(creds_path):
        print(f"Error: Credentials not found at {creds_path}")
        sys.exit(1)
        
    creds = Credentials.from_authorized_user_file(creds_path, ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents.readonly"])
    service = build("docs", "v1", credentials=creds)
    
    docs_dir = r"C:\Users\erik\My Drive (mechanistic@gmail.com)\Antigravity_Shared_Bus\local-agentic-architecture_swarm-control_engineering-automation"
    compiled_text = ""
    
    print("Reading directory...")
    for f in os.listdir(docs_dir):
        if f.endswith(".gdoc"):
            try:
                with open(os.path.join(docs_dir, f), 'r') as fp:
                    data = json.load(fp)
                    doc_id = data.get("doc_id")
                    if doc_id:
                        print(f"Fetching {f}...")
                        doc = service.documents().get(documentId=doc_id).execute()
                        content = doc.get("body").get("content")
                        text = ""
                        for element in content:
                            if "paragraph" in element:
                                elements = element.get("paragraph").get("elements")
                                for elem in elements:
                                    text += elem.get("textRun", {}).get("content", "")
                        compiled_text += f"\n\n=== {f.upper()} ===\n{text}"
            except Exception as e:
                print(f"Error reading {f}: {e}")
                
    with open(r"d:\GitHub\global_agent\walk_transcripts.txt", "w", encoding="utf-8") as out:
        out.write(compiled_text)
    print("EXTRACTION COMPLETE")

except Exception as e:
    print("FATAL ERROR:", e)
