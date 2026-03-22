import os
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
import traceback

try:
    print("Loading Service Account credentials...")
    sa_path = r"D:\Assets\mechanistic-gmail-mcp-5e0f2d2d80eb.json"
    if not os.path.exists(sa_path):
        print(f"Error: Credentials not found at {sa_path}")
        sys.exit(1)
        
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/documents.readonly']
    creds = service_account.Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    service = build('docs', 'v1', credentials=creds)
    
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
                                if elements:
                                    for elem in elements:
                                        text += elem.get("textRun", {}).get("content", "")
                        compiled_text += f"\n\n=== {f.upper()} ===\n{text}"
            except Exception as e:
                print(f"Error reading {f}: {e}")
                
    with open(r"d:\GitHub\global_agent\walk_transcripts.txt", "w", encoding="utf-8") as out:
        out.write(compiled_text)
    print("EXTRACTION COMPLETE")

except Exception as e:
    print("FATAL ERROR:")
    traceback.print_exc()
