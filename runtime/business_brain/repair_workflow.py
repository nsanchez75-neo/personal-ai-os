"""Controlled repair proposal, sandbox regression gate, and human-approved promotion.

Untrusted model output is treated as evidence only. It is never executed as code,
a shell command, a patch, or an instruction. Promotion is restricted to Markdown
assets under explicit allowlisted directories and requires a fresh baseline hash,
a passing fixed regression suite, and an exact approval phrase.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST_ROOTS = ("brains", "skills", "evaluations", "workflows", "knowledge")
FIXED_TESTS = (
    "runtime.business_brain.test_t02_semantic_adjudicator",
    "runtime.business_brain.test_learning_loop",
    "runtime.business_brain.test_voi_analysis",
    "runtime.business_brain.test_repair_workflow",
)
REGRESSION_COMPONENTS = {
    "REG-VOI-UNDEREXPLICIT": ("skills", "business reasoning / VoI skill or decision contract"),
    "REG-HYPOTHESIS-EXPERIMENT-MISMATCH": ("skills", "experiment-design skill or scenario"),
    "REG-UNSUPPORTED-NUMERIC-ASSUMPTION": ("brains", "Business Brain reasoning contract"),
    "REG-DECLARATION-VS-BEHAVIOR": ("evaluations", "behavioral evaluation scenario"),
}
ID_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9_-]{2,95}$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object.")
    return data


def _write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _audit(root: Path, event: dict[str, Any]) -> None:
    ledger = root / "evolution" / "repair-audit.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps({"at_utc": _utc(), **event}, ensure_ascii=False) + "\n")


def _safe_target(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts or rel.suffix.lower() != ".md":
        raise ValueError("Target must be a relative Markdown path without traversal.")
    if not rel.parts or rel.parts[0] not in ALLOWLIST_ROOTS:
        raise ValueError(f"Target root must be one of: {', '.join(ALLOWLIST_ROOTS)}.")
    resolved_root = root.resolve()
    target = (resolved_root / rel).resolve()
    if target == resolved_root or resolved_root not in target.parents:
        raise ValueError("Target escapes repository root.")
    return target


def create_proposal(report_path: Path, output_path: Path, target: str, root: Path = REPO_ROOT) -> dict[str, Any]:
    report_bytes = report_path.read_bytes()
    report = json.loads(report_bytes.decode("utf-8"))
    if not isinstance(report, dict):
        raise ValueError("Learning report must be a JSON object.")
    matching: list[dict[str, Any]] = []
    for item in report.get("learning", {}).get("items", []):
        regression_id = str(item.get("id", "UNCLASSIFIED"))
        if regression_id in REGRESSION_COMPONENTS:
            matching.append(item)
    if not matching:
        raise ValueError("Report contains no supported, mapped regression suitable for a repair proposal.")
    item = matching[0]
    regression_id = str(item.get("id"))
    component, component_hint = REGRESSION_COMPONENTS[regression_id]
    target_path = _safe_target(root, target)
    if target_path.exists():
        baseline_hash = sha256_bytes(target_path.read_bytes())
    else:
        baseline_hash = None
    proposal_id = hashlib.sha256(
        (sha256_bytes(report_bytes) + regression_id + target).encode("utf-8")
    ).hexdigest()[:16]
    proposal = {
        "schema_version": "1.0",
        "proposal_id": proposal_id,
        "created_at_utc": _utc(),
        "status": "PROPOSED",
        "regression_id": regression_id,
        "source_run_id": report.get("run_id"),
        "source_report_sha256": sha256_bytes(report_bytes),
        "diagnosis": str(item.get("diagnosis", item.get("reason", "")))[:3000],
        "evidence": str(item.get("evidence", ""))[:3000],
        "responsible_component": component,
        "component_hint": component_hint,
        "target": target,
        "baseline_sha256": baseline_hash,
        "candidate_path": None,
        "candidate_sha256": None,
        "regression_gate": None,
        "approval": None,
        "promotion": None,
        "safety": {
            "model_output_is_untrusted_evidence": True,
            "model_output_executed": False,
            "automatic_production_mutation": False,
            "requires_human_approval": True,
        },
    }
    _write(output_path, proposal)
    _audit(root, {"event": "PROPOSAL_CREATED", "proposal_id": proposal_id, "regression_id": regression_id,
                  "report_sha256": proposal["source_report_sha256"], "target": target})
    return proposal


def stage_candidate(proposal_path: Path, candidate_source: Path, root: Path = REPO_ROOT) -> dict[str, Any]:
    proposal = _load(proposal_path)
    if proposal.get("status") != "PROPOSED":
        raise ValueError("Candidate can only be staged for a PROPOSED repair.")
    target_path = _safe_target(root, str(proposal["target"]))
    current_hash = sha256_bytes(target_path.read_bytes()) if target_path.exists() else None
    if current_hash != proposal.get("baseline_sha256"):
        raise ValueError("Target changed since proposal creation; regenerate proposal against current baseline.")
    candidate_bytes = candidate_source.read_bytes()
    if not candidate_bytes.strip():
        raise ValueError("Empty candidate content is not allowed.")
    # Candidate is data, not a patch or executable program. Promotion only accepts .md targets.
    sandbox_dir = root / "evolution" / "sandbox" / str(proposal["proposal_id"])
    sandbox_dir.mkdir(parents=True, exist_ok=True)
    candidate_path = sandbox_dir / "candidate.md"
    candidate_path.write_bytes(candidate_bytes)
    proposal["candidate_path"] = str(candidate_path.relative_to(root))
    proposal["candidate_sha256"] = sha256_bytes(candidate_bytes)
    proposal["status"] = "SANDBOXED"
    _write(proposal_path, proposal)
    _audit(root, {"event": "CANDIDATE_STAGED", "proposal_id": proposal["proposal_id"],
                  "candidate_sha256": proposal["candidate_sha256"], "target": proposal["target"]})
    return proposal


def run_regression_gate(proposal_path: Path, root: Path = REPO_ROOT) -> dict[str, Any]:
    proposal = _load(proposal_path)
    if proposal.get("status") != "SANDBOXED":
        raise ValueError("Regression gate requires a SANDBOXED candidate.")
    candidate_path = (root / str(proposal["candidate_path"])).resolve()
    sandbox_root = (root / "evolution" / "sandbox" / str(proposal["proposal_id"])).resolve()
    if sandbox_root not in candidate_path.parents or not candidate_path.is_file():
        raise ValueError("Candidate path is outside its repair sandbox.")
    candidate_hash = sha256_bytes(candidate_path.read_bytes())
    if candidate_hash != proposal.get("candidate_sha256"):
        raise ValueError("Candidate changed after staging; restage it before validation.")
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", *FIXED_TESTS, "-v"],
        cwd=root, capture_output=True, text=True, timeout=300, check=False,
    )
    gate = {
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "return_code": completed.returncode,
        "command": [sys.executable, "-m", "unittest", *FIXED_TESTS, "-v"],
        "candidate_sha256": candidate_hash,
        "stdout": completed.stdout[-12000:],
        "stderr": completed.stderr[-12000:],
        "completed_at_utc": _utc(),
    }
    proposal["regression_gate"] = gate
    proposal["status"] = "REGRESSION_PASSED" if gate["status"] == "PASS" else "REGRESSION_FAILED"
    _write(proposal_path, proposal)
    _audit(root, {"event": "REGRESSION_GATE_" + gate["status"], "proposal_id": proposal["proposal_id"],
                  "candidate_sha256": candidate_hash, "return_code": completed.returncode})
    return proposal


def approve_and_promote(proposal_path: Path, approver: str, approval_phrase: str,
                        root: Path = REPO_ROOT) -> dict[str, Any]:
    proposal = _load(proposal_path)
    if proposal.get("status") != "REGRESSION_PASSED" or proposal.get("regression_gate", {}).get("status") != "PASS":
        raise ValueError("Promotion blocked: the fixed regression gate has not passed.")
    approver = approver.strip()
    if not approver or len(approver) > 160:
        raise ValueError("A named human approver is required.")
    expected = f"PROMOTE {proposal['proposal_id']} {proposal['candidate_sha256']}"
    if approval_phrase != expected:
        raise ValueError("Approval phrase mismatch. No changes promoted.")
    target_path = _safe_target(root, str(proposal["target"]))
    current_hash = sha256_bytes(target_path.read_bytes()) if target_path.exists() else None
    if current_hash != proposal.get("baseline_sha256"):
        raise ValueError("Promotion blocked: target changed since proposal creation.")
    candidate_path = (root / str(proposal["candidate_path"])).resolve()
    sandbox_root = (root / "evolution" / "sandbox" / str(proposal["proposal_id"])).resolve()
    if sandbox_root not in candidate_path.parents or not candidate_path.is_file():
        raise ValueError("Candidate path is outside its repair sandbox.")
    candidate_bytes = candidate_path.read_bytes()
    if sha256_bytes(candidate_bytes) != proposal.get("candidate_sha256"):
        raise ValueError("Promotion blocked: candidate hash mismatch.")
    # This is the only production write in the module, guarded by explicit approval and checks above.
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes(candidate_bytes)
    proposal["approval"] = {"approver": approver, "phrase_verified": True, "approved_at_utc": _utc()}
    proposal["promotion"] = {"status": "PROMOTED", "target_sha256": sha256_bytes(candidate_bytes),
                             "promoted_at_utc": _utc()}
    proposal["status"] = "PROMOTED"
    _write(proposal_path, proposal)
    _audit(root, {"event": "PROMOTED", "proposal_id": proposal["proposal_id"], "approver": approver,
                  "target": proposal["target"], "target_sha256": proposal["promotion"]["target_sha256"]})
    return proposal


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("propose")
    p.add_argument("report", type=Path)
    p.add_argument("--target", required=True)
    p.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("stage")
    s.add_argument("proposal", type=Path)
    s.add_argument("--candidate", type=Path, required=True)
    g = sub.add_parser("gate")
    g.add_argument("proposal", type=Path)
    m = sub.add_parser("promote")
    m.add_argument("proposal", type=Path)
    m.add_argument("--approver", required=True)
    m.add_argument("--approval-phrase", required=True)
    args = parser.parse_args()
    if args.command == "propose":
        result = create_proposal(args.report, args.out, args.target)
    elif args.command == "stage":
        result = stage_candidate(args.proposal, args.candidate)
    elif args.command == "gate":
        result = run_regression_gate(args.proposal)
    else:
        result = approve_and_promote(args.proposal, args.approver, args.approval_phrase)
    print(json.dumps({
        "proposal_id": result.get("proposal_id"),
        "status": result.get("status"),
        "regression_id": result.get("regression_id"),
        "target": result.get("target"),
        "regression_gate": result.get("regression_gate", {}).get("status") if result.get("regression_gate") else None,
        "promotion": result.get("promotion", {}).get("status") if result.get("promotion") else None,
    }, ensure_ascii=False, indent=2))
    return 0 if result.get("status") not in {"REGRESSION_FAILED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
