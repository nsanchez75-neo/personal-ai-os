# LEGACY EVALUATION INPUTS

The legacy archive contains 51 skill evaluation suites. Each typically contains:
- skill name
- test prompt
- expected output
- assertions

## Reusable evaluation standard

Every future skill should aim to define:
1. trigger/use case
2. required context
3. expected reasoning/output behavior
4. assertions/acceptance criteria
5. guardrails
6. failure cases
7. regression examples

## Reuse rule
Use legacy evals as seed regression cases. Normalize terminology and remove assumptions tied to the old repository layout.
