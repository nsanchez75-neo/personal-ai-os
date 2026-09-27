# MODEL QUALIFICATION BATTERY v0.1

## Purpose

Qualify a concrete model for use by the provider-neutral Business Brain runtime.

A model profile records observed capabilities and limitations. It does not redefine
the Business Brain around that model.

## Qualification layers

### Layer 1 — Smoke
- adapter connectivity;
- response extraction;
- system/user instruction following;
- metadata capture;
- structured-output readiness.

### Layer 2 — Critical behavioral
Prioritize observed regression risks:
- unsupported numeric assumptions;
- declaration vs behavior;
- evidence vs inference;
- absence vs negative evidence;
- information-value prioritization;
- hypothesis/experiment alignment;
- internal consistency;
- negation reversal;
- self-audit reliability;
- error attribution;
- repair verification.

### Layer 3 — Full qualification
Run the fixed T01–T18 battery when the model is a serious candidate.

## Qualification result

Use:
- QUALIFIED
- CONDITIONAL
- NOT_QUALIFIED
- INSUFFICIENT_EVIDENCE

Never infer model-wide capability from one scenario.

## Evidence requirements

For every observed limitation record:
- model/provider;
- test id;
- prompt version;
- runtime parameters;
- elapsed time;
- visible output;
- exact problematic text;
- evaluator reasoning;
- severity;
- replication status.

## Core invariants vs model-sensitive tests

Core invariants belong to Business Brain behavior and must survive model changes.

Model-sensitive tests measure:
- reasoning reliability;
- instruction following;
- consistency;
- context handling;
- structured output;
- tool use;
- self-correction.

Adapter tests measure:
- transport;
- protocol;
- timeout/error handling;
- thinking/temperature mapping;
- metadata extraction.

## Portability rule

Changing model should not require changing the Business Brain architecture.
It should require:
1. an adapter;
2. a model profile;
3. qualification evidence;
4. targeted regression tests;
5. full qualification when warranted.
