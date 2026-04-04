import json
try:
    with open('project_items.json', encoding='utf-16') as f:
        data = f.read()
    items = json.loads(data)
    out_items = []
    for i in items.get('items', []):
        c = i.get('content', {})
        out_items.append({
            'id': i['id'], 'number': c.get('number'), 'title': c.get('title'),
            'status': i.get('Status'), 'priority': i.get('Priority'), 'iteration': i.get('Iteration')
        })
    with open('output_items.json', 'w', encoding='utf-8') as out:
        json.dump(out_items, out, indent=2)
except Exception as e:
    print(f"Error: {e}")
