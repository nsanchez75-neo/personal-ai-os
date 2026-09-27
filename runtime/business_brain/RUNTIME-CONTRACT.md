# BUSINESS BRAIN RUNTIME CONTRACT v0.1

## Purpose

Execute the Business Brain through interchangeable model providers while keeping
business reasoning, evidence rules and human authority provider-neutral.

## Runtime pipeline

USER / SCENARIO
→ CONTEXT BUILDER
→ BUSINESS BRAIN CONTRACT
→ MODEL ADAPTER
→ RAW MODEL RESPONSE
→ OUTPUT PARSER
→ EVIDENCE ADJUDICATOR
→ CONSISTENCY CHECKER
→ REPAIR (only when justified)
→ INDEPENDENT RE-AUDIT
→ EVALUATION GATE

## Non-negotiable invariants

1. Evidence is not the same as conclusion.
2. Declaration is not the same as behavior.
3. Absence of evidence is not negative evidence.
4. Payment is not proof of profitability, scalability, repeatable acquisition or retention.
5. Contextual evidence must not be generalized without support.
6. Mentioning an error theme is not committing the error.
7. A candidate error is not an actual error until traceability and semantic checks support it.
8. Negation must be checked before classifying a candidate error.
9. Repairs must change only demonstrated errors and preserve valid information.
10. A repair is not accepted until an independent re-audit verifies the repaired text.
11. Self-evaluation is evidence to inspect, not authoritative ground truth.
12. Material or irreversible actions require human approval.

## Evidence record

Where practical, represent evidence with separate dimensions:

- observation;
- existence;
- relevance;
- support strength;
- attribution/confounding;
- contamination;
- scope/generalization;
- contradiction;
- inference;
- residual uncertainty.

Do not collapse these dimensions into one binary "validated/not validated" label.

## Error attribution protocol

For every candidate error:

1. locate exact text;
2. determine whether the semantic phenomenon is actually present;
3. check polarity/negation;
4. inspect surrounding context;
5. run a contrary test;
6. classify: NO_PRESENTE / ERROR_REAL / INDETERMINATE;
7. repair only ERROR_REAL;
8. verify the repair independently;
9. check for over-correction and internal inconsistency.

## Runtime gate

- PASS: no material invariant violation detected.
- REPAIR: a demonstrated repairable violation exists.
- HUMAN: high-impact or irreversible decision requires approval.
- FAIL: runtime contract cannot be trusted for the requested operation.

The deterministic checks are guardrails, not substitutes for semantic model evaluation.
