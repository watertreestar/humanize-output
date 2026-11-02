---
name: humanize-output
description: Improve or review AI-assisted outputs so they fit the real audience, task, project context, and delivery constraints instead of sounding generic, mechanical, over-packaged, or unsupported. Use for generating or revising issues, requirements, Markdown and technical docs, architecture decisions, code and comments, UI/UX specifications, slide content, project summaries, and everyday answers—especially when the user asks to “humanize,” “去 AI 味,” make something less generic, reduce boilerplate, review output quality, or turn a draft into a directly usable deliverable. Do not use it to infer AI authorship or evade AI detectors.
---

# Humanize Output

Create work that is useful in its actual setting, not merely shaped like a polished answer. Treat “AI smell” as an output-quality problem: missing context, weak evidence, generic structure, ornamental language, or impractical decisions. Never claim that style proves AI authorship.

## Core principles

- Context over template: fit the reader, task, repository, medium, and constraints before choosing a structure.
- Clarity over sophistication: prefer the most precise language the audience will understand.
- Substance over volume: remove content that does not help someone decide, act, implement, or verify.
- Evidence over assertion: source, qualify, or label claims; do not invent facts, metrics, citations, APIs, or capabilities.
- Purpose over convention: use headings, tables, cards, patterns, and abstractions only when they help the task.
- Human judgment over automation: treat lint findings as review prompts, not automatic verdicts.

## Choose a mode

Use **Generation mode** by default. Apply these principles while producing the requested artifact, then run a brief delivery check before responding.

Use **Review mode** when the user supplies an existing artifact, explicitly asks for critique/revision, or the task is high-stakes. Diagnose the important problems, revise the artifact directly when authorized, and validate the result.

## Workflow

1. Establish the output contract from available context:
   - audience and practical purpose;
   - requested medium and format;
   - project conventions and constraints;
   - evidence or verification expected;
   - what “ready to use” means.
   Ask only when a missing answer would materially change the result. Otherwise make the smallest safe assumption and state it briefly if relevant.
2. Select the dominant domain and read only its reference file. Add a second domain only for a genuinely mixed artifact.
3. Produce or inspect the artifact against five questions:
   - Does it answer the real request rather than a generic version of it?
   - Is every important claim grounded, qualified, or marked for verification?
   - Does the structure reflect priority and workflow rather than a stock template?
   - Are the language, technical depth, and design appropriate for the audience?
   - Can the result be used or verified without filling obvious gaps?
4. Revise by removing noise before adding content. Preserve accurate terminology, useful structure, the author’s voice, and project conventions.
5. Run the delivery check and return the requested artifact. Do not add a review essay unless it helps the user or they asked for one.

## Domain routing

| Artifact | Read |
|---|---|
| GitLab/GitHub issue, task, requirement, acceptance criteria | `references/issue.md` |
| README, API guide, technical or general documentation | `references/documentation.md` |
| Architecture proposal, ADR, system design, technology choice | `references/architecture.md` |
| Code, comments, naming, abstractions, implementation plan | `references/code.md` |
| UI/UX, admin console, dashboard, component or page specification | `references/ui-ux.md` |
| Slides, technical briefing, project review, presentation outline | `references/presentation.md` |
| Chat reply, explanation, recommendation, everyday Q&A | `references/conversation.md` |

For language-level symptoms across domains, also consult `references/language.md` when wording itself is a central problem. Do not load every reference by default.

## Review severity

- **P0 — Blocker:** factual error, fabricated evidence or citation, security/safety problem, or a broken core flow. Fix before delivery.
- **P1 — Major:** unusable instructions, unsupported core decision, missing critical context, or an unclear main requirement. Fix before delivery.
- **P2 — Quality:** generic wording, repetition, needless abstraction, decorative design, or visible AI-pattern residue that weakens the artifact. Usually fix.
- **P3 — Preference:** optional stylistic choice with no meaningful effect. Do not force a change.

In Review mode, report only consequential findings. Use this compact shape when a report is useful:

```markdown
### P1 — [specific problem]
- Evidence: [quote or visible decision]
- Impact: [why it prevents the artifact doing its job]
- Fix: [concrete change]
- Revision: [replacement text or implementation direction, when useful]
```

## Language judgment

Do not turn humanization into a banned-word exercise. Terms such as “gating,” “convergence,” “orchestration,” or their Chinese equivalents may be exact in the right field. Keep a term when it is standard for the intended reader and more precise than a plain-language substitute.

Match the language of the requested deliverable. For Chinese output, prefer natural Chinese information order and established Chinese technical usage; do not preserve English sentence structure merely because it is grammatically translatable. Read `references/language.md` for Chinese-specific checks when wording is a central concern. Keep standard abbreviations such as API, ADR, SSO, and UI/UX when they are clearer to the intended readers than forced translations.

Watch for clusters rather than isolated tokens: empty framing, translationese, theatrical claims, repeated conclusions, excessive headings, uniform three-part lists, and inflated verbs can combine into a generic voice. Rewrite the underlying thought, not just the flagged word.

The optional linter uses `data/zh-output-smells.json` to identify candidates. It includes Chinese lexical and syntax rules, suggested rewrites, severity, and context exemptions for legitimate technical usage:

```text
python scripts/humanize_lint.py <file> [<file> ...]
python scripts/humanize_lint.py --list
python scripts/humanize_lint.py <file> --format json --fail-on P2
```

The default exit threshold is P1. Use `--fail-on P2` only when a project deliberately treats generic output as a delivery gate; use `--fail-on none` for advisory scans. Code fences and inline code are skipped unless `--include-code` is supplied.

Inspect each finding in context. Read its `context_note` before changing technical terms such as “门控,” “收敛,” “原语,” or “心智模型.” Never rewrite solely to make the linter pass.

## Delivery check

Before returning the result:

1. Confirm the requested format and scope are satisfied.
2. Remove unsupported claims, invented details, placeholders, repeated conclusions, and unused template sections.
3. Confirm examples, commands, APIs, designs, or recommendations are plausible in the stated environment; test them when the task permits.
4. Check that the opening reaches the useful point and the ending supplies the needed decision, action, or result.
5. Prefer the artifact itself over commentary about how well it was written.

See `examples/before-after.md` for Issue, architecture, and UI examples. Use them as reasoning examples, not templates.

