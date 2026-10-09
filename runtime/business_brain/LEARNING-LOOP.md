# Business Brain integrated learning loop

## What this adds

The runner remains responsible for model execution. The integrated learning loop consumes its JSON output and runs the independent behavioral evaluator, semantic adjudicator, and explicit value-of-information (VoI) diagnostic. It produces one report plus an append-only JSONL ledger.

    Ollama / supported provider adapter
      → runner JSON (preserved as evidence)
      → behavioral evaluator
      → semantic adjudicator
      → explicit VoI diagnostic
      → consolidated report
      → append-only learning ledger
      → targeted sandbox repair + regression gate
      → human approval before material promotion

## Reproducible command

Run from the repository root after an existing real-model run:

    python -m runtime.business_brain.learning_loop evaluations/results/BUSINESS-BRAIN-T02-COMPACT-QWEN3-8B-640.json --report-out evaluations/results/BUSINESS-BRAIN-T02-COMPACT-QWEN3-8B-640-LEARNING.json --ledger evolution/learning-ledger.jsonl

The input is read-only. The report includes source and raw-output SHA-256 hashes, separate evaluator results, VoI factor evidence, traceable learning items, and the next stage. The ledger is append-only; rerunning adds a new record and does not erase previous evidence.

## Learning and safety contract

- A regression is recorded with its source, evidence, diagnosis, and next action.
- A finding is a candidate learning item, not automatic proof that the model alone is at fault.
- Corrections should target the responsible prompt, skill, context builder, adapter, evaluator, or scenario after attribution.
- Candidate repairs are tested in a sandbox and must pass regression tests before promotion.
- Production mutation is never performed by this script. Human approval is required for promotion.
- The loop evaluates a saved run; it does not regenerate model output. Model execution remains an explicit runner command.
- This release's runner natively supports fixture and Ollama. A cloud provider is usable only after a provider adapter is implemented and tested; provider neutrality of the evaluator does not imply cloud connectivity already exists.

## Current limitations

VoI detection is deterministic diagnostic support, not a complete semantic proof. It requires explicit factors in the priority rationale and can miss paraphrases. PARTIAL or FAIL requests review/targeted experiments, not automatic prompt mutation. Model qualification and Business Brain qualification remain separate.


## Controlled repair lifecycle

The `repair_workflow` CLI implements a gated lifecycle:

1. `propose`: select a supported regression from a learning report, record source hashes, target baseline hash, component mapping and diagnosis.
2. `stage`: place a human-authored Markdown candidate in `evolution/sandbox/<proposal-id>/candidate.md`. Candidate content is data; the system never executes model-generated text or patches.
3. `gate`: run a fixed allowlisted Python unittest suite, record command/output, candidate hash and pass/fail in the proposal and append-only audit ledger.
4. `promote`: require a passing gate, unchanged baseline, unchanged candidate, allowlisted Markdown target, named approver and exact approval phrase `PROMOTE <proposal-id> <candidate-sha256>`.

Only the final explicit `promote` command writes to a target, and target writes are restricted to Markdown files under `brains/`, `skills/`, `evaluations/`, `workflows/` or `knowledge/`. Runtime Python, shell scripts, path traversal and arbitrary test commands are not promotable. Model output cannot choose commands or be applied as an executable patch. Candidate content should be reviewed by a human before approval.

### CLI example

```powershell
python -m runtime.business_brain.repair_workflow propose evaluations/results/BUSINESS-BRAIN-T02-COMPACT-QWEN3-8B-640-LEARNING.json --target skills/business-reasoning.md --out evolution/repairs/voi-repair.json
python -m runtime.business_brain.repair_workflow stage evolution/repairs/voi-repair.json --candidate path/to/human-reviewed-candidate.md
python -m runtime.business_brain.repair_workflow gate evolution/repairs/voi-repair.json
# Only after reviewing candidate content and a PASS gate:
python -m runtime.business_brain.repair_workflow promote evolution/repairs/voi-repair.json --approver "Full Name" --approval-phrase "PROMOTE <proposal-id> <candidate-sha256>"
```

Replace `skills/business-reasoning.md` with an existing intended Markdown target in the repository, and replace the placeholders in the approval phrase with the values in the proposal. The proposal command captures the current baseline hash; concurrent edits invalidate promotion.

The fixed regression gate checks the established runtime/evaluator unit tests. It does not prove business quality for arbitrary prose changes, so scenario-level evaluation and human review remain required before promoting a substantive skill/prompt revision. The gate is a minimum safety control, not a claim of semantic correctness.
