---
description: The official ritual for moving a drafted LinkedIn post to published status
---
# /publish_post

Run this workflow to execute the actual posting maneuver. This ensures the EN-OS state machine remains perfectly synced with the public LinkedIn feed.

## Prerequisites
- A finished markdown draft in `registry/linkedin/drafts/`
- A drafted cross-comment in `registry/linkedin/drafts/comments/`

## Visual & Asset Laws

1. **The Brand Image Law:** *Every* post must have a high-quality, well-considered, relevant, and impactful image that correctly represents the Erik Norris brand. Never post plain text.
2. **The Hybrid Asset Strategy (TBD/Optional):** The optimal strategy for complex interactive visualizations is a native video hook (uploaded directly to LinkedIn for algorithmic reach) + a sovereign redirect link in the comments (pointing to the live interactive view on `assets.eriknorris.com`).
   - **Current Stance:** Do *not* require video or interactive motion graphics for every post. Until the creation of PDF carousels or video captures is trivialized by new tooling, stick to high-impact static images to avoid the time trap.

## Steps

1. Read the canonical draft file and display the **clean plain-text** (stripped of frontmatter) to the operator for easy copy-pasting to the LinkedIn UI.

2. Wait for the operator to publish the post on the LinkedIn UI and request the **live LinkedIn URL**. 

3. Read the pre-drafted self-comment from `drafts/comments/` and display it to the operator.
   > **REMINDER TO OPERATOR:** Post this comment within the 30-90 minute engagement window!

4. Update the draft's frontmatter:
   - `status: posted`
   - `post_url: [Live URL]`
   - `pubDate: [Today's Date]`

5. If part of a thread arc (e.g., `trilogy_001`), update `registry/linkedin/threads/<thread_id>.md` to reflect the published status and append the post URL to the ledger.

// turbo-all
6. Move the draft files from `drafts/` to `posted/`.
```powershell
Move-Item -Path "registry\linkedin\drafts\<filename>.md" -Destination "registry\linkedin\posted\"
Move-Item -Path "registry\linkedin\drafts\comments\<filename>_comment.md" -Destination "registry\linkedin\posted\comments\"
```

// turbo
7. Commit the state changes to Git.
```powershell
git add registry/linkedin/
git commit -m "chore: linkedin post published - <filename>"
git push
```
