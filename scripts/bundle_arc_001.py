import os

posts = [
    "2026-03-22_git_as_agent_substrate.md",
    "2026-03-22_the-loop-is-closing.md",
    "2026-03-23_jigs_and_amnesia.md",
    "2026-03-24_the-gatekeeper.md",
    "2026-03-24_mechanical-fmea.md",
    "2026-03-26_the_cache_problem.md"
]

base_dir = r"d:\GitHub\global_agent\registry\linkedin"
out_path = os.path.join(base_dir, "arc_001_bundle.txt")

with open(out_path, "w", encoding="utf-8") as out_f:
    out_f.write("# ARC 001 SOURCE BUNDLE\n\n")

    for i, p in enumerate(posts):
        post_num = i + 1
        out_f.write(f"## POST {post_num} ({p})\n")
        
        # Find the post file
        post_path = os.path.join(base_dir, "posted", p)
        if not os.path.exists(post_path):
            post_path = os.path.join(base_dir, "drafts", p)
            
        if os.path.exists(post_path):
            with open(post_path, "r", encoding="utf-8") as pf:
                out_f.write(pf.read())
        else:
            out_f.write(f"[File not found: {p}]\n")
            
        out_f.write("\n\n### COMMENT FOR POST {}\n".format(post_num))
        
        # Check for comment file
        basename = p.replace(".md", "")
        # Note: Post 1's comment was the retrospective we just worked on
        if post_num == 1:
            comment_name = "2026-03-26_arc_001_retrospective_comment.md"
        else:
            comment_name = f"{basename}_comment.md"
            
        c_path = os.path.join(base_dir, "posted", "comments", comment_name)
        if not os.path.exists(c_path):
            c_path = os.path.join(base_dir, "drafts", "comments", comment_name)
            
        if os.path.exists(c_path):
            with open(c_path, "r", encoding="utf-8") as cf:
                out_f.write(cf.read())
        else:
            out_f.write(f"[Comment file not found: {comment_name}]\n")
            
        out_f.write("\n\n" + "="*80 + "\n\n")

print(f"Bundled successfully into {out_path}")
