"""Provider adapter for local Ollama models.

The adapter intentionally uses Python's standard library only so the runtime
remains portable and does not couple the Business Brain to an SDK.
"""

import json
import urllib.request
from typing import Any

from runtime.business_brain.models import ModelResponse
from runtime.business_brain.adapters.base import ModelAdapter


class OllamaAdapter(ModelAdapter):
    name = "ollama"

    def __init__(
        self,
        model: str = "qwen3:8b",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.6,
        thinking: bool = True,
        timeout: int = 300,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.thinking = thinking
        self.timeout = timeout

    def generate(self, system_prompt: str, scenario_input: str) -> ModelResponse:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": scenario_input},
            ],
            "stream": False,
            "options": {"temperature": self.temperature},
            "think": self.thinking,
        }
        request = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            raw = json.loads(response.read().decode("utf-8"))

        message = raw.get("message", {})
        text = message.get("content", "")
        return ModelResponse(
            text=text,
            provider=self.name,
            metadata={
                "model": self.model,
                "base_url": self.base_url,
                "thinking": self.thinking,
                "temperature": self.temperature,
                "done": raw.get("done"),
                "total_duration_ns": raw.get("total_duration"),
                "prompt_eval_count": raw.get("prompt_eval_count"),
                "eval_count": raw.get("eval_count"),
            },
        )
