from abc import ABC, abstractmethod
from pathlib import Path
from runtime.business_brain.models import ModelResponse

class ModelAdapter(ABC):
    name = "unknown"
    @abstractmethod
    def generate(self, system_prompt: str, scenario_input: str) -> ModelResponse:
        raise NotImplementedError

def load_system_prompt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")
