import json
import tempfile
import unittest
from pathlib import Path

from runtime.business_brain.context import build_context
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
    def test_context_includes_active_business_model_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            system = root / "system.md"
            skill = root / "skill.md"
            contract = root / "contract.md"
            system.write_text("BUSINESS BRAIN", encoding="utf-8")
            skill.write_text("BUSINESS MODEL SKILL: VoI protocol", encoding="utf-8")
            contract.write_text("RUNTIME CONTRACT", encoding="utf-8")

            context = build_context(str(system), str(contract), str(skill))

        self.assertIn("BUSINESS BRAIN", context)
        self.assertIn("--- BUSINESS MODEL SKILL ---", context)
        self.assertIn("VoI protocol", context)
        self.assertIn("--- RUNTIME CONTRACT ---", context)

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
            "status": "Selected",
            "selected": "B",
            "reason": (
                "Compare A and B. A concerns problem importance, while B concerns "
                "actual willingness to pay. B is more actionable than A for the next "
                "decision because a real paid offer can produce observable payment "
                "behavior; A remains important but does not by itself establish "
                "whether customers will pay. Information cost and reversibility "
                "remain unknown, so this is a provisional priority, not certainty. "
                "Decision impact, information cost, reversibility and dependencies "
                "were considered."
            ),
        }
        data["experiment"] = {
            "tests": (
                "Present a real paid offer at a price supplied by the business owner "
                "and observe payment or rejection."
            ),
            "observable_behavior": "Payment or rejection for that offer.",
        }
        self.assertEqual(
            adjudicate_payload(payload(data))["status"],
            "PASS",
        )


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


    def test_keyword_only_priority_does_not_pass_voi(self):
        data = base()
        data["priority"] = {
            "status": "Indeterminate",
            "selected": None,
            "reason": (
                "Decision impact, information cost, reversibility, "
                "decision-changing value, dependencies and trade-offs "
                "are all important. Available information is insufficient "
                "to establish a unique priority."
            ),
        }
        result = adjudicate_payload(payload(data))
        self.assertNotEqual(
            result["semantic_adjudication"]["voi"]["status"],
            "PASS",
            "Mentioning factor names alone must not pass the VoI gate.",
        )


    def test_listing_two_uncertainties_without_comparing_them_does_not_pass_voi(self):
        data = base()
        data["priority"] = {
            "status": "Indeterminate",
            "selected": None,
            "reason": (
                "A is important. B is also important. "
                "Decision impact, information cost, reversibility, "
                "decision-changing value, dependencies and trade-offs "
                "were considered. Available information is insufficient "
                "to establish a unique priority."
            ),
        }

        result = adjudicate_payload(payload(data))

        self.assertNotEqual(
            result["semantic_adjudication"]["voi"]["status"],
            "PASS",
            "Listing two uncertainties and factor names is not a real comparison.",
        )


    def test_comparison_must_reference_two_uncertainties(self):
        data = base()
        data["priority"] = {
            "status": "Selected",
            "selected": "B",
            "reason": (
                "B is more actionable than the current alternatives. "
                "Decision impact, information cost, reversibility, "
                "decision-changing value, dependencies and trade-offs "
                "were considered."
            ),
        }

        result = adjudicate_payload(payload(data))

        self.assertNotEqual(
            result["semantic_adjudication"]["voi"]["status"],
            "PASS",
        )

    def test_comparison_language_without_real_comparison_does_not_pass(self):
        data = base()
        data["priority"] = {
            "status": "Indeterminate",
            "selected": None,
            "reason": (
                "A and B are important. While both remain uncertain, "
                "there is insufficient information to establish a unique priority. "
                "Decision impact, information cost, reversibility, "
                "decision-changing value, dependencies and trade-offs "
                "were considered."
            ),
        }

        result = adjudicate_payload(payload(data))

        self.assertNotEqual(
            result["semantic_adjudication"]["voi"]["status"],
            "PASS",
        )

    def test_explicit_comparison_with_multiple_factors_can_pass_voi(self):
        data = base()
        data["priority"] = {
            "status": "Selected",
            "selected": "B",
            "reason": (
                "Compared with A, B is more actionable because a real paid offer "
                "can test willingness to pay, whereas A measures problem importance. "
                "The decision impact is material, but information cost, "
                "reversibility, decision-changing value, dependencies and trade-offs "
                "must also be considered."
            ),
        }
        data["experiment"] = {
            "tests": (
                "Present a real paid offer at a price supplied by the business owner "
                "and observe payment or rejection."
            ),
            "observable_behavior": "Payment or rejection for that offer.",
        }

        result = adjudicate_payload(payload(data))

        self.assertEqual(
            result["semantic_adjudication"]["voi"]["status"],
            "PASS",
        )

    def test_indeterminate_priority_passes_when_unresolved_evidence_is_explained(self):
        data = base()
        data["priority"] = {
            "status": "Indeterminate",
            "selected": None,
            "reason": (
                "A may have greater decision impact than B because A concerns the "
                "severity of the problem while B concerns willingness to pay, but "
                "we cannot rank them because evidence about customer behavior, "
                "information cost, reversibility and dependencies is missing. "
                "The decision-changing value and trade-offs therefore remain unknown."
            ),
        }

        result = adjudicate_payload(payload(data))
        voi = result["semantic_adjudication"]["voi"]

        self.assertTrue(voi["indeterminate_detected"])
        self.assertEqual(voi["status"], "PASS")

    def test_explicit_comparison_across_all_uncertainties_can_pass_voi(self):
        data = base()
        data["priority"] = {
            "status": "Indeterminate",
            "selected": None,
            "reason": (
                "Decision impact, current evidence and uncertainty are comparable "
                "across all uncertainties. Information cost and reversibility are "
                "similar, while decision-changing value is not clearly differentiated. "
                "The available information does not support a unique priority."
            ),
        }

        voi = adjudicate_payload(payload(data))["semantic_adjudication"]["voi"]

        self.assertEqual(voi["status"], "PASS")
        self.assertEqual(voi["uncertainties_referenced"], list("ABCDE"))
        self.assertTrue(voi["comparative_reasoning_detected"])

    def test_all_uncertainties_factor_list_without_comparison_does_not_pass(self):
        data = base()
        data["priority"] = {
            "status": "Indeterminate",
            "selected": None,
            "reason": (
                "All uncertainties matter. Decision impact, information cost, "
                "reversibility, decision-changing value, dependencies and trade-offs "
                "were considered. Insufficient information to establish a unique priority."
            ),
        }

        voi = adjudicate_payload(payload(data))["semantic_adjudication"]["voi"]

        self.assertNotEqual(voi["status"], "PASS")

    def test_indeterminate_keywords_without_evidence_rationale_do_not_pass(self):
        data = base()
        data["priority"] = {
            "status": "Indeterminate",
            "selected": None,
            "reason": (
                "A, B, decision impact, information cost, reversibility, "
                "decision-changing value, dependencies and trade-offs. "
                "Insufficient information."
            ),
        }

        result = adjudicate_payload(payload(data))

        self.assertNotEqual(
            result["semantic_adjudication"]["voi"]["status"],
            "PASS",
        )

    def test_comparator_and_factor_list_without_justification_do_not_pass(self):
        data = base()
        data["priority"] = {
            "status": "Selected",
            "selected": "B",
            "reason": (
                "Compared with A, B is more important. Decision impact, "
                "information cost, reversibility, decision-changing value, "
                "dependencies and trade-offs."
            ),
        }

        result = adjudicate_payload(payload(data))

        self.assertNotEqual(
            result["semantic_adjudication"]["voi"]["status"],
            "PASS",
        )


if __name__ == "__main__":
    unittest.main()
