# Negative Trigger Tests

These cases verify that the skill does not over-design simple requests.

Shared rule:
do not over-design when the user only asks for a one-off answer, a definition, a temporary checklist, or a normal code review.

## Should Not Trigger: One-Off Rewrite

Input:
帮我把这句话改得更礼貌：明天之前必须给我。

Expected behavior:
Return a rewritten sentence. Do not over-design a workflow, loop, MCP, or orchestrator.

Actual response:
请在明天之前发给我，方便我及时跟进。谢谢。

Pass/fail:
Pass. The response rewrites the sentence directly and does not design a reusable system.

## Should Not Trigger: Pure Definition

Input:
MCP 是什么？

Expected behavior:
Explain MCP directly. Do not over-design unless the user asks how to apply MCP to a workflow.

Actual response:
MCP 是一种让 AI 应用连接外部工具、数据和服务的协议。简单说，它让 AI 不只靠聊天内容回答，也能在被允许的边界内读取资料或调用工具。

Pass/fail:
Pass. The response gives a direct definition and does not design a reusable system.

## Should Not Trigger: Temporary Checklist

Input:
给我一个今天开会前的检查清单。

Expected behavior:
Return a simple checklist. Do not over-design unless the user says the checklist should become a repeated system.

Actual response:
- 明确会议目标
- 确认参会人和议程
- 准备要展示的材料
- 写下 1-3 个必须得到答案的问题
- 会后记录结论、负责人和截止时间

Pass/fail:
Pass. The response gives a temporary checklist and does not design a reusable system.

## Should Not Trigger: Code Review

Input:
Review this PR for bugs.

Expected behavior:
Use a review process or code-review skill. Do not use this skill unless the user asks to productize the review workflow.

Actual response:
我会按代码 review 方式先看 bug、风险、回归和缺失测试，并用文件行号列 findings。请提供 PR diff 或仓库路径。

Pass/fail:
Pass. The response routes to code review and does not design a reusable system.
