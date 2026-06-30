# Actual Test: Founder-Level Vague Idea

## Test Input

用户想法：Founder 说“我想做一个 AI 帮我管理公司的系统，但不知道怎么设计。”

## Idea Diagnostic

Raw idea:
用户想用 AI 改善公司管理，但目标过大，不能直接设计平台。

Real job:
先找到一个高频、高价值、低风险的管理循环，例如每日运营检查或每周决策复盘。

Decision level:
Organization routine -> Loop。第一版应是管理节奏，不是 MCP、平台或 application orchestrator。

Missing decisions:
公司规模、核心业务、管理痛点、数据来源、权限边界、谁做最终决策。

## Confirmation

- Outcome: 先做一个每周决策复盘 loop。
- Main user: founder 或高级管理者。
- Recurring task: 每周收集团队事实、风险、决策、下周行动。
- Available context: 周报、会议纪要、指标、客户反馈。
- Tools allowed: 第一版人工粘贴资料，AI 生成复盘草案。
- Human approval points: 优先级、责任人、对外承诺、资源调整。
- What I will not automate yet: 不自动读取所有公司系统、不自动下达任务、不自动评价员工。

## Plain-Language Brief

What this helps with:
把“公司很多事很乱”变成每周一次的事实、风险、决策和行动清单。

What the user gives it:
本周事实、关键指标、客户/团队反馈、正在卡住的事情。

What the AI does:
整理事实，找出风险，提出需要 founder 判断的决策，生成下周行动。

What the human still decides:
什么最重要、谁负责、哪些承诺可以对外说、哪些问题暂时不做。

How to check whether it worked:
输出必须让 founder 更快做出 1 到 3 个明确决策。

What gets saved for next time:
决策理由、误判、反复出现的风险和有效的管理规则。

First task:
用一周的事实做一次手动复盘，不接公司系统。

## Work System Card

System name:
Founder Weekly Decision Loop

Intended user:
Founder 或管理负责人。

Job-to-be-done:
每周把杂乱信息变成少量关键决策和下周行动。

Trigger:
每周固定复盘、重大项目卡住、团队信息失真时。

Inputs:
周报、指标、客户反馈、会议纪要、风险、上周承诺。

Outputs:
事实摘要、风险列表、待决策问题、建议行动、责任人候选、下周检查点。

Prompt layer:
角色是 founder 参谋；任务是整理事实和提出决策问题；约束是不代替 founder 做价值判断；格式为事实、风险、决策、行动、记忆。

Context layer:
需要公司目标、当前优先级、指标、团队事实、历史决策；事实优先于情绪；禁止把未经确认的传闻当事实。

Harness layer:
第一版在对话中运行；人工粘贴材料；不自动连接公司系统；验证包括事实来源、决策是否具体、责任是否可确认。

Loop layer:
每周输入事实 -> AI 整理 -> founder 决策 -> 下周检查执行 -> 记录误判和规则。每月复盘管理规则是否有效。

Human judgment gates:
优先级、资源分配、人员评价、对外承诺、是否升级为系统集成。

MCP decision:
MCP needed: no for v1; maybe later.
MCP primitive: future resource for metrics/docs; future tool only for creating approved tasks; future prompt for weekly review template.
control model: manual now; future resource is application-driven; future task creation tool is model-controlled with approval; prompt is user-controlled.
auth/data scope: limited to selected weekly facts, metrics, and meeting notes; no full-company blanket access.
read/write side effects: read side may expose sensitive company data; write side may create tasks or decisions that affect teams.
approval gate: founder approval before any write, assignment, or external message.
Fallback without MCP: paste weekly facts into the template.

Orchestrator decision:
Orchestrator needed: not for v1; yes if team roles and approvals scale.
Orchestrator type: manual/staged workflow in the first version; subagent for independent department summaries; application orchestrator only when app code manages state, approvals, assignments, and audit logs.
Roles: founder, ops collector, department reviewer, decision recorder.
Stages: collect -> summarize -> challenge -> decide -> assign -> check next week.
Quality gates: fact/source check, owner confirmation, approval before assignment.

