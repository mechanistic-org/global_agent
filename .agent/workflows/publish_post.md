---
description: The official ritual for moving a drafted LinkedIn post to published status, syncing OS file states with the public feed.
---
# /publish_post

This workflow formalizes the schema enforcement and state transition for posting to LinkedIn, preventing orphan drafts and schema drifts.

## Setup
You must know exactly which file in `registry/linkedin/drafts/` the operator intends to publish.
- *Strict Rule:* Never operate on iterative duplicates (e.g. `_v2`). The Git history is the iteration. Ensure only one canonical draft file exists before proceeding.

## Execution

1. Confirm canonical draft path within `registry/linkedin/drafts/`.
2. Extract the file content using `view_file`.
3. Strip the YAML frontmatter from the file. Display **ONLY the clean plain-text body** in your response to the operator within a markdown codeblock so they can easily copy-paste it.
4. **Remind the Operator:** "Please copy the text above, post it to LinkedIn, and then immediately paste the live post URL here in the chat."
5. **Yield the floor.** You must halt execution and WAIT for the operator to reply with the live URL.

*(Wait for Operator Input)*

6. Once the URL is provided:
   - Inject the URL back into the `post_url` field of the draft's frontmatter.
   - Ensure the frontmatter `status` is set to `posted`.
7. Move the file from `registry/linkedin/drafts/` to `registry/linkedin/posted/`. Do this via CLI or by recreating the file and deleting the old one.
8. Look for a pre-drafted self-comment in `registry/linkedin/drafts/comments/` matching this post. If it exists, display it for the operator.
9. **Remind the Operator:** "Post this comment on your live post within the next 30 minutes to optimize the engagement loop."
10. Update the corresponding thread ledger in `registry/linkedin/threads/<thread_id>.md` by appending the new post file pointer and live URL.
11. Commit the state changes to git so the agent amnesia substrate is updated:
```powershell
// turbo
git add registry/linkedin/
// turbo
git commit -m "Publish post to LinkedIn and update thread state"
```
