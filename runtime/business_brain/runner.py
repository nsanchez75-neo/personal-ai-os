"""Provider-neutral Business Brain runtime runner with context-integrity gating."""

import argparse
import hashlib
import json
import re
from pathlib import Path

from runtime.business_brain.context import build_context
from runtime.business_brain.adapters.fixture import FixtureAdapter
from runtime.business_brain.adapters.ollama import OllamaAdapter
from runtime.business_brain.models import Scenario
from runtime.business_brain.evaluator import evaluate_scenario
from runtime.business_brain.consistency import check_runtime_output


PLACEHOLDER_MARKERS = ("[PEGA AQUÍ", "[PASTE HERE", "TODO_SYSTEM_PROMPT", "TODO_SCENARIO")
EXPECTED_CONTEXT_MARKERS = ("BUSINESS BRAIN", "RUNTIME CONTRACT")


def check_context_integrity(system_prompt, scenario_input):
    reasons = []
    system_upper = system_prompt.upper()
    scenario_upper = scenario_input.upper()
    if not system_prompt.strip():
        reasons.append("empty_system_prompt")
    if not scenario_input.strip():
        reasons.append("empty_scenario")
    if any(marker.upper() in system_upper or marker.upper() in scenario_upper for marker in PLACEHOLDER_MARKERS):
        reasons.append("placeholder_detected")
    for marker in EXPECTED_CONTEXT_MARKERS:
        if marker not in system_upper:
            reasons.append(f"missing_system_marker:{marker}")
    return {
        "status": "CLEAR" if not reasons else "INVALID_CONTEXT",
        "reasons": reasons,
        "system_chars": len(system_prompt),
        "scenario_chars": len(scenario_input),
        "system_sha256": hashlib.sha256(system_prompt.encode("utf-8")).hexdigest(),
        "scenario_sha256": hashlib.sha256(scenario_input.encode("utf-8")).hexdigest(),
    }


def load_scenarios(path):
    text = Path(path).read_text(encoding="utf-8")
    chunks = re.split(r"(?=^## (?:Scenario|X))", text, flags=re.M)
    out = []
    for chunk in chunks:
        m = re.match(r"^## (Scenario|X)(?: |)(\d+)? ?— ?(.+)$", chunk, re.M)
        if not m:
            continue
        kind, num, title = m.groups()
        sid = ("X" + num if kind == "X" else num)
        im = re.search(r"\*\*Input:\*\* (.+?)(?=\n\n|\n##|$)", chunk, re.S)
        assertions = re.findall(r"^- (.+)$", chunk, re.M)
        if not assertions:
            continue
        input_text = im.group(1).strip() if im else ""
        fixture = input_text + "\n\nASSERTIONS_FOR_HARNESS:\n" + "\n".join(assertions)
        out.append(Scenario(sid, title, fixture, assertions, kind == "X"))
    return out


def build_adapter(provider, model, base_url, temperature, thinking):
    if provider == "fixture":
        return FixtureAdapter()
    if provider == "ollama":
        return OllamaAdapter(
            model=model,
            base_url=base_url,
            temperature=temperature,
            thinking=thinking,
        )
    raise ValueError(f"Unsupported provider: {provider}")


def run(
    system_prompt_path,
    scenario_path,
    output_path,
    provider="fixture",
    model="qwen3:8b",
    base_url="http://localhost:11434",
    temperature=0.6,
    thinking=True,
):
    system = build_context(system_prompt_path)
    scenarios = load_scenarios(scenario_path)
    adapter = build_adapter(provider, model, base_url, temperature, thinking)
    results = []
    raw_outputs = []

    for scenario in scenarios:
        context_integrity = check_context_integrity(system, scenario.input_text)
        if context_integrity["status"] != "CLEAR":
            raw_outputs.append({
                "scenario_id": scenario.scenario_id,
                "title": scenario.title,
                "provider": provider,
                "metadata": {"context_integrity": context_integrity},
                "text": "",
            })
            results.append({
                "scenario_id": scenario.scenario_id,
                "title": scenario.title,
                "status": "INVALID_CONTEXT",
                "provider": provider,
                "assertions": [],
                "metadata": {"context_integrity": context_integrity},
            })
            continue

        response = adapter.generate(system, scenario.input_text)
        consistency = check_runtime_output(response.text)
        response_metadata = {
            **response.metadata,
            "context_integrity": context_integrity,
            "consistency_check": consistency,
        }
        response_with_metadata = type(response)(
            text=response.text,
            provider=response.provider,
            metadata=response_metadata,
        )
        raw_outputs.append({
            "scenario_id": scenario.scenario_id,
            "title": scenario.title,
            "provider": response.provider,
            "metadata": response_metadata,
            "text": response.text,
        })
        evaluated = evaluate_scenario(scenario, response_with_metadata)
        results.append(evaluated)

    validation_mode = (
        "HARNESS_VALIDATION" if provider == "fixture"
        else "LLM_BEHAVIOR_VALIDATION"
    )
    payload = {
        "validation_mode": validation_mode,
        "provider": provider,
        "model": model if provider != "fixture" else "fixture",
        "scenario_count": len(results),
        "results": [
            {
                "scenario_id": r["scenario_id"] if isinstance(r, dict) else r.scenario_id,
                "title": r["title"] if isinstance(r, dict) else r.title,
                "status": r["status"] if isinstance(r, dict) else r.status,
                "provider": r["provider"] if isinstance(r, dict) else r.provider,
                "assertions": r.get("assertions", []) if isinstance(r, dict) else [a.__dict__ for a in r.assertion_results],
                "metadata": r.get("metadata", {}) if isinstance(r, dict) else r.metadata,
            }
            for r in results
        ],
        "raw_outputs": raw_outputs,
    }
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--system-prompt", default="brains/business/BUSINESS-BRAIN-SYSTEM-PROMPT.md")
    parser.add_argument("--scenarios", default="evaluations/BUSINESS-BRAIN-v0.1-SCENARIOS.md")
    parser.add_argument("--output", default="evaluations/results/BUSINESS-BRAIN-v0.1-RUNTIME-RESULTS.json")
    parser.add_argument("--provider", choices=["fixture", "ollama"], default="fixture")
    parser.add_argument("--model", default="qwen3:8b")
    parser.add_argument("--base-url", default="http://localhost:11434")
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--thinking", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()

    payload = run(
        args.system_prompt,
        args.scenarios,
        args.output,
        provider=args.provider,
        model=args.model,
        base_url=args.base_url,
        temperature=args.temperature,
        thinking=args.thinking,
    )

    counts = {}
    for result in payload["results"]:
        counts[result["status"]] = counts.get(result["status"], 0) + 1

    print(json.dumps({
        "validation_mode": payload["validation_mode"],
        "provider": payload["provider"],
        "model": payload["model"],
        "scenario_count": payload["scenario_count"],
        "counts": counts,
    }))
