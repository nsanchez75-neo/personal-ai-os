"""Integrated Business Brain evaluation and append-only learning ledger.

Consumes an existing runner result, evaluates it independently, and records
traceable learning items. It never edits prompts, skills, memory, or production
behavior automatically.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from runtime.business_brain.t02_behavioral_evaluator import evaluate_payload
from runtime.business_brain.t02_semantic_adjudicator import adjudicate_payload


def _raw_text(payload: dict[str, Any]) -> str:
    results = payload.get("results") or []
    if results and isinstance(results[0], dict):
        raw = results[0].get("raw_output")
        if isinstance(raw, str):
            return raw
    outputs = payload.get("raw_outputs") or []
    if outputs and isinstance(outputs[0], dict):
        return str(outputs[0].get("text") or "")
    return ""


def _learning_items(behavioral: dict[str, Any], semantic: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for finding in behavioral.get("findings", []):
        if finding.get("status") in {"FAIL", "PARTIAL"}:
            items.append({
                "id": finding.get("id", "UNCLASSIFIED"),
                "source": "behavioral_evaluator",
                "severity": finding.get("status"),
                "evidence": finding.get("evidence", ""),
                "diagnosis": finding.get("reason", ""),
                "next_action": "Create a targeted sandbox experiment and regression test.",
            })
    for regression in semantic.get("regressions", []):
        items.append({
            "id": regression.get("id", "UNCLASSIFIED"),
            "source": "semantic_adjudicator",
            "severity": regression.get("status", "OBSERVED"),
            "evidence": "",
            "diagnosis": regression.get("reason", ""),
            "next_action": "Trace to the responsible prompt/skill/runtime item; propose a sandbox-only repair.",
        })
    # Keep separate evidence sources, but avoid duplicate item records in one run.
    deduped: dict[tuple[str, str], dict[str, Any]] = {}
    for item in items:
        key = (str(item["id"]), str(item["source"]))
        deduped[key] = item
    return list(deduped.values())


def evaluate_run(payload: dict[str, Any], source_bytes: bytes) -> dict[str, Any]:
    behavioral = evaluate_payload(payload)
    semantic = adjudicate_payload(payload)
    raw = _raw_text(payload)
    provider = payload.get("provider", "unknown")
    model = payload.get("model", "unknown")
    learning_items = _learning_items(behavioral, semantic)
    now = datetime.now(timezone.utc).isoformat()
    run_id = hashlib.sha256(source_bytes).hexdigest()[:16]
    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "created_at_utc": now,
        "source": {
            "provider": provider,
            "model": model,
            "validation_mode": payload.get("validation_mode", "unknown"),
            "sha256": hashlib.sha256(source_bytes).hexdigest(),
            "raw_output_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        },
        "evaluation": {
            "behavioral": behavioral,
            "semantic": semantic,
            "overall": (
                "INVALID_EXECUTION"
                if "INVALID_EXECUTION" in {behavioral.get("status"), semantic.get("status")}
                else "FAIL"
                if "FAIL" in {behavioral.get("status"), semantic.get("status")}
                else "CONDITIONAL"
                if learning_items or behavioral.get("status") == "CONDITIONAL_PASS" or semantic.get("status") == "PARTIAL"
                else "PASS"
            ),
        },
        "learning": {
            "items": learning_items,
            "next_stage": "SANDBOX_AND_REGRESSION_GATE" if learning_items else "MONITOR",
            "production_mutation_allowed": False,
            "human_approval_required_for_promotion": True,
            "principle": "Learning is not mutation; preserve evidence and validate candidate repairs before promotion.",
        },
    }


def run(input_path: Path, report_path: Path, ledger_path: Path) -> dict[str, Any]:
    source_bytes = input_path.read_bytes()
    payload = json.loads(source_bytes.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("runner result must be a JSON object")
    report = evaluate_run(payload, source_bytes)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    # Append-only: never overwrite earlier learning evidence.
    with ledger_path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps({
            "run_id": report["run_id"],
            "created_at_utc": report["created_at_utc"],
            "source_sha256": report["source"]["sha256"],
            "overall": report["evaluation"]["overall"],
            "learning_items": report["learning"]["items"],
            "next_stage": report["learning"]["next_stage"],
            "production_mutation_allowed": False,
        }, ensure_ascii=False) + "\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Existing Business Brain runner JSON; preserved unchanged")
    parser.add_argument("--report-out", type=Path, default=Path("evaluations/results/BUSINESS-BRAIN-LEARNING-REPORT.json"))
    parser.add_argument("--ledger", type=Path, default=Path("evolution/learning-ledger.jsonl"))
    args = parser.parse_args()
    report = run(args.input, args.report_out, args.ledger)
    print(json.dumps({
        "run_id": report["run_id"],
        "overall": report["evaluation"]["overall"],
        "behavioral": report["evaluation"]["behavioral"].get("status"),
        "semantic": report["evaluation"]["semantic"].get("status"),
        "learning_items": len(report["learning"]["items"]),
        "next_stage": report["learning"]["next_stage"],
        "production_mutation_allowed": False,
        "report": str(args.report_out),
        "ledger": str(args.ledger),
    }, ensure_ascii=False, indent=2))
    return 2 if report["evaluation"]["overall"] == "INVALID_EXECUTION" else 0


if __name__ == "__main__":
    raise SystemExit(main())
