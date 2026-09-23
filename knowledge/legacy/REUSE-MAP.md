# LEGACY REUSE MAP

This file maps reusable legacy assets to the canonical PERSONAL AI OS architecture.

## CEO BRAIN
- Strategic lenses: business-intelligence, pricing, offers, high-ticket-offers.
- Decision support: analytics, attribution, ab-testing, competitor-profiling, customer-research.
- Strategy workflow: marketing-plan, marketing-loops.
- Multi-lens review: marketing-council.
- Source material only; validate before canonization.

## AI ARCHITECT / BUILDER BRAIN
- Skill contract pattern from all 51 skills.
- Evaluation contract from 51 eval suites.
- Tool/provider documentation patterns from the CLI library.
- Failure-mode + verification pattern from Google Flow/Hermes.
- State/idempotency patterns from marketing-loops.
- External-content untrusted-input pattern from competitor-profiling.
- Do not import provider-specific implementations into portable core.

## BUSINESS BRAIN
- Product/context: product-marketing.
- Customer: customer-research.
- Offer/pricing: offers, high-ticket-offers, pricing.
- GTM: marketing-plan, prospecting, sales-enablement, revops.
- Acquisition: cold-email, ads, SEO, social, content, PR, referrals.
- Conversion: CRO, signup, onboarding, paywalls.
- Retention: churn-prevention.
- Experimentation: ab-testing, attribution, analytics.
- Brand: personal-branding.
- Launch: launch.

## AI DIRECTOR
Reuse the legacy objective → specialist mapping → execution → validation pattern.
Do not reuse the old identity "CEO Director". The canonical Director remains an orchestrator.

## AGENTS
- Marketing Agent ← CMO
- Sales Agent ← CSO
- Builder Agent ← CTO
- Researcher/Analyst ← competitive intelligence, customer research, analytics
- Finance Agent ← pricing/economics inputs, but no legacy finance brain was found
- Evaluator ← 51 eval patterns
- CPO/COO capabilities become skills/workflows unless a future distinct agent is justified.

## SKILLS
The 51 marketing skills form a candidate legacy skill library. Normalize before canonical import.
Use a manifest and avoid duplicate copies.

## WORKFLOWS
- marketing-loops → reusable loop template
- marketing-plan → resumable state-machine template
- Google Flow process → provider-specific automation template

## KNOWLEDGE
- advisor dossiers
- marketing frameworks
- pricing/offers frameworks
- competitive intelligence methodology
- channel playbooks
- reference docs

## MEMORY
No complete legacy memory architecture was found.
Do not import memory claims as if they existed.

## EVALUATION
Use the 51 eval suites as seed cases for the canonical skill-test system.

## PROVIDERS / TOOLS
The 65 CLI integrations and Google Flow kit are provider-specific references only.
They should be normalized into tool/provider adapters when actually needed.

## PORTABILITY
Portable intellectual assets:
Markdown/YAML/JSON schemas, framework descriptions, evaluation cases, workflows, guardrails.
Non-portable assets:
credentials, local paths, provider APIs, UI hacks, provider-specific tokens, browser assumptions.

## HUMAN AUTHORITY
Keep legacy automation behind the current rule:
"Automatizar lo reversible. Aprobar lo irreversible."
