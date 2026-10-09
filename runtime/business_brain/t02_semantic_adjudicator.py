from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

STATUS_ORDER = {"PASS": 0, "PARTIAL": 1, "FAIL": 2}
FACTORS = {
    "decision_impact": (r"decision impact", r"impacto.*decisi[oó]n"),
    "information_cost": (r"information cost", r"coste.*informaci[oó]n", r"cost.*obtain"),
    "reversibility": (r"reversib",),
    "decision_change": (r"decision[- ]changing", r"change.*decision"),
    "dependencies": (r"dependenc", r"prerequis", r"bloquea"),
    "comparative": (r"compar", r"versus", r"vs\\.", r"trade.?off"),
}
INDET = (
    r"indeterminate", r"indeterminado", r"insufficient information",
    r"informaci[oó]n insuficiente", r"cannot establish", r"no permite establecer",
)
PAY = (r"payment", r"pago", r"pay", r"pag[ao]", r"purchase", r"compra", r"paid")
LOW = (
    r"free", r"gratis", r"trial", r"prueba", r"low[- ]commitment",
    r"bajo compromiso", r"engagement", r"feedback",
)
WTP = (r"willingness to pay", r"disposici[oó]n.*pagar", r"willing.*pay", r"WTP")


def text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {text(item)}" for key, item in value.items())
    return str(value)


def has(value: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, value, re.I) for pattern in patterns)


def gate(payload: dict[str, Any]) -> tuple[str, str]:
    results = payload.get("results")
    if not isinstance(results, list) or len(results) != 1:
        return "INVALID_EXECUTION", "expected exactly one result"
    result = results[0]
    if not isinstance(result, dict):
        return "INVALID_EXECUTION", "result must be an object"
    metadata = result.get("metadata") or {}
    for key, expected in (
        ("context_integrity", "CLEAR"),
        ("generation_gate", "COMPLETE"),
        ("json_gate", "VALID"),
    ):
        actual = (metadata.get(key) or {}).get("status")
        if actual != expected:
            return "INVALID_EXECUTION", f"{key} is {actual}"
    return "CLEAR", ""


def extract_raw_output(payload: dict[str, Any]) -> tuple[str | None, str | None]:
    """Read both supported runner payload shapes; return (raw text, error)."""
    results = payload.get("results")
    result = results[0] if isinstance(results, list) and len(results) == 1 else {}
    raw = result.get("raw_output") if isinstance(result, dict) else None
    if raw is None:
        raw_outputs = payload.get("raw_outputs") or []
        if isinstance(raw_outputs, list) and raw_outputs and isinstance(raw_outputs[0], dict):
            raw = raw_outputs[0].get("text")
    if not isinstance(raw, str) or not raw.strip():
        return None, "raw model output missing"
    return raw, None


def voi(data: dict[str, Any]) -> dict[str, Any]:
    priority = data.get("priority") or {}
    priority_text = text(priority)
    hits = [name for name, patterns in FACTORS.items() if has(priority_text, patterns)]
    indeterminate = has(priority_text, INDET)
    selected = str(priority.get("selected", "")).upper()
    status = "PASS" if len(hits) >= 4 else "PARTIAL"
    if selected in {"B", "D"} and len(hits) < 2:
        status = "FAIL"
    return {
        "status": status,
        "factors_detected": hits,
        "selected": selected,
        "indeterminate_detected": indeterminate,
        "reason": "Detected VoI factors: " + (", ".join(hits) if hits else "none"),
    }


def alignment(data: dict[str, Any]) -> dict[str, Any]:
    experiment = text(data.get("experiment") or {})
    all_text = text(data)
    selected = str((data.get("priority") or {}).get("selected", "")).upper()
    if not experiment.strip():
        return {"status": "FAIL", "selected": selected, "reason": "Experiment is empty."}
    payment = has(experiment, PAY)
    low_commitment = has(experiment, LOW)
    mentions_wtp = has(all_text, WTP)
    status = "PASS"
    reasons = []
    if selected not in set("ABCDE"):
        status = "PARTIAL"
        reasons.append("No single uncertainty is selected.")
    if mentions_wtp and low_commitment and not payment:
        status = "PARTIAL"
        reasons.append(
            "WTP is discussed but the experiment uses free/low-commitment engagement "
            "instead of economic commitment."
        )
    if selected == "B" and not payment:
        status = "PARTIAL" if low_commitment else "FAIL"
        reasons.append(
            "B is willingness to pay but no direct payment/economic commitment is observable."
        )
    if selected == "D" and payment and not has(experiment, (r"cost", r"coste", r"margin", r"economics")):
        status = "PARTIAL"
        reasons.append("Payment informs demand but does not directly observe delivery economics for D.")
    if not reasons:
        reasons.append("Observable behavior is aligned with the selected uncertainty.")
    return {
        "status": status,
        "selected": selected,
        "payment_behavior_detected": payment,
        "low_commitment_signal_detected": low_commitment,
        "reason": " ".join(reasons),
    }


def adjudicate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    status, reason = gate(payload)
    if status != "CLEAR":
        return {
            "adjudicator_version": "0.1",
            "test": "T02-COMPACT-v0.1",
            "status": status,
            "reason": reason,
        }

    raw, raw_error = extract_raw_output(payload)
    if raw_error:
        return {
            "adjudicator_version": "0.1",
            "test": "T02-COMPACT-v0.1",
            "status": "INVALID_EXECUTION",
            "reason": raw_error,
        }
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        return {
            "adjudicator_version": "0.1",
            "test": "T02-COMPACT-v0.1",
            "status": "INVALID_EXECUTION",
            "reason": f"raw output is not valid JSON: {exc}",
        }
    if not isinstance(data, dict):
        return {
            "adjudicator_version": "0.1",
            "test": "T02-COMPACT-v0.1",
            "status": "INVALID_EXECUTION",
            "reason": "raw output JSON must be an object",
        }

    voi_result = voi(data)
    alignment_result = alignment(data)
    overall = max(
        (voi_result["status"], alignment_result["status"]),
        key=lambda item: STATUS_ORDER[item],
    )
    regressions = []
    if voi_result["status"] != "PASS":
        regressions.append({
            "id": "REG-VOI-UNDEREXPLICIT",
            "status": "OBSERVED",
            "reason": voi_result["reason"],
        })
    if alignment_result["status"] != "PASS":
        regressions.append({
            "id": "REG-HYPOTHESIS-EXPERIMENT-MISMATCH",
            "status": "OBSERVED",
            "reason": alignment_result["reason"],
        })
    return {
        "adjudicator_version": "0.1",
        "test": "T02-COMPACT-v0.1",
        "status": overall,
        "semantic_adjudication": {
            "voi": voi_result,
            "experiment_alignment": alignment_result,
        },
        "regressions": regressions,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--text-out", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    report = adjudicate_payload(payload)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    for output_path in (args.json_out, args.text_out):
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered + "\\n", encoding="utf-8")
    return 0 if report.get("status") not in {"INVALID_EXECUTION"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
