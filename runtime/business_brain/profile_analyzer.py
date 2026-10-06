"""Analyze profiler JSON outputs without scoring model behavior.

This tool is execution-analysis only. It deliberately treats TRUNCATED/TIMEOUT
runs as non-evaluable for behavioral conclusions.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any


ANALYSIS_VERSION = "0.3"

METRICS = (
    "wall_seconds",
    "prompt_seconds",
    "generation_seconds",
    "output_tokens_per_second",
)


def _metric_value(row: dict[str, Any], key: str) -> Any:
    """Read metrics from the profiler's canonical nested schema, with legacy aliases."""
    aliases = {
        "wall_seconds": ["wall_time_seconds", "wall_seconds"],
        "prompt_seconds": ["generation.prompt_eval_duration_ns", "prompt_seconds"],
        "generation_seconds": ["generation.eval_duration_ns", "generation_seconds"],
        "output_tokens_per_second": [
            "generation.generation_tokens_per_second",
            "output_tokens_per_second",
        ],
    }
    for path in aliases.get(key, [key]):
        value: Any = row
        for part in path.split("."):
            if not isinstance(value, dict) or part not in value:
                value = None
                break
            value = value[part]
        if "_duration_ns" in path:
            if isinstance(value, (int, float)) and math.isfinite(value):
                return float(value) / 1_000_000_000
        elif isinstance(value, (int, float)) and math.isfinite(value):
            return float(value)
    return None


def _finite_values(rows: list[dict[str, Any]], key: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        value = _metric_value(row, key)
        if isinstance(value, (int, float)) and math.isfinite(value):
            values.append(float(value))
    return values


def _stats(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"n": 0, "min": None, "median": None, "max": None}
    return {
        "n": len(values),
        "min": min(values),
        "median": statistics.median(values),
        "max": max(values),
    }


def _load(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise ValueError(f"{path}: expected JSON object with a results array")
    rows = []
    for row in data["results"]:
        if isinstance(row, dict):
            item = dict(row)
            item["_source"] = str(path)
            rows.append(item)
    return rows


def analyze(paths: list[Path]) -> dict[str, Any]:
    rows = [row for path in paths for row in _load(path)]
    by_probe: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_probe.setdefault(str(row.get("probe", "unknown")), []).append(row)

    probes: dict[str, Any] = {}
    for probe, probe_rows in sorted(by_probe.items()):
        status_counts: dict[str, int] = {}
        for row in probe_rows:
            status = str(row.get("status", "UNKNOWN"))
            status_counts[status] = status_counts.get(status, 0) + 1

        metric_stats = {
            metric: _stats(_finite_values(probe_rows, metric))
            for metric in METRICS
        }

        complete = status_counts.get("COMPLETE", 0)
        truncated = status_counts.get("TRUNCATED", 0)
        timeout = status_counts.get("TIMEOUT", 0)
        if timeout and truncated:
            execution_class = "EXECUTION_MIXED_INCOMPLETE"
        elif timeout:
            execution_class = "TIMEOUT"
        elif truncated:
            execution_class = "EXECUTION_TRUNCATED"
        elif complete == len(probe_rows) and complete:
            execution_class = "EXECUTION_COMPLETE"
        else:
            execution_class = "EXECUTION_MIXED"

        complete_rows = [row for row in probe_rows if row.get("status") == "COMPLETE"]
        incomplete_rows = [
            row for row in probe_rows
            if row.get("status") in {"TRUNCATED", "TIMEOUT", "GENERATION_INCOMPLETE"}
        ]
        if complete_rows and incomplete_rows:
            behavioral_evaluation = "PARTIALLY_EVALUABLE"
        elif complete_rows:
            behavioral_evaluation = "POTENTIALLY_EVALUABLE"
        else:
            behavioral_evaluation = "NOT_EVALUABLE"

        probes[probe] = {
            "runs": len(probe_rows),
            "status_counts": status_counts,
            "complete_runs": len(complete_rows),
            "incomplete_runs": len(incomplete_rows),
            "execution_class": execution_class,
            "metrics": metric_stats,
            "behavioral_evaluation": behavioral_evaluation,
        }

    return {
        "analysis_version": ANALYSIS_VERSION,
        "mode": "OLLAMA_EXECUTION_PROFILING_ANALYSIS",
        "source_files": [str(path) for path in paths],
        "probes": probes,
        "global_rule": (
            "Execution completeness is a prerequisite for behavioral evaluation; "
            "TRUNCATED and TIMEOUT runs are not model-behavior failures."
        ),
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def render_text(report: dict[str, Any]) -> str:
    lines = [
        "QWEN3 EXECUTION PROFILING ANALYSIS",
        "=" * 34,
        "",
        "Rule: TRUNCATED/TIMEOUT = execution outcome, not behavioral failure.",
        "",
    ]
    for probe, data in report["probes"].items():
        lines.extend(
            [
                f"[{probe}]",
                f"  runs: {data['runs']}",
                f"  status: {data['status_counts']}",
                f"  execution_class: {data['execution_class']}",
                f"  complete_runs: {data['complete_runs']} / {data['runs']}",
                f"  incomplete_runs: {data['incomplete_runs']} / {data['runs']}",
                f"  behavioral_evaluation: {data['behavioral_evaluation']}",
            ]
        )
        for metric, stats in data["metrics"].items():
            lines.append(
                f"  {metric}: min={_fmt(stats['min'])} "
                f"median={_fmt(stats['median'])} max={_fmt(stats['max'])} "
                f"(n={stats['n']})"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="Profiler JSON files")
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path for the normalized analysis JSON",
    )
    parser.add_argument(
        "--text-out",
        type=Path,
        default=None,
        help="Optional path for the human-readable analysis",
    )
    args = parser.parse_args()

    report = analyze(args.files)
    text = render_text(report)
    print(text, end="")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    if args.text_out:
        args.text_out.parent.mkdir(parents=True, exist_ok=True)
        args.text_out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
