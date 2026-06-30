# SystemWright

> **别再调更强的 Prompt 了——把模糊想法设计成一个会自我复盘的 AI 工作系统。**

SystemWright 是一个跨平台的 [Agent Skill](https://agentskills.io)(开放的 `SKILL.md` 标准),它把一个模糊目标转化成可重复使用的**AI 工作系统**——由四层构成:**Prompt(指令)· Context(上下文)· Harness(工具与权限)· Loop(循环)**。

它能在任何支持 Agent Skills 标准的环境运行——Claude Code、OpenAI Codex CLI、Gemini CLI、Cursor,以及兼容 Claude Code 的模型后端如 Kimi(月之暗面)、GLM(智谱)。skill 本体与运行时无关,各 host 只是安装位置不同。

[![CI](https://github.com/EthanQC/SystemWright/actions/workflows/ci.yml/badge.svg)](https://github.com/EthanQC/SystemWright/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Hosts](https://img.shields.io/badge/hosts-Claude_Code_·_Codex_·_Gemini_·_Cursor-6E56CF)

📖 English: **[README.md](README.md)**  ·  ⭐ 如果它帮你省了时间，点个 star 能帮更多人发现它。

## 30 秒看懂它在做什么

一个创始人把本周五条凌乱的事实贴进来,说"帮我用 AI 管公司"。SystemWright **不会**上来就给你建平台,而是返回一个**今天就能手动跑起来的第一版周度 Loop**:

```text
你给它(原始、凌乱):
  · 本周 28 个销售线索(+6),但只有 3 个进入报价
  · 客户 B 要求周五前确认交付时间
  · "优化审核流"已经口头拍板——但没人负责
  · 客服本周同一个问题重复出现 5 次

它返回(一个可运行的 Loop,而不是一个平台):
  事实 ≠ 观点  ·  2 个具体决策  ·  明确的人工审批点  ·  下周检查项
  → 决策 1:今天就指定审核流 owner,周四前给出最小改动方案。
  → 决策 2:明天中午前给客户 B 一个明确交付时间——别拖到周五。
  → 动作:10 分钟内发 2 条消息;周报先写 5 条事实,不追求完整叙述。
```

**这个 skill 本身就是产品。** MCP、orchestrator、loop、prompt、context pack 都是它在诊断清楚真实需求之后**可能设计的产出**,而**不是前提**。

<!-- TODO(demo): 录一段 30–60 秒的真实运行 asciinema/GIF 嵌在这里。 -->

## 它做两件事

1. **想法澄清(Idea refinement)**——把模糊目标变成一个确认过的工作目标。
2. **工作系统设计(Work-system design)**——把目标转成 Prompt、Context、Harness、Loop 与人工判断规则。

典型产出:平实语言简报(Plain-Language Brief)→ 工作系统卡(Work System Card)→ MCP 与 orchestrator 决策(作为产出)→ 日常使用协议 → 可复制起手 Prompt → Markdown 记录模板 → 试运行 → 复盘规则。

## 为什么是"工作系统"而不是"更强的提示词"

| 层级 | 你以为在学 | 其实要学的 |
|---|---|---|
| Prompt | 怎么问 AI | 怎么把意图表达清楚 |
| Context | 多给 AI 信息 | 怎么筛选、组织、更新背景 |
| Harness | 给 AI 工具 | 怎么设计权限、规则、验证与护栏 |
| Loop | 让 AI 自动跑 | 怎么设计一个可持续、可检查、可停止、可改进的系统 |

低效用法:问一句,得一个答案。
高效用法:设计一个工作系统,让 AI 在里面持续推进一类任务,且每一轮都有检查、反馈和沉淀——而价值判断仍由你来下。

## 安装

skill 就是一个普通的 `SKILL.md` 目录,安装 = "把 `system-wright/` 拷进 host 的 skills 目录"。自带的安装脚本可移植完成(不写死 home):

```sh
# 克隆后选择你的 host:claude | codex | gemini | cursor
git clone https://github.com/EthanQC/SystemWright && cd SystemWright
sh scripts/install.sh --host claude

# 或安装到自定义 / 项目级 skills 目录:
sh scripts/install.sh --dir /path/to/skills
sh scripts/install.sh --host claude --project   # 装到 ./.claude/skills
```

### 各 host 对照

| Host | 用户级 skills 目录 | 项目级 | 调用方式 |
|------|----------------------|---------------|------------|
| **Claude Code** | `~/.claude/skills/system-wright` | `.claude/skills/system-wright` | 自然语言,或 `/system-wright` |
| **OpenAI Codex CLI** | `~/.codex/skills/system-wright` | `.agents/skills/` 或 `.codex/skills/` | `$system-wright` |
| **Gemini CLI** | `~/.gemini/skills/system-wright` | `.gemini/skills/` | 自然语言 / `/skills` |
| **Cursor** | `~/.cursor/skills/system-wright` | `.cursor/skills/` | Agent 聊天里输入 `/` |

GitHub Copilot、Cline、Windsurf、OpenCode 也从各自的 skills 目录读取同一个 `SKILL.md`。跨工具别名 `~/.agents/skills/` 与 `.agents/skills/` 被多个 host 识别。

### Kimi(月之暗面)与 GLM(智谱)

Kimi 和 GLM 没有独立的 skill 系统——你是通过 Anthropic 兼容端点**在 Claude Code 内**运行它们,所以 skill 在 harness 层从 `~/.claude/skills/` 加载。用 `--host claude` 安装,再把 Claude Code 指向后端:

```sh
# Kimi(月之暗面)
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"   # 国内用 .cn
export ANTHROPIC_AUTH_TOKEN="<your-moonshot-key>"
export ANTHROPIC_MODEL="kimi-k2.7-code"                          # 或你套餐提供的模型

# GLM(智谱)
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"       # 注意 /api/ 段
export ANTHROPIC_AUTH_TOKEN="<your-z.ai-key>"
export ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.6"                     # 或你套餐提供的模型
```

模型名会变——用你套餐当前提供的型号即可,只有环境变量的形状是固定的。

### Windows

在 Git Bash / WSL 下运行安装脚本,或在 PowerShell 里手动拷贝目录:

```powershell
$dest = "$env:USERPROFILE\.claude\skills\system-wright"
Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue
Copy-Item -Recurse system-wright $dest
```

## 怎么用

自然语言描述需求(每个 host 都适用):

```text
我想优化 xhs-ops-system，但我不知道应该做 prompt、context、harness、loop、MCP、orchestrator 还是 skill。请先帮我拆解想法，再设计一个能试跑的工作系统。
```

或在支持显式调用的 host(如 Codex)里:

```text
$system-wright
我有一个模糊想法，想把它设计成一个可重复使用的 AI 工作系统：[贴上你的想法]
```

## 实测记录(`test-output/`)

- `actual-test-messy-ai-article-loop.md`:把一段凌乱、非技术的输入变成可用的阅读/工作 Loop。
- `actual-test-xhs-ops-system.md`:小红书运营用例,含 MCP/orchestrator 边界判定。
- `actual-test-founder-level-idea.md`:创始人级模糊目标变成一个周度决策 Loop。
- `negative-trigger-tests.md`:一次性改写、纯定义、临时清单、普通 code review **不会**触发本 skill。

## 校验

所有检查都不依赖第三方库、不联网,任何 clone 都能跑:

```sh
python3 quick_validate.py                 # 结构校验(自包含)
python3 scripts/test_validate_skill.py    # 校验器单测
python3 tests/check_skill_quality.py      # 完整性 lint
```

CI(`.github/workflows/ci.yml`)在干净检出上跨 Python 3.9 / 3.12 运行这些检查。

## 许可

[MIT](LICENSE)。
