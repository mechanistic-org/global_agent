# Board Governance Protocol
## EN-OS GitHub Project Board - Issue Structure, Lifecycle, and Triage Discipline

---

sources:
- https://github.com/eriknorris/global_agent/issues/135
- Session: 2026-04-17 board triage and governance discussion
- enos_architecture_analysis.md (Gemini brain: e85c8cd6-2de2-4387-a4d8-87b1e6aed91a)

---

## 1. Milestone Structure

Five milestones define the active planning horizon. Every open issue must be assigned to one.

| Milestone | Scope |
|---|---|
| **Toolmaker v1** | Skill schema migration to SKILL_TEMPLATE v2, skill_linter.py, assertion log, BDD validation, passive memory, FastMCP plumbing |
| **Board Governance v1** | Protocol discipline, issue lifecycle, session ritual, scope isolation, GWS ingress daemon |
| **Content Pipeline** | LinkedIn arcs, posts, assets, MootMoat V18, Venn diagrams, linkedin_master.ts |
| **Engineering Platform v1** | Mechanical Claws, Storyteller Claws, GD&T, FMEA/DFMEA pipeline, design review, session_spar |
| **Icebox** | Parked - not closed, no current momentum. Reactivate by moving to an active milestone and writing AC. |

**Rules:**
- No issue exists without a milestone. Unassigned = invisible = doesn't get worked.
- Icebox is not a trash can. Close issues that are truly abandoned. Icebox is for valid work with no current traction.
- New milestones require a scoping session and explicit DoD before being created.

---

## 2. Issue Lifecycle

Three states. An issue must earn its way forward.

```
idea  -->  triaged  -->  sprint-ready
```

### idea
- Raw capture. Allowed to be vague.
- Must have: title, one label, milestone assignment.
- Must NOT be worked without advancing to `triaged` first.
- Label: `backlog`

### triaged
- Has been reviewed against the triage rubric.
- Must have: label, milestone, at least one AC bullet or DoD sentence.
- May have: size estimate, parent Epic reference.

### sprint-ready
- Fully executable. An agent or operator can open a branch and begin without asking questions.
- Must have: full DoD with acceptance criteria, threading to parent Epic (if applicable), milestone.
- Branch opens only when issue reaches this state.

**The gate is the DoD.** An issue without acceptance criteria is not sprint-ready regardless of how long it has been open.

---

## 3. Triage Protocol

### Rubric - 3 Questions Per Issue

1. **Is it still relevant?** Not superseded, not abandoned, not blocked by an upstream dependency that isn't moving.
2. **Does it have acceptance criteria or DoD?**
3. **Does it have a milestone?**

### 3 Outcomes Only

| State | Action |
|---|---|
| Relevant + has AC + has milestone | No action needed |
| Relevant + missing AC or milestone | Write 1-3 AC bullets, assign milestone |
| Stale, superseded, or no foreseeable action | Close with one-line reason OR move to Icebox |

### Triage Session Format

- **Frequency:** Once per week, fixed timebox.
- **Duration:** 25 minutes maximum. Hard stop.
- **Input:** `gh issue list --no-milestone --state open` - anything without a milestone is the triage queue.
- **Output:** Zero unassigned issues, or a documented decision to defer.
- **Anything not touched in the timebox** goes to Icebox automatically.

The time cap is load-bearing. Triage without a cap expands into its own project.

---

## 4. Branch and PR Protocol

### Branch Naming

```
feature/N-short-description
```

Example: `feature/155-skill-linter-yaml-enforcement`

No branch without a ticket. The issue is the spec. Opening a branch without an issue is an uncontrolled part.

### Commit Convention

```
feat(scope): description - closes #N
fix(scope): description - closes #N
```

The `closes #N` tag auto-closes the issue on merge and creates the audit trail connecting commit to spec.

### PR Gate

Every PR must include a verification step proving acceptance criteria are met. This is the inspection record. A merge without verification is a part shipped without inspection.

---

## 5. Label Taxonomy

### Canonical Type Labels (what kind of work)

| Label | Color | Meaning |
|---|---|---|
| `Epic` | `#3E4B9E` | Multi-sprint architectural bounding box. Contains child Tasks. |
| `Task` | `#0E8A16` | Linear execution subroutine within a sprint. References parent Epic. |
| `Enhancement` | `#A2EEEF` | Local feature upgrade extending an existing system boundary. |
| `Bug` | `#D73A4A` | Lethal structural fault in executing code or UI framework. |
| `Pivot` | `#D93F0B` | Fundamental shift in architectural theory or core engine state. |
| `content` | `#ededed` | LinkedIn posts, assets, drafts, and content pipeline work. |

### Canonical Domain Labels (what area)

| Label | Meaning |
|---|---|
| `architecture` | Structural design decisions |
| `infrastructure` | Daemons, PM2, routing, deployment |
| `mcp` | MCP server and tool surface |
| `security` | Auth, scope, adversarial ops |
| `ui` | Frontend, Astro components, dashboards |
| `registry` | Flat-file registry structure and content |
| `maintenance` | Refactor, cleanup, debt reduction |
| `dx` | Developer experience, tooling, ritual |
| `performance` | Speed, latency, resource usage |

### State Labels

| Label | Meaning |
|---|---|
| `backlog` | Raw idea, not yet triaged |

### Priority Labels

| Label | Meaning |
|---|---|
| `p1` | Blocking active sprint work |
| `p2` | Important but not blocking |

### Deprecated - Do Not Use

The following labels exist but are superseded. Do not apply to new issues. Migrate existing issues on contact.

| Deprecated | Canonical Replacement |
|---|---|
| `Type: Bug` | `Bug` |
| `Type: Feature/Enhancement` | `Enhancement` |
| `Invalid/Wontfix` | Close the issue |
| `invalid` | Close the issue |
| `Validation` | `diagnostics` (pending cleanup) |
| `good first issue` | Not applicable to solo operator |
| `help wanted` | Not applicable to solo operator |
| `question` | Not applicable - open a discussion or use session notes |

---

## 6. Parent-Child Threading

Epics must list their child tasks. Child tasks must reference their parent Epic.

**In the Epic body:**
```markdown
## Child Tasks
- [ ] #156 Migrate skill: ast-patcher
- [ ] #157 Migrate skill: create-issue
```

**In the child task body:**
```markdown
## Parent
Part of: #154 [Epic] Skill Schema Migration - SKILL_TEMPLATE v2
```

An agent reading a Task issue must be able to identify its Epic without searching. An agent reading an Epic must be able to see completion state across all children.

---

## 7. The ME Analogy (Reference Frame)

For an operator coming from mechanical engineering:

| Onshape / ME | EN-OS SWE |
|---|---|
| Drawing package | GitHub Issue with acceptance criteria |
| ECO process | PR with verification step |
| BOM | Milestone (coherent deliverable) |
| Uncontrolled part | Code without a test or AC |
| Branch (exploration) | `feature/N-description` |
| Abort branch | `git branch -D` |
| Revision history | `git log` |
| Configuration freeze | `main` is always deployable |

An issue without acceptance criteria is an uncontrolled part. It cannot be inspected. It cannot be verified. It cannot be shipped.

---

## 8. Triage History

| Date | Action |
|---|---|
| 2026-04-11 | First board audit: 31 issues, zero milestones, inconsistent labels. Opened #135. |
| 2026-04-17 | Full triage execution: 5 milestones created, 63 issues assigned, 1 closed (#93). Board fully structured for first time. /triage skill created. board_governance.md written. CLAUDE.md pointer added. |
