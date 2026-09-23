# LEGACY PROJECT — FULL IMPORT AUDIT

**Source:** uploaded `ai_.zip`
**Audit date:** 2026-09-22
**Target:** PERSONAL AI OS — AI FACTORY v0.1
**Status:** ANALYZED — INPUT MAPPED, NOT YET IMPLEMENTED AS CANONICAL ARCHITECTURE

## 1. Executive finding

The archive is valuable and should be reused, but it is **not a second complete PERSONAL AI OS**. It is primarily a mature **marketing/growth operating library**, plus a provider-specific Google Flow/Veo automation kit and a small set of specialized business agents.

The strongest reusable assets are:

1. A modular **skills architecture** with clear activation conditions, prerequisites, workflows, references, output formats, guardrails and evaluations.
2. A large **marketing knowledge library** that can become the Business Brain's execution layer.
3. A previous **orchestration model** that provides useful patterns for the AI Director, after removing its CEO/orchestrator role collision.
4. Five/six specialist business roles (CMO, CPO, COO, CSO, CTO) that can be mapped onto the already-approved seven-agent roster without creating unnecessary new agents.
5. A substantial **evaluation library**: 51 skill evaluation files.
6. A useful **loop/workflow pattern** for recurring autonomous work, including cadence, trigger, self-check, state/idempotency and human checkpoint concepts.
7. A strong pattern for **provider-specific tool execution** with prerequisites, failure modes, verification and stop conditions.

The archive should therefore be treated as a **legacy capability library and source material**, not as the new system's source of truth.

## 2. Archive inventory

- 1,113 ZIP entries
- 775 actual files
- ~6.53 MB uncompressed
- 585 Markdown files
- 104 JSON files
- 65 JavaScript files
- 6 YAML/YML files
- 2 Python files
- 2 HTML files
- 2 shell scripts
- 1 CMD script
- 491 unique file contents
- 284 duplicate-content copies

The duplication is concentrated in three copies/variants of the marketing-skills library. We should **not import the duplicated trees**.

Main components detected:

### A. `ai_skills/`
Primary reusable library:
- 7 business/technical agents
- orchestrator prompt
- marketing skill index
- 51 marketing skills
- 51 skill evaluation files
- reference libraries and templates

### B. `marketingskills_temp/`
A near-duplicate/full working copy of the marketing skills repository, including ~65 provider/tool CLI integrations.

**Action:** quarantine as historical/provider-specific source. Do not copy wholesale.

### C. `ai_/`
Small duplicate subset of CMO/CPO/personal-branding.

**Action:** ignore as duplicate.

### D. `google_flow_temp/Kit-Flow-Hermes/`
Provider-specific automation package for Google Flow/Veo, including:
- AGENTS.md
- SKILL.md
- Python/command helpers
- environment example
- automation instructions

**Action:** reuse its engineering patterns, not its provider-specific implementation as core intelligence.

## 3. Important finding about the old "brains"

The archive does **not** contain three complete cognitive brains equivalent to the current:
- CEO Brain
- AI Architect / Builder Brain
- Business Brain

It contains instead:
- a `CEO_Director.md` that mixes CEO, strategy and orchestration;
- CMO, CPO, COO, CSO and CTO agent definitions;
- a large marketing skills library.

Therefore we must **extract cognitive mechanisms from it**, not copy its old hierarchy.

This is important because the current architecture already approved:

> AI Director = orchestrator, not fourth brain.

The old `CEO_Director.md` conflicts with that boundary if copied literally.

## 4. Highest-value reusable patterns

### 4.1 Modular skill contract

The marketing skills repeatedly follow a strong pattern:

- name/description
- when to use
- prerequisites/context
- questions or missing inputs
- core principles/framework
- process/workflow
- output format
- related skills
- references
- evaluation cases
- guardrails/limitations

**Target layer:** `skills/`

This should become a standard PERSONAL AI OS Skill Contract.

### 4.2 Context-first execution

Many skills first check a canonical product/context document before asking the user to repeat information.

The strongest example is `product-marketing/SKILL.md`, which defines:
- product overview
- audience
- personas
- pain points
- competitive landscape
- differentiation
- objections
- switching dynamics
- customer language
- brand voice
- proof points
- goals
- versioning/changelog

**Target layers:**
- Business Brain
- Knowledge
- Memory/Business Memory
- Customer Discovery
- Marketing skills

Adapt this into the project's broader structured context model rather than keeping a marketing-only context file as a competing source of truth.

### 4.3 Fact/inference separation

