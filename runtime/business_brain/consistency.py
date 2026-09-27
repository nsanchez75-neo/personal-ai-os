"""Lightweight deterministic consistency checks for runtime outputs.

These checks are guardrails, not semantic adjudication. In particular, a phrase
such as "no demuestra" must not be treated as equivalent to "demuestra".
"""

import re


def _has_unnegated_phrase(text: str, phrase: str) -> bool:
    """Detect phrase only when a nearby negation does not explicitly reverse it."""
    lower = text.lower()
    start = 0
    while True:
        index = lower.find(phrase, start)
        if index < 0:
            return False
        context = lower[max(0, index - 60):index]
        negations = (
            "no ",
            "no se ",
            "no puede ",
            "no permite ",
            "no demuestra ",
            "cannot ",
            "does not ",
            "doesn't ",
            "not ",
        )
        if not any(context.endswith(n) or f" {n}" in context for n in negations):
            return True
        start = index + len(phrase)


def check_no_unsupported_numeric_claims(text: str) -> list[str]:
    findings = []
    patterns = [
        r"\b\d+(?:\.\d+)?\s*%",
        r"\b(?:sample|muestra)\s+(?:de\s+)?\d+",
        r"\b(?:5|10|15|20|30|50|100)\s*(?:€|\$|USD|EUR)",
    ]
    for pattern in patterns:
        if re.search(pattern, text, flags=re.I):
            findings.append(f"numeric_claim_detected:{pattern}")
    return findings


def check_epistemic_language(text: str) -> list[str]:
    findings = []
    risky = [
        "demuestra que",
        "proves that",
        "confirma definitivamente",
        "valida completamente",
        "business validated",
        "negocio validado",
    ]
    for phrase in risky:
        if _has_unnegated_phrase(text, phrase):
            findings.append(f"strong_inference:{phrase}")
    return findings


def check_runtime_output(text: str) -> dict[str, object]:
    numeric = check_no_unsupported_numeric_claims(text)
    epistemic = check_epistemic_language(text)
    return {
        "unsupported_numeric_claims": numeric,
        "epistemic_risk_phrases": epistemic,
        "status": "REVIEW_REQUIRED" if numeric or epistemic else "CLEAR",
    }
