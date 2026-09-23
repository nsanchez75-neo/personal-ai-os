from runtime.business_brain.adapters.base import ModelAdapter
from runtime.business_brain.models import ModelResponse

class FixtureAdapter(ModelAdapter):
    """Harness-only adapter; does not test LLM behavior."""
    name = "fixture"
    def generate(self, system_prompt: str, scenario_input: str) -> ModelResponse:
        marker = "ASSERTIONS_FOR_HARNESS:\n"
        payload = scenario_input.split(marker, 1)[1] if marker in scenario_input else ""
        return ModelResponse(payload, self.name, {"validation_mode": "HARNESS_VALIDATION"})
