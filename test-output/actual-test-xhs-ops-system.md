# Actual Test: xhs-ops-system Work System Design

## Test Input

用户想法：我想优化 xhs-ops-system，让它帮助我做小红书内容生产、审核、风控和复盘，但我不确定应该做 prompt、context、harness、loop、MCP 还是 orchestrator。

## Idea Diagnostic

Raw idea:
用户想让 xhs-ops-system 变成内容运营工作系统，而不是只生成小红书文案。

Real job:
把内容生产、审核、风控、发布前判断、复盘沉淀串成可重复流程。

Decision level:
Loop + Harness。是否需要 MCP/Orchestrator 取决于是否要读写真实数据、多人分工或审批。

Missing decisions:
真实数据源、是否自动发布、是否多人审核、是否连接飞书或数据库还未确认。

## Confirmation

- Outcome: 每条选题从 idea 到发布前检查再到复盘都有固定路径。
- Main user: 小红书内容/运营负责人。
- Recurring task: 选题、草稿、审核、风险检查、复盘。
- Available context: 品牌定位、账号历史数据、违规案例、爆文样例、产品目标。
- Tools allowed: 第一版在 agentic IDE 中生成和检查；不自动发布。
- Human approval points: 选题方向、最终文案、风险接受、发布。
- What I will not automate yet: 不自动登录小红书、不自动发布、不自动私信用户。

## Plain-Language Brief

What this helps with:
让每条小红书内容都经过同一套“生产、检查、批准、复盘”流程。

What the user gives it:
选题、目标人群、参考爆文、品牌边界、禁用表达、历史表现。

What the AI does:
生成草稿，检查风险，提出修改，输出发布前确认清单，复盘结果。

What the human still decides:
是否采用选题、是否发布、是否接受风险、是否把经验沉淀为规则。

How to check whether it worked:
每次输出都必须有草稿、风险点、修改理由、发布前 checklist 和复盘字段。

What gets saved for next time:
有效标题结构、踩坑表达、审核规则、内容表现反馈。

First task:
用一个选题跑完整的手动 v1，不接任何外部系统。

## Work System Card

System name:
xhs-ops-system Content Loop

Intended user:
小红书内容运营者或账号负责人。

Job-to-be-done:
稳定地产出、审核、发布前判断和复盘小红书内容。

Trigger:
有新选题、要改草稿、要做发布前检查、要复盘内容表现时。

Inputs:
选题、账号定位、目标用户、参考内容、禁用表达、历史反馈。

Outputs:
内容草稿、审核意见、风险等级、发布前 checklist、复盘记录、规则更新。

Prompt layer:
角色是小红书内容运营编辑 + 审核员；任务是生成和审查内容；约束是不得编造数据、不得绕过平台规则；格式是选题判断、草稿、风险、修改、发布前确认。

Context layer:
需要账号定位、内容样例、品牌边界、平台风险规则、历史表现；真实数据优先于泛化建议；未验证的爆款公式不得沉淀为规则。

Harness layer:
运行在 Codex/Claude Code 或项目仓库内；可读取本地 specs、样例和历史记录；发布动作必须人工完成；验证包括禁用词检查、事实检查、品牌一致性和发布前 checklist。

Loop layer:
每条内容经历 idea -> draft -> review -> revise -> approve -> publish manually -> retrospective -> memory update。每周复盘一次有效规则和误判规则。

Verification ladder（先便宜后贵）：确定性（禁用词命中、事实字段齐全、发布前 checklist 完整）> 规则（品牌一致性、平台风险词）> 多模型/人（审美与风险接受）。
Permission tier（逐动作）：读 specs/样例/历史 = read-only；生成草稿 = draft；发布/私信/写回数据 = real-world，必须人工审批，v1 不做。
Loop types：agent（生成）+ verification（审核回退）；稳定后可加 event-driven（新选题触发）。maker ≠ checker：生成与审核分离。
Observability（每次运行记录）：运行时刻、输入选题、动作、失败步、重试次数、成本、最终证据（草稿与 checklist）。

Human judgment gates:
选题是否值得做、文案是否符合账号气质、风险是否可接受、是否发布、哪些经验进入长期规范。

MCP decision:
MCP needed: not yet for v1; yes later if real Feishu/database/analytics access is required.
MCP primitive: resource for reading content specs/history; tool for writing review records or tasks; prompt for reusable content review workflow.
control model: resource is application-driven; prompt is user-controlled; write tool is model-controlled and must require approval.
auth/data scope: selected xhs-ops-system project records, Feishu tables, analytics exports, and approved content examples only.
read/write side effects: read side can expose private ops data; write side can create review rows, tasks, or memory updates.
approval gate: human approval before any external write, publish, DM, or platform-facing action.
Fallback without MCP: user pastes relevant context and manually stores the Markdown record.

