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

## D-004 — GitHub as source of truth
**Status:** APPROVED  
**Decision:** Git repository is the persistent canonical source for project artifacts.

## D-005 — Explicit continuity pack
**Status:** APPROVED  
**Decision:** BOOTSTRAP, PROJECT-CONTEXT, DECISIONS, MASTER-BLUEPRINT, CHANGELOG, and README form the continuity pack.

## D-006 — Human-in-the-loop
**Status:** APPROVED  
**Decision:** Automate reversible actions; require approval for irreversible or high-impact actions.

## D-007 — Provider portability
**Status:** APPROVED  
**Decision:** Keep core intelligence provider-neutral and separate provider-specific implementations.

## D-008 — Progressive complexity
**Status:** APPROVED  
**Decision:** Evolve from simple to modular to testable to reusable to scalable.

## D-009 — Legacy project as reference input, not canonical authority
**Status:** APPROVED  
**Decision:** Legacy project may be reused selectively; canonical authority remains the current PERSONAL AI OS repository and approved decision records.

## D-010 — User-provided business frameworks as reference mechanisms
**Status:** APPROVED  
**Decision:** User-provided business, sales, marketing, personal-brand and content frameworks may be normalized into Business Brain skills and knowledge, but do not become universal rules without validation.

## D-011 — Business Brain as commercial learning system
**Status:** APPROVED  
**Decision:** Business Brain owns customer intelligence, market/offer design, pricing, GTM, lifecycle, commercial economics and experimentation, while CEO Brain retains strategic authority, AI Director retains orchestration, and AI Architect retains technical authority.
**Reason:** Prevents overlap between brains and makes the Business Brain operationally useful without turning it into a second CEO or technical architect.
