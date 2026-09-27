"""Evidence adjudication primitives.

The adjudicator is deliberately conservative. It separates textual traceability,
semantic phenomenon, polarity/negation, context, and inference strength instead
of treating a candidate error label as proof that an error occurred.
"""

from dataclasses import dataclass


@dataclass
class TraceCheck:
    candidate: str
    exact_text: str | None
    phenomenon_present: bool
    negated: bool
    context_note: str
    classification: str


def contrary_test(text: str, candidate_phrase: str, contrary_markers: tuple[str, ...] = (
    "no ", "not ", "cannot ", "does not ", "doesn't ", "cannot conclude",
    "no se puede", "no demuestra", "no permite concluir", "sin demostrar",
)) -> bool:
    """Return True when the local text explicitly negates the candidate phenomenon."""
    lower = text.lower()
    phrase = candidate_phrase.lower()
    if phrase not in lower:
        return False
    start = max(0, lower.find(phrase) - 100)
    context = lower[start: lower.find(phrase) + len(phrase) + 100]
    return any(marker in context for marker in contrary_markers)


def classify_trace(
    candidate: str,
    exact_text: str | None,
    phenomenon_present: bool,
    negated: bool,
    context_note: str = "",
) -> TraceCheck:
    if not exact_text or not phenomenon_present:
        classification = "NO_PRESENTE"
    elif negated:
        classification = "NO_PRESENTE"
    else:
        classification = "ERROR_POTENCIAL"
    return TraceCheck(
        candidate=candidate,
        exact_text=exact_text,
        phenomenon_present=phenomenon_present,
        negated=negated,
        context_note=context_note,
        classification=classification,
    )


def evidence_inference_boundary(
    observation: str,
    inference: str,
    supported: bool,
    scope: str = "contextual",
) -> dict[str, str | bool]:
    """Represent evidence separately from the conclusion it can support."""
    return {
        "observation": observation,
        "inference": inference,
        "supported": supported,
        "scope": scope,
        "overreach_check": "required",
    }
