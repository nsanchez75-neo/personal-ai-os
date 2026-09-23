# DECISIONS

This file is the durable institutional memory of architectural decisions.

## Status vocabulary

- PROPOSED
- APPROVED
- REJECTED
- SUPERSEDED
- DEPRECATED

## D-001 — Three specialized brains
**Status:** APPROVED  
**Decision:** Use CEO Brain, AI Architect / Builder Brain, and Business Brain.  
**Reason:** Separates strategic, technical, and business responsibilities.

## D-002 — AI Director is an orchestrator
**Status:** APPROVED  
**Decision:** AI Director coordinates brains, agents, skills, tools, sequence, approvals, and evaluation. It is not a fourth brain.  
**Reason:** Prevents role duplication and centralizes orchestration.

## D-003 — Initial specialist agents
**Status:** APPROVED  
**Decision:** Start with Researcher, Analyst, Builder, Marketing, Sales, Finance, and Evaluator.  
**Reason:** Covers core workflows without premature agent proliferation.

## D-004 — GitHub as source of truth
**Status:** APPROVED  
**Decision:** Git-based repository is the persistent canonical source for project artifacts.  
**Reason:** Versioning, portability, auditability, and provider independence.

## D-005 — Explicit continuity pack
**Status:** APPROVED  
**Decision:** BOOTSTRAP, PROJECT-CONTEXT, DECISIONS, MASTER-BLUEPRINT, CHANGELOG, and README form the continuity pack.  
**Reason:** A new AI must reconstruct the project without the original conversation.

## D-006 — Human-in-the-loop
**Status:** APPROVED  
**Decision:** Automate reversible actions; require approval for irreversible or high-impact actions.  
**Reason:** Preserve human authority and reduce operational risk.

## D-007 — Provider portability
**Status:** APPROVED  
**Decision:** Keep core intelligence provider-neutral and separate provider-specific implementations.  
**Reason:** Avoid lock-in.

## D-008 — Progressive complexity
**Status:** APPROVED  
**Decision:** Evolve from simple to modular to testable to reusable to scalable.  
**Reason:** Prevent premature infrastructure complexity.

## D-009 — Legacy project as reference input, not canonical authority
**Status:** APPROVED  
**Decision:** The uploaded legacy project may be reused selectively, but canonical authority remains the current PERSONAL AI OS repository and its approved architecture/decision records.  
**Reason:** Preserves valuable prior work without allowing legacy hierarchy, provider-specific implementation, duplication, or unsupported claims to override the approved portable architecture.

## D-010 — User-provided business frameworks as reference mechanisms
**Status:** APPROVED  
**Decision:** User-provided business, sales, marketing, personal-brand and content frameworks may be normalized into the relevant Business Brain skills and knowledge layer, but do not become universal project rules without validation. 
**Reason:** Preserves high-value reusable mechanisms while preventing source-specific claims, thresholds, formulas or tactics from becoming unverified canonical doctrine.
