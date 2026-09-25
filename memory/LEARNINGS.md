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
