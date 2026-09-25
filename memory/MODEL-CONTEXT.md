# MODEL CONTEXT

## Purpose

Portable operational context for any AI model continuing PERSONAL AI OS.

This file summarizes the minimum durable context needed to understand the project without relying on a prior conversation. It does not replace DECISIONS.md or PROJECT-CONTEXT.md.

## Mission

Build a portable, modular personal AI operating system / AI Factory that can turn ideas into validated decisions, businesses, AI systems, agents, automation and measurable learning while preserving human authority, provider portability and continuity.

## Canonical architecture

USER
→ AI DIRECTOR / ORCHESTRATOR
→ CEO BRAIN | AI ARCHITECT / BUILDER BRAIN | BUSINESS BRAIN
→ SPECIALIST AGENTS
→ SKILLS
→ TOOLS
→ MCP / APIs
→ MEMORY
→ EVALUATION

AI Director is an orchestrator, not a fourth brain.

## Source of truth

GitHub repository: nsanchez75-neo/personal-ai-os

Authority hierarchy:
1. DECISIONS.md
2. PROJECT-CONTEXT.md
3. MASTER-BLUEPRINT.md
4. Specialized project files
5. Conversations and temporary context

## Continuity Pack

Read:
1. BOOTSTRAP.md
2. PROJECT-CONTEXT.md
3. DECISIONS.md
4. MASTER-BLUEPRINT.md
5. CHANGELOG.md
6. AI-HANDOFF.md

Then read only specialized files required for the current objective.

## Current phase

Block 2 — Business Brain real-model provider-neutral behavioral validation.

Harness validation is complete. Real LLM behavioral validation remains OPEN.

## Current objective

Validate actual Business Brain behavior against real local models before changing canonical prompts, skills or architecture.

## Current model

Qwen3 8B via local Ollama.

Thinking: ON.

## Evaluation state

T01: PARTIAL PASS.
- Strengths: distinguishes declarations from behavior; separates facts/assumptions/unknowns; recognizes positive signal is not full validation.
- Weaknesses: invented unsupported 5%/15%/30% thresholds; overstrong business-viability inference from arbitrary thresholds.
- Candidate regression: do not invent decision thresholds; if unsupported, status is UNKNOWN.

T02: PARTIAL PASS.
- Strengths: better epistemic discipline; no invented numeric thresholds; controls overgeneralization.
- Weaknesses: selected interviews as the primary experiment despite explicit instruction not to assume interviews are best evidence; partially conflated future/intention statements with behavioral evidence; experiment criteria were vague; self-check did not detect these weaknesses.
- Candidate regressions: declaration-vs-behavior; minimum-credible-experiment; weak/adversarial self-check; information-value prioritization.

T03: in progress in the user environment. Await the complete output before evaluation.

## Important methodological rule

Observed model behavior is evidence about the model under a specific test protocol. It is not automatically a model-wide capability claim, a Business Brain rule, or an architecture decision.

Promotion path:
observation → replication → stable pattern → regression case → responsible-layer correction → re-test.

## Do not confuse

- Evidence ≠ Decision
- Decision ≠ Project State
- Project State ≠ Learning
- Learning ≠ Canonical Rule
- Model Capability ≠ Brain Capability
- Prompt Compliance ≠ Reliable Reasoning
- Harness Validation ≠ LLM Behavioral Validation

## Business Brain boundary

Business Brain owns customer intelligence, market/offer design, pricing, GTM, lifecycle, commercial economics and experimentation.

CEO Brain retains strategic authority.
AI Director retains orchestration.
AI Architect retains technical authority.

## Protected constraints

- Do not reinvent approved architecture.
- Do not create unnecessary agents.
- Keep portable intelligence separate from provider-specific implementation.
- Do not store secrets.
- Automate reversible actions; require human approval for irreversible/high-impact actions.
- Do not promote user-provided frameworks or model observations to universal rules without validation.

## Interaction preference

For AI Factory construction/evaluation questions, prefer one integrated response block that both executes the requested work and teaches the relevant concept. This is a project interaction preference, not a universal formatting requirement.

## Session continuity

Current immediate next action:
1. User runs Qwen3 8B T03.
2. User provides complete output including elapsed time.
3. Evaluate T03 against T01/T02.
4. Do not modify canonical Business Brain prompts/skills from T03 alone.
5. Continue accumulating evidence until repeated patterns justify regression updates.

## Related memory files

- memory/SESSION-CONTEXT.md — current session state
- memory/USER-PREFERENCES.md — project interaction preferences
- memory/LEARNINGS.md — observations and provisional learnings
