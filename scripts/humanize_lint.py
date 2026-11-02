#!/usr/bin/env python3
"""扫描中文输出中的模板化、翻译腔和证据风险候选项。

这是上下文审查工具，不是 AI 作者身份检测器，也不会自动改写文本。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RULES = ROOT / "data" / "zh-output-smells.json"
FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
SEVERITY_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


@dataclass(frozen=True)
class Finding:
    rule_id: str
    category: str
    severity: str
    line: int
    column: int
    match: str
    message: str
    suggestions: list[str]
    context_note: str = ""
    count: int = 1


def load_rules(path: Path = DEFAULT_RULES) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def visible_lines(text: str, include_code: bool = False) -> Iterable[tuple[int, str]]:
    """Yield scannable lines while masking inline code to preserve columns."""
    in_fence = False
    fence = ""
    for number, line in enumerate(text.splitlines(), start=1):
        marker = FENCE_RE.match(line)
        if marker and not include_code:
            token = marker.group(1)
            if not in_fence:
                in_fence, fence = True, token
            elif token == fence:
                in_fence, fence = False, ""
            continue
        if in_fence and not include_code:
            continue
        yield number, line if include_code else INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)


def _is_exempt(line: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, line, re.IGNORECASE) for pattern in patterns)


def scan(text: str, ruleset: dict[str, Any] | None = None, include_code: bool = False) -> list[Finding]:
    ruleset = ruleset or load_rules()
    findings: list[Finding] = []
    lines = list(visible_lines(text, include_code=include_code))
    for line_number, line in lines:
        for rule in ruleset["rules"]:
            if _is_exempt(line, rule.get("exempt_if_line_matches", [])):
                continue
            pattern = re.escape(rule["pattern"]) if rule["kind"] == "literal" else rule["pattern"]
            for match in re.finditer(pattern, line, re.IGNORECASE):
                findings.append(Finding(
                    rule_id=rule["id"], category=rule["category"], severity=rule["severity"],
                    line=line_number, column=match.start() + 1, match=match.group(0),
                    message=rule["message"], suggestions=rule.get("suggestions", []),
                    context_note=rule.get("context_note", "")))
    visible_text = "\n".join(line for _, line in lines)
    for rule in ruleset.get("document_rules", []):
        matches = list(re.finditer(rule["pattern"], visible_text, re.IGNORECASE))
        if len(matches) < rule["minimum_count"]:
            continue
        first_line = next((n for n, line in lines if re.search(rule["pattern"], line)), 1)
        findings.append(Finding(
            rule_id=rule["id"], category=rule["category"], severity=rule["severity"],
            line=first_line, column=1, match=rule["pattern"], message=rule["message"],
            suggestions=rule.get("suggestions", []), context_note=rule.get("context_note", ""),
            count=len(matches)))
    return sorted(findings, key=lambda item: (item.line, item.column, SEVERITY_RANK[item.severity]))


def list_rules(ruleset: dict[str, Any]) -> None:
    for category_id, title in ruleset["categories"].items():
        print(f"\n{title} [{category_id}]")
        for rule in ruleset["rules"]:
            if rule["category"] != category_id:
                continue
            suggestions = " / ".join(rule.get("suggestions", []))
            note = f"；语境：{rule['context_note']}" if rule.get("context_note") else ""
            print(f"  {rule['severity']} {rule['id']}: {rule['pattern']} → {suggestions}{note}")


def finding_to_dict(path: Path, finding: Finding) -> dict[str, Any]:
    return {"file": str(path), **asdict(finding)}


def print_text(path: Path, findings: list[Finding], categories: dict[str, str]) -> None:
    if not findings:
        print(f"{path}: 未发现候选问题")
        return
    for item in findings:
        count = f"，全文 {item.count} 次" if item.count > 1 else ""
        print(f"{path}:{item.line}:{item.column} {item.severity} {item.rule_id}（{categories.get(item.category, item.category)}{count}）")
        print(f"  命中：{item.match}")
        print(f"  原因：{item.message}")
        if item.suggestions:
            print(f"  建议：{' / '.join(item.suggestions)}")
        if item.context_note:
            print(f"  语境：{item.context_note}")
    print(f"{path}: {len(findings)} 个候选问题；请结合上下文判断，不要机械替换。")


def should_fail(findings: list[Finding], fail_on: str) -> bool:
    if fail_on == "none":
        return False
    threshold = SEVERITY_RANK[fail_on]
    return any(SEVERITY_RANK[item.severity] <= threshold for item in findings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES, help="规则 JSON 文件")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--fail-on", choices=("P0", "P1", "P2", "P3", "none"), default="P1")
    parser.add_argument("--include-code", action="store_true", help="同时扫描代码块和行内代码")
    parser.add_argument("--list", action="store_true", help="列出全部规则")
    args = parser.parse_args(argv)
    try:
        ruleset = load_rules(args.rules)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"无法读取规则文件 {args.rules}: {error}", file=sys.stderr)
        return 2
    if args.list:
        list_rules(ruleset)
        return 0
    if not args.files:
        parser.error("请提供至少一个文件，或使用 --list")
    all_results: list[dict[str, Any]] = []
    has_failure = False
    for path in args.files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            print(f"无法读取 {path}: {error}", file=sys.stderr)
            return 2
        findings = scan(text, ruleset, include_code=args.include_code)
        has_failure = has_failure or should_fail(findings, args.fail_on)
        if args.format == "json":
            all_results.extend(finding_to_dict(path, item) for item in findings)
        else:
            print_text(path, findings, ruleset["categories"])
    if args.format == "json":
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    return 1 if has_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())

