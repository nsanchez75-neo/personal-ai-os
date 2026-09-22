# MEMORY POLICY

Memory is distinct from knowledge.

## Domains

### Personal Memory
Stable user preferences and personal context that the user explicitly wants retained.

### Business Memory
Customers, offers, experiments, business assumptions, metrics, and business decisions.

### Project Memory
Architecture, decisions, project state, requirements, and implementation history.

### Operational Memory
Execution logs, workflow state, incidents, task state, and temporary operational context.

## Rules

- Critical project state must exist in repository artifacts.
- Native model memory must not be the sole source of truth.
- Sensitive information should be minimized.
- Secrets and credentials never belong in Git.
- Memory changes should be auditable where practical.
