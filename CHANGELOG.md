# CHANGELOG

## 2026-09-26 — Business Brain Runtime v0.1 foundations
- Added provider-neutral Business Brain Runtime contract and context builder.
- Added OllamaAdapter using the standard library, keeping provider SDKs out of the core runtime.
- Added Evidence Adjudicator primitives with traceability, polarity/negation and contrary-test controls.
- Added deterministic consistency guardrails for unsupported numeric claims and strong epistemic language.
- Added Model Qualification Battery v0.1.
- Added Qwen3 8B model profile with CONDITIONAL qualification status based on T01–T18 evidence.
- Added D-013 through D-016 covering runtime separation, model qualification, trace-based repair and repository-first execution preference.
- Kept Block 2 OPEN; no real-model runtime PASS is claimed by these structural changes.

## 2026-09-24 — Portable project memory/context layer
- Added memory/MODEL-CONTEXT.md for provider-neutral operational context.
- Added memory/SESSION-CONTEXT.md for current session state and exact next action.
- Added memory/USER-PREFERENCES.md for project interaction preferences.
- Added memory/LEARNINGS.md for provisional observations that require replication before becoming rules.
- Added D-012: portable project memory/context layer; DECISIONS.md remains the durable architectural authority.
- Recorded Qwen3 8B T01/T02 observations as provisional evaluation learnings.
- Kept Block 2 OPEN and canonical Business Brain changes gated on repeated behavioral evidence.

## 2026-09-22 — Business Brain scenario validation preparation
- Converted all 22 acceptance tests into concrete behavioral scenarios.
- Added five cross-brain workflow scenarios covering CEO, Business, AI Director and AI Architect boundaries.
- Added an explicit six-state ambiguous-experiment protocol and integrated it into the Business Brain system prompt and decision engine.
- Added a pre-runtime scenario validation report.
- Result: 22/22 PASS for scenario/specification conformance; this is not a runtime/model-behavior benchmark.
- Block 2 remains open until a reproducible provider-neutral runtime/evaluator executes the scenarios and cross-brain workflows.

## 2026-09-22 — Business Brain v0.1 architecture validation
- Validated the Business Brain architecture against all 22 acceptance requirements.
- Result: 19 PASS, 3 PARTIAL, 0 FAIL at specification/architecture level.
- Added evaluations/BUSINESS-BRAIN-v0.1-VALIDATION-REPORT.md.
- Identified remaining validation gaps: ambiguous experiment decisions, contextual scaling decisions, and real behavioral execution.
- Business Brain v0.1 is conditionally passed for architecture validation but Block 2 remains open until scenario and cross-brain behavioral tests pass.

## 2026-09-22 — Business Brain v0.1 architecture
- Researched business-model validation, customer discovery, market research, value proposition testing and GTM coherence.
- Created Business Brain architecture, system prompt, decision engine, memory interface and evaluation suite.
- Defined customer intelligence, market intelligence, value proposition, offer, pricing, GTM, lifecycle, economics, experimentation, learning, memory and governance systems.
- Added evidence hierarchy, hypothesis-driven experimentation, proxy controls, B0–B3 decision classes and human approval boundaries.
- Preserved source-derived mechanisms as mechanisms rather than universal laws.

## 2026-09-22 — Business source integration: Hormozi + personal brand/content
- Analyzed the user-provided business and personal-brand corpora.
- Added the normalized source inputs and business-model, sales, marketing and content skill contracts.
- Preserved source-derived frameworks as reference inputs rather than universal laws or personas.
- Explicitly excluded unsupported universal pricing/margin/follower thresholds, causal claims without validation, deceptive tactics, and provider-specific implementation.

## 2026-09-22 — CEO Brain v0.1
- Completed external leadership research using primary/current sources.
- Integrated validated mechanisms with legacy-project inputs.
- Created CEO Brain architecture, decision engine, system prompt, research register and evaluation suite.
- Added closed-loop learning, prediction calibration, anti-bias controls, decision classification, capital allocation, risk governance, human-approval boundaries and cross-brain interfaces.

## 2026-09-22 — Legacy Project Import Audit
- Completed full structural/content audit of uploaded ai_.zip.
- Mapped legacy agents, skills, evaluation suites, workflows, knowledge assets, and provider-specific automation to the canonical architecture.
- Added legacy audit and reuse-map artifacts.
- Added D-009: legacy project is reusable reference material, not canonical authority.

## v0.1 — Foundation
- Canonical architecture, three brains, AI Director, specialist agents, skills/tools, memory/knowledge separation, workflows, evaluation, HITL, portability, continuity pack and repository structure established.

## 2026-09-22 — Business Brain provider-neutral runtime harness
- Added minimal provider-neutral runtime under runtime/business_brain/.
- Added adapter contract plus deterministic fixture adapter.
- Added machine-readable harness results.
- Added CI workflow definition.
- Expanded cross-brain scenarios so the suite is 27 executable scenarios.
- Harness contract execution: 27/27 PASS.
- Explicitly classified this result as HARNESS_VALIDATION, not LLM behavior validation.
- GitHub Actions endpoint returned no available workflow run at validation time, so no CI execution is claimed.
- Added runtime harness validation report.
- Block 2 remains OPEN; legacy skill incorporation remains blocked until real-model behavioral validation.


## 2026-10-04 — Evolution Loop v0.1 + Business Brain context integrity
- Added provider-neutral Evolution / Improvement Loop architecture for brains, agents, skills and workflows.
- Established the rule: learning is not mutation; production mutation remains gated and auditable.
- Added improvement protocol, ledger and Business Brain evolution proposal artifacts.
- Added Business Brain context-integrity checks to prevent malformed/placeholder prompts from being interpreted as model failures.
- This change is architectural/runtime guardrail work and does not claim new LLM behavioral qualification.



## 2026-10-04 — Runtime evaluation gates

- Added single-scenario execution to the Business Brain runner via `--scenario-id`.
- Added explicit Ollama generation controls: `--timeout` and `--num-predict`.
- Added generation gating for timeout, incomplete generation and `done_reason=length` truncation.
- Added optional `--require-json` structural gate.
- Preserved provider-neutral fixture behavior while preventing harness assertions from being injected into real LLM prompts.
- Canonicalized the previously manual T02-COMPACT experiment as `evaluations/T02-COMPACT-v0.1.md`.
- T02-COMPACT remains OPEN until a complete, context-valid, structurally valid real-model run is obtained.


## 2026-10-08 — T02 semantic adjudication
- Added provider-neutral semantic adjudication for T02-COMPACT.
- Added explicit VoI comparison checks and hypothesis/experiment alignment checks.
- Added regression catalog entries for `REG-VOI-UNDEREXPLICIT` and `REG-HYPOTHESIS-EXPERIMENT-MISMATCH`.
- Added deterministic unit tests.
- This change does not claim new Qwen3 qualification; it prepares the next adjudication of the already completed T02-640 run.
