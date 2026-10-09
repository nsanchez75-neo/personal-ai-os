"""Evidence-aware value-of-information (VoI) diagnostics for T02 priorities.

This is a diagnostic, not an autonomous business decision-maker. Factors count
only when the priority rationale contains explicit reasoning, not when a term
appears somewhere else in the answer.
"""
from __future__ import annotations

import re
from typing import Any

FACTOR_PATTERNS = {
    "decision_impact": (
        r"decision impact", r"impacto en la decisión", r"impacto de la decisión",
        r"consecuencia.*decisión", r"decision consequence",
    ),
    "uncertainty_reduction": (
        r"reduce uncertainty", r"reduc(?:e|es|ing) uncertainty",
        r"reduce la incertidumbre", r"reducción de incertidumbre",
        r"resuelve.*incertidumbre", r"uncertainty reduction",
    ),
    "information_cost": (
        r"information cost", r"coste de la información", r"costo de la información",
        r"cost to obtain", r"coste de obtener", r"costo de obtener",
        r"time to obtain", r"tiempo para obtener",
    ),
    "reversibility": (
        r"reversib", r"reversible", r"irreversible", r"reversibilidad",
        r"cost of waiting", r"coste de esperar", r"costo de esperar",
    ),
    "decision_change": (
        r"decision[- ]changing", r"change the decision", r"would change.*decision",
        r"cambiaría la decisión", r"cambiar la decisión", r"modificaría la decisión",
    ),
    "dependencies": (
        r"dependenc", r"prerequis", r"prerrequisito", r"bloquea", r"blocked by",
        r"depends on", r"depende de",
    ),
    "comparative_value": (
        r"compared with", r"compared to", r"versus", r"\bvs\b",
        r"frente a", r"comparado con", r"alternativa", r"trade.?off",
        r"higher value than", r"mayor valor que",
    ),
}


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key}: {_text(item)}" for key, item in value.items())
    return "" if value is None else str(value)


def analyze_voi(payload: dict[str, Any]) -> dict[str, Any]:
    priority = payload.get("priority") or {}
    rationale = _text(priority.get("reason", "")) if isinstance(priority, dict) else ""
    # Only the actual priority rationale can establish comparative VoI reasoning.
    hits: dict[str, str] = {}
    for factor, patterns in FACTOR_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, rationale, re.IGNORECASE)
            if match:
                hits[factor] = match.group(0)
                break

    explicit_indeterminate = bool(re.search(
        r"indeterminate|indeterminado|información insuficiente|insufficient information|"
        r"cannot determine|no se puede determinar|no permite establecer",
        _text(priority), re.IGNORECASE,
    ))
    # Decision impact, uncertainty reduction, information cost, and comparison are
    # core; reversibility/dependencies/decision-change enrich the analysis.
    core = {"decision_impact", "uncertainty_reduction", "information_cost", "comparative_value"}
    core_missing = sorted(core - set(hits))
    status = "PASS" if not core_missing else "PARTIAL"
    selected = str(priority.get("selected") or "NONE").upper() if isinstance(priority, dict) else "NONE"
    if selected in {"B", "D"} and len(hits) < 2:
        status = "FAIL"

    return {
        "status": status,
        "selected": selected,
        "explicitly_indeterminate": explicit_indeterminate,
        "factors_detected": sorted(hits),
        "factor_evidence": hits,
        "core_factors_missing": core_missing,
        "reason": (
            "Explicit comparative VoI rationale covers the core factors."
            if not core_missing
            else "Priority rationale lacks explicit core VoI factors: " + ", ".join(core_missing) + "."
        ),
        "human_decision_required": explicit_indeterminate or status != "PASS",
    }
