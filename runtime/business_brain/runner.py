import argparse
import json
import re
from pathlib import Path

from runtime.business_brain.adapters.base import load_system_prompt
from runtime.business_brain.adapters.fixture import FixtureAdapter
from runtime.business_brain.adapters.ollama import OllamaAdapter
from runtime.business_brain.models import Scenario
from runtime.business_brain.evaluator import evaluate_scenario


def load_scenarios(path):
    text = Path(path).read_text(encoding="utf-8")
    chunks = re.split(r"(?=^## (?:Scenario|X))", text, flags=re.M)
    out = []
    for chunk in chunks:
        m = re.match(r"^## (Scenario|X)(?: |)(\\d+)? ?— ?(.+)$", chunk, re.M)
        if not m:
            continue
        kind, num, title = m.groups()
        sid = ("X" + num if kind == "X" else num)
        im = re.search(r"\\*\\*Input:\\*\\* (.+?)(?=\\n\\n|\\n##|$)", chunk, re.S)
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
    system = load_system_prompt(system_prompt_path)
    scenarios = load_scenarios(scenario_path)
    adapter = build_adapter(provider, model, base_url, temperature, thinking)
    results = []
    raw_outputs = []

    for scenario in scenarios:
        response = adapter.generate(system, scenario.input_text)
        raw_outputs.append({
            "scenario_id": scenario.scenario_id,
            "title": scenario.title,
            "provider": response.provider,
            "metadata": response.metadata,
            "text": response.text,
        })
        results.append(evaluate_scenario(scenario, response))

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
                "scenario_id": r.scenario_id,
                "title": r.title,
                "status": r.status,
                "provider": r.provider,
                "assertions": [a.__dict__ for a in r.assertion_results],
                "metadata": r.metadata,
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
