# BUSINESS BRAIN RUNTIME v0.1 — SMOKE BATTERY

## Purpose

Fast qualification gate for the real-model runtime before targeted regressions or the full T01–T18 battery.

The smoke battery checks:
1. customer/evidence discipline;
2. declaration vs behavior;
3. evidence vs inference / negation-sensitive guardrails.

It is not a Business Brain qualification by itself.

## Execution

    powershell
    python -m runtime.business_brain.runner `
      --provider ollama `
      --model qwen3:8b `
      --thinking `
      --temperature 0.6 `
      --scenarios evaluations/SMOKE-BUSINESS-BRAIN-v0.1.md `
      --output evaluations/results/BUSINESS-BRAIN-v0.1-SMOKE-QWEN3-8B.json

## Scenario 01 — Customer before solution

**Input:** Founder wants to build an AI scheduling app because competitors have one. No customer interviews, observed behavior or transactions exist.

**Required assertions:**
- identify missing customer/problem evidence;
- do not treat the feature idea as validated demand;
- propose a small customer-discovery or behavioral test;
- distinguish facts from assumptions.

## Scenario 02 — Stated preference vs behavior

**Input:** Several target customers say they would pay for a service, but none has paid, pre-ordered or accepted a binding commercial commitment.

**Required assertions:**
- distinguish stated preference from behavioral/economic evidence;
- do not claim willingness to pay is validated;
- propose a behavioral validation step;
- preserve uncertainty about offer, price, segment and context.

## Scenario 03 — Evidence vs inference

**Input:** Three customers paid in a founder-known context. Delivery costs and repeatable acquisition are not measured. A draft conclusion says: "The payments demonstrate that the business is profitable and scalable."

**Required assertions:**
- identify payments as evidence relevant to willingness to pay in the observed context;
- reject payment → profitability inference;
- reject payment → scalability/repeatable acquisition inference;
- preserve contextual scope and residual uncertainty;
- if the draft conclusion is discussed, recognize that the wording overstates the evidence.

## Smoke gate

The smoke run is considered technically usable only when:
- Ollama returns a real response for every scenario;
- raw output and runtime metadata are preserved;
- consistency findings are recorded;
- no transport/parser failure occurs.

Behavioral qualification remains conditional until the assertions are reviewed against the actual model outputs.