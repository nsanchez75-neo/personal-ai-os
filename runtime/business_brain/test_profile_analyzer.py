import json

from runtime.business_brain.profile_analyzer import analyze, render_text


def test_truncated_and_timeout_are_not_behavioral_failures(tmp_path):
    truncated = tmp_path / "truncated.json"
    timeout = tmp_path / "timeout.json"

    truncated.write_text(
        json.dumps({
            "results": [{
                "probe": "t02",
                "status": "TRUNCATED",
                "wall_seconds": 10,
                "prompt_seconds": 1,
                "generation_seconds": 9,
                "output_tokens_per_second": 3,
            }]
        }),
        encoding="utf-8",
    )
    timeout.write_text(
        json.dumps({
            "results": [{
                "probe": "t02",
                "status": "TIMEOUT",
                "wall_seconds": 180,
            }]
        }),
        encoding="utf-8",
    )

    report = analyze([truncated, timeout])
    t02 = report["probes"]["t02"]

    assert t02["execution_class"] == "TIMEOUT"
    assert t02["behavioral_evaluation"] == "NOT_EVALUABLE"


def test_complete_probe_is_potentially_evaluable(tmp_path):
    source = tmp_path / "complete.json"
    source.write_text(
        json.dumps({
            "results": [
                {
                    "probe": "minimal",
                    "status": "COMPLETE",
                    "wall_seconds": 3,
                    "prompt_seconds": 0.3,
                    "generation_seconds": 1.2,
                    "output_tokens_per_second": 5,
                },
                {
                    "probe": "minimal",
                    "status": "COMPLETE",
                    "wall_seconds": 4,
                    "prompt_seconds": 0.4,
                    "generation_seconds": 1.5,
                    "output_tokens_per_second": 4,
                },
            ]
        }),
        encoding="utf-8",
    )

    report = analyze([source])
    stats = report["probes"]["minimal"]["metrics"]["wall_seconds"]

    assert report["probes"]["minimal"]["execution_class"] == "EXECUTION_COMPLETE"
    assert report["probes"]["minimal"]["behavioral_evaluation"] == "POTENTIALLY_EVALUABLE"
    assert stats["median"] == 3.5
    assert stats["n"] == 2
