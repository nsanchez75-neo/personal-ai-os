# BUSINESS BRAIN REGRESSION CATALOG v0.1

## Purpose

Centralize observed failure modes from T01–T18 so future model/runtime tests can target
the same failure classes without coupling the Business Brain to one model.

| Regression | Evidence | Current status |
|---|---|---|
| REG-UNSUPPORTED-NUMERIC-ASSUMPTION | T01, T03, T05, T06, T07, T11 | OBSERVED |
| REG-DECLARATION-VS-BEHAVIOR | T02, T03, T06, T08, T09 | OBSERVED |
| REG-MINIMUM-CREDIBLE-EXPERIMENT | T03, T04, T06 | OBSERVED |
| REG-INFORMATION-VALUE-PRIORITIZATION | T04, T05, T06, T07, T08, T09 | OBSERVED |
| REG-INTERNAL-CONSISTENCY | T06, T12, T13 | OBSERVED |
| REG-ADVERSARIAL-SELF-CHECK | T03, T05, T06, T07, T11, T12, T13 | OBSERVED |
| REG-SELF-AUDIT-FAILURE | T07, T12, T13, T18 | OBSERVED |
| REG-HYPOTHESIS-EXPERIMENT-MISMATCH | T07, T08, T11 | OBSERVED |
| REG-EVIDENCE-GRADING-COLLAPSE | T13, T14 | OBSERVED |
| REG-SELF-EVALUATION-MISATTRIBUTION | T16 | OBSERVED |
| REG-REPAIR-NONREPAIR | T16, T18 | OBSERVED |
| REG-EPISTEMIC-OVERCOMMITMENT | T09, T12, T13, T14 | OBSERVED |
| REG-NEGATION-REVERSAL | T18 | OBSERVED |

## Important interpretation

"Observed" means the failure occurred under at least one test condition. It does not
mean the model fails every time or that the regression is universal across models.

## Architecture response

The runtime addresses these classes with:
- provider-neutral model profiles;
- evidence/inference boundaries;
- trace-based adjudication;
- negation/contrary checks;
- consistency checks;
- constrained repair;
- independent re-audit;
- qualification batteries.

## Promotion rule

A regression becomes a durable acceptance assertion only when:
1. the behavior is reproduced;
2. the failure mechanism is understood;
3. the responsible layer is identified;
4. the fix is tested;
5. no material regression is introduced.
