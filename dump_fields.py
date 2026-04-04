import json
with open('project_fields.json', encoding='utf-16') as f:
    data = json.load(f)
    with open('fields_out_real.txt', 'w', encoding='utf-8') as out:
        for field in data.get('fields', []):
            name = field.get('name')
            if name in ['Status', 'Priority', 'Size', 'Iteration']:
                out.write(f"--- {name} ({field.get('id')}) ---\n")
                if 'options' in field:
                    for opt in field['options']:
                        out.write(f"  {opt['name']}: {opt['id']}\n")
                elif field.get('configuration'):
                    for iter in field['configuration'].get('iterations', []):
                        out.write(f"  {iter['title']}: {iter['id']}\n")
