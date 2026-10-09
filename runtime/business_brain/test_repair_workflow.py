import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

from runtime.business_brain.repair_workflow import (
    approve_and_promote,
    create_proposal,
    run_regression_gate,
    stage_candidate,
)


class RepairWorkflowTests(unittest.TestCase):
    def fixture(self, root):
        (root / "skills").mkdir(parents=True)
        target = root / "skills" / "business-reasoning.md"
        target.write_text("# Existing contract\n", encoding="utf-8")
        report = root / "report.json"
        report.write_text(json.dumps({
            "run_id": "run-test",
            "learning": {"items": [{
                "id": "REG-VOI-UNDEREXPLICIT",
                "diagnosis": "The rationale omitted comparative value.",
                "evidence": "VoI factors missing",
            }]}
        }), encoding="utf-8")
        candidate = root / "candidate.md"
        candidate.write_text("# Candidate contract\nExplicitly compare decision impact, uncertainty reduction, information cost and alternatives.\n", encoding="utf-8")
        proposal = root / "proposal.json"
        return report, target, candidate, proposal

    def test_full_lifecycle_requires_gate_and_exact_human_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report, target, candidate, proposal_path = self.fixture(root)
            proposal = create_proposal(report, proposal_path, "skills/business-reasoning.md", root)
            self.assertEqual(proposal["status"], "PROPOSED")
            staged = stage_candidate(proposal_path, candidate, root)
            self.assertEqual(staged["status"], "SANDBOXED")

            success = SimpleNamespace(returncode=0, stdout="8 tests passed", stderr="")
            with patch("runtime.business_brain.repair_workflow.subprocess.run", return_value=success):
                gated = run_regression_gate(proposal_path, root)
            self.assertEqual(gated["status"], "REGRESSION_PASSED")

            with self.assertRaisesRegex(ValueError, "Approval phrase mismatch"):
                approve_and_promote(proposal_path, "Human Reviewer", "yes", root)
            expected = f"PROMOTE {gated['proposal_id']} {gated['candidate_sha256']}"
            promoted = approve_and_promote(proposal_path, "Human Reviewer", expected, root)
            self.assertEqual(promoted["status"], "PROMOTED")
            self.assertEqual(target.read_text(encoding="utf-8"), candidate.read_text(encoding="utf-8"))
            audit = (root / "evolution" / "repair-audit.jsonl").read_text(encoding="utf-8")
            self.assertIn('"event": "PROMOTED"', audit)

    def test_failed_gate_blocks_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report, target, candidate, proposal_path = self.fixture(root)
            create_proposal(report, proposal_path, "skills/business-reasoning.md", root)
            stage_candidate(proposal_path, candidate, root)
            failed = SimpleNamespace(returncode=1, stdout="", stderr="test failed")
            with patch("runtime.business_brain.repair_workflow.subprocess.run", return_value=failed):
                gated = run_regression_gate(proposal_path, root)
            self.assertEqual(gated["status"], "REGRESSION_FAILED")
            phrase = f"PROMOTE {gated['proposal_id']} {gated['candidate_sha256']}"
            with self.assertRaisesRegex(ValueError, "regression gate"):
                approve_and_promote(proposal_path, "Reviewer", phrase, root)
            self.assertEqual(target.read_text(encoding="utf-8"), "# Existing contract\n")

    def test_target_traversal_and_non_markdown_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report, _, _, proposal = self.fixture(root)
            with self.assertRaises(ValueError):
                create_proposal(report, proposal, "../outside.md", root)
            with self.assertRaises(ValueError):
                create_proposal(report, proposal, "skills/payload.py", root)

    def test_stale_target_or_candidate_hash_blocks_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report, target, candidate, proposal_path = self.fixture(root)
            proposal = create_proposal(report, proposal_path, "skills/business-reasoning.md", root)
            stage_candidate(proposal_path, candidate, root)
            success = SimpleNamespace(returncode=0, stdout="ok", stderr="")
            with patch("runtime.business_brain.repair_workflow.subprocess.run", return_value=success):
                gated = run_regression_gate(proposal_path, root)
            target.write_text("# Concurrent change\n", encoding="utf-8")
            phrase = f"PROMOTE {gated['proposal_id']} {gated['candidate_sha256']}"
            with self.assertRaisesRegex(ValueError, "target changed"):
                approve_and_promote(proposal_path, "Reviewer", phrase, root)


if __name__ == "__main__":
    unittest.main()
