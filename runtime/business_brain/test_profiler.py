"""Unit tests for the inference profiling helpers."""

from runtime.business_brain.profiler import _generation_status, _rate


def test_generation_status_complete():
    status, _ = _generation_status({"done": True, "done_reason": "stop"})
    assert status == "COMPLETE"


def test_generation_status_truncated():
    status, _ = _generation_status({"done": True, "done_reason": "length"})
    assert status == "TRUNCATED"


def test_generation_status_timeout():
    status, _ = _generation_status({"timeout": True, "error": "timed out"})
    assert status == "TIMEOUT"


def test_rate():
    assert _rate(100, 2_000_000_000) == 50
