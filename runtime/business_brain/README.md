# Business Brain Runtime

Minimal provider-neutral runtime/evaluator for Business Brain v0.1.

Validation modes:
- HARNESS_VALIDATION: deterministic fixture validates loading, adapter contract, assertion evaluation and serialization. It does NOT prove LLM behavior.
- LLM_BEHAVIOR_VALIDATION: future real-model adapters use the same contract.

The core has no provider SDK dependency. Legacy skills remain out of scope until real-model runtime validation is available.
