# SystemWright

> **Stop writing better prompts. Design the system that runs them.**

SystemWright is a cross-platform [Agent Skill](https://agentskills.io) (the open `SKILL.md` standard) that turns a vague goal into a reusable **AI work system** — built from four layers: **Prompt · Context · Harness · Loop**.

It runs anywhere the Agent Skills standard is supported — Claude Code, OpenAI Codex CLI, Gemini CLI, Cursor, and Claude-Code-compatible model backends such as Kimi (Moonshot) and GLM (Zhipu). The skill body is runtime-neutral; only the install location differs per host.

[![CI](https://github.com/EthanQC/SystemWright/actions/workflows/ci.yml/badge.svg)](https://github.com/EthanQC/SystemWright/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Hosts](https://img.shields.io/badge/hosts-Claude_Code_·_Codex_·_Gemini_·_Cursor-6E56CF)

📖 中文说明请见 **[README.zh-CN.md](README.zh-CN.md)**  ·  ⭐ if SystemWright saves you time, a star helps others find it.

## See it in 30 seconds

A founder pastes five messy facts from their week and says "help me run my company with AI." Instead of building a platform, SystemWright returns a **first weekly loop you can run by hand today**:

```text
You give it (raw, messy):
  · 28 leads this week (+6), but only 3 reached a quote
  · Customer B needs a delivery date confirmed by Friday
  · "Optimize the review flow" was decided — but nobody owns it
  · Support hit the same question 5× this week

It returns (a runnable loop, not a platform):
  facts ≠ opinions  ·  2 concrete decisions  ·  explicit human-approval gates  ·  next-week checks
  → Decision 1: assign an owner for the review flow today; minimal plan by Thursday.
  → Decision 2: give Customer B a firm date by tomorrow noon — don't let it slip to Friday.
  → Action: send 2 messages in the next 10 minutes; write 5 facts, not a full report.
```

The skill itself is the product. MCPs, orchestrators, loops, prompts, and context packs are possible *outputs* it may design after diagnosing the real need — never prerequisites.

## What it does

A two-layer process:

1. **Idea refinement** — turn a vague goal into a confirmed work target.
2. **Work-system design** — convert the target into Prompt, Context, Harness, Loop, and human-judgment rules.

Expected output: Plain-Language Brief → Work System Card (Prompt / Context / Harness / Loop) → MCP & orchestrator decisions as *outputs* → Daily-Use Protocol → Copyable Starting Prompt → Markdown Record Template → Trial Run → Review Rule.

## Why a work system, not a stronger prompt

| Layer | What you think you're learning | What actually matters |
|---|---|---|
| Prompt | How to ask the AI | How to express intent clearly |
| Context | Giving the AI more information | How to select, organize, and refresh the background |
| Harness | Giving the AI tools | How to design permissions, rules, verification, and guardrails |
| Loop | Letting the AI run on its own | How to design a system that is sustainable, checkable, stoppable, and improvable |

Low-leverage use: ask once, get one answer.
High-leverage use: design a work system where the AI keeps advancing a class of tasks — with a check, feedback, and memory each round — while you still make the value calls.

## Repository structure

```text
system-wright/            # the skill (copy this dir into a host's skills folder)
  SKILL.md                # entry point: name + description + workflow
  openai.yaml             # Codex display metadata (ignored by other hosts)
  references/             # progressive-disclosure detail, one level deep
scripts/
  install.sh              # cross-platform installer
  validate_skill.py       # self-contained, dependency-free validator
  test_validate_skill.py  # validator unit tests
  check_packaging.py      # manifest + landing-page validation
tests/
  check_skill_quality.py  # completeness lint
test-output/              # recorded design walkthroughs + negative-trigger tests
LICENSE
```

## Installation

The skill is a plain `SKILL.md` directory, so installation is "copy `system-wright/` into the host's skills folder." The bundled installer does this portably (no hardcoded home):

```sh
# clone, then pick your host: claude | codex | gemini | cursor
git clone https://github.com/EthanQC/SystemWright && cd SystemWright
sh scripts/install.sh --host claude

# or a custom / project-local skills directory:
sh scripts/install.sh --dir /path/to/skills
sh scripts/install.sh --host claude --project   # installs into ./.claude/skills
```

### As a Claude Code plugin

In Claude Code you can also install it from the bundled plugin marketplace:

```text
/plugin marketplace add EthanQC/SystemWright
/plugin install system-wright@system-wright
```

### Per-host reference

| Host | User-level skills dir | Project-level | Invocation |
|------|----------------------|---------------|------------|
| **Claude Code** | `~/.claude/skills/system-wright` | `.claude/skills/system-wright` | natural language, or `/system-wright` |
| **OpenAI Codex CLI** | `~/.codex/skills/system-wright` | `.agents/skills/` or `.codex/skills/` | `$system-wright` |
| **Gemini CLI** | `~/.gemini/skills/system-wright` | `.gemini/skills/` | natural language / `/skills` |
| **Cursor** | `~/.cursor/skills/system-wright` | `.cursor/skills/` | `/` in Agent chat |

GitHub Copilot, Cline, Windsurf, and OpenCode also read the same `SKILL.md` from their own skills directories. The cross-tool aliases `~/.agents/skills/` and `.agents/skills/` are honored by several hosts.

### Kimi (Moonshot) & GLM (Zhipu)

Kimi and GLM don't have a separate skill system — you run them **inside Claude Code** via an Anthropic-compatible endpoint, so skills load at the harness level from `~/.claude/skills/`. Install with `--host claude`, then point Claude Code at the backend:

```sh
# Kimi (Moonshot)
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"   # .cn for China
export ANTHROPIC_AUTH_TOKEN="<your-moonshot-key>"
export ANTHROPIC_MODEL="kimi-k2.7-code"                          # or the model your plan serves

# GLM (Zhipu)
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"       # note the /api/ segment
export ANTHROPIC_AUTH_TOKEN="<your-z.ai-key>"
export ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.6"                     # or the model your plan serves
```

Model names drift — use whichever current model your plan exposes; only the env-var shape matters.

### Windows

Run the installer under Git Bash or WSL, or copy the folder manually in PowerShell:

```powershell
$dest = "$env:USERPROFILE\.claude\skills\system-wright"
Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue
Copy-Item -Recurse system-wright $dest
```

## Usage

Describe the need naturally (works on every host):

```text
我想优化 xhs-ops-system，但我不知道应该做 prompt、context、harness、loop、MCP、orchestrator 还是 skill。请先帮我拆解想法，再设计一个能试跑的工作系统。
```

Or invoke explicitly where the host supports it (Codex):

```text
$system-wright
我有一个模糊想法，想把它设计成一个可重复使用的 AI 工作系统：[paste your idea]
```

## Validation

All checks are dependency-free (no PyYAML, no network) and run on any clone:

```sh
python3 quick_validate.py                 # structural validation (self-contained)
python3 scripts/test_validate_skill.py    # validator unit tests
python3 tests/check_skill_quality.py      # completeness lint
python3 scripts/check_packaging.py        # manifest + landing-page validation
python3 -m py_compile scripts/*.py tests/check_skill_quality.py quick_validate.py && git diff --check
```

CI (`.github/workflows/ci.yml`) runs these on a clean checkout across Python 3.9 and 3.12 — the "fresh machine" that catches any reintroduced hardcoded path.

## Test Outputs

These are recorded **design walkthroughs** — self-authored, design-consistency runs that show the skill's end-to-end shape. They are not yet replays over real production data (real-data runs will replace them).

- `test-output/actual-test-messy-ai-article-loop.md`: a messy, non-technical input becoming a usable reading/work loop.
- `test-output/actual-test-xhs-ops-system.md`: the XHS ops use case, including MCP/orchestrator boundaries.
- `test-output/actual-test-founder-level-idea.md`: a founder-level vague goal becoming a weekly decision loop.
- `test-output/actual-test-saas-support.md`: a SaaS support workflow reaching a triage/response loop with MCP=yes and maker-checker.
- `test-output/negative-trigger-tests.md`: simple rewrites, pure definitions, temporary checklists, and ordinary code review do **not** trigger this skill.

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for the validator commands to run first and [SECURITY.md](SECURITY.md) to report a concern privately. SystemWright is **unversioned by design**: there is no version field, and releases are pinned by git commit on `main` rather than a version number.

## License

[MIT](LICENSE).

## Research sources

Official / primary standards this skill conforms to:

- Agent Skills standard: https://agentskills.io/specification
- Anthropic Agent Skills best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code Skills: https://code.claude.com/docs/en/skills
- OpenAI Codex Skills: https://developers.openai.com/codex/skills
- Model Context Protocol: https://modelcontextprotocol.io/docs/getting-started/intro
- Kimi (Moonshot) Anthropic-compatible API: https://platform.moonshot.ai
- GLM (Zhipu) coding API: https://docs.z.ai
