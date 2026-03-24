---
description: Process walk notes from a Google Drive folder into the registry
---

# /process_walk_notes

Run this when bringing back notes from a walk, voice session, or any batch of Google Docs saved to Drive for offline review.

## Input

A Google Drive folder URL:
```
https://drive.google.com/drive/folders/<FOLDER_ID>
```

## Steps

// turbo
1. List files in the Drive folder using the node shim (avoids Windows gws.cmd quoting bug):
```powershell
node C:\tmp\gws-drive-list.js <FOLDER_ID>
```
> If `C:\tmp\gws-drive-list.js` doesn't exist, create it first — see **Windows gws Shim** section below.

// turbo
2. Export each Google Doc to a local temp file:
```powershell
node C:\tmp\gws-doc-export.js <FILE_ID_1> C:\tmp\walk_doc1.txt
node C:\tmp\gws-doc-export.js <FILE_ID_2> C:\tmp\walk_doc2.txt
# ... repeat for each doc
```

3. Read all temp files and synthesize them into a single structured registry intelligence note:
   - File path: `registry/global_agent/intelligence/YYYY-MM-DD_<topic-slug>.md`
   - Frontmatter: `title`, `date`, `source`, `source_folder_id`, `status: processed`, `tags`, `linked_tickets`
   - Sections: one per document or logical theme, with action items linked to open tickets at the bottom

4. Identify any new tickets that need to be created from the notes. Create them via MCP GitHub.

5. Commit the new registry note:
```powershell
git add registry/global_agent/intelligence/
git commit -m "chore: process walk notes — <topic-slug>"
git push
```

6. State the session scope for the next ticket to execute.

---

## Windows gws Shim (Required — Created Once)

The `gws.cmd` wrapper on Windows has a known argument splitting bug with JSON containing spaces (e.g., Drive API `'FOLDER_ID' in parents` queries). Use these Node.js shims instead:

**`C:\tmp\gws-drive-list.js`**
```javascript
const { execFileSync } = require('child_process');
const folderId = process.argv[2];
const params = JSON.stringify({ q: `'${folderId}' in parents and trashed=false`, fields: 'files(id,name,mimeType,createdTime,size)' });
const gwsJs = 'C:\\Users\\erik\\AppData\\Roaming\\npm\\node_modules\\@googleworkspace\\cli\\run-gws.js';
const result = execFileSync('node', [gwsJs, 'drive', 'files', 'list', '--params', params], { encoding: 'utf8', stdio: ['inherit', 'pipe', 'pipe'] });
console.log(result);
```

**`C:\tmp\gws-doc-export.js`**
```javascript
const { execFileSync } = require('child_process');
const fileId = process.argv[2];
const outPath = process.argv[3] || 'download.txt';
const params = JSON.stringify({ fileId, mimeType: 'text/plain' });
const gwsJs = 'C:\\Users\\erik\\AppData\\Roaming\\npm\\node_modules\\@googleworkspace\\cli\\run-gws.js';
execFileSync('node', [gwsJs, 'drive', 'files', 'export', '--params', params, '-o', outPath], { encoding: 'utf8', stdio: ['inherit', 'inherit', 'pipe'] });
```

> **Why shims?** `gws.cmd` uses `%*` which causes cmd.exe to split JSON arguments on spaces before Node.js receives them. `execFileSync` passes each arg as an unmodified argv element, bypassing shell parsing entirely.

---

## Notes

- **What format are the notes?** Could be raw voice memos (via Google Recorder transcripts), structured Gemini output saved to Drive, or typed notes.
- **Folder convention:** Name Drive folders as `walk-notes_<topic-slug>` for easy identification.
- **Temp files:** Cleaned automatically by the OS from `C:\tmp\` — don't commit them.
- **Registry convention:** One intelligence note per walk session, not one file per doc.
