# CEO BRAIN — DECISION ENGINE v0.1

## Decision Record

```yaml
decision_id:
date:
objective:
decision_class: D0 | D1 | D2 | D3

situation:
desired_outcome:

facts: []
observations: []
unknowns: []
assumptions: []
hypotheses: []

constraints: []
options: []

tradeoffs:
opportunity_cost:

downside:
risks: []
mitigations: []
leading_indicators: []

reversibility:
time_to_information:
time_to_payoff:

disconfirming_evidence: []

scenario_analysis:
  base:
  upside:
  downside:

decision:
why_now:

action:
owner:
dependencies: []

primary_metric:
guardrail_metrics: []

review_date:
review_trigger:

human_approval_required:
approval_status:

postmortem:
prediction_vs_outcome:
lessons:
model_updates:
```

## Decision procedure

### 1. Define the objective
State what must become true.

### 2. Establish reality
Separate facts, observations, assumptions and unknowns.

### 3. Determine decision class
D0–D3.

### 4. Generate alternatives
Never evaluate only the first plausible option for material decisions.

Include:
- do nothing;
- smaller experiment;
- alternative approach;
- defer;
- stop.

### 5. Evaluate trade-offs
Explicitly identify:
- upside;
- downside;
- cost;
- opportunity cost;
- dependencies;
- second-order effects.

### 6. Test reversibility
Ask:
- Can we undo it?
- At what cost?
- How quickly?
- What becomes irreversible after execution?

### 7. Seek disconfirming evidence
Actively search for evidence that would invalidate the thesis.

### 8. Choose action proportional to uncertainty
High uncertainty + low downside → experiment.
High uncertainty + high downside → research + human review.
Low uncertainty + low downside → execute.
Low uncertainty + high impact → execute with governance.

### 9. Define measurement before action
At least one primary outcome and appropriate guardrails.

### 10. Define the review trigger
Time-based, metric-based or event-based.

### 11. Record
Material decisions go to DECISIONS.md or an appropriate durable decision record.

### 12. Learn
Compare predicted vs actual results and update assumptions.

## Anti-proxy rule

A metric is not the objective.

Every major KPI must answer:
- What underlying outcome does this proxy?
- When can the proxy become misleading?
- What second metric/qualitative signal prevents gaming?

## Capital allocation check

Before allocating scarce resources:

```
Strategic fit?
Customer value?
Expected upside?
Downside bounded?
Learning value?
Time to information?
Time to payoff?
Opportunity cost?
Reversibility?
Capability compounding?
```

## Pre-mortem

Before D2/D3 decisions:

> Assume this decision failed badly. What are the most plausible reasons?

Convert plausible failure modes into:
- mitigations;
- monitoring signals;
- stop conditions.

## Post-mortem

After resolution:

1. What did we predict?
2. What happened?
3. Which assumptions were wrong?
4. Which signals were missed?
5. Was the decision process good even if the outcome was bad?
6. Was the decision process bad even if the outcome was good?
7. What should change?

Outcome quality and decision quality must be evaluated separately.
