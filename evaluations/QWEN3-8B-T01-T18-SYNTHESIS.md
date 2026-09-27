# Qwen3 8B — T01–T18 Behavioral Synthesis

## Scope

This document records observed behavior from the fixed Qwen3 8B Business Brain battery.
It is evidence under the specific test protocol, not a universal model capability claim.

Runtime:
- Provider: Ollama
- Model: qwen3:8b
- Thinking: ON
- Visible final responses evaluated
- Elapsed time recorded during local execution

## Overall interpretation

T01–T18 provide sufficient architectural evidence to build guardrails, but not to
declare Qwen3 8B universally reliable or to close Block 2.

The model can demonstrate strong explicit understanding of evidence boundaries under
structured prompts, while still producing inconsistent application, self-audit,
attribution and repair behavior.

## Repeated/important observed risks

- REG-UNSUPPORTED-NUMERIC-ASSUMPTION
- REG-DECLARATION-VS-BEHAVIOR
- REG-MINIMUM-CREDIBLE-EXPERIMENT
- REG-INFORMATION-VALUE-PRIORITIZATION
- REG-INTERNAL-CONSISTENCY
- REG-ADVERSARIAL-SELF-CHECK
- REG-SELF-AUDIT-FAILURE
- REG-HYPOTHESIS-EXPERIMENT-MISMATCH
- REG-EVIDENCE-GRADING-COLLAPSE
- REG-SELF-EVALUATION-MISATTRIBUTION
- REG-REPAIR-NONREPAIR
- REG-EPISTEMIC-OVERCOMMITMENT
- REG-NEGATION-REVERSAL

## Key architectural findings

### 1. Evidence needs dimensions

Do not collapse evidence into a single binary label. Track:
- existence;
- relevance;
- support strength;
- attribution/confounding;
- contamination;
- scope/generalization;
- contradiction;
- inference;
- residual uncertainty.

### 2. Error attribution needs provenance

Use:

candidate
→ exact text
→ semantic phenomenon
→ negation/polarity
→ context
→ contrary test
→ classification

A model's self-verdict is not authoritative.

### 3. Repair needs independent verification

Repair only demonstrated errors, preserve valid evidence, and re-audit the repaired
response independently. "Deleted" is not evidence that the problematic text disappeared.

### 4. Prompt scaffolding helps but is not a sufficient system boundary

T10 and T17 show improved behavior under explicit structure. T16 and T18 show that
the same model can still fail self-attribution, negation handling and repair verification.

## Qualification state

**CONDITIONAL**

This status is provisional and must be updated only from reproducible runtime evidence.

Block 2 remains OPEN.