Skill decision:
Reusable skill needed: yes if this becomes weekly operating rhythm.

Minimal first version:
Manual weekly review prompt and record template.

Expansion path:
After 4 weekly runs, decide whether metrics/docs need MCP resources and whether subagents should summarize independent departments.

## Daily-Use Protocol

1. Collect weekly facts.
2. Paste them with current priorities.
3. AI returns facts, risks, decisions, actions.
4. Founder approves decisions.
5. Save decision rationale and next-week checks.

## Copyable Starting Prompt

```text
Run the Founder Weekly Decision Loop once.

Raw input:
[weekly facts, metrics, meeting notes, customer/team feedback]

Current goal:
[company priority this week]

Hard boundaries:
Do not assign people, change priorities, or send messages without founder approval.

Return: Plain-Language Brief, Work System Card delta if needed, decision brief, human approvals, memory update, Review Rule result.
```

## Markdown Record Template

```markdown
# Founder Weekly Decision Loop
Week:
Current priority:
Facts used:

## Facts

## Risks

## Decisions Needed

## Founder Decision

## Actions

## Review Rule
Did this produce 1-3 concrete decisions and next-week checks?

## Memory Update
Save:
Do not save:
```

## First task

Run one weekly review using only manually pasted facts from the current week.

## Review Rule

Pass only if the output separates facts from opinions, gives 1-3 decisions, names approval gates, and defines next-week checks.

## Trial Run

Weekly facts:
- 本周销售线索 28 个，比上周多 6 个，但只有 3 个进入报价。
- 客户 A 两天没回复，客户 B 要求本周五前确认交付时间。
- 产品会决定先做审核流优化，但没有明确负责人。
- 客服反馈同一个问题重复出现 5 次：用户不知道下一步该提交什么材料。
- Founder 本周时间被临时沟通切碎，周报还没写。

Actual run output:

Facts:
- 线索数量上升，但报价转化低，问题可能在资格筛选或跟进节奏。
- 客户 B 有明确截止时间，是本周外部承诺风险。
- 审核流优化已经被口头决定，但缺 owner，容易变成悬空事项。
- 客服重复问题说明 onboarding 或材料说明可能有缺口。

Risks:
- 如果周五前不确认客户 B 的交付时间，会形成信任风险。
- 如果审核流没有 owner，下周复盘时很难判断进度。
- 如果继续让 founder 处理所有临时沟通，管理 loop 本身会失效。

Decision 1:
今天先指定审核流优化 owner，并要求 owner 在周四前给出一个最小改动方案。

Decision 2:
明天 12:00 前给客户 B 一个明确交付时间或备选方案，不让它拖到周五。

Action:
- 10 分钟内发出两条确认消息：一条给审核流 owner，一条给客户 B 负责人。
- 周报先写 5 条事实，不追求完整叙述。

Human approval gates:
- Founder 确认 owner。
- Founder 确认客户 B 对外承诺。
- Founder 决定客服重复问题是否进入下周优先级。

Next-week check:
- 审核流 owner 是否交付最小方案。
- 客户 B 是否收到明确交付时间。
- 客服重复问题是否从 5 次下降。

Memory update candidate:
- Candidate rule：founder weekly loop 每周最多推出 1-3 个决策，超过 3 个就不是决策复盘，而是任务堆叠。
- Save status：candidate only，等下周检查结果后再保存。

Check:
The design avoids over-building and keeps sensitive company actions behind human approval.

Revision:
Add explicit “do not evaluate employees automatically” boundary.

Observed capability:
The skill narrows an organization-scale idea into a first loop that can run manually in one week.

Observed limitation:
It cannot design real integrations until company data sources, permissions, and management cadence are known.
