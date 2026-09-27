# SESSION CONTEXT

## Session
Date: 2026-09-26
Project: PERSONAL AI OS — AI FACTORY
Phase: Block 2 — Business Brain real-model provider-neutral validation

## Current objective

Move from isolated model tests T01–T18 to a provider-neutral Business Brain runtime while preserving the evidence already accumulated.

## Completed in this phase

### Runtime integration integrity
- Runner now builds the full Business Brain + Runtime Contract context instead of loading only the Business Brain system prompt.
- Runner records deterministic consistency-check findings alongside raw model metadata.
- Epistemic guardrail is negation-aware so `no demuestra` is not treated as `demuestra`.
- Scenario-suite status now reflects that the runtime path exists; no real-model PASS is claimed until local execution.

### T01–T18 evidence synthesis
- Qwen3 8B was evaluated under a fixed methodology with thinking ON.
- T01–T18 remain evidence, not universal model claims.
- Key observed risks include unsupported numeric assumptions, declaration/behavior confusion, information-value prioritization, internal consistency, self-audit failure, self-evaluation misattribution, epistemic overcommitment, repair-nonrepair and negation reversal.

### Runtime architecture added
- runtime/business_brain/RUNTIME-CONTRACT.md
- runtime/business_brain/context.py
- runtime/business_brain/adjudicator.py
- runtime/business_brain/consistency.py
- runtime/business_brain/adapters/ollama.py
- evaluations/MODEL-QUALIFICATION-BATTERY-v0.1.md
- evaluations/model-profiles/qwen3-8b.yaml

### Architectural decisions
- D-013 Provider-neutral Business Brain runtime
- D-014 Model qualification separate from Business Brain qualification
- D-015 Trace-based error attribution and repair
- D-016 Repository-first execution preference

## Runtime invariants

- Evidence ≠ conclusion.
- Declaration ≠ behavior.
- Absence of evidence ≠ negative evidence.
- Payment ≠ profitability/scalability/repeatable acquisition/retention.
- Theme mentioned ≠ error committed.
- Candidate error ≠ actual error.
- Negation must be checked.
- Repair only demonstrated errors.
- Repair requires independent re-audit.
- Self-evaluation is not authoritative.

## Current model

Qwen3 8B via local Ollama.
Thinking: ON.
Profile status: CONDITIONAL based on T01–T18.

## Next actions

1. Run smoke qualification locally against qwen3:8b using the integrated runner.
2. Execute targeted critical behavioral regressions before full T01–T18 runtime execution.
3. Preserve raw outputs, metadata and consistency findings in evaluations/results/.
4. Add/strengthen semantic adjudication only where runtime evidence demonstrates a gap.
5. Record results in evaluations/results/ without claiming runtime PASS until actual execution is completed.
6. Reassess Block 2 only after reproducible behavioral evidence.

## Execution preference

For this project, repository write tools may be used directly; a separate Work handoff is not required merely to persist changes.
