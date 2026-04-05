---
title: Global Agent Quickstart (Sovereign OS)
slug: quickstart-global-agent
sidebar:
  group: Handbook
  order: 1
description: Documentation for Multi-Project Sovereign OS Era operations.
---
# 🌐 Quickstart: Global Agent & Sovereign OS

> **Role:** EN-OS Administrator
> **Objective:** Manage the global multi-project sovereign infrastructure.

## 1. R2 Data Sync (Multi-Project)

Asset management is now unified through a centralized synchronization protocol mapping between local workspaces and remote execution context. 

**Central Asset Sync Command:**

```powershell
cd D:\GitHub\global_agent
python scripts\sync_r2.py --target <project_slug>
```

The script manages a `BUCKET_MAP` internally to route assets appropriately across distributed edge architectures.

## 2. MCP Router & Local Intelligence

The Model Context Protocol (MCP) Router connects our LLM agents directly with local data substrates.

**Startup Command:**
```powershell
cd D:\GitHub\global_agent
npm run router:start
# OR
pm2 start ecosystem.config.js
```

**Router Features:**
- Reads local structural metrics via `/mcp` hooks.
- Routes queries through `ChromaDB` for architectural constraints.

## 3. ChromaDB Context Persistence

When drafting deep engineering documentation or processing legacy repositories, we persist metadata to vector memory.
- **Tools:** Use the native `enos_router` tool `push_forensic_doc`.
- **Database:** Local embeddings are kept strictly sovereignty bound.

## 4. Edge Deployment (Cloudflare Pages)

Direct deployment skipping CI/CD pipelines when bypassing github-triggered actions or managing global sub-deployments:

```powershell
wrangler pages deploy dist/ --project-name <project_name>
```

## 5. Multi-Repo Git Workflows

As of the Sovereign OS era, operations frequently span `global_agent`, `portfolio`, `mechanistic`, and `hyphen`.

Ensure context boundaries are respected.
1. Run `python scripts\diag.py` globally to verify multi-repo statuses.
2. Agents must **not** run recursive shell commands for safety. Use point-tooling exclusively (e.g. `ast-patcher` for Astro, `view_file` for reads).
