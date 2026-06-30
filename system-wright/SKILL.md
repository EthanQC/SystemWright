---
name: system-wright
description: Turns a vague goal, messy repeated workflow, AI adoption problem, or product/operations idea into a reusable AI work system built from Prompt, Context, Harness, and Loop, with a plain-language brief, human-approval gates, and a small trial run. Use when the user wants to productize a recurring way of working with an agent (Codex, Claude Code, Gemini CLI, Cursor, or compatible) rather than get a single answer. Do not use for one-off rewrites, pure definitions, temporary checklists, or ordinary code review unless productizing a reusable workflow.
license: MIT
metadata:
  author: EthanQC
  version: 1.0.0
---

# SystemWright

## Core Rule

This skill itself is the product layer for idea refinement and AI work-system design.

Do not treat MCP, orchestrators, tools, dashboards, or new agents as prerequisites for this skill. They are possible outputs that may be designed after the user's goal is understood and confirmed.

Always separate two layers:

1. Layer 1: refine the user's vague idea into a confirmed work target.
2. Layer 2: design the best-fit work system using Prompt, Context, Harness, Loop, and human judgment.

If the user is non-technical, explain every design choice in ordinary work language before naming the technical pattern.

## Required Workflow

### 0. Route the Request

Use this skill when the user asks for:

- turning a vague idea into an AI workflow or AI operating system
- improving a recurring business process with AI
- deciding whether something should become a prompt, skill, MCP, automation, loop, or orchestrator
- applying Prompt, Context, Harness, and Loop to a real project
- building a reusable way to work with an agent CLI or agentic IDE (Codex, Claude Code, Gemini CLI, Cursor, or compatible)

If the user only needs a one-off answer, do not over-design. Offer a one-off prompt or checklist instead.

### 1. Layer 1: Idea Refinement

Produce an "Idea Diagnostic" before designing any system.

Core fields (always include):

- Raw idea: repeat the user's idea in plain language.
- Real job: what work the user is actually trying to get done.
- Decision level: one-off answer, reusable prompt, context pack, harness, loop, MCP, orchestrator, or organization routine.
- Missing decisions: only ask questions that change the system design.

Additional fields (include when known; otherwise infer briefly or defer — never block the user on them):

- User role: owner, operator, creator, analyst, manager, or learner.
- Success signal: what would make the user say "this works".
- Failure risk: what would make the system useless, unsafe, or misleading.
- Working assumptions: when missing information is not blocking, state assumptions and continue.

Question rules:

- Ask at most 7 questions in one round.
- Group questions by outcome, data, tools, constraints, and review.
- If the user asks for speed or testing, proceed with explicit assumptions.
- Never make "idea clarity" a barrier to using AI. The skill should create clarity.

Use `references/design-playbook.md` when the idea is broad, emotional, or underspecified.

### 2. Confirmation Gate

Before Layer 2, give the user a compact confirmation block:

```text
I will design for:
- Outcome:
- Main user:
- Recurring task:
- Available context:
- Tools allowed:
- Human approval points:
- What I will not automate yet:
```

If the user is present and the missing information changes risk, ask for confirmation.
If the user asked for direct output or is unavailable, continue with assumptions and label them.

### 3. Plain-Language Brief

Before technical terms, produce a "Plain-Language Brief" that a non-technical user can act on.

Required fields:

- What this helps with
- What the user gives it
- What the AI does
- What the human still decides
- How to check whether it worked
- What gets saved for next time
- First task to run

After this brief, map the same design to Prompt, Context, Harness, Loop, and human judgment.

Use `references/daily-use-protocol.md` when the user needs a copyable starting prompt, record template, or operating protocol.

### 4. Layer 2: Work-System Design

Produce a "Work System Card" with these sections:

- System name
- Intended user
- Job-to-be-done
- Trigger: when to use it
- Inputs: what the user provides
- Outputs: what the system returns or changes
- Prompt layer: role, task, constraints, output format, decision rules
- Context layer: required facts, files, examples, memories, source-of-truth rules
- Harness layer: tools, permissions, environment, guardrails, verification commands
- Loop layer: repeat cycle, review cadence, feedback capture, memory, next-round improvement, and forbidden means (what the system must never do to satisfy the completion check, so it improves the real goal instead of gaming the metric)
- Human judgment gates: what the human must decide
- MCP decision: needed or not, MCP primitive, control model, auth/data scope, read/write side effects, approval gate, fallback without MCP
- Orchestrator decision: needed or not, orchestrator type, roles, stages, quality gates, fallback without orchestrator
- Skill decision: whether the final workflow itself should become a reusable skill
- Minimal first version
- Expansion path

Use `references/four-layer-framework.md` for definitions and fit rules.

### 5. Design-Output Decision Rules

Choose the smallest durable form that can do the job:

- Prompt: the task is one-off or low-risk, and no persistent facts/tools are needed.
- Context pack: the task depends on stable background, examples, brand rules, schemas, or project memory.
- Harness: the task needs files, code, browser actions, APIs, command execution, validation, or tool permissions.
- Loop: the task repeats and improves through feedback, checks, memory, and next actions.
- MCP: the designed system needs live access to an external app, database, API, file service, or tool surface.
- Orchestrator: the designed system needs multiple roles, parallel agents, staged reviews, approvals, or quality gates.
- Skill: the designed workflow should be reusable by a human through an agent CLI or agentic IDE.

MCP and orchestrator are design artifacts, not default infrastructure.

### 6. Trial Run

After designing the system, run one small real example whenever possible.

Record:

- Test input
- Assumptions
- First output
- Verification or critique
- Revision
- Observed capability
- Observed limitation

The trial run must test whether the system clarifies the goal and produces a usable next action, not merely whether the text sounds good.

### 7. Final Handoff

End with a practical handoff:

- The final work-system card
- A copyable daily-use protocol or starting prompt
- Required context files or examples
- Tools/MCPs to request only if needed
- First task to run next
- Review rule for improving the loop after real use

If the workflow will be reused, include:

- Daily-Use Protocol
- Copyable Starting Prompt
- Markdown Record Template
- First task
- Review Rule

Do not end with abstract theory. The user should know exactly what to do next.

## Quality Bar

The output is acceptable only if:

- It preserves the distinction between the product skill and the designed work system.
- It does not force MCP or orchestrator into the architecture unless the task needs them.
- It makes Prompt, Context, Harness, and Loop visible as separate layers.
- It asks for confirmation before risky automation or external actions.
- It includes a trial-run path or performs a small trial run.
- A non-technical user can understand the system in ordinary work terms.

## References

- `references/four-layer-framework.md`: definitions and decision rules for Prompt, Context, Harness, Loop, MCP, Orchestrator, and Skill.
- `references/design-playbook.md`: detailed diagnostic questions, templates, and trial-run protocol.
- `references/daily-use-protocol.md`: read when producing copyable prompts, plain-language handoffs, daily protocols, or record templates.
- `references/research-notes.md`: audit/background only; read when reviewing the skill against the Agent Skills standard and other external specifications.
