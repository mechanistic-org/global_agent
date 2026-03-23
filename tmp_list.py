import subprocess, json
out = subprocess.check_output(['gh', 'project', 'item-list', '5', '--owner', 'mechanistic-org', '--format', 'json', '--limit', '100'])
obj = json.loads(out.decode('utf-8'))
with open('gh_items.txt', 'w', encoding='utf-8') as f:
    for i in obj['items']:
        status = i.get('status')
        if status in ['Ready', 'In progress', 'Backlog']:
            f.write(f"[{status}] {i.get('title')} (#{i.get('number', '?')})\n")
