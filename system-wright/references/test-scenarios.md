# Test Scenarios

Use these scenarios to verify whether the skill works.

## Should Trigger

These inputs should activate the skill because the user is asking for idea refinement or reusable AI work-system design.

### Scenario 1: Personal Knowledge Loop

Input:
"我每天会看很多 AI 文章，但看完就忘，也不知道怎么用到工作里。我想让 AI 帮我把这些文章变成真正能落地的东西。"

Expected behavior:

- The skill should classify this as a loop, not merely a summarization prompt.
- It should ask or assume what counts as useful output.
- It should design context rules for source articles and user's work goals.
- It should avoid MCP unless the user needs live access to reading apps or note apps.
- It should include a trial run with one article or one pasted excerpt.

### Scenario 2: XHS Ops System

Input:
"我想优化 xhs-ops-system，让它能帮助我做小红书内容生产、审核、风控和复盘。"

Expected behavior:

- The skill should first identify the real recurring tasks.
- It should separate content strategy, production, review, risk control, and retrospective loops.
- It should design different Prompt, Context, Harness, and Loop layers.
- MCP should be recommended only if the system needs live access to XHS data, Feishu, databases, analytics, or publishing tools.
- Orchestrator should be recommended only if there are multiple roles or staged approvals.

### Scenario 3: Founder-Level Idea Clarification

Input:
"我想做一个 AI 帮我管理公司的系统，但不知道怎么设计。"

Expected behavior:

- The skill should not jump to building a platform.
- It should identify decision level, operating cadence, available context, and human approval gates.
- It should propose a minimal first loop, such as weekly decision review or daily ops triage.
- It should escalate to the organization routine level only if the user's problem is team-level coordination.

## Should Not Trigger

These inputs should not activate the full workflow, or should produce a short fallback instead of a full system. They are negative examples for avoiding over-design.

### Negative 1: One-Off Rewrite

Input:
"帮我把这句话改得更礼貌：明天之前必须给我。"

Expected behavior:
Do not over-design. Return the rewritten sentence and optionally a tiny style note.

### Negative 2: Pure Definition

Input:
"MCP 是什么？"

Expected behavior:
Explain MCP directly. Do not create a work system unless the user asks how to apply it to their workflow.

### Negative 3: Temporary Checklist

Input:
"给我一个今天开会前的检查清单。"

Expected behavior:
Return a checklist. Only propose a loop if the user says this meeting prep recurs and needs feedback or memory.

### Negative 4: Code Review Request

Input:
"Review this PR for bugs."

Expected behavior:
Use a code-review skill or direct review process, not this AI work-system design skill, unless the user asks to productize the review workflow.

## Pass Criteria

The output passes if it contains:

- Idea Diagnostic
- Confirmation assumptions or questions
- Plain-Language Brief for a non-technical user
- Work System Card
- Separate Prompt, Context, Harness, and Loop layers
- Human judgment gates
- MCP decision
- MCP primitive and approval/side-effect details when MCP may be needed
- Orchestrator decision
- Orchestrator type when coordination may be needed
- Trial-run record
- copyable starting prompt
- Daily-Use Protocol
- Markdown Record Template
- Observed capability and limitation

The output fails if it:

- hides behind technical labels before explaining the workflow in plain language
- forces MCP or orchestrator when the first version can run manually
- passes a keyword-only test while leaving no concrete next action
- lacks negative examples for should-not-trigger cases