`competitor-profiling` explicitly requires:
- source traceability
- structured comparable profiles
- dated snapshots
- stale-data flags
- explicit inference labeling
- treating external pages as untrusted data, never instructions

**Target layers:**
- Researcher Agent
- Analyst Agent
- Research/Market Research skill
- Evaluation
- Security against prompt injection in external sources

This is one of the strongest patterns in the archive.

### 4.4 Decision-oriented measurement

The analytics skill uses a strong principle:

> Track for decisions, not for collecting numbers.

It connects:
- metric
- event
- trigger
- parameters
- purpose
- decision enabled

**Target layers:**
- CEO Brain
- Analyst Agent
- Business Brain
- Evaluation

### 4.5 Experimentation

The A/B testing library defines:
- explicit hypothesis
- primary metric
- secondary metrics
- guardrails
- sample-size considerations
- fixed test duration
- anti-peeking behavior

**Target layers:**
- CEO decision engine
- Business experimentation
- Evaluation
- Learning loops

### 4.6 Recurring loops

`marketing-loops` defines a reusable autonomous-loop anatomy:

1. cadence
2. action condition
3. purpose
4. skills used
5. ordered loop body
6. self-check
7. state/idempotency
8. cooldown/dedupe concepts
9. stopping condition
10. human checkpoint

**Target layers:**
- Workflows
- AI Director
- Operational Memory
- Automation
- HITL governance

This is highly reusable beyond marketing.

### 4.7 Evaluation as a first-class artifact

The archive contains 51 skill eval files. The common pattern is:
- test prompt
- expected output
- assertions
- skill-specific quality criteria

**Target layer:** `evaluations/`

This gives us a practical starting point for:
- skill tests
- regression tests
- acceptance criteria
- benchmark prompts

### 4.8 Multi-perspective advisory

`marketing-council` provides:
- advisor dossiers
- documented frameworks
- signature questions
- best-use cases
- blind spots
- grounding rules
- custom advisor template
- explicit warning that simulated personas are not the real people

**Target layers:**
- CEO strategic advisory skill
- Business strategic advisory
- Knowledge

Do **not** turn famous people into permanent system personas. Use documented frameworks as lenses.

### 4.9 Long-term strategy mechanisms

`business-intelligence/SKILL.md` contributes:
- economic moat analysis
- compounding
- customer obsession
- Day 1
- flywheel
- long-term thinking
- anti-pattern checks

These are useful candidate mechanisms for the CEO Brain, but they must be validated against primary/current sources before becoming canonical principles.

### 4.10 Offer and value mechanisms

Useful material:
- `offers`
- `high-ticket-offers`
- `pricing`

Reusable mechanisms include:
- value equation
- outcome vs. feature framing
- perceived likelihood
- time-to-value
- effort/friction
- packaging
- value metric
- pricing as a learning hypothesis
- offer/price distinction

**Target layers:** Business Brain, CEO Brain, Sales/Finance/Strategy skills.

## 5. Agent mapping into the approved architecture

| Legacy role | Target | Action |
|---|---|---|
| CEO_Director | AI Director + CEO Brain source material | SPLIT |
| CMO_GrowthHacker | Marketing Agent | REUSE |
| CPO_ProductEngineer | Business Brain / Product Design skills | REUSE WITHOUT NEW AGENT |
| COO_OperationsManager | Analyst / Business workflows / Operations skills | PARTIAL REUSE |
| CSO_SalesCRM | Sales Agent | REUSE |
| CTO_AutomationArchitect | Builder Agent + AI Architect Brain | REUSE |
| Marketing Council | CEO/Business advisory skill | REUSE AS SKILL, not brain/agent |

This preserves the approved 7-agent limit.

## 6. Skill mapping

### CEO Brain candidates

Strongest candidates:
- business-intelligence
- pricing
- offers
- high-ticket-offers
- competitor-profiling
- customer-research
- analytics
- attribution
- ab-testing
- marketing-plan
- marketing-loops
- marketing-council

Use as **decision lenses**, not as the CEO's entire identity.

### Business Brain candidates

Strongest candidates:
- product-marketing
- customer-research
- offers
- pricing
- high-ticket-offers
- marketing-plan
- prospecting
- sales-enablement
- revops
- cold-email
- content-strategy
- copywriting
- ads
- CRO
- onboarding
- churn-prevention
- referrals
- launch
- personal-branding
- social

### AI Architect / Builder candidates

