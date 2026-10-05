# T02-COMPACT v0.1 — Value of Information / Uncertainty Prioritization

**Purpose:** Canonicalize the previously manual T02-COMPACT experiment so it is executed through the provider-neutral runtime with full context and generation provenance.

**Status:** OPEN — real-model behavioral validation pending.

## Scenario 02 — Value of information / uncertainty prioritization

**Input:** A consultancy has several people who expressed that they would pay, but nobody has paid. Price is untested, delivery costs are unknown, repeatable acquisition is unknown, and delegation consistency is unknown. The five uncertainties are: A = problem importance, B = real willingness to pay, C = repeatable acquisition, D = delivery economics/cost, E = standardize/delegate. Only one experiment may be chosen. Do not invent price, percentage, sample size, duration, cost or threshold. Do not assume B must be first merely because nobody paid. Do not assume D must be first merely because costs are unknown. If the available information is insufficient to establish a priority, return an indeterminate or conditional priority. Consider decision impact, current evidence, uncertainty, information cost, reversibility and ability to change the decision. Distinguish declarations from behavior and absence of evidence from negative evidence. Return JSON with: uncertainties (id, decision_impact, current_evidence), priority (status, selected, reason), experiment (tests, observable_behavior, evidence_for, evidence_against), legitimate_conclusions, illegitimate_conclusions.

**Required assertions:**
- compare A-E using decision impact, uncertainty, information cost, reversibility and decision-changing ability rather than a fixed dependency order;
- do not automatically prioritize B because there has been no payment;
- do not automatically prioritize D because delivery cost is unknown;
- distinguish expressed willingness from behavioral/economic evidence;
- do not invent price, percentage, sample size, duration, cost or threshold;
- allow an indeterminate or conditional priority when the available information cannot justify a unique ranking;
- design the experiment so the observable behavior is relevant to the selected uncertainty;
- distinguish absence of evidence from evidence against a hypothesis;
- keep conclusions within the evidence actually produced by the experiment;
- return the requested JSON structure.

## Behavioral evaluation note

This scenario must be evaluated from the raw model output, generation metadata and context-integrity metadata. The legacy lexical evaluator is a harness aid, not sufficient semantic adjudication for this compact experiment.

A complete generation is required before behavioral scoring:
- context_integrity.status = CLEAR;
- generation_gate.status = COMPLETE;
- JSON must be valid before the structured output is treated as executable evidence.

A timeout, truncation, invalid context or malformed JSON is a test-execution result, not a Business Brain behavioral failure.