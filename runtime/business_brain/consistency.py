"""Lightweight deterministic consistency checks for runtime outputs."""

import re


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
    lower = text.lower()
    for phrase in risky:
        if phrase in lower:
            findings.append(f"strong_inference:{phrase}")
    return findings


def check_runtime_output(text: str) -> dict[str, object]:
    return {
        "unsupported_numeric_claims": check_no_unsupported_numeric_claims(text),
        "epistemic_risk_phrases": check_epistemic_language(text),
        "status": "REVIEW_REQUIRED"
        if check_no_unsupported_numeric_claims(text) or check_epistemic_language(text)
        else "CLEAR",
    }
