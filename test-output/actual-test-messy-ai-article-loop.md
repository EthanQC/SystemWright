# Actual Test: Messy AI Article to Action Loop

## Test Input

用户想法：我每天会看很多 AI 文章，但看完就忘，也不知道怎么用到工作里。我想让 AI 帮我把这些文章变成真正能落地的东西。

messy excerpt：

> Agent workflows are the future. Teams that use them will be 10x faster. You should connect every tool, let AI read your notes, write content, make decisions, and update your backlog. The real value is not a better prompt but a persistent loop. Most companies are already behind. Start by automating everything.

Current goal:
把这类 AI 文章转成能服务“小红书素材、工作系统设计、产品化 Skill”的行动。

## Idea Diagnostic

Raw idea:
用户不是要摘要，而是要把杂乱文章转成行动、规则和是否继续投入的判断。

Real job:
建立“读文章 -> 判断关联 -> 生成行动 -> 执行/放弃 -> 沉淀规则”的循环。

Decision level:
Loop。第一版不需要 MCP，因为用户可以手动粘贴文章；也不需要 orchestrator，因为当前是个人处理。

Missing decisions:
用户还没说明优先服务内容素材、产品策略还是个人知识库。这里按“工作行动 + 小红书素材候选”继续。

## Confirmation

- Outcome: 每篇文章至少产出一个可执行动作或明确放弃理由。
- Main user: 高频阅读 AI 内容但缺少转化系统的人。
- Recurring task: 每次读到 AI 文章后运行一次。
- Available context: 文章片段、当前项目、用户目标。
- Tools allowed: 对话分析和文件记录。
- Human approval points: 是否执行动作、是否公开发布、是否沉淀为规则。
- What I will not automate yet: 不自动抓取文章、不自动写入笔记软件、不自动发布内容。

## Plain-Language Brief

What this helps with:
把“看过的文章”变成“今天能做什么、以后记住什么、哪些观点不要信”。

What the user gives it:
文章原文/片段、当前目标、已有项目或内容方向。

What the AI does:
挑出与用户目标有关的内容，过滤夸张说法，给出一个小行动和一条候选规则。

What the human still decides:
是否相信这篇文章、是否执行行动、是否把规则保存。

How to check whether it worked:
输出必须包含一个 30 分钟内能做的动作，且说明为什么和当前目标有关。

What gets saved for next time:
只保存执行过或明确验证过的规则。

First task:
用这篇 messy excerpt 产出一个行动和一条候选规则。

## Work System Card

System name:
AI Article to Action Loop

Intended user:
想把 AI 信息流转成工作行动的人。

Job-to-be-done:
过滤 hype，把文章转成行动、判断和可沉淀规则。

Trigger:
读完一篇 AI 文章、收藏一个观点、看到一个工具宣传时。

Inputs:
文章正文、当前目标、项目列表、已有尝试。

Outputs:
一句话结论、关联度、可执行动作、风险、候选规则、下次复盘问题。

Prompt layer:
角色是信息转行动助手；任务是把文章和用户目标连接；约束是不输出泛泛启发；格式固定为结论、关联、动作、风险、规则、复盘。

Context layer:
必需上下文是文章片段和当前目标；用户项目目标优先于文章观点；排除未经验证的宣传承诺。

Harness layer:
运行在 Codex/Claude Code 对话中；允许读取用户粘贴内容和本地记录文件；不允许自动发布或写入外部系统；验证标准是是否有明确动作和复盘点。

Loop layer:
每篇文章处理一次；每 5 篇复盘主题；反馈标记为执行、放弃、待查证；经过真实执行的规则才进入长期记忆。

Human judgment gates:
是否相信观点、是否执行动作、是否公开发布、是否保存为规则。

MCP decision:
MCP needed: not yet.
MCP primitive: none for v1; future resource if connecting Readwise/Notion/Feishu article stores; future tool if writing back tags or tasks.
control model: manual now; future resource is application-driven; future write tool is model-controlled with approval.
auth/data scope: none now; future scope limited to selected reading records and target project notes.
read/write side effects: none now; future write could create tags, notes, or tasks.
approval gate: required before any external write.
Fallback without MCP: user pastes article and manually saves the Markdown record.

Orchestrator decision:
Orchestrator needed: no for v1.
Orchestrator type: manual/staged workflow.
Reason: one user, one repeated processing cycle.
Future: subagent only if doing parallel source-checking and content adaptation; application orchestrator only if a product owns ingestion, review, memory, and publishing.

Skill decision:
Reusable skill needed: yes if this is weekly recurring.

Minimal first version:
Copyable Starting Prompt + Markdown Record Template + five-article review rule.

Expansion path:
After 20 real runs, decide whether to connect reading app MCP or content backlog.

## Daily-Use Protocol

1. Paste the article or messy excerpt.
2. Paste the current goal.
3. Ask for one run of the loop.
4. Approve, revise, or discard the action.
5. Save only verified rules.

## Copyable Starting Prompt

```text
Run my AI Article to Action Loop once.

Raw input:
[paste article or messy excerpt]

Current goal:
[paste current project/content/work goal]

Hard boundaries:
Do not invent facts. Do not recommend external automation unless needed. Do not save a rule unless it is verified or clearly marked as candidate.

Return: Plain-Language Brief, Work System Card delta if needed, first output, human approvals, memory update, Review Rule result.
```

## Markdown Record Template

```markdown
# AI Article to Action Run
Date:
Article/source:
Current goal:

## Output
Conclusion:
Action:
Risk:
Candidate rule:

## Human Decision
Execute / revise / discard:
Reason:

## Memory Update
Save:
Do not save:
```

## First task

Turn the provided messy excerpt into one action:
Draft one XHS post outline explaining why “automate everything” is the wrong first move; use “start with one loop before connecting tools” as the practical point.

## Review Rule

Pass only if the output has a concrete action, rejects or qualifies hype, names what the human approves, and says what to save.

## Trial Run

First output:
The messy excerpt is useful for one rule: do not start with connecting every tool; start by proving one feedback loop works. Concrete action: write a 7-card XHS outline on “为什么不是先接 MCP，而是先跑一个 Loop”. Candidate rule: tool access comes after repeated manual runs prove the context and review rules.

Check:
It connects to the user's content goal and avoids blindly accepting “automate everything”.

Revision:
Add a “candidate, not verified” label until the user tests this with one real article.

Observed capability:
The skill turned a promotional messy input into a small action, a risk filter, and a reusable candidate rule.

Observed limitation:
Without the user's real project list and prior attempts, it cannot know which action should outrank other work.
