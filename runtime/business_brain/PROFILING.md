# Ollama Runtime Profiling Harness v0.2

## Purpose

This harness measures inference cost and execution behavior. It is not a Business Brain behavioral evaluator and it does not modify T02.

Controlled probes:

1. minimal — tiny prompt/task baseline.
2. json — small JSON-generation baseline.
3. full-context — full Business Brain runtime context + trivial task.
4. t02 — full Business Brain runtime context + canonical T02 input.

For every probe it records:
- wall-clock duration;
- model, provider, thinking, temperature, timeout and num_predict;
- system/task/combined prompt size and SHA-256;
- context-integrity status;
- Ollama done / done_reason;
- prompt/evaluation token counts;
- prompt/evaluation/total/load durations;
- prompt and evaluation tokens/second;
- output length and SHA-256;
- timeout/truncation/incomplete status.

A timeout or truncation is an execution observation, not a Business Brain behavioral verdict.

## Diagnostic ladder

    minimal
      ↓
    JSON
      ↓
    full Business Brain context
      ↓
    full Business Brain context + T02

This isolates baseline model/runtime cost, small structured-output cost, context/prompt cost, and task-specific generation cost.

The canonical T02 scenario is read from evaluations/T02-COMPACT-v0.1.md. Its text is not modified, its assertions are not passed to the model, and this harness does not score its behavioral correctness.

## PowerShell — canonical profiling run

Run from the repository root:

```powershell
git pull --ff-only origin main

python -m runtime.business_brain.profiler `
  --probe all `
  --model qwen3:8b `
  --temperature 0.6 `
  --timeout 180 `
  --num-predict 128 `
  --output evaluations/results/OLLAMA-PROFILE-QWEN3-8B.json
```

Expected console output is a compact JSON summary with one row per probe.

## If a probe times out

Do not interpret that as a Business Brain failure. First isolate the probe:

```powershell
python -m runtime.business_brain.profiler `
  --probe minimal json `
  --model qwen3:8b `
  --temperature 0.6 `
  --timeout 120 `
  --num-predict 64 `
  --output evaluations/results/OLLAMA-PROFILE-QWEN3-8B-MINIMAL-JSON.json
```

Then test only the full context:

```powershell
python -m runtime.business_brain.profiler `
  --probe full-context `
  --model qwen3:8b `
  --temperature 0.6 `
  --timeout 180 `
  --num-predict 64 `
  --output evaluations/results/OLLAMA-PROFILE-QWEN3-8B-CONTEXT.json
```

Finally test the canonical T02 input:

```powershell
python -m runtime.business_brain.profiler `
  --probe t02 `
  --model qwen3:8b `
  --temperature 0.6 `
  --timeout 180 `
  --num-predict 128 `
  --output evaluations/results/OLLAMA-PROFILE-QWEN3-8B-T02.json
```

## Interpretation

Use the JSON result rather than console time alone.

Key comparisons:
- minimal slow → baseline local inference bottleneck.
- minimal fast but full-context much slower → context/prompt processing cost.
- full-context completes but t02 times out → task generation cost or requested output budget is the main suspect.
- done_reason = length → generation reached num_predict; this is truncation, not behavioral failure.
- TIMEOUT → insufficient execution budget for that probe; no behavioral score is assigned.

The profiler is intentionally separate from the canonical Business Brain evaluation runner. Its job is to tell us what the runtime costs before we optimize prompts, token budgets, model selection, or provider adapters.

## Repetition and phase timing

The profiler supports `--repeat N` to expose local runtime variability. The console summary now includes prompt-processing seconds and generation seconds separately. The JSON artifact retains the raw Ollama nanosecond counters.

Recommended diagnostic run after pulling the latest commit:

```powershell
python -m runtime.business_brain.profiler `
  --probe minimal json `
  --model qwen3:8b `
  --temperature 0.6 `
  --timeout 120 `
  --num-predict 64 `
  --repeat 3 `
  --output evaluations/results/OLLAMA-PROFILE-QWEN3-8B-BASELINE.json
```

Then run the context/task probes once:

```powershell
python -m runtime.business_brain.profiler `
  --probe full-context t02 `
  --model qwen3:8b `
  --temperature 0.6 `
  --timeout 180 `
  --num-predict 128 `
  --output evaluations/results/OLLAMA-PROFILE-QWEN3-8B-CONTEXT-T02.json
```
