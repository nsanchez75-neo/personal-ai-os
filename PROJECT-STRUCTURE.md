# PROJECT STRUCTURE

## Core
- `README.md` — human overview
- `BOOTSTRAP.md` — recovery/migration protocol
- `PROJECT-CONTEXT.md` — current operational state
- `DECISIONS.md` — durable architectural decisions
- `MASTER-BLUEPRINT.md` — canonical architecture
- `CHANGELOG.md` — historical evolution

## Architecture
- `brains/` — three cognitive domains
- `director/` — orchestration
- `agents/` — specialist execution roles
- `skills/` — reusable capabilities
- `tools/` — external capabilities and integrations
- `workflows/` — repeatable business/system processes
- `knowledge/` — reference knowledge
- `memory/` — structured memory domains
- `evaluations/` — validation and regression
- `providers/` — provider-specific adapters
- `exports/` — portable snapshots

## Design rule
The repository separates cognition, orchestration, reusable capabilities, external tools, state, knowledge, workflows, and evaluation so that each layer can evolve independently.