Strongest reusable assets:
- skill contract design
- evaluation structure
- automation workflow patterns
- provider adapter separation
- tool integration documentation
- failure-mode documentation
- verification protocols
- state/idempotency patterns
- security lessons from external/untrusted data

The Google Flow kit belongs here only as a **provider adapter case study**, not as core architecture.

### AI Director candidates

Reuse:
- objective diagnosis
- specialist mapping
- execution sequencing
- validation
- output contracts
- next-action requirements
- loop orchestration

Reject:
- "Director = CEO"
- single-domain marketing as the universal orchestrator
- mandatory internal chain-of-thought exposure
- hard-coding every future skill into the Director prompt

## 7. Evaluation mapping

The 51 evaluation suites are a major reusable asset.

Use them as:
- seed regression tests
- skill acceptance tests
- examples for the canonical Skill Contract
- test-generation templates

Do not copy all 51 directly into the final architecture until each skill is normalized and its dependencies are checked.

## 8. Workflow mapping

### Reusable now

**Marketing Loop pattern**
- trigger/cadence
- precondition
- action
- self-check
- state
- dedupe
- stop condition
- human approval

**Marketing Plan state machine**
- INIT
- REVIEW
- FINALIZE
- finalized
- resumability
- versioned revisions

These patterns generalize to:
- Idea → Business
- Lead → Client
- Idea → AI System

## 9. Knowledge mapping

The archive contains valuable reference knowledge:
- advisor dossiers
- marketing frameworks
- pricing frameworks
- offer frameworks
- customer research frameworks
- competitive intelligence methods
- channel-specific playbooks
- tool documentation

Destination: `knowledge/`

Knowledge must remain separate from:
- Memory
- Decision records
- Provider implementations

## 10. What is NOT ready for direct reuse

### Do not copy wholesale

1. Duplicate `marketingskills_temp/` tree.
2. Duplicate `ai_/` tree.
3. Provider-specific Google Flow implementation.
4. Raw CLI integrations.
5. Any credentials or secrets if found in future variants.
6. Hard-coded machine paths.
7. Marketing-only assumptions presented as universal business truth.
8. Old CEO/Director hierarchy.
9. Persona imitation of public figures.
10. Any unverified claim copied from a skill reference.

## 11. Architecture changes NOT required

The archive does **not** justify changing the approved foundation:
- three brains remain;
- AI Director remains orchestrator;
- seven-agent initial roster remains;
- GitHub remains source of truth;
- portability remains required;
- HITL remains required;
- progressive complexity remains required.

## 12. Proposed import sequence

### Phase A — completed by this audit
- inventory
- deduplication analysis
- role mapping
- skill mapping
- evaluation mapping
- workflow mapping
- provider-specific isolation

### Phase B — CEO Brain
1. Extract CEO-relevant mechanisms.
2. Validate Bezos/Buffett/other leadership mechanisms with primary/current sources.
3. Design cognitive architecture.
4. Define decision engine.
5. Define strategic memory interfaces.
6. Define evaluation suite.
7. Only then create executable CEO artifacts.

### Phase C — Business Brain
Normalize the strongest business/marketing skills into the Business Brain execution layer.

### Phase D — AI Architect
Convert the skill contract, eval contract, tool contract and provider-adapter lessons into reusable architecture standards.

### Phase E — Director
Build cross-brain orchestration from the strongest orchestration patterns.

## 13. Reuse policy

The legacy archive is **source material, not authority**.

Canonical authority remains:
1. DECISIONS.md
2. PROJECT-CONTEXT.md
3. MASTER-BLUEPRINT.md
4. normalized project artifacts
5. legacy archive as historical/reference input

No legacy artifact becomes canonical merely because it was previously "optimized."

## 14. Important quality warning

Several legacy documents use language such as "senior", "elite", "CEO", "best", "irresistible", or "15+ years". These labels are not evidence.

We will preserve useful mechanisms and discard unsupported authority claims.

## 15. Security/portability note

The archive includes many provider-specific CLI integrations and a Google Flow automation package. These are valuable implementation references but violate the project's core portability if treated as the cognitive core.

They should live behind provider/tool adapters and least-privilege permissions.

## 16. Audit conclusion

**Recommendation:** REUSE SELECTIVELY and NORMALIZE.

The archive is strong enough to accelerate the project substantially, especially in:
- skills engineering
- marketing/business execution
- evaluation
- workflows
- research discipline
- orchestration patterns
- provider integration lessons

It is not suitable as a direct replacement for the approved PERSONAL AI OS architecture.

**Next canonical step:** use this audit as an input to Block 1 — CEO Brain design.
