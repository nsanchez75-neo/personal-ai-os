import unittest

from runtime.business_brain.voi_analysis import analyze_voi


class VoIAnalysisTests(unittest.TestCase):
    def test_explicit_comparative_voi_passes_core_factors(self):
        result = analyze_voi({
            "priority": {
                "selected": "C",
                "reason": (
                    "C has greater decision impact because it reduces uncertainty. "
                    "Information cost is low compared with alternatives, and the result "
                    "would change the decision; reversibility makes waiting acceptable."
                ),
            }
        })
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["core_factors_missing"], [])
        self.assertIn("decision_impact", result["factors_detected"])
        self.assertIn("comparative_value", result["factors_detected"])

    def test_keyword_mentions_outside_priority_reason_do_not_count(self):
        result = analyze_voi({
            "priority": {"selected": None, "status": "Indeterminate", "reason": "Insufficient information."},
            "experiment": {
                "tests": "Compare decision impact, cost, reversibility and alternatives."
            },
        })
        self.assertEqual(result["status"], "PARTIAL")
        self.assertTrue(result["explicitly_indeterminate"])
        self.assertEqual(result["factors_detected"], [])
        self.assertTrue(result["human_decision_required"])

    def test_automatic_b_priority_without_voi_reasoning_fails(self):
        result = analyze_voi({
            "priority": {"selected": "B", "reason": "B is important."}
        })
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(result["human_decision_required"])


if __name__ == "__main__":
    unittest.main()
