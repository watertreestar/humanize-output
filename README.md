# humanize-output

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?logo=openai&logoColor=white)](https://developers.openai.com/codex/skills)
[![Tests](https://img.shields.io/github/actions/workflow/status/watertreestar/humanize-output/test.yml?branch=main&label=tests)](https://github.com/watertreestar/humanize-output/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Last commit](https://img.shields.io/github/last-commit/watertreestar/humanize-output)](https://github.com/watertreestar/humanize-output/commits/main)

[English](README_EN.md)

让 AI 输出贴合真实读者、项目和交付场景，而不是只把句子改得更像人。

`humanize-output` 是一个 Codex Skill，可生成或审查 Issue、技术文档、架构决策、代码说明、UI/UX 规格、演示稿和日常回答。它会优先处理缺少上下文、证据不足、结构模板化、措辞空泛和结果不可执行等问题。

它不是 AI 作者身份检测器，也不是禁词替换器。中文词库的命中只是一条审查线索，最终判断仍要结合语境、证据和实际用途。

## 效果

下面是一个简化的 Issue 示例。Skill 不会凭空补数字；示例里的版本、行号和产品规则都属于已知上下文。

### 改写前

> **修复 CSV 导入问题**
>
> CSV 导入不稳定，有时数据不完整但页面还是成功。请优化异常处理，提升导入可靠性。

### 改写后

> **CSV 第 143 行校验失败后，前 142 行仍被写入**
>
> **环境：** 生产环境 `v3.8.1`
>
> **复现步骤：**
> 1. 导入一份包含 200 行订单的 CSV。
> 2. 第 143 行不填写 `country`，其余字段合法。
>
> **实际结果：** 接口返回 `200`，前 142 行已经写入，页面提示“成功导入 200 条”。
>
> **期望结果：** 任一行校验失败时整批不写入，并指出失败行和校验原因。
>
> **验收条件：**
> - 使用上述文件后，数据库新增订单数为 0。
> - 错误结果包含第 143 行和 `country` 缺失信息。
> - 合法的 200 行文件仍能完整导入。
> - 增加部分写入回归测试。

变化不只是“语气更自然”：

| 改写前 | 改写后 |
|---|---|
| “有时有问题” | 可复现的环境、输入和实际结果 |
| “提升可靠性” | 明确的期望行为和验收条件 |
| 默认让研发猜范围 | 区分已知事实、待确认项和非目标 |
| 容易补造完整故事 | 没有证据的内容会保留为待确认 |

更多效果示例：

- [七类输出的完整前后对比](examples/before-after.md)
- [缺陷、需求、性能、技术债、事故等 Issue 示例](examples/issue-before-after.md)

## 能做什么

- **Issue / 任务：** 补齐复现条件、范围、非目标、验收条件和阻塞信息。
- **技术文档：** 删除宣传式开场，让安装、配置、验证和故障恢复可直接执行。
- **架构决策：** 用约束、证据、代价和回滚条件代替架构名词堆叠。
- **代码与注释：** 避免无依据的抽象，关注真实失败路径和业务约束。
- **UI/UX：** 让信息层级和组件服从用户任务，而不是套用卡片、渐变和动效。
- **演示稿：** 用有口径的结果、风险和决策代替成果包装。
- **日常回答：** 先解决问题，减少套话、重复总结和无效铺垫。

Skill 支持两种工作方式：生成新内容时使用 Generation mode；收到现有草稿、审查请求或高风险内容时使用 Review mode。

## 安装

在 Codex 中调用内置安装器：

```text
$skill-installer Install the skill from https://github.com/watertreestar/humanize-output
```

也可以使用 GitHub CLI 安装到 OpenAI 官方文档列出的用户级 Skill 目录。

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
gh repo clone watertreestar/humanize-output "$env:USERPROFILE\.agents\skills\humanize-output"
```

```bash
mkdir -p ~/.agents/skills
gh repo clone watertreestar/humanize-output ~/.agents/skills/humanize-output
```

Codex 通常会自动发现新 Skill；如果没有出现，请重启 Codex。安装位置和调用机制以 [OpenAI Skills 官方文档](https://developers.openai.com/codex/skills) 为准。

## 使用示例

### 审查并重写 Issue

```text
$humanize-output 审查下面的 GitLab Issue。不要猜测缺失信息；把已知事实、待确认项和验收条件分开，返回可直接粘贴的版本：

优化月报性能。现在打开比较慢，需要增加缓存，全面提升查询效率。
```

### 起草架构决策

```text
$humanize-output 根据我提供的测量结果起草一份 ADR，评估是否把 PDF 渲染迁移到现有 worker。写清约束、代价、验证指标和回滚条件，不要补造数据。
```

### 改写 README

```text
$humanize-output 重写这份 README 的快速开始。读者使用 Windows，需要在 5 分钟内启动项目。核对仓库中真实存在的命令、环境变量和失败恢复步骤。
```

### 审查 UI 规格

```text
$humanize-output 审查这个运营后台规格。按运营人员处理失败付款的任务流重新排信息优先级，并补齐加载、空数据、无权限和批量处理状态。
```

也可以直接说“去 AI 味”“减少模板感”或“把草稿改成可交付版本”，Codex 会根据 Skill 的 `description` 判断是否自动使用它。显式调用更适合需要稳定复现的工作流。

## 中文检查器

检查器读取 [`data/zh-output-smells.json`](data/zh-output-smells.json)，识别翻译腔、膨胀措辞、填充语、戏剧化表达、弱归因、占位内容和重复句式。它默认跳过代码块，并为合理的技术语境提供豁免。

```powershell
python scripts\humanize_lint.py README.md Spec.md
python scripts\humanize_lint.py README.md --format json
python scripts\humanize_lint.py --list
python scripts\humanize_lint.py README.md --fail-on P2
```

默认在发现 P1 或更严重问题时返回非零退出码。使用 `--fail-on none` 可只报告、不阻断；使用 `--include-code` 可同时检查代码块和行内代码。

检查结果示例：

```text
draft.md:3:7 P1 unsupported-absolute（证据风险）
  命中：绝对安全
  原因：绝对化结论需要证据、适用范围或验证条件。
  建议：说明验证范围 / 改为有条件的结论
```

命中不等于错误，不应脱离上下文机械替换。

## 目录结构

```text
humanize-output/
├── SKILL.md
├── README.md
├── README_EN.md
├── data/          # 中文检查规则
├── evals/         # 模型评测用例
├── examples/      # 前后对比
├── references/    # 分领域中文参考
├── scripts/       # 可选检查器
└── tests/
```

## 开发与验证

检查器只使用 Python 标准库。

```bash
python -m unittest discover -s tests -v
python -m py_compile scripts/humanize_lint.py
```

中文词库和审查设计参考了 [`androidZzT/anti-ai-smell`](https://github.com/androidZzT/anti-ai-smell)。来源和许可证说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。该说明只适用于引用的第三方材料；本仓库目前没有声明项目级许可证。
