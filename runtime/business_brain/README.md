# Business Brain Runtime v0.1

Provider-neutral runtime for executing Business Brain contracts against interchangeable
models.

## Architecture

```
Context Builder
      ↓
Business Brain Contract
      ↓
Model Adapter
      ↓
Raw Model Response
      ↓
Evidence Adjudicator
      ↓
Consistency Checker
      ↓
Repair / Independent Re-audit
      ↓
Evaluation Gate
```

## Current adapter

- OllamaAdapter
- First qualified candidate: qwen3:8b
- Local endpoint: http://localhost:11434
- Standard-library HTTP client; no provider SDK dependency

## Validation modes

- HARNESS_VALIDATION: deterministic fixture validates runtime plumbing only.
- LLM_BEHAVIOR_VALIDATION: real model output evaluated against the Business Brain contract.

The harness PASS does not imply LLM behavior PASS.

## Guardrail philosophy

The runtime must compensate for observed model failure modes without redefining
the Business Brain around one model.

Important controls include:
- evidence/inference separation;
- declaration vs behavior;
- absence vs negative evidence;
- trace-based error attribution;
- negation/contrary test;
- repair-only-real-errors;
- independent repair verification;
- internal consistency checks.

## Qualification

See:
- `evaluations/MODEL-QUALIFICATION-BATTERY-v0.1.md`
- `evaluations/model-profiles/qwen3-8b.yaml`

Block 2 remains OPEN until real-model behavioral validation is reproducible and
material regressions are addressed.


## Context Integrity Gate

Before behavioral evaluation, the runtime checks that constructed context is non-empty, contains expected Business Brain/runtime markers, and contains no known manual-test placeholders. It records character counts and SHA-256 provenance. INVALID_CONTEXT results are not adjudicated as model behavior.

## Evolution

Business Brain participates in the shared evolution protocol. Learning, proposals and sandbox experiments are versioned separately from production mutation. See evolution/IMPROVEMENT-PROTOCOL.md.
