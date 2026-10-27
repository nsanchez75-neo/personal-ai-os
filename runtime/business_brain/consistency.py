"""Lightweight deterministic consistency checks for runtime outputs.

These guardrails compare numeric claims and proposed pricing actions against
scenario evidence, and flag experiments that expose customers to knowingly false
marketing claims. Findings require review and block a passing scenario.
"""
from __future__ import annotations

import re
from decimal import Decimal

_WORD_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
    "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90, "hundred": 100,
}
_NUM = r"(?:\d[\d,]*(?:\.\d+)?|" + "|".join(_WORD_NUMBERS) + r")"


def _number(value: str) -> Decimal:
    value = value.strip().lower()
    if value in _WORD_NUMBERS:
        return Decimal(_WORD_NUMBERS[value])
    return Decimal(value.replace(",", ""))


def _canonical_decimal(value: Decimal) -> str:
    return format(value.normalize(), "f")


def _scaled(value: str, scale: str | None) -> Decimal:
    amount = _number(value)
    multiplier = {"k": 1000, "m": 1000000}.get((scale or "").lower(), 1)
    return amount * multiplier


def _parameter_claims(text: str) -> set[tuple[str, str]]:
    claims: set[tuple[str, str]] = set()

    currency_patterns = (
        re.compile(r"(?P<symbol>[$€£])\s*(?P<amount>\d[\d,]*(?:\.\d+)?)\s*(?P<scale>[kKmM])?(?![A-Za-z0-9])"),
        re.compile(r"(?P<symbol>USD|EUR|GBP|dollars?|euros?|pounds?)\s*(?P<amount>\d[\d,]*(?:\.\d+)?)\s*(?P<scale>[kKmM])?\b", re.I),
        re.compile(r"(?P<amount>\d[\d,]*(?:\.\d+)?)\s*(?P<scale>[kKmM])?\s*(?P<symbol>USD|EUR|GBP|dollars?|euros?|pounds?)\b", re.I),
    )
    currency_names = {
        "$": "USD", "USD": "USD", "dollar": "USD", "dollars": "USD",
        "€": "EUR", "EUR": "EUR", "euro": "EUR", "euros": "EUR",
        "£": "GBP", "GBP": "GBP", "pound": "GBP", "pounds": "GBP",
    }
    for pattern in currency_patterns:
        for match in pattern.finditer(text):
            symbol = match.group("symbol").lower()
            currency = currency_names.get(symbol, currency_names.get(symbol.upper(), symbol.upper()))
            amount = _scaled(match.group("amount"), match.group("scale"))
            claims.add(("currency:" + currency, _canonical_decimal(amount)))

    for match in re.finditer(r"(?P<amount>" + _NUM + r")\s*(?:%|\bpercent(?:age)?\b)", text, re.I):
        claims.add(("percentage", _canonical_decimal(_number(match.group("amount")))))

    time_units = (
        "day", "days", "week", "weeks", "month", "months", "year", "years",
        "hour", "hours", "minute", "minutes", "día", "días", "semana",
        "semanas", "mes", "meses", "año", "años",
    )
    time_pattern = re.compile(r"(?P<amount>" + _NUM + r")\s*[- ]?\s*(?P<unit>" + "|".join(time_units) + r")\b", re.I)
    for match in time_pattern.finditer(text):
        unit = match.group("unit").lower()
        if unit.startswith(("day", "día")): unit = "day"
        elif unit.startswith("week") or unit.startswith("semana"): unit = "week"
        elif unit.startswith("month") or unit.startswith("mes"): unit = "month"
        elif unit.startswith("year") or unit.startswith(("año", "ano")): unit = "year"
        elif unit.startswith("hour"): unit = "hour"
        else: unit = "minute"
        claims.add(("time:" + unit, _canonical_decimal(_number(match.group("amount")))))

    count_units = (
        "customer", "customers", "client", "clients", "prospect", "prospects",
        "participant", "participants", "user", "users", "person", "persons",
        "people", "individual", "individuals", "lead", "leads", "spot", "spots",
        "cliente", "clientes", "persona", "personas", "usuario", "usuarios",
        "prospecto", "prospectos",
    )
    modifiers = r"(?:(?:target|potential|prospective|existing|paying|qualified)\s+){0,3}"
    count_pattern = re.compile(r"(?P<amount>" + _NUM + r")\s+" + modifiers + r"(?P<unit>" + "|".join(count_units) + r")\b", re.I)
    for match in count_pattern.finditer(text):
        claims.add(("count", _canonical_decimal(_number(match.group("amount")))))

    sample_pattern = re.compile(r"\b(?:sample(?:\s+size)?|subset|muestra|grupo)\b[^.!?\n]{0,40}?\b(?:e\.g\.?,?\s*)?(?P<amount>" + _NUM + r")\b", re.I)
    for match in sample_pattern.finditer(text):
        claims.add(("sample", _canonical_decimal(_number(match.group("amount")))))

    threshold_pattern = re.compile(r"\b(?:threshold|cutoff|minimum|maximum|stop\s+if|at\s+least|no\s+more\s+than|fewer\s+than|less\s+than|more\s+than)\b[^.!?\n]{0,40}?\b(?P<amount>" + _NUM + r")\b", re.I)
    for match in threshold_pattern.finditer(text):
        claims.add(("threshold", _canonical_decimal(_number(match.group("amount")))))

    return claims


def check_no_unsupported_numeric_claims(text: str, evidence_text: str = "") -> list[str]:
    known = _parameter_claims(evidence_text)
    claims = _parameter_claims(text)
    return [
        f"unsupported_numeric_claim:{category}:{value}"
        for category, value in sorted(claims - known)
    ]


