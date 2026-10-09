import json
import tempfile
import unittest
from pathlib import Path

from runtime.business_brain.learning_loop import evaluate_run, run


def runner_payload():
    data = {
        "uncertainties": [
            {"id": key, "decision_impact": "unknown", "current_evidence": "not tested"}
            for key in "ABCDE"
        ],
        "priority": {
            "status": "Indeterminate",
            "selected": None,
            "reason": "Information insufficient to establish a unique priority.",
        },
        "experiment": {
            "tests": "Offer a free trial and discuss possible payment.",
            "observable_behavior": "Customers complete the free trial and provide feedback.",
        },
        "legitimate_conclusions": ["Trial engagement occurred."],
        "illegitimate_conclusions": ["Profitability is not established."],
    }
    return {
        "validation_mode": "LLM_BEHAVIOR_VALIDATION",
        "provider": "ollama",
        "model": "qwen3:8b",
        "scenario_count": 1,
        "results": [{
            "scenario_id": "02",
            "status": "PASS",
            "metadata": {
                "context_integrity": {"status": "CLEAR"},
                "generation_gate": {"status": "COMPLETE"},
                "json_gate": {"status": "VALID"},
            },
        }],
        "raw_outputs": [{"scenario_id": "02", "text": json.dumps(data)}],
    }


class LearningLoopTests(unittest.TestCase):
    def test_report_keeps_evaluators_separate_and_blocks_mutation(self):
        source = json.dumps(runner_payload()).encode("utf-8")
        report = evaluate_run(runner_payload(), source)
        self.assertIn(report["evaluation"]["behavioral"]["status"], {"PASS", "PARTIAL", "CONDITIONAL_PASS"})
        self.assertIn(report["evaluation"]["semantic"]["status"], {"PASS", "PARTIAL", "FAIL"})
        self.assertFalse(report["learning"]["production_mutation_allowed"])
        self.assertTrue(report["learning"]["human_approval_required_for_promotion"])
        self.assertEqual(report["source"]["provider"], "ollama")
        self.assertEqual(len(report["source"]["sha256"]), 64)

    def test_run_appends_ledger_without_overwriting_previous_evidence(self):
        payload = runner_payload()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input.json"
            report_path = root / "report.json"
            ledger_path = root / "ledger.jsonl"
            source.write_text(json.dumps(payload), encoding="utf-8")
            ledger_path.write_text('{"prior_evidence":true}\n', encoding="utf-8")
            first = run(source, report_path, ledger_path)
            second = run(source, report_path, ledger_path)
            lines = ledger_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 3)
            self.assertIn('"prior_evidence":true', lines[0])
            self.assertEqual(first["run_id"], second["run_id"])
            persisted = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertFalse(persisted["learning"]["production_mutation_allowed"])


if __name__ == "__main__":
    unittest.main()
