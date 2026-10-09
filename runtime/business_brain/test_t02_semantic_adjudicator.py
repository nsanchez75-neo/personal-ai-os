import json
import unittest

from runtime.business_brain.t02_semantic_adjudicator import adjudicate_payload


def payload(data):
    return {
        "results": [{
            "metadata": {
                "context_integrity": {"status": "CLEAR"},
                "generation_gate": {"status": "COMPLETE"},
                "json_gate": {"status": "VALID"},
            },
            "raw_output": json.dumps(data),
        }]
    }


def base():
    uncertainties = [
        {"id": key, "decision_impact": "x", "current_evidence": "x"}
        for key in "ABCDE"
    ]
    uncertainties[1]["decision_impact"] = "Willingness to pay is uncertain."
    return {
        "uncertainties": uncertainties,
        "priority": {
            "status": "Indeterminate",
            "selected": None,
            "reason": "Available information is insufficient to establish a unique priority.",
        },
        "experiment": {
            "tests": "Offer a free diagnostic or trial.",
            "observable_behavior": "Customers engage, give feedback, or express continued interest.",
        },
    }


class SemanticAdjudicatorTests(unittest.TestCase):
    def test_voi_partial(self):
        self.assertEqual(
            adjudicate_payload(payload(base()))["semantic_adjudication"]["voi"]["status"],
            "PARTIAL",
        )

    def test_alignment_partial(self):
        self.assertEqual(
            adjudicate_payload(payload(base()))["semantic_adjudication"]["experiment_alignment"]["status"],
            "PARTIAL",
        )

    def test_aligned_pass(self):
        data = base()
        data["priority"] = {
            "selected": "B",
            "reason": (
                "Compare decision impact, information cost, reversibility and dependencies; "
                "B has the highest decision-changing value."
            ),
        }
        data["experiment"] = {
            "tests": "Present a concrete paid offer and observe payment or rejection.",
            "observable_behavior": "Payment or rejection.",
        }
        self.assertEqual(adjudicate_payload(payload(data))["status"], "PASS")

    def test_reads_raw_outputs_fallback(self):
        data = base()
        wrapped = {
            "results": [{
                "metadata": {
                    "context_integrity": {"status": "CLEAR"},
                    "generation_gate": {"status": "COMPLETE"},
                    "json_gate": {"status": "VALID"},
                }
            }],
            "raw_outputs": [{"text": json.dumps(data)}],
        }
        result = adjudicate_payload(wrapped)
        self.assertEqual(result["status"], "PARTIAL")
        self.assertIn("semantic_adjudication", result)

    def test_missing_raw_output_returns_structured_invalid_execution(self):
        wrapped = {
            "results": [{
                "metadata": {
                    "context_integrity": {"status": "CLEAR"},
                    "generation_gate": {"status": "COMPLETE"},
                    "json_gate": {"status": "VALID"},
                }
            }]
        }
        result = adjudicate_payload(wrapped)
        self.assertEqual(result["status"], "INVALID_EXECUTION")
        self.assertEqual(result["reason"], "raw model output missing")

    def test_invalid_json_returns_structured_invalid_execution(self):
        wrapped = payload(base())
        wrapped["results"][0]["raw_output"] = "{not json"
        result = adjudicate_payload(wrapped)
        self.assertEqual(result["status"], "INVALID_EXECUTION")
        self.assertIn("raw output is not valid JSON", result["reason"])

    def test_indeterminate_priority_is_not_mislabeled_as_alignment_error(self):
        data = base()
        data["uncertainties"][1]["decision_impact"] = "Willingness to pay remains uncertain."
        data["experiment"] = {
            "tests": "Offer a free diagnostic or trial and discuss whether customers might pay.",
            "observable_behavior": "Customers engage, give feedback, or express continued interest.",
        }
        result = adjudicate_payload(payload(data))
        alignment = result["semantic_adjudication"]["experiment_alignment"]
        self.assertTrue(alignment["explicitly_indeterminate"])
        self.assertFalse(alignment["payment_behavior_detected"])
        self.assertEqual(alignment["status"], "PARTIAL")
        self.assertIn("observable behavior", alignment["reason"])
        self.assertNotIn("No single uncertainty is selected", alignment["reason"])

    def test_payment_mentioned_but_not_observable_is_not_counted_as_payment(self):
        data = base()
        data["uncertainties"][1]["decision_impact"] = "Willingness to pay is unknown."
        data["experiment"] = {
            "tests": "Discuss payment and offer a free trial.",
            "observable_behavior": "Customers complete the trial and provide feedback.",
        }
        result = adjudicate_payload(payload(data))
        alignment = result["semantic_adjudication"]["experiment_alignment"]
        self.assertFalse(alignment["payment_behavior_detected"])
        self.assertEqual(alignment["status"], "PARTIAL")


if __name__ == "__main__":
    unittest.main()