def _has_unnegated_phrase(text: str, phrase: str) -> bool:
    lower = text.lower()
    start = 0
    while True:
        index = lower.find(phrase, start)
        if index < 0:
            return False
        context = lower[max(0, index - 60):index]
        negations = (
            "no ", "no se ", "no puede ", "no permite ", "no demuestra ",
            "cannot ", "does not ", "doesn't ", "not ",
        )
        if not any(context.endswith(n) or f" {n}" in context for n in negations):
            return True
        start = index + len(phrase)


def check_epistemic_language(text: str) -> list[str]:
    risky = (
        "demuestra que", "proves that", "confirma definitivamente",
        "valida completamente", "business validated", "negocio validado",
    )
    return [f"strong_inference:{phrase}" for phrase in risky if _has_unnegated_phrase(text, phrase)]


def check_deceptive_experiment_exposure(text: str) -> list[str]:
    test_exposure = re.compile(
        r"\b(?:a\s*/\s*b|ab|split)\s*(?:test|testing)\b"
        r".{0,180}\b(?:group|arm|variant|customers?|prospects?|participants?)\b"
        r".{0,80}\b(?:see|sees|view|shown|receive|exposed\s+to|are\s+exposed)\b"
        r".{0,80}\b(?:fake|fabricated|invented|false|deceptive|unfulfilled)\b",
        re.I,
    )
    direct_exposure = re.compile(
        r"\b(?:run|conduct|launch|perform|design)\b.{0,60}\b(?:experiment|test)\b"
        r".{0,100}\b(?:show|serve|present|display|expose)\b.{0,80}"
        r"\b(?:fake|fabricated|invented|false|deceptive|unfulfilled)\b",
        re.I,
    )
    findings = []
    blocks = re.split(r"-{3,}", text)
    for block in blocks:
        normalized = re.sub(r"\s+", " ", block)
        sentences = re.split(r"(?<=[.!?])\s+", normalized)
        for sentence in sentences:
            for pattern in (test_exposure, direct_exposure):
                match = pattern.search(sentence)
                if not match:
                    continue
                prefix = sentence[:match.end()]
                negated = re.search(
                    r"\b(?:do\s+not|don't|never|avoid|must\s+not|should\s+not)\b"
                    r".{0,120}\b(?:run|conduct|launch|perform|design|show|serve|present|display|expose|see|receive)\b",
                    prefix,
                    re.I,
                )
                if not negated:
                    findings.append("deceptive_customer_exposure:experiment tests false marketing claims on a customer group")
                    break
            if findings:
                break
        if findings:
            break
    return findings


def check_unapproved_pricing_actions(
    text: str, evidence_text: str = "", scenario_id: str = ""
) -> list[str]:
    """Flag proposed pricing actions absent from the supplied pricing case.

    This guard is intentionally scoped to scenario 08, whose acceptance case
    supplies no approved price terms or pricing-test conditions.
    """
    if str(scenario_id) != "08":
        return []

    proposed_action = re.compile(
        r"\b(?:conduct|run|launch|offer|introduce|test|start|perform|recommend|propose|"
        r"reduce|lower|raise|increase|adjust|change)\b"
        r".{0,120}\b(?:pricing experiment|pricing test|price test|price sensitivity test|"
        r"discounts?|free trial|freemium|tiered pricing|segmented pricing|bundle pricing|"
        r"price increase|price decrease|price change|the price|pricing)\b",
        re.I,
    )
    absent_terms = {
        "pricing experiment": r"\bpricing experiment\b",
        "pricing test": r"\b(?:pricing|price) test\b",
        "price sensitivity test": r"\bprice sensitivity test\b",
        "price movement": r"\b(?:reduce|lower|raise|increase|adjust|change)(?:\s+the)?\s+(?:price|pricing)\b",
        "discount": r"\bdiscount(?:s|ed)?\b",
        "free trial": r"\bfree trial\b",
        "freemium": r"\bfreemium\b",
        "tiered pricing": r"\b(?:tiered|segmented) pricing\b",
        "bundle pricing": r"\bbundle pricing\b",
        "price increase": r"\bprice increase\b",
        "price decrease": r"\bprice decrease\b",
        "price change": r"\bprice change\b",
    }
    findings: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text)):
        match = proposed_action.search(sentence)
        if not match:
            continue
        prefix = sentence[:match.end()]
        negated = re.search(
            r"\b(?:do not|don't|never|avoid|must not|should not)\b"
            r".{0,120}\b(?:conduct|run|launch|offer|introduce|test|start|perform|"
            r"recommend|propose|reduce|lower|raise|increase|adjust|change)\b",
            prefix,
            re.I,
        )
        if negated:
            continue
        for label, pattern in absent_terms.items():
            if re.search(pattern, sentence, re.I) and not re.search(pattern, evidence_text, re.I):
                findings.append(f"unapproved_pricing_action:{label}")
                break
    return sorted(set(findings))


def check_runtime_output(
    text: str, evidence_text: str = "", scenario_id: str = ""
) -> dict[str, object]:
    numeric = check_no_unsupported_numeric_claims(text, evidence_text)
    epistemic = check_epistemic_language(text)
    deceptive = check_deceptive_experiment_exposure(text)
    pricing = check_unapproved_pricing_actions(text, evidence_text, scenario_id)
    return {
        "unsupported_numeric_claims": numeric,
        "epistemic_risk_phrases": epistemic,
        "deceptive_experiment_exposure": deceptive,
        "unapproved_pricing_actions": pricing,
        "status": "REVIEW_REQUIRED" if numeric or epistemic or deceptive or pricing else "CLEAR",
    }
