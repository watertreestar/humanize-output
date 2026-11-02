import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("humanize_lint", ROOT / "scripts" / "humanize_lint.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class HumanizeLintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = MODULE.load_rules(ROOT / "data" / "zh-output-smells.json")

    def ids(self, text, include_code=False):
        return {item.rule_id for item in MODULE.scan(text, self.rules, include_code=include_code)}

    def test_detects_grandiose_and_evidence_patterns(self):
        ids = self.ids("这套方案将全面提升体验，为业务保驾护航，并保证零故障。")
        self.assertIn("zh-all-round", ids)
        self.assertIn("zh-new-chapter", ids)
        self.assertIn("unsupported-absolute", ids)

    def test_skips_fenced_and_inline_code(self):
        text = "~~~text\n全面赋能\n~~~\n`全面赋能` 是待检查样例。"
        self.assertNotIn("zh-empower", self.ids(text))
        self.assertIn("zh-empower", self.ids(text, include_code=True))

    def test_exempts_precise_technical_context(self):
        ids = self.ids("训练过程在第 20 轮收敛。机器学习门控网络负责选择专家。")
        self.assertNotIn("zh-converge", ids)
        self.assertNotIn("zh-gating", ids)

    def test_flags_ambiguous_terms_outside_technical_context(self):
        ids = self.ids("讨论终于收敛了，再加一道门控保证所有人同意。")
        self.assertIn("zh-converge", ids)
        self.assertIn("zh-gating", ids)

    def test_document_rule_requires_repetition(self):
        self.assertNotIn("zh-em-dash-overuse", self.ids("一次——合理停顿。"))
        self.assertIn("zh-em-dash-overuse", self.ids("一——二——三——四。"))

    def test_fail_threshold(self):
        findings = MODULE.scan("值得注意的是，这个方案绝对安全。", self.rules)
        self.assertTrue(MODULE.should_fail(findings, "P1"))
        self.assertFalse(MODULE.should_fail(findings, "P0"))
        self.assertFalse(MODULE.should_fail(findings, "none"))


if __name__ == "__main__":
    unittest.main()

