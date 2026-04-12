# /publish_post

Publish a drafted LinkedIn post and sync all OS file states. The canonical policy lives in `.agent/skills/publish-post/SKILL.md` (v2.0.0). This is the Claude Code environment shim.

**Usage:** `/publish_post $ARGUMENTS`

`$ARGUMENTS` = draft filename base name (without extension), e.g. `2026-04-10_vibe_coding_vulnerability`

---

## Pre-flight

Before executing, confirm all three:
- Exactly one canonical draft file exists at `registry/linkedin/drafts/$ARGUMENTS.md`
- No `_v2`, `_revised`, or duplicate variants exist alongside it — Git history is the iteration record
- Draft frontmatter `status` is not already `posted`

If any fail, halt and surface to the operator.

---

## Step 1 — Display Clean Post Body

Read the draft file and strip the YAML frontmatter. Display **only the clean plain-text body** in a code block for copy-paste:

```bash
# Read the file — display body only (everything after the closing ---)
```

Then say exactly:
> "Copy the text above and post it to LinkedIn. Once it is live, paste the URL here."

**Yield. Wait for the operator to reply with the live URL before proceeding.**

---

## Step 2 — Update Frontmatter and Surface Self-Comment

Once the URL is provided:

1. Update the draft file frontmatter:
   - `status: posted`
   - `pubDate: [today's date YYYY-MM-DD]`
   - `post_url: [the URL provided]`

2. Check for a pre-drafted self-comment at `registry/linkedin/drafts/comments/$ARGUMENTS_comment.md`. If it exists, display it and say:
   > "Post this comment on your live LinkedIn post within the next 90 minutes to optimize the engagement loop."

3. If this post is part of an arc, append the live URL and file pointer to the corresponding thread ledger at `registry/linkedin/threads/<thread_id>.md`.

---

## Step 3 — Migrate Files

Move files from drafts to posted:

```bash
# Move the post
mv "D:/GitHub/global_agent/registry/linkedin/drafts/$ARGUMENTS.md" \
   "D:/GitHub/global_agent/registry/linkedin/posted/$ARGUMENTS.md"

# Move the self-comment if it exists
mv "D:/GitHub/global_agent/registry/linkedin/drafts/comments/${ARGUMENTS}_comment.md" \
   "D:/GitHub/global_agent/registry/linkedin/posted/comments/${ARGUMENTS}_comment.md" 2>/dev/null || true
```

---

## Step 4 — Commit

```bash
cd D:/GitHub/global_agent
git add registry/linkedin/
git diff --cached --stat
git commit -m "chore: linkedin post published - $ARGUMENTS"
git push
```

---

## Step 5 — Terminate

State completion: confirm files moved, frontmatter updated, git pushed. Yield.
