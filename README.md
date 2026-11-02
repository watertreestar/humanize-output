# humanize-output

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?logo=openai&logoColor=white)](https://developers.openai.com/codex/skills)
[![Tests](https://img.shields.io/github/actions/workflow/status/watertreestar/humanize-output/test.yml?branch=main&label=tests)](https://github.com/watertreestar/humanize-output/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Last commit](https://img.shields.io/github/last-commit/watertreestar/humanize-output)](https://github.com/watertreestar/humanize-output/commits/main)

[简体中文](#简体中文) · [English](#english)

## 简体中文

`humanize-output` 是一个面向真实交付场景的 Codex Skill。它帮助模型生成或修订 Issue、文档、架构决策、代码说明、UI/UX 规格、演示稿和日常回答，让内容贴合读者、项目和媒介，而不是套用一份“看起来很完整”的模板。

它不是 AI 作者身份检测器，也不是禁词替换器。词库命中只是一条审查线索；最终判断仍要结合语境、证据和实际用途。

### 能做什么

- 在生成模式下，从一开始就按受众、目标、格式和约束组织内容。
- 在审查模式下，定位空泛结构、翻译腔、证据不足、过度包装和不可执行要求，并直接修订。
- 覆盖 Issue/任务、技术文档、架构、代码、UI/UX、演示稿和对话七类输出。
- 提供中文原生规则、每类前后对比示例，以及专门的 Issue 改写示例集。
- 附带上下文感知的中文检查器，可跳过代码、输出 JSON，并按严重级别控制退出码。

### 安装

推荐在 Codex 中直接调用内置安装器：

```text
$skill-installer Install the skill from https://github.com/watertreestar/humanize-output
```

也可以使用 GitHub CLI 手动安装到 OpenAI 文档列出的用户级 Skill 目录。

PowerShell：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
gh repo clone watertreestar/humanize-output "$env:USERPROFILE\.agents\skills\humanize-output"
```

Bash：

```bash
mkdir -p ~/.agents/skills
gh repo clone watertreestar/humanize-output ~/.agents/skills/humanize-output
```

Codex 通常会自动发现新增 Skill；如果没有出现，请重启 Codex。安装位置和调用方式以 [OpenAI Skills 官方文档](https://developers.openai.com/codex/skills) 为准。

### 使用

显式调用：

```text
$humanize-output 审查这个 GitLab Issue，补齐含糊的验收条件，返回可以直接粘贴的版本。
```

```text
$humanize-output 根据我提供的测量结果起草一份图片处理迁移到 worker 的 ADR，不要补造数据。
```

也可以直接说“去 AI 味”“减少模板感”“审查这份 UI 规格”或“把草稿改成可交付版本”，由 Codex 根据 Skill 描述自动选择。

### 中文检查器

检查器默认读取 [`data/zh-output-smells.json`](data/zh-output-smells.json)，不会自动改写内容，也不会判断文本是否由 AI 创作。

```powershell
python scripts\humanize_lint.py README.md Spec.md
python scripts\humanize_lint.py README.md --format json
python scripts\humanize_lint.py --list
python scripts\humanize_lint.py README.md --fail-on P2
```

默认在发现 P1 或更严重问题时返回非零退出码。使用 `--fail-on none` 可只报告、不阻断；使用 `--include-code` 可同时检查代码块和行内代码。

### 示例与参考

- [七类输出的前后对比](examples/before-after.md)
- [更多 Issue 描述前后对比](examples/issue-before-after.md)
- `references/`：按领域拆分的中文参考规则
- `evals/evals.json`：模型评测提示与预期结果

## English

`humanize-output` is a Codex Skill for producing work that fits a real audience, project, and medium. It generates or revises issues, documentation, architecture decisions, code explanations, UI/UX specifications, presentations, and everyday answers without forcing them into a generic “polished AI response” template.

It is neither an AI-authorship detector nor a banned-word replacer. A vocabulary match is a review signal, not a verdict; context, evidence, and practical purpose still decide whether the wording is appropriate.

### What it does

- Uses Generation mode to shape new work around the audience, objective, format, and constraints.
- Uses Review mode to find generic structure, translation artifacts, unsupported claims, over-packaging, and requirements that cannot be verified, then revises the artifact.
- Covers seven domains: issues/tasks, technical documentation, architecture, code, UI/UX, presentations, and conversation.
- Includes Chinese-native guidance, before/after examples for every domain, and a dedicated collection of issue rewrites.
- Bundles a context-aware Chinese linter with code skipping, JSON output, and severity-based exit codes.

### Install

The simplest option is to invoke Codex's built-in installer:

```text
$skill-installer Install the skill from https://github.com/watertreestar/humanize-output
```

Or clone it with GitHub CLI into the user-level Skill directory documented by OpenAI.

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
gh repo clone watertreestar/humanize-output "$env:USERPROFILE\.agents\skills\humanize-output"
```

Bash:

```bash
mkdir -p ~/.agents/skills
gh repo clone watertreestar/humanize-output ~/.agents/skills/humanize-output
```

Codex normally detects new Skills automatically. Restart it if the Skill does not appear. See the [official OpenAI Skills documentation](https://developers.openai.com/codex/skills) for the current locations and invocation behavior.

### Use

Invoke it explicitly:

```text
$humanize-output Review this GitLab issue, resolve the vague acceptance criteria, and return a ready-to-paste version.
```

```text
$humanize-output Draft an ADR for moving image processing to a worker. Keep every claim tied to the measurements I provide.
```

Codex can also select the Skill implicitly for requests such as “make this less generic,” “review this UI spec,” or “turn this draft into a usable deliverable.”

### Chinese linter

The linter reads [`data/zh-output-smells.json`](data/zh-output-smells.json) by default. It does not rewrite text or infer who wrote it.

```bash
python scripts/humanize_lint.py README.md Spec.md
python scripts/humanize_lint.py README.md --format json
python scripts/humanize_lint.py --list
python scripts/humanize_lint.py README.md --fail-on P2
```

The default exit threshold is P1. Use `--fail-on none` for advisory-only output or `--include-code` to scan fenced and inline code.

### Examples and references

- [Before/after examples for all seven domains](examples/before-after.md)
- [Additional issue-description comparisons](examples/issue-before-after.md)
- `references/`: domain-specific Chinese guidance
- `evals/evals.json`: model evaluation prompts and expected outcomes

## Repository layout

```text
humanize-output/
├── SKILL.md
├── README.md
├── data/
├── evals/
├── examples/
├── references/
├── scripts/
└── tests/
```

## Development

The linter uses only the Python standard library.

```bash
python -m unittest discover -s tests -v
python -m py_compile scripts/humanize_lint.py
```

The Chinese vocabulary and review design draw on [`androidZzT/anti-ai-smell`](https://github.com/androidZzT/anti-ai-smell). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution and license details. This attribution applies to the referenced third-party material; the repository does not currently declare a project-wide license.
