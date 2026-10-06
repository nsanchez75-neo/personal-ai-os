"""Controlled Ollama inference profiling for the Business Brain runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any

from runtime.business_brain.adapters.ollama import OllamaAdapter
from runtime.business_brain.context import build_context
from runtime.business_brain.runner import check_context_integrity

DEFAULT_SYSTEM_PROMPT = 'Return exactly one short JSON object: {"status":"ok"}.'
DEFAULT_TASK = DEFAULT_SYSTEM_PROMPT
DEFAULT_CONTEXT_PATH = "brains/business/BUSINESS-BRAIN-SYSTEM-PROMPT.md"
DEFAULT_T02_PATH = "evaluations/T02-COMPACT-v0.1.md"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _seconds(ns: Any) -> float | None:
    if not isinstance(ns, (int, float)):
        return None
    return ns / 1_000_000_000


def _rate(count: Any, duration_ns: Any) -> float | None:
    seconds = _seconds(duration_ns)
    if not isinstance(count, (int, float)) or not seconds or seconds <= 0:
        return None
    return count / seconds


def _generation_status(metadata: dict[str, Any]) -> tuple[str, str]:
    if metadata.get("timeout"):
        return "TIMEOUT", metadata.get("error", "model request timed out")
    if metadata.get("done") is not True:
        return "GENERATION_INCOMPLETE", f"done={metadata.get('done')!r}"
    reason = metadata.get("done_reason")
    if reason == "length":
        return "TRUNCATED", "Ollama stopped at the requested token limit"
    if reason not in (None, "stop"):
        return "GENERATION_INCOMPLETE", f"done_reason={reason!r}"
    return "COMPLETE", "generation completed"


def _extract_t02_input(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8")
    match = re.search(r"\*\*Input:\*\*\s*(.+?)(?=\n\n|\n##|$)", text, re.S)
    if not match:
        raise ValueError(f"Could not extract canonical Input from {path}")
    return match.group(1).strip()


def _probe_definitions(context_path: str, t02_path: str) -> dict[str, dict[str, Any]]:
    full_context = build_context(context_path)
    t02_input = _extract_t02_input(t02_path)
    return {
        "minimal": {
            "description": "Tiny baseline.",
            "system_prompt": DEFAULT_SYSTEM_PROMPT,
            "task": DEFAULT_TASK,
            "context_kind": "minimal",
        },
        "json": {
            "description": "Small JSON generation without Business Brain context.",
            "system_prompt": "You are a deterministic test endpoint. Return only valid JSON.",
            "task": '{"status":"ok","answer":"ready"}',
            "context_kind": "json",
        },
        "full-context": {
            "description": "Full Business Brain context plus trivial task.",
            "system_prompt": full_context,
            "task": DEFAULT_TASK,
            "context_kind": "business_brain",
        },
        "t02": {
            "description": "Full Business Brain context plus canonical T02 input.",
            "system_prompt": full_context,
            "task": t02_input,
            "context_kind": "business_brain_t02",
        },
    }


def _run_one(
    adapter: OllamaAdapter,
    probe_name: str,
    repetition: int,
    probe: dict[str, Any],
) -> dict[str, Any]:
    system_prompt = probe["system_prompt"]
    task = probe["task"]
    integrity = check_context_integrity(system_prompt, task)

    started = time.perf_counter()
    try:
        response = adapter.generate(system_prompt, task)
    except TimeoutError as exc:
        response = None
        timeout_error = str(exc)
    else:
        timeout_error = None
    wall_seconds = time.perf_counter() - started

    if response is None:
        metadata: dict[str, Any] = {
            "timeout": True,
            "error": timeout_error or "timeout",
        }
        text = ""
    else:
        metadata = dict(response.metadata)
        text = response.text

    status, reason = _generation_status(metadata)
    return {
        "probe": probe_name,
        "repetition": repetition,
        "description": probe["description"],
        "context_kind": probe["context_kind"],
        "status": status,
        "status_reason": reason,
        "wall_time_seconds": round(wall_seconds, 4),
        "prompt": {
            "system_chars": len(system_prompt),
            "task_chars": len(task),
            "combined_chars": len(system_prompt) + len(task),
            "system_sha256": _sha256(system_prompt),
            "task_sha256": _sha256(task),
        },
        "context_integrity": integrity,
        "generation": {
            "done": metadata.get("done"),
            "done_reason": metadata.get("done_reason"),
            "prompt_eval_count": metadata.get("prompt_eval_count"),
            "eval_count": metadata.get("eval_count"),
            "prompt_eval_duration_ns": metadata.get("prompt_eval_duration_ns"),
            "eval_duration_ns": metadata.get("eval_duration_ns"),
            "total_duration_ns": metadata.get("total_duration_ns"),
            "load_duration_ns": metadata.get("load_duration_ns"),
            "prompt_tokens_per_second": _rate(
                metadata.get("prompt_eval_count"),
                metadata.get("prompt_eval_duration_ns"),
            ),
            "generation_tokens_per_second": _rate(
                metadata.get("eval_count"),
                metadata.get("eval_duration_ns"),
            ),
        },
        "output": {
            "chars": len(text),
            "sha256": _sha256(text),
            "preview": text[:500],
        },
    }


def profile(
    output_path: str,
    probes: list[str],
    model: str = "qwen3:8b",
    base_url: str = "http://localhost:11434",
    temperature: float = 0.6,
    thinking: bool = False,
    timeout: int = 180,
    num_predict: int = 128,
    context_path: str = DEFAULT_CONTEXT_PATH,
    t02_path: str = DEFAULT_T02_PATH,
    repeat: int = 1,
) -> dict[str, Any]:
    if repeat < 1:
        raise ValueError("repeat must be >= 1")

    definitions = _probe_definitions(context_path, t02_path)
    adapter = OllamaAdapter(
        model=model,
        base_url=base_url,
        temperature=temperature,
        thinking=thinking,
        timeout=timeout,
        num_predict=num_predict,
    )

    results = []
    for probe_name in probes:
        if probe_name not in definitions:
            raise ValueError(f"Unknown probe: {probe_name}")
        for repetition in range(1, repeat + 1):
            results.append(
                _run_one(adapter, probe_name, repetition, definitions[probe_name])
            )

    payload = {
        "profiling_mode": "OLLAMA_INFERENCE_PROFILING",
        "version": "0.2",
        "model": model,
        "provider": "ollama",
        "probe_count": len(results),
        "repeat": repeat,
        "results": results,
    }
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Profile Ollama inference cost without scoring Business Brain behavior."
    )
    parser.add_argument(
        "--probe",
        nargs="+",
        choices=["minimal", "json", "full-context", "t02", "all"],
        default=["all"],
    )
    parser.add_argument(
        "--output",
        default="evaluations/results/OLLAMA-PROFILE-QWEN3-8B.json",
    )
    parser.add_argument("--model", default="qwen3:8b")
    parser.add_argument("--base-url", default="http://localhost:11434")
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--thinking", action="store_true")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--num-predict", type=int, default=128)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--context-path", default=DEFAULT_CONTEXT_PATH)
    parser.add_argument("--t02-path", default=DEFAULT_T02_PATH)
    args = parser.parse_args()

    if args.repeat < 1:
        parser.error("--repeat must be >= 1")

    probes = (
        ["minimal", "json", "full-context", "t02"]
        if "all" in args.probe
        else args.probe
    )
    payload = profile(
        output_path=args.output,
        probes=probes,
        model=args.model,
        base_url=args.base_url,
        temperature=args.temperature,
        thinking=args.thinking,
        timeout=args.timeout,
        num_predict=args.num_predict,
        context_path=args.context_path,
        t02_path=args.t02_path,
        repeat=args.repeat,
    )

    summary = []
    for item in payload["results"]:
        generation = item["generation"]
        summary.append(
            {
                "probe": item["probe"],
                "repetition": item["repetition"],
                "status": item["status"],
                "wall_seconds": item["wall_time_seconds"],
                "prompt_chars": item["prompt"]["combined_chars"],
                "prompt_tokens": generation["prompt_eval_count"],
                "prompt_seconds": round(
                    _seconds(generation["prompt_eval_duration_ns"]) or 0, 3
                ),
                "output_tokens": generation["eval_count"],
                "generation_seconds": round(
                    _seconds(generation["eval_duration_ns"]) or 0, 3
                ),
                "output_tokens_per_second": generation["generation_tokens_per_second"],
                "done_reason": generation["done_reason"],
            }
        )
    print(
        json.dumps(
            {"profiling_mode": payload["profiling_mode"], "results": summary},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