Orchestrator decision:
Orchestrator needed: not yet for one-person v1; likely yes for team workflow.
Orchestrator type: v1 is a manual/staged workflow, not an orchestrator runtime; subagent for parallel content/review/risk checks later; application orchestrator only if the product manages states, approvals, queues, and observability.
Roles: creator, reviewer, risk checker, owner.
Stages: brief -> draft -> review -> revise -> approve -> retrospective.
Quality gates: risk checklist, brand fit, factual claims, publishing approval.

Skill decision:
Reusable skill needed: yes if the same content workflow runs weekly.

Minimal first version:
One manual loop with Markdown records and no external writes.

Expansion path:
After 10 content runs, decide whether to connect Feishu/database as MCP resources and whether review should use subagents.

## Daily-Use Protocol

1. Paste one XHS topic and target user.
2. Paste brand/context/risk rules.
3. Generate draft and review in one run.
4. Human approves or revises.
5. Save only verified performance or review lessons.

## Copyable Starting Prompt

```text
Run the xhs-ops-system Content Loop once.

Raw input:
[topic, target user, draft or rough notes]

Current goal:
[what this post should achieve]

Available context:
[account positioning, examples, risk rules, history]

Hard boundaries:
Do not publish. Do not invent data. Do not write to external systems without approval.

Return: Plain-Language Brief, Work System Card delta if needed, draft/review output, approval points, memory update, Review Rule result.
```

## Markdown Record Template

```markdown
# XHS Content Loop Run
Date:
Topic:
Target user:
Goal:

## Draft

## Review
Risk:
Brand fit:
Fact check:

## Human Approval
Publish / revise / discard:
Reason:

## Retrospective
Performance:
Save as rule:
Do not save:
```

## First task

Run one manual content loop for the topic: “为什么不是先接 MCP，而是先跑一个 AI 工作 Loop”.

## Review Rule

Pass only if the output includes a draft, risk review, human approval gate, and memory update candidate without automatic publishing.

## Trial Run

Trial mode: design-consistency（自演设计自洽验证，非真实数据实测）。真实实测应回放 10 条历史内容，测审核一致率、零编造事实、零漏风险。

Actual run output:

Draft:
标题候选：别急着接 MCP，先把一个 AI 工作 Loop 跑通。

开头：很多人一想到 AI 工作系统，就先问要不要接 MCP、要不要做自动化、要不要弄多 agent。但对小红书 ops 来说，第一步不是接工具，而是证明一条内容能不能稳定走完“选题 -> 草稿 -> 审核 -> 修改 -> 人工发布 -> 复盘”的循环。

正文要点：
1. Prompt 只解决“这次怎么写”，不能保证下次更好。
2. Context 解决“AI 知不知道账号定位、爆文样例、禁用表达”。
3. Harness 解决“AI 能看哪些文件、能做哪些检查、不能做哪些动作”。
4. Loop 解决“每次发布后怎么把反馈沉淀成下一次的规则”。
5. MCP 是后面的事：当手动循环跑出稳定记录，再考虑接飞书、数据库或分析数据。

结尾：先手动跑 10 条内容，记录每次误判和有效规则，再决定要不要接 MCP。

Risk review:
- 风险等级：低。
- 平台风险：没有引导违规自动化，没有承诺自动发布。
- 品牌风险：表达偏方法论，适合教育型内容；如果账号更偏实操，需要加一个真实案例。
- 事实风险：没有引用具体数据，不能写“效率提升 10 倍”。

Approval gate:
- 人需要确认：是否用“MCP”这个词，是否改成“小白更懂的工具连接”，是否加入真实 xhs-ops-system 例子。
- Blocked actions：不自动发布，不写入外部任务系统，不更新内容库。

Memory update candidate:
- Candidate rule：小红书 ops 的第一版 AI 系统先跑手动内容 loop，等 10 条记录证明上下文和审核规则稳定后，再设计 MCP。
- Save status：candidate only，等实际跑完 10 条内容后再变成长期规则。

Check:
The workflow keeps MCP and orchestrator as designed outputs, not default dependencies.

Revision:
Add a weekly retrospective step after 10 posts to decide whether MCP resources are justified.

Observed capability:
The skill converts a broad xhs-ops-system optimization idea into a staged manual loop with clear future MCP and subagent conditions.

Observed limitation:
Without inspecting the real xhs-ops-system repo and real data sources, the design remains a workflow spec rather than implementation-ready integration.
