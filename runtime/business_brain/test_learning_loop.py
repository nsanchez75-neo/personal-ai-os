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
            "title": "Value of information / uncertainty prioritization",
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

    def test_partial_voi_diagnostic_creates_sandbox_learning_item(self):
        source = json.dumps(runner_payload()).encode("utf-8")
        report = evaluate_run(runner_payload(), source)

        voi_items = [
            item for item in report["learning"]["items"]
            if item["source"] == "voi_analysis"
        ]

        self.assertTrue(voi_items)
        self.assertEqual(voi_items[0]["id"], "REG-VOI-UNDEREXPLICIT")
        self.assertEqual(report["learning"]["next_stage"], "SANDBOX_AND_REGRESSION_GATE")
        self.assertFalse(report["learning"]["production_mutation_allowed"])

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

    def test_non_t02_prose_scenario_does_not_get_t02_invalid_json_diagnosis(self):
        payload = runner_payload()
        payload["results"][0].update({
            "scenario_id": "06",
            "title": "Offer integrity",
            "status": "PARTIAL",
            "metadata": {"json_gate": {"status": "NOT_REQUIRED"}},
            "assertions": [{"assertion": "preserve customer trust", "status": "PARTIAL", "reason": "partial evidence"}],
        })
        payload["raw_outputs"][0]["scenario_id"] = "06"
        payload["raw_outputs"][0]["text"] = "The answer is prose, as this scenario requests."
        source = json.dumps(payload).encode("utf-8")

        report = evaluate_run(payload, source)

        self.assertEqual(report["evaluation"]["behavioral"]["status"], "PARTIAL")
        self.assertEqual(report["evaluation"]["semantic"]["status"], "NOT_APPLICABLE")
        self.assertEqual(report["evaluation"]["value_of_information"]["status"], "NOT_APPLICABLE")
        self.assertEqual(report["evaluation"]["overall"], "CONDITIONAL")

    def test_general_runtime_guardrail_maps_unapproved_pricing_action(self):
        payload = runner_payload()
        payload["results"][0].update({
            "scenario_id": "08",
            "title": "Pricing",
            "status": "FAIL",
            "metadata": {
                "json_gate": {"status": "NOT_REQUIRED"},
                "consistency_check": {
                    "unsupported_numeric_claims": [],
                    "deceptive_experiment_exposure": [],
                    "unapproved_pricing_actions": [
                        "unapproved_pricing_action:pricing experiment"
                    ],
                },
            },
            "assertions": [{
                "assertion": "no unapproved pricing action",
                "status": "FAIL",
                "reason": "pricing terms absent from case",
            }],
        })
        payload["raw_outputs"][0]["scenario_id"] = "08"
        payload["raw_outputs"][0]["text"] = (
            "Conduct a pricing experiment with a discount."
        )
        source = json.dumps(payload).encode("utf-8")

        report = evaluate_run(payload, source)

        pricing_items = [
            item for item in report["learning"]["items"]
            if item["id"] == "REG-UNAPPROVED-PRICING-ACTION"
        ]
        self.assertTrue(pricing_items)
        self.assertEqual(report["evaluation"]["overall"], "FAIL")
        self.assertEqual(report["evaluation"]["semantic"]["status"], "NOT_APPLICABLE")

    def test_general_runtime_guardrail_maps_ethical_exposure_to_sandbox_learning(self):
        payload = runner_payload()
        payload["results"][0].update({
            "scenario_id": "06",
            "title": "Offer integrity",
            "status": "FAIL",
            "metadata": {
                "json_gate": {"status": "NOT_REQUIRED"},
                "consistency_check": {
                    "unsupported_numeric_claims": [],
                    "deceptive_experiment_exposure": ["deceptive_customer_exposure"],
                },
            },
            "assertions": [{"assertion": "ethical experiment", "status": "FAIL", "reason": "unsafe exposure"}],
        })
        payload["raw_outputs"][0]["scenario_id"] = "06"
        source = json.dumps(payload).encode("utf-8")

        report = evaluate_run(payload, source)

        ethical_items = [
            item for item in report["learning"]["items"]
            if item["id"] == "REG-DECEPTIVE-EXPERIMENT-EXPOSURE"
        ]
        self.assertTrue(ethical_items)
        self.assertEqual(report["evaluation"]["overall"], "FAIL")
        self.assertEqual(report["evaluation"]["semantic"]["status"], "NOT_APPLICABLE")


if __name__ == "__main__":
    unittest.main()
