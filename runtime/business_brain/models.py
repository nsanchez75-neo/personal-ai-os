from dataclasses import dataclass, field
from typing import Any

@dataclass
class Scenario:
    scenario_id: str
    title: str
    input_text: str
    assertions: list[str]
    cross_brain: bool = False

@dataclass
class ModelResponse:
    text: str
    provider: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AssertionResult:
    assertion: str
    status: str
    reason: str = ""

@dataclass
class ScenarioResult:
    scenario_id: str
    title: str
    status: str
    provider: str
    assertion_results: list[AssertionResult]
    metadata: dict[str, Any] = field(default_factory=dict)
