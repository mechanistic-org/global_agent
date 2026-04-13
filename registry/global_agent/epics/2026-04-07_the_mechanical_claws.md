---
title: "\"The Mechanical Claws: Physics and Constraint Engines\""
date: "2026-04-07"
status: "DRAFT"
project: "global_agent"
---

## Strategic Overview
Implement a fully deterministic, mathematically constrained Failure Modes and Effects Analysis (FMEA) engine that extracts qualitative failure modes from narrative PRDs and applies rigorous structural risk calculations. 

## Core Constraints
- Must enforce explicit $Severity \times Occurrence \times Detection$ arithmetic inside the Python boundary.
- Must eliminate LLM hallucination of Risk Priority Numbers (RPN).
- Schema compliance with the established `PhysicsVault` Pydantic model is absolute.

## System Interactions
- **Input:** Unstructured PRD markdown detailing hardware logic or product scope.
- **Processing:** Small language model (e.g. qwen_coder) extracts components and identifies failure modes; Python enforces the RPN math.
- **Output:** A strict liability matrix written directly into the `registry/` file system and indexed in ChromaDB.

## Definition of Done (DoD)
- [ ] Stand up discrete FMEA Agent/Python boundary structure.
- [ ] Implement GD&T Vision stack with bounding constraint scripts.
- [ ] Generate one automated DOE D3 visualization locally.
