"""Deterministic behavioral evaluator for canonical T02-COMPACT output.

This evaluator is deliberately conservative. It does not infer correctness from
lexical overlap alone and never treats the model's self-audit as ground truth.
It evaluates the raw structured response plus execution gates.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

REQUIRED_KEYS = (
    "uncertainties",
    "priority",
    "experiment",
    "legitimate_conclusions",
    "illegitimate_conclusions",
)

FORBIDDEN_PARAMETER_PATTERNS = (
    r"\b\d+(?:\.\d+)?\s*%",
    r"\b(?:sample|muestra)\s+(?:de\s+)?\d+",
    r"\b(?:n|N)\s*=\s*\d+",
    r"\b(?:€|\$|USD|EUR)\s*\d+",
    r"\b\d+\s*(?:€|\$|USD|EUR)",
)

DECLARATION_PATTERNS = (
    r"would pay",
    r"\bpagarían\b",
    r"\bpagarían\b",
    r"\bexpresaron\b",
    r"\bsaid they would",
    r"\bdeclara",
    r"\bdeclar",
    r"\bexpressed",
)
BEHAVIOR_PATTERNS = (
    r"payment",
    r"pago",
    r"pay",
    r"pag[ao]",
    r"purchase",
    r"compra",
    r"transaction",
    r"transacci",
)

NEGATIVE_ABSENCE_PATTERNS = (
    r"absence of evidence",
    r"absence",
    r"\bno evidence\b",
    r"ausencia de evidencia",
    r"no hay evidencia",
    r"no evidencia",
    r"no se ha probado",
    r"untested",
    r"no probado",
)

VI_NEGATION_PATTERNS = (
    r"not automatically",
    r"no automáticamente",
    r"no asumir",
    r"no necesariamente",
    r"indeterminate",
    r"indeterminado",
    r"conditional",
    r"condicional",
)

OVERREACH_PATTERNS = (
    r"proves? profitability",
    r"demuestra.*rentabilidad",
    r"proves?.*scal",
    r"demuestra.*escal",
    r"proves?.*repeatable",
    r"demuestra.*adquisición.*repet",
    r"proves?.*retention",
    r"demuestra.*retención",
    r"fully validated",
    r"validado completamente",
    r"business validated",
    r"negocio validado",
)


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(_text(x) for x in value)
    if isinstance(value, dict):
        return " ".join(f"{k} {_text(v)}" for k, v in value.items())
    return str(value)


def _has(text: str, patterns: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(re.search(p, lower, flags=re.I) for p in patterns)


def _finding(check_id: str, status: str, evidence: str, reason: str) -> dict[str, str]:
    return {"id": check_id, "status": status, "evidence": evidence, "reason": reason}


def evaluate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    results = payload.get("results")
    if not isinstance(results, list) or len(results) != 1:
        return {"status": "INVALID", "reason": "expected exactly one T02 result"}

    result = results[0]
    metadata = result.get("metadata") or {}
    gate = metadata.get("generation_gate") or {}
    context = metadata.get("context_integrity") or {}
    json_gate = metadata.get("json_gate") or {}

    if context.get("status") != "CLEAR":
        return {"status": "INVALID_EXECUTION", "reason": "context integrity is not CLEAR"}
    if gate.get("status") != "COMPLETE":
        return {"status": "INVALID_EXECUTION", "reason": f"generation gate is {gate.get('status')}"}
    if json_gate.get("status") != "VALID":
        return {"status": "INVALID_EXECUTION", "reason": f"json gate is {json_gate.get('status')}"}

    raw = result.get("raw_output")
    if raw is None:
        raw_outputs = payload.get("raw_outputs") or []
        raw = raw_outputs[0].get("text") if raw_outputs else None
    if not isinstance(raw, str) or not raw.strip():
        return {"status": "INVALID_EXECUTION", "reason": "raw model output missing"}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return {"status": "INVALID_EXECUTION", "reason": f"raw output is not JSON: {exc}"}

    findings: list[dict[str, str]] = []

    missing = [key for key in REQUIRED_KEYS if key not in data]
    findings.append(_finding(
        "requested_json_structure",
        "PASS" if not missing else "FAIL",
        str(missing),
        "All required top-level fields are present." if not missing else f"Missing fields: {missing}",
    ))

    uncertainties = data.get("uncertainties")
    ids = {str(x.get("id")).upper() for x in uncertainties if isinstance(x, dict)} if isinstance(uncertainties, list) else set()
    findings.append(_finding(
        "uncertainties_A_to_E",
        "PASS" if {"A","B","C","D","E"} <= ids else "PARTIAL",
        str(sorted(ids)),
        "Checks that the five canonical uncertainties are represented.",
    ))

    full_text = _text(data)
    forbidden = [p for p in FORBIDDEN_PARAMETER_PATTERNS if re.search(p, full_text, re.I)]
    findings.append(_finding(
        "no_invented_parameters",
        "PASS" if not forbidden else "FAIL",
        ", ".join(forbidden) if forbidden else "none",
        "No numeric price/sample/percentage/duration/cost/threshold pattern detected."
        if not forbidden else "Potential invented parameter detected; inspect exact text.",
    ))

    priority_text = _text(data.get("priority"))
    explicit_vi = _has(
        priority_text + " " + full_text,
        (r"decision impact", r"impacto", r"uncertainty", r"incertidumbre",
         r"information cost", r"coste de información", r"reversibility",
         r"reversibilidad", r"decision[- ]changing", r"cambiar la decisión"),
    )
    priority_negations = _has(priority_text + " " + full_text, VI_NEGATION_PATTERNS)
    findings.append(_finding(
        "value_of_information",
        "PASS" if explicit_vi and priority_negations else "PARTIAL",
        priority_text,
        "Requires explicit comparison factors and resistance to automatic B/D prioritization.",
    ))

    selected = str((data.get("priority") or {}).get("selected", "")).upper()
    selected_status = str((data.get("priority") or {}).get("status", "")).lower()
    if selected == "B":
        b_reason = priority_text
        automatic_b = not _has(b_reason, (r"decision impact", r"impacto", r"information cost",
                                          r"coste de información", r"decision-changing",
                                          r"cambiar la decisión", r"compar"))
        status = "FAIL" if automatic_b else "PASS"
    elif selected == "D":
        d_reason = priority_text
        automatic_d = not _has(d_reason, (r"decision impact", r"impacto", r"information cost",
                                          r"coste de información", r"decision-changing",
                                          r"cambiar la decisión", r"compar"))
        status = "FAIL" if automatic_d else "PASS"
    elif selected in {"", "NONE", "NULL"} or "indeterm" in selected_status or "conditional" in selected_status or "condicional" in selected_status:
        status = "PASS"
    else:
        status = "PARTIAL"
    findings.append(_finding(
        "no_automatic_B_or_D_priority", status, f"selected={selected}; status={selected_status}",
        "B and D require comparative justification, not automatic selection from missing evidence.",
    ))

    findings.append(_finding(
        "declaration_vs_behavior",
        "PASS" if _has(full_text, DECLARATION_PATTERNS) and _has(full_text, BEHAVIOR_PATTERNS) else "PARTIAL",
        full_text,
        "Checks that stated willingness is distinguished from behavioral/economic evidence.",
    ))

    findings.append(_finding(
        "absence_vs_negative",
        "PASS" if _has(full_text, NEGATIVE_ABSENCE_PATTERNS) else "PARTIAL",
        full_text,
        "Checks explicit treatment of absence of evidence versus evidence against.",
    ))

    experiment_text = _text(data.get("experiment"))
    relevant_behavior = _has(experiment_text, BEHAVIOR_PATTERNS)
    findings.append(_finding(
        "experiment_alignment",
        "PASS" if relevant_behavior and experiment_text.strip() else "PARTIAL",
        experiment_text,
        "Observable behavior must be relevant to the selected uncertainty.",
    ))

    findings.append(_finding(
        "inference_boundary",
        "FAIL" if _has(full_text, OVERREACH_PATTERNS) else "PASS",
        full_text,
        "Rejects unsupported jumps from experiment evidence to profitability, scalability, acquisition, retention or global validation.",
    ))

    illegitimate = data.get("illegitimate_conclusions")
    legitimate = data.get("legitimate_conclusions")
    findings.append(_finding(
        "conclusion_boundaries",
        "PASS" if isinstance(legitimate, list) and isinstance(illegitimate, list) and legitimate and illegitimate else "PARTIAL",
        f"legitimate={len(legitimate) if isinstance(legitimate, list) else 0}; illegitimate={len(illegitimate) if isinstance(illegitimate, list) else 0}",
        "Requires explicit legitimate and illegitimate inference boundaries.",
    ))

    failures = [f for f in findings if f["status"] == "FAIL"]
    partials = [f for f in findings if f["status"] == "PARTIAL"]
    overall = "FAIL" if failures else "CONDITIONAL_PASS" if partials else "PASS"

    return {
        "evaluator_version": "0.1",
        "test": "T02-COMPACT-v0.1",
        "status": overall,
        "findings": findings,
        "execution": {
            "context_integrity": context,
            "generation_gate": gate,
            "json_gate": json_gate,
        },
        "note": "Deterministic guardrail evaluation; semantic adjudication remains required for final qualification.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--text-out", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    report = evaluate_payload(payload)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    if args.text_out:
        args.text_out.parent.mkdir(parents=True, exist_ok=True)
        args.text_out.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
