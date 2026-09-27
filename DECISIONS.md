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

## D-012 — Portable project memory/context layer
**Status:** APPROVED  
**Decision:** Maintain a provider-neutral project memory/context layer under memory/ with separate MODEL-CONTEXT.md, SESSION-CONTEXT.md, USER-PREFERENCES.md and LEARNINGS.md. These files support continuity across AI models and sessions but do not override the canonical authority hierarchy; DECISIONS.md remains the durable authority for architectural decisions.
**Reason:** Project continuity must remain auditable, versionable and available to any provider, rather than depending exclusively on provider-native memory.

## D-013 — Provider-neutral Business Brain runtime
**Status:** APPROVED  
**Decision:** Build Business Brain Runtime v0.1 as a provider-neutral execution layer between the Business Brain contract and concrete model adapters.
**Reason:** The Business Brain must remain model-agnostic while the runtime can add context construction, evidence adjudication, consistency checks, repair and evaluation gates around model-specific behavior.

## D-014 — Model qualification separate from Business Brain qualification
**Status:** APPROVED  
**Decision:** Qualify concrete models through model profiles and a dedicated qualification battery. Do not redesign the Business Brain around the first local model.
**Reason:** Model capabilities, adapter behavior and Business Brain invariants are different layers and must remain diagnosable.

## D-015 — Trace-based error attribution and repair
**Status:** APPROVED  
**Decision:** Candidate errors require exact textual traceability, semantic phenomenon confirmation, polarity/negation checking, context checking and contrary testing before attribution. Repairs must modify demonstrated errors only and pass an independent re-audit.
**Reason:** T16–T18 showed self-evaluation can misattribute errors and T18 exposed negation reversal plus repair-nonrepair.

## D-016 — Repository-first execution preference
**Status:** APPROVED  
**Decision:** For PERSONAL AI OS work, when repository write tools are directly available, changes may be executed through those tools without requiring a separate Work handoff.
**Reason:** The user explicitly prefers direct repository execution and wants this treated as a project interaction preference.
