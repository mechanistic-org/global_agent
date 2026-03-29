### The Gap
We are injecting over 100+ native `googleworkspace/cli` markdown skills (`SKILL.md`) into our `.agent/skills/` control file registry. Because these are external dependencies written by Google, local drift poses a massive failure risk if Google updates an endpoint and our `SKILL.md` is six months out of date.

### Implementation Objective
1. Treat `.agent/skills/` as a strictly protected dependency boundary.
2. Implement either a Git Submodule mapping to `googleworkspace/cli`, OR write a simple `sync_skills.ps1` script triggered automatically that downloads the latest official `SKILL.md` releases from GitHub and syncs/overwrites the `.agent/skills/` directories recursively.
