# PORTABILITY POLICY

PERSONAL AI OS must not depend on one AI provider for its core identity or logic.

## Portable core

Prefer:
- Markdown
- YAML
- JSON
- Python

## Provider-specific layer

Provider-specific prompts, adapters, APIs, model configuration, and authentication belong under `providers/`.

## Migration requirement

A new AI provider should be able to reconstruct the project from the repository without access to the original provider account.
