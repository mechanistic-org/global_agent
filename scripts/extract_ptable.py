import json
import os

filepath = '.gemini/scratch/figma_board.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

def extract_text(node, indent=0):
    node_type = node.get('type')
    node_name = node.get('name', 'Unnamed')
    
    if node_type in ['FRAME', 'COMPONENT', 'GROUP', 'SECTION']:
        print('  ' * indent + f"[{node_type}] {node_name}")
        indent += 1
        
    if node_type == 'TEXT':
        text = node.get('characters', '')
        if text:
            clean_text = repr(text)
            if len(clean_text) > 200:
                clean_text = clean_text[:200] + "...'"
            print('  ' * indent + f"\"text\": {clean_text}")
            
    for child in node.get('children', []):
        extract_text(child, indent)

doc = data.get('document', {})
print(f"Document: {data.get('name')}")
for page in doc.get('children', []):
    print(f"\n--- PAGE: {page.get('name')} ---")
    for child in page.get('children', []):
        extract_text(child, 0)
