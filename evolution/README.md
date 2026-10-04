# Evolution / Improvement Loop v0.1

The Evolution Loop is the provider-neutral mechanism for improving brains, agents, skills, and workflows without allowing uncontrolled self-modification.

## Core rule

**Learning is not mutation.** An observation can change what the system believes about a component without changing the component itself.

## Lifecycle

OBSERVE → EVIDENCE → DIAGNOSE → HYPOTHESIZE → PROPOSE → SANDBOX → EVALUATE → REGRESSION GATE → APPROVE → PROMOTE → MONITOR → LEARN

Changes that affect production behavior, permissions, memory, tools, safety rules, or promotion require human approval.

## Scope

The same protocol is reusable by Business Brain, CEO Brain, AI Architect, agents, skills, and workflows. GitHub is the source of truth and every accepted change must remain versioned and auditable.

## Directories

- `IMPROVEMENT-PROTOCOL.md` — operating contract
- `IMPROVEMENT-LEDGER.md` — append-only improvement history
- `hypotheses/` — improvement hypotheses
- `proposals/` — versioned change proposals
- `experiments/` — sandbox experiment records
- `evaluations/` — evaluation reports
- `regressions/` — regression findings
- `promotions/` — approved promotions

The initial implementation is a governance and artifact protocol. It does not claim autonomous production mutation.
