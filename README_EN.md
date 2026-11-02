# humanize-output

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?logo=openai&logoColor=white)](https://developers.openai.com/codex/skills)
[![Tests](https://img.shields.io/github/actions/workflow/status/watertreestar/humanize-output/test.yml?branch=main&label=tests)](https://github.com/watertreestar/humanize-output/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Last commit](https://img.shields.io/github/last-commit/watertreestar/humanize-output)](https://github.com/watertreestar/humanize-output/commits/main)

[简体中文](README.md)

Make AI-assisted output fit its real audience, project, and delivery context—not merely sound more human.

`humanize-output` is a Codex Skill for generating or reviewing issues, technical documentation, architecture decisions, code explanations, UI/UX specifications, presentations, and everyday answers. It focuses on missing context, unsupported claims, generic structure, inflated wording, and results that cannot be acted on or verified.

It is neither an AI-authorship detector nor a banned-word replacer. A vocabulary match is only a review signal; context, evidence, and practical purpose determine whether the wording is appropriate.

## Effect

This shortened issue example shows the kind of change the Skill makes. The version, row number, and product rule are known context in the example; the Skill must not invent them when they are absent.

### Before

> **Fix CSV import**
>
> CSV import is unreliable. Sometimes data is incomplete even though the page says it succeeded. Improve error handling and reliability.

### After

> **Rows 1–142 remain saved after validation fails on CSV row 143**
>
> **Environment:** production `v3.8.1`
>
> **Steps:**
> 1. Import a 200-row order CSV.
> 2. Leave `country` empty on row 143; keep the other fields valid.
>
> **Actual:** the API returns `200`, rows 1–142 are saved, and the page reports “200 rows imported.”
>
> **Expected:** if any row fails validation, save none of the batch and identify the failing row and reason.
>
> **Acceptance criteria:**
> - Importing the file above creates zero orders.
> - The error identifies row 143 and the missing `country` value.
> - A valid 200-row file still imports completely.
> - A regression test covers partial writes.

The improvement is not just a more natural tone:

| Before | After |
|---|---|
| “Sometimes unreliable” | Reproducible environment, input, and actual result |
| “Improve reliability” | Explicit behavior and acceptance criteria |
| Engineers must guess the scope | Facts, open questions, and non-goals are separated |
| A complete story may be fabricated | Unsupported details remain marked for confirmation |

See more examples:

- [Before/after comparisons for all seven domains](examples/before-after.md)
- [Issue examples covering bugs, features, performance, technical debt, and incidents](examples/issue-before-after.md)

## What it does

- **Issues and tasks:** adds reproduction details, scope, non-goals, acceptance criteria, and blockers.
- **Technical documentation:** removes promotional openings and makes setup, configuration, verification, and recovery executable.
- **Architecture decisions:** replaces architecture-name stacking with constraints, evidence, trade-offs, and rollback conditions.
- **Code and comments:** avoids speculative abstractions and focuses on real failure paths and business rules.
- **UI/UX:** makes hierarchy and components follow user tasks instead of defaulting to cards, gradients, and motion.
- **Presentations:** replaces achievement packaging with measurable results, risks, and decisions.
- **Everyday answers:** solves the problem first and removes filler, repeated summaries, and ceremonial phrasing.

The Skill uses Generation mode for new work and Review mode when the user provides a draft, asks for critique, or supplies high-stakes content.

## Install

Invoke Codex's built-in installer:

```text
$skill-installer Install the skill from https://github.com/watertreestar/humanize-output
```

Alternatively, use GitHub CLI to clone it into the user-level Skill directory documented by OpenAI.

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
gh repo clone watertreestar/humanize-output "$env:USERPROFILE\.agents\skills\humanize-output"
```

```bash
mkdir -p ~/.agents/skills
gh repo clone watertreestar/humanize-output ~/.agents/skills/humanize-output
```

Codex normally detects new Skills automatically. Restart it if the Skill does not appear. See the [official OpenAI Skills documentation](https://developers.openai.com/codex/skills) for current locations and invocation behavior.

## Usage examples

### Review and rewrite an issue

```text
$humanize-output Review the GitLab issue below. Do not guess missing information. Separate known facts, open questions, and acceptance criteria, then return a ready-to-paste version:

Optimize monthly report performance. It is slow now, so add caching and comprehensively improve query efficiency.
```

### Draft an architecture decision

```text
$humanize-output Using only the measurements I provide, draft an ADR that evaluates moving PDF rendering to our existing worker. Include constraints, trade-offs, validation metrics, and rollback conditions.
```

### Rewrite a README

```text
$humanize-output Rewrite this README's quick start for Windows developers who need to run the project within five minutes. Verify the actual commands, environment variables, expected output, and recovery steps in the repository.
```

### Review a UI specification

```text
$humanize-output Review this operations-dashboard specification. Reorder information around the task of resolving failed payments and cover loading, empty, unauthorized, and batch-processing states.
```

Codex may also select the Skill implicitly for prompts such as “make this less generic” or “turn this draft into a usable deliverable.” Explicit invocation is preferable when you need a reproducible workflow.

## Chinese linter

The linter reads [`data/zh-output-smells.json`](data/zh-output-smells.json). It reports Chinese translation artifacts, inflated wording, filler, theatrical phrasing, weak attribution, placeholders, and repeated syntax. It skips code by default and includes exemptions for legitimate technical contexts.

```bash
python scripts/humanize_lint.py README.md Spec.md
python scripts/humanize_lint.py README.md --format json
python scripts/humanize_lint.py --list
python scripts/humanize_lint.py README.md --fail-on P2
```

The default failure threshold is P1. Use `--fail-on none` for advisory-only output or `--include-code` to scan fenced and inline code.

Example output:

```text
draft.md:3:7 P1 unsupported-absolute (evidence risk)
  match: absolutely safe
  reason: an absolute claim needs evidence, a defined scope, or validation conditions
  suggestion: state the validation scope / make the conclusion conditional
```

A finding is not automatically an error and should not be replaced without reading its context.

## Repository layout

```text
humanize-output/
├── SKILL.md
├── README.md
├── README_EN.md
├── data/          # Chinese lint rules
├── evals/         # model evaluation cases
├── examples/      # before/after comparisons
├── references/    # domain-specific Chinese guidance
├── scripts/       # optional linter
└── tests/
```

## Development

The linter uses only the Python standard library.

```bash
python -m unittest discover -s tests -v
python -m py_compile scripts/humanize_lint.py
```

The Chinese vocabulary and review design draw on [`androidZzT/anti-ai-smell`](https://github.com/androidZzT/anti-ai-smell). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution and license details. This attribution applies only to the referenced third-party material; this repository does not currently declare a project-wide license.
