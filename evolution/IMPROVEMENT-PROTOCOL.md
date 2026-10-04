# Improvement Protocol v0.1

## 1. Purpose

Provide a repeatable, auditable loop for improving any AI Factory component while preventing self-validation and uncontrolled mutation.

## 2. State model

`OBSERVED → HYPOTHESIS → PROPOSED → SANDBOXED → EVALUATED → REGRESSION_CHECKED → APPROVED → PROMOTED`

Terminal states: `REJECTED`, `BLOCKED`, `INSUFFICIENT_EVIDENCE`.

## 3. Evidence discipline

- An observation is not automatically a defect.
- A candidate defect is not an actual defect.
- A model self-assessment is not ground truth.
- A repair claim is not proof of repair.
- Historical evidence must not be silently rewritten.
- Absence of evidence is not negative evidence.
- Evidence must retain provenance and scope.

## 4. Improvement proposal

Every proposal should record:

- component and current version
- observed problem
- evidence and provenance
- hypothesis
- proposed change
- expected benefit
- regression risks
- evaluation plan
- promotion criteria
- rollback plan

## 5. Sandbox

Never mutate production directly. Evaluate the proposed change against a frozen baseline plus targeted tests and the relevant regression battery.

## 6. Regression gate

Promotion requires:

1. target failure improves or the evidence for the proposed change is otherwise sufficient;
2. existing critical behavior is preserved;
3. no unacceptable new regression appears;
4. provenance is recorded;
5. the promotion decision is auditable.

A change that improves one metric while materially damaging another is not automatically an improvement.

## 7. Human authority

Human approval is required for irreversible or high-impact changes, including production promotion of behavior rules, memory policies, permissions, tool access, safety constraints, or deletion/rewriting of historical evidence.

Reversible low-risk experiments may be automated inside a sandbox.

## 8. Promotion

Promotion creates a versioned Git change. The accepted proposal, evaluation evidence, regression result, and decision must be linked from the ledger.

## 9. Portability

The protocol is provider-neutral. Model-specific behavior belongs in model profiles/adapters, not in the core improvement contract.
