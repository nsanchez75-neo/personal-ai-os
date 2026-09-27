# PERSONAL AI OS

**Version:** v0.1  
**Status:** Foundation / Architecture Approved  
**Source of truth:** Git repository (GitHub target: `nsanchez75-neo/personal-ai-os`)

PERSONAL AI OS is a portable, modular personal AI operating system designed to coordinate specialized AI brains, agents, skills, tools, memory, workflows, and evaluation.

## Architecture

```text
USER
  │
  ▼
AI DIRECTOR / ORCHESTRATOR
  │
  ├── CEO BRAIN
  ├── AI ARCHITECT / BUILDER BRAIN
  └── BUSINESS BRAIN
          │
          ▼
   SPECIALIST AGENTS
          │
          ▼
        SKILLS
          │
          ▼
      TOOLS / MCP / APIs
          │
          ├── MEMORY
          ├── KNOWLEDGE
          └── EVALUATION
```

## v0.1 objective

Establish the durable foundation before implementing the CEO Brain:
- architecture
- continuity
- decisions
- memory policy
- portability
- repository structure
- evaluation protocol
- operating principles

## Core principle

> Automatizar lo reversible. Aprobar lo irreversible.

See `BOOTSTRAP.md` for recovery and migration instructions.


## Business Brain Runtime v0.1

The Business Brain now has a provider-neutral runtime layer:

```text
Business Brain Contract
        ↓
Context Builder
        ↓
Model Adapter
        ↓
Evidence Adjudicator
        ↓
Consistency Checker
        ↓
Repair / Independent Re-audit
        ↓
Evaluation Gate
```

The first local model profile is qwen3:8b through Ollama. Model qualification is separate from Business Brain qualification. See:
- runtime/business_brain/RUNTIME-CONTRACT.md
- evaluations/MODEL-QUALIFICATION-BATTERY-v0.1.md
- evaluations/model-profiles/qwen3-8b.yaml
- evaluations/REGRESSION-CATALOG-v0.1.md

**Block 2 remains OPEN:** the existing 27/27 result is harness validation, not real LLM behavioral validation.
