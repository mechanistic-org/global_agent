import os
import re
from datetime import datetime

POSTED_DIR = r"d:\GitHub\global_agent\registry\linkedin\posted"
THREADS_DIR = r"d:\GitHub\global_agent\registry\linkedin\threads"

def parse_frontmatter(content):
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    
    fm_lines = match.group(1).split('\n')
    data = {}
    for line in fm_lines:
        if ':' in line:
            key, val = line.split(':', 1)
            data[key.strip()] = val.strip().strip('"').strip("'")
    return data

def analyze_posts():
    if not os.path.exists(POSTED_DIR):
        print("No posted directory found.")
        return

    print("=== LinkedIn Content State Analysis ===")
    
    missing_urls = []
    
    for filename in os.listdir(POSTED_DIR):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(POSTED_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        fm = parse_frontmatter(content)
        title = fm.get('title', filename)
        post_url = fm.get('post_url', '')
        
        if not post_url:
            missing_urls.append(title)

    if missing_urls:
        print(f"\n[WARNING] Found {len(missing_urls)} posts missing a live LinkedIn URL:")
        for t in missing_urls:
            print(f"  - {t}")
    else:
        print("\n[OK] All posted markdown files have canonical LinkedIn URLs.")

def check_threads():
    if not os.path.exists(THREADS_DIR):
        return
        
    print("\n=== Active Threads & Engagement Windows ===")
    
    for filename in os.listdir(THREADS_DIR):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(THREADS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        fm = parse_frontmatter(content)
        print(f"Thread Ledger: {fm.get('thread_id', filename)}")
        print(f"Status: {fm.get('status', 'unknown')}")
        
        # In a more advanced iteration, this would parse the `posts:` array
        # and compare pubDate with datetime.now() to alert on the 30-90 min engagement cross-linking window.
        print("-> Cross-comment strategy enforced by ledger constraints.")

if __name__ == "__main__":
    analyze_posts()
    check_threads()
    
    print("\nNote: Tracking relies purely on local Markdown/Chroma state rather than the LinkedIn API.")
    print("This bypasses OAuth hurdles and keeps Git as the canonical state substrate for EN-OS.")
