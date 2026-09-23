# AI HANDOFF

## Purpose

This file is the universal handoff protocol for PERSONAL AI OS. It allows the project to continue across ChatGPT sessions, accounts, models, providers, or other AI systems without depending on the original conversation.

It complements the canonical project files. It does not replace them.

## Source of Truth

GitHub repository:
https://github.com/nsanchez75-neo/personal-ai-os

Authority hierarchy:

1. DECISIONS.md
2. PROJECT-CONTEXT.md
3. MASTER-BLUEPRINT.md
4. Specialized project files
5. Conversations and temporary context

When sources conflict, do not silently choose. Identify the conflict and resolve it according to the authority hierarchy or request human approval.

## Continuity Pack

Before continuing substantive work, read:

1. BOOTSTRAP.md
2. PROJECT-CONTEXT.md
3. DECISIONS.md
4. MASTER-BLUEPRINT.md
5. CHANGELOG.md
6. AI-HANDOFF.md

Then read only the specialized files required for the current objective.

## START PROTOCOL

A new AI must:

1. Identify itself as a temporary execution context, not the owner of project truth.
2. Read the Continuity Pack.
3. Reconstruct:
   - project mission
   - current version
   - current phase
   - completed work
   - protected decisions and constraints
   - current objective
   - next objective
   - open questions
   - blockers
4. Confirm what is known versus unknown.
5. Never invent missing history, decisions, files, versions, progress, credentials, or requirements.
6. Never replace an approved architecture merely because another design is possible.
7. Before substantive work, state the exact objective it is continuing.

## WORK PROTOCOL

During work:

- Treat GitHub as the persistent source of truth.
- Keep provider-specific implementation separate from portable core intelligence.
- Preserve the separation between brains, agents, skills, tools, memory, knowledge, workflows, and evaluation.
- Prefer simple, modular, testable changes.
- Reuse existing components before creating new ones.
- Record durable architectural decisions in DECISIONS.md.
- Record meaningful project evolution in CHANGELOG.md.
- Keep PROJECT-CONTEXT.md current and concise.
- Do not store secrets, API keys, tokens, passwords, or private credentials in the repository.
- Use least privilege for tools and integrations.
- Do not perform irreversible or high-impact external actions without human approval.
- Do not claim an action was completed unless it was actually verified.

## DECISION PROTOCOL

When a proposed change affects architecture, boundaries, source of truth, memory, portability, security, agents, skills, workflows, or other durable project behavior:

1. Identify the proposed change.
2. Explain why it is needed.
3. Check existing decisions for conflicts.
4. If approved by the human owner, record the decision in DECISIONS.md before relying on it as an architectural fact.
5. Mark superseded decisions explicitly rather than silently rewriting history.

## END / HANDOFF PROTOCOL

Before ending a meaningful session or transferring work to another AI:

1. Finish or clearly identify incomplete work.
2. Update PROJECT-CONTEXT.md.
3. Update DECISIONS.md if a durable decision was made.
4. Update CHANGELOG.md for meaningful completed changes.
5. Update this file's Session Handoff Record below.
6. Verify that the repository is internally consistent.
7. Commit the changes to GitHub.
8. Verify the commit/ref when possible.
9. Report:
   - completed
   - in progress
   - decisions
   - files created
   - files modified
   - open questions
   - blockers
   - exact next action
   - validation performed

The handoff is not complete until another AI can determine the next action without needing the original conversation.

## Session Handoff Record

Keep only the latest meaningful handoff here; historical evolution belongs in CHANGELOG.md.

```yaml
session:
  date: 2026-09-22
  ai: GPT-5.6 Luna / current execution context
  provider: OpenAI
  project_version: v0.1

state:
  phase: Block 2 — Business Brain v0.1 scenario validation
  status: Scenario suite and ambiguity protocol completed; pre-runtime conformance PASS; runtime evaluator still required.

completed:
  - 22 acceptance scenarios created and reviewed for pre-runtime conformance
  - Five cross-brain workflow scenarios created
  - Ambiguous experiment protocol integrated into Business Brain prompt and decision engine
  - Scenario validation report created
  - 

in_progress:
  - Implement minimal provider-neutral Business Brain runtime/evaluator
  - 

decisions:
  - 

files_created:
  - 

files_modified:
  - 

open_questions:
  - 

blockers:
  - 

next_action: Implement and execute the provider-neutral evaluator against the 22 scenarios plus five cross-brain scenarios; record assertion-level results and regressions.

validation:
  - 22/22 PASS for pre-runtime scenario/specification conformance
  - Runtime/model-behavior validation not yet executed
  - Block 2 remains open

handoff_ready: true
```

## Universal Resume Prompt

A new AI may be given:

"Continue PERSONAL AI OS from the repository source of truth. Read BOOTSTRAP.md, PROJECT-CONTEXT.md, DECISIONS.md, MASTER-BLUEPRINT.md, CHANGELOG.md, and AI-HANDOFF.md. Reconstruct the current state without relying on the original conversation. Do not invent decisions or progress. Identify the exact next action from PROJECT-CONTEXT.md and continue only within the approved architecture. At the end, execute the END / HANDOFF PROTOCOL and leave GitHub ready for the next AI."

## Universal Close Prompt

At the end of a session:

"Prepare PERSONAL AI OS for handoff. Execute the END / HANDOFF PROTOCOL. Update the canonical project records, record durable decisions, update the Session Handoff Record, verify consistency, commit to GitHub, and report the exact next action. Do not claim completion without verification."

## Human Authority

The human owner remains the final authority for important business, strategic, financial, legal, security, architectural, and irreversible decisions.

Principle:

**Automate the reversible. Approve the irreversible.**
