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
7. memory/MODEL-CONTEXT.md
8. memory/SESSION-CONTEXT.md
9. memory/USER-PREFERENCES.md
10. memory/LEARNINGS.md

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

```yaml
session: 2026-09-24
ai: GPT-5.6 Luna
provider: OpenAI
project_version: v0.1
phase: Block 2 — Business Brain real-model behavioral validation
state: Qwen3 8B validation in progress
completed:
  - provider-neutral runtime harness created and validated: 27/27 PASS
  - portable project memory/context layer created under memory/
  - MODEL-CONTEXT, SESSION-CONTEXT, USER-PREFERENCES and LEARNINGS established
  - D-012 recorded as approved
  - Qwen3 8B T01 and T02 evaluated as PARTIAL PASS
in_progress:
  - Qwen3 8B T03 execution by user
  - assertion-level behavioral evaluation and regression loop
  - Block 2 closure decision
decisions:
  - harness PASS is not LLM behavior PASS
  - legacy skills remain blocked until real-model validation
  - isolated model observations remain provisional until replicated
  - project memory/context is portable and does not override DECISIONS.md
files_created:
  - memory/MODEL-CONTEXT.md
  - memory/SESSION-CONTEXT.md
  - memory/USER-PREFERENCES.md
  - memory/LEARNINGS.md
files_modified:
  - PROJECT-CONTEXT.md
  - DECISIONS.md
  - CHANGELOG.md
open_questions:
  - How will Qwen3 8B perform on T03-T06?
  - Which observed failure modes replicate across scenarios/models?
blockers:
  - No completed real-model battery yet.
next_action: Receive the complete Qwen3 8B T03 output, evaluate it against T01/T02, and do not modify canonical Business Brain behavior from one isolated result.
validation:
  harness_validation: 27/27 PASS
  llm_behavior_validation: IN_PROGRESS
handoff_ready: true
```

## Universal Resume Prompt

Continue PERSONAL AI OS from repository source of truth. Read BOOTSTRAP.md, PROJECT-CONTEXT.md, DECISIONS.md, MASTER-BLUEPRINT.md, CHANGELOG.md, AI-HANDOFF.md, and the memory context files. Reconstruct current state without original conversation. Do not invent decisions/progress. Identify exact next action from PROJECT-CONTEXT.md and SESSION-CONTEXT.md. Preserve the distinction between HARNESS_VALIDATION and LLM_BEHAVIOR_VALIDATION. Do not add legacy skills until real-model behavioral validation is complete. Treat LEARNINGS.md as provisional unless promoted through evidence and decision records.

## Universal Close Prompt

Prepare PERSONAL AI OS for handoff. Execute END/HANDOFF. Update canonical records, record decisions, update Session Handoff Record, verify consistency, commit to GitHub, report exact next action. Do not claim LLM behavior validation from fixture/harness results.

## Human Authority

Human owner final authority for important business, strategic, financial, legal, security, architectural, and irreversible decisions.
“Automate the reversible. Approve the irreversible.”
