# LEARNINGS

This file stores observations and provisional learnings. It is not a replacement for DECISIONS.md and does not automatically create canonical rules.

## L-001 — Explicit principle knowledge does not guarantee method execution

Status: OBSERVED
Confidence: MEDIUM
Source: Qwen3 8B T01/T02
Needs replication: YES

### Observation

Qwen3 8B can explicitly state the distinction between declarative interest and behavioral evidence, and can state that positive evidence does not equal full validation. In T02 it nevertheless selected interviews as the primary experiment and partially treated future/intention statements as behavioral evidence.

### Implication

A model can know a methodological principle without applying it consistently in an end-to-end experimental design.

### Candidate failure modes

- declaration_vs_behavior
- minimum_credible_experiment
- information_value_prioritization
- weak_adversarial_self_check

### Do not promote yet

This observation must not be treated as a universal model capability claim or a permanent Business Brain rule until replicated.

## L-002 — Unsupported thresholds are an epistemic regression candidate

Status: OBSERVED
Confidence: MEDIUM
Source: Qwen3 8B T01
Needs replication: YES

### Observation

T01 introduced 5%, 15% and 30% thresholds without contextual justification and drew a stronger business-viability conclusion from them than the evidence supported.

### Implication

The evaluator should detect invented decision thresholds and unsupported conclusions, not merely factual hallucinations.

### Candidate regression

REG-UNSUPPORTED-THRESHOLD

### Do not promote yet

Requires replication across scenarios/models before becoming a permanent assertion.

## L-003 — Traceability reduces error-misattribution risk

Status: OBSERVED
Confidence: MEDIUM
Source: Qwen3 8B T16/T17/T18
Needs replication: YES

### Observation

T16 showed self-evaluation misattributing errors that were not present in the audited response. T17 improved when the task required exact textual traceability. T18 then exposed a different failure: a correctly negated statement was classified as the error itself.

### Implication

Error adjudication should not rely on model self-verdicts. It needs exact-text provenance plus semantic, polarity and context checks.

### Candidate regressions

- REG-SELF-EVALUATION-MISATTRIBUTION
- REG-NEGATION-REVERSAL
- REG-REPAIR-NONREPAIR
- REG-SELF-AUDIT-FAILURE

### Do not promote yet

These are strong architecture inputs, but replication and runtime tests remain necessary before declaring model-wide behavior.

## L-004 — Repair must preserve valid evidence

Status: OBSERVED
Confidence: MEDIUM
Source: Qwen3 8B T18
Needs replication: YES

### Observation

T18 removed or claimed to remove text that was actually a valid negation, and its repair verification did not independently establish that the problematic statement had disappeared.

### Implication

Repair should be a constrained transformation: modify demonstrated errors only, preserve valid evidence, then independently re-audit the resulting text.

## L-005 — Model qualification is distinct from Business Brain qualification

Status: ARCHITECTURAL LEARNING
Confidence: HIGH
Source: T01–T18 synthesis
Needs replication: NOT_APPLICABLE

### Observation

The same Business Brain contract can be evaluated across different concrete models. Model-specific strengths, weaknesses and adapter/runtime behavior must be recorded separately.

### Implication

A new model requires an adapter/profile and qualification evidence; it should not force a redesign of the provider-neutral Business Brain.

## L-006 — Runtime guardrails should be layered, not model-specific

Status: ARCHITECTURAL LEARNING
Confidence: HIGH
Source: T16–T18 synthesis
Needs replication: NOT_APPLICABLE

### Observation

Observed failures span generation, evaluation, self-audit, error attribution and repair. A single prompt instruction is insufficient as a reliable system boundary.

### Implication

Use layered controls:
Context Builder → Model → Parser → Evidence Adjudicator → Consistency Checker → Repair → Independent Re-audit → Evaluation Gate.
