import json

files = [
    ('portfolio', 'C:/Users/erik/.gemini/antigravity/brain/02011d45-a0d4-4911-bcd6-515128e4fa58/.system_generated/steps/59/output.txt'),
    ('global_agent', 'C:/Users/erik/.gemini/antigravity/brain/02011d45-a0d4-4911-bcd6-515128e4fa58/.system_generated/steps/60/output.txt')
]

for repo, path in files:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            if "pull_request" not in item:
                print(f"- **{repo}#{item['number']}**: {item['title']}")
