# 🌐 EN-OS: Agent Orientation & Structural Manifesto

*This document is the master context layer. Any external Autonomous Agent entering the `mechanistic-org` ecosystem must ingest this topology prior to executing code modifications.*

---

## 1. The Principal Node & The Ecosystem
You operate under the command of **Erik Norris**, the Principal Node. 
The ecosystem is hosted entirely within the **`mechanistic-org`** GitHub Organization. This is a Sovereign Architecture built for a solo operator managing a swarm of autonomous agents. The system prioritizes **mathematical constraints over trust**, meaning you are physically barred from breaking production gracefully.

### The Hub-and-Spoke Topology
The organization is divided into strictly isolated repositories (Hubs and Spokes). You must never assume you have cross-repository access unless explicitly granted.
*   **The Global Brain (`global_agent`):** The central orchestrator. It houses all multi-agent Python/TS scripts, Small Language Models (SLMs), and global automation daemons.
*   **The Command Hub (`mechanistic` / `portfolio`):** The overarching agency infrastructure and UI component libraries. 
*   **The Forensic Registry (`mootmoat`):** The central documentation hub. A weekly daemon scrapes all client repositories and compiles their markdown architecture into this central registry to prevent Agent Context Window Death.
*   **The Client Spokes (e.g., `MO`):** mathematically isolated client repositories spawned from `TEMPLATE_client`. They have their own dedicated Cloudflare compute pipelines and dedicated R2 Storage buckets (`assets-[client]`).

---

## 2. The Infrastructure Constraints (Sovereignty)
When building UI or data routing for a client spoke, you must never hardcode API keys or global references. 
*   **Storage:** Client data is stored in isolated Cloudflare R2 buckets (e.g., `assets-mo`). You access this data securely via Cloudflare Bindings (typically bound to `env.PROJECTS` or `env.R2_ASSETS`) in the Astro SSR endpoints.
*   **Component Purity:** You may not copy global components from `mechanistic` and leave legacy code intact. If you extract an architecture (e.g., moving `holy-grail-v31` out of the monolith and into a direct Client Spoke), you must aggressively **purge** all unrelated dependencies (e.g., `hyphen-lid`).

---

## 3. The SDLC "Constraint Cage" (Your Operational Bounds)
You are an autonomous agent capable of writing thousands of lines of code. Because you occasionally hallucinate, you operate inside a strictly enforced Gitflow pipeline. **You do not have push access to the [main](file:///D:/GitHub/portfolio/scripts/nuke_cloudflare_deployments.py#39-103) branch.**

### The Execution Loop:
1.  **The Sandbox:** When executing a feature, you must create a new isolated git branch (e.g., `feature/v32-slm-integration`). You will do all your raw coding and JSON routing here.
2.  **The Zod Enforcer:** You are writing Astro/React TSX files driven by JSON payloads (DFMEA architectures, PRD-3 specifications). You must strictly adhere to the Zod schemas located in the `src/schemas/` directory.
3.  **The Pull Request:** To deploy your code, you must push your branch and open a Pull Request into [main](file:///D:/GitHub/portfolio/scripts/nuke_cloudflare_deployments.py#39-103). The PR triggers the **Constraint Cage**:
    *   GitHub Actions spins up an Ubuntu server and runs `npm run check` (Astro check + TS validation).
    *   If your code hallucinates a variable, drops a mandatory Zod field, or introduces a Type error, the PR is instantly blocked. You cannot merge.
4.  **The Cloudflare Preview:** Simultaneously, Cloudflare builds your branch into a temporary, secret Preview URL (e.g., `feature-v32.mo.pages.dev`). The Principal Node will visually inspect this URL before merging.
5.  **The Production Merge:** Once the Principal Node clicks *Merge Pull Request*, your code lands on [main](file:///D:/GitHub/portfolio/scripts/nuke_cloudflare_deployments.py#39-103) and Cloudflare autonomously overwrites the live production server (e.g., `mo.mechanistic.com`) in milliseconds.

---

## 4. The Autonomy Bankruptcy Clause
If your Pull Request fails the `npm run check` Zod validation, you are permitted to attempt to fix the hallucination and push a new commit to the branch.

**CRITICAL DIRECTIVE:** You are bound by a hard `MAX_RETRIES = 3` limitation. If you fail to resolve the Build/Zod error after 3 consecutive commits to a Pull Request, you are in an algorithmic death loop. 
You must instantly **halt execution**, `exit 1`, and write a comment on the GitHub Pull Request explicitly tagging `@eriknorris` for a human override. Do not burn API credits attempting a 4th fix.

---

## 5. The Forensic Documentation Law
You operate in a finite context window. 
Whenever you successfully modify a complex [.tsx](file:///d:/GitHub/portfolio/keystatic.config.tsx), generate a raw JSON payload, or establish a new data binding, you must protect future Agents from having to re-read your 50,000 lines of code.

**If you establish new logic, you must simultaneously overwrite/create the corresponding [.md](file:///C:/Users/erik/temp_spec.md) file in the repository's `src/content/docs/` folder.**
This markdown file must be a compressed, terse explanation (under 500 words) of the exact variables you bound and the structural intent of the component. 

*If your JSON payload schemas dictate a mandatory `__forensicSummary` field, you must write the markdown string directly into the JSON object.* Failure to comply will result in a Zod PR rejection.
