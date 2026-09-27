# USER PREFERENCES

These are project interaction preferences, not canonical architecture decisions.

## AI Factory work

When the user asks about constructing, evaluating, debugging or extending PERSONAL AI OS:

- Prefer one integrated response block.
- Execute the requested work where the available tools permit it.
- Explain the underlying concept while doing the work so the user learns the architecture/methodology.
- Be explicit about what was actually changed versus what remains proposed.
- Preserve continuity and avoid claiming memory, commits or actions that were not actually completed.
- When repository write tools are directly available, execute repository changes directly; do not require a separate Work handoff merely to save changes to the repository.

## Evaluation work

- Use practical, step-by-step instructions when the user must run a local test.
- Preserve fixed test prompts once a test is established.
- Compare results across models using the same methodology.
- Separate model behavior, prompt compliance, skill execution and system-level reliability.

## Memory instruction

The repository is the durable project memory/source of truth. The user explicitly prefers project instructions and architectural changes to be persisted in GitHub when repository write tools are available.
