# MootMoat: Vision & Architectural Primer

This document outlines the core thesis, problem space, and technical mechanisms of **MootMoat**—The Open Standard for Agentic Professional Identity.

## 1. The Core Problem: "Round Zero"
Before a human recruiter ever reads a resume, an AI parsing agent processes it to perform **Entity Resolution**. Its job is to map an applicant onto a structured knowledge graph. If the agent cannot resolve the applicant into a coherent entity, they are disqualified silently before the game even begins. This is "Round Zero."

Hardware and mechanical engineers are disproportionately slaughtered in Round Zero. The gatekeeping ontologies were built by and for software engineers. While an ATS easily parses "React" or "AWS," it has zero native vocabulary for thermal resistance budgets, EMI mitigation strategies, or DFM tradeoffs. The physical hardware engineer is rendered entirely invisible by the schema design itself.

## 2. The Vision: A Protocol for Sovereignty
MootMoat is not an ATS bypass; it is an **empowerment protocol for legibility**. It empowers people who build the physical world (systems, hardware, mechanical) to translate their lived constraints into machine-readable digital signals. You control the data. You host it. You own the entity.

## 3. The Two Core Mechanisms
To make the invisible legible, MootMoat relies on two primary mechanics:

*   **The Tri-Node Footprint (Coherence as Signal):** You maintain synchronized, hyper-specific truth across three independent surfaces: Your canonical domain, your GitHub, and your LinkedIn. Bots cannot easily fake multi-substrate coherence of thermal budgets and DFM tradeoffs. Maintaining this Tri-Node schema is an unfakeable proof-of-work.
*   **Depth Signals (Translation of Lived Experience):** A taxonomy of twelve techniques (such as the *Structural Rhyme*) designed to pull "The Source" (an engineer's direct memory of constraint environments, failure events, and consequences) out of unstructured human memory and into formal, parsable parameters.

## 4. The Conformance Stack
MootMoat defines four strict levels of agentic legibility:
1.  **Level 1 (Entity Resolvable):** Prevents Entity Resolution Failure. Exposes a valid JSON-LD context and `/llms.txt`. You are no longer invisible to the parser.
2.  **Level 2 (Domain Legible):** Exposes `constraintDomain` entries and `physicalConstraintSummary`. ATS-invisible hardware schemas become machine-readable.
3.  **Level 3 (Proof Present):** The enrichment layer is active. Utilizes `isomorphicProof` blocks tying structural mappings to shared failure modes and quantified outcomes. 
4.  **Level 4 (Vivisection Complete):** The full metabolic layer fused with the structural layer. (e.g., the `eriknorris.com` reference implementation). Career data is rendered at multiple resolution layers for different agentic and human consumer classes.

## 5. The Infrastructure Reality
To execute this sovereignly, MootMoat operates under strict physical engineering principles:
*   **Asset Sovereignty:** Binary assets (CAD, PDFs, M4As) are never committed to the git index. They must be staged locally and proxied via an R2 Virtual Proxy Bridge.
*   **Air-Gapped Extraction:** ITAR-restricted or highly proprietary engineering data must never be dumped into a cloud LLM to generate the schema. Extraction happens completely offline.
*   **WAF Transparency:** By default, Web Application Firewalls (like Cloudflare's Bot Fight Mode) block crawlers with 403s. MootMoat dictates explicit, mandatory edge-routing bypasses for `ClaudeBot` and `GPTBot` specifically targeting `/llms.txt` and `/docs/meta/agent_profile.json`. If you build the node but the agent can't hit it, the node doesn't exist.
