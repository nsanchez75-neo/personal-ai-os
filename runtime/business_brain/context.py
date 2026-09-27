"""Context construction for the provider-neutral Business Brain runtime."""

from pathlib import Path


def build_context(
    system_prompt_path: str = "brains/business/BUSINESS-BRAIN-SYSTEM-PROMPT.md",
    runtime_contract_path: str = "runtime/business_brain/RUNTIME-CONTRACT.md",
) -> str:
    system = Path(system_prompt_path).read_text(encoding="utf-8").strip()
    contract = Path(runtime_contract_path).read_text(encoding="utf-8").strip()
    return f"{system}\n\n--- RUNTIME CONTRACT ---\n{contract}\n"
