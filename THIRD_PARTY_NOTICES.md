# 第三方来源说明

本项目的中文表达规则设计参考了以下开源项目：

- 项目：`anti-ai-smell`
- 作者：androidZzT
- 地址：https://github.com/androidZzT/anti-ai-smell
- 许可证：MIT

本 Skill 吸收了该项目“结构化词库、软硬提示、替代表达、专业语境备注”的设计思路，并参考其中部分公开词条重新整理了 `data/zh-output-smells.json`。当前规则按跨领域输出质量审查目标重新划分严重性，增加了上下文豁免、证据风险、代码块跳过、全文重复检查和可配置失败阈值。

## MIT License

Copyright (c) 2026 androidZzT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

