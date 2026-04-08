import urllib.request
import json
import os

url = 'https://api.figma.com/v1/files/bnlr4OKBds8pCLfGKR4aQ3'
token = 'REDACTED'
req = urllib.request.Request(url, headers={'X-Figma-Token': token})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        os.makedirs('.gemini/scratch', exist_ok=True)
        out_path = '.gemini/scratch/figma_board.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
            
        print('SUCCESS! HTTP 200 OK')
        print(f"Document name: {data.get('name')}")
        
        doc = data.get('document', {})
        pages = doc.get('children', [])
        for page in pages:
            children_count = len(page.get('children', []))
            print(f"- Page: {page.get('name')} (ID: {page.get('id')}) | Nodes: {children_count}")
            
except urllib.error.HTTPError as e:
    print('FAILED:', e.code, e.reason)
    print(e.read().decode('utf-8'))
except Exception as e:
    print('FAILED:', e)
