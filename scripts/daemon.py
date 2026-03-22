import os
from google import genai
from google.genai import types

def ingest_multimodal_payload(file_path: str, mime_type: str = "application/pdf"):
    """
    Sovereign Node 0: Multimodal Senses.
    Demonstrates native binary consumption using massive Gemini APIs over brittle OCR text loops.
    """
    client = genai.Client()
    
    try:
        # Pushing the physical bytes directly to the 2M+ Context Window API parameter.
        uploaded_file = client.files.upload(file=file_path, config={'mime_type': mime_type})
        print(f"-> MULTIMODAL SENSORS ENGAGED: Successfully ingested {file_path} into Node 0's structural buffer.")
        return uploaded_file
    except Exception as e:
        print(f"-> SENSORY FAILURE: Node 0 violently rejected the raw payload ingestion: {e}")
        return None
