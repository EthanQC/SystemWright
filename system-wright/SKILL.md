---
name: system-wright
description: Turns a vague goal, messy repeated workflow, AI adoption problem, or product/operations idea into a reusable AI work system built from Prompt, Context, Harness, and Loop, with a plain-language brief, human-approval gates, and a small trial run. Use when the user wants to productize a recurring way of working with an agent (Codex, Claude Code, Gemini CLI, Cursor, or compatible) rather than get a single answer. Do not use for one-off rewrites, pure definitions, temporary checklists, or ordinary code review unless productizing a reusable workflow.
license: MIT
metadata:
  author: EthanQC
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

If the user only needs a one-off answer, do not over-design. Deliver the concrete thing they asked for first (the summary, the speech, the checklist), then offer in one optional line to systematize it later. Do not produce a Work System Card, MCP decision, or Trial Run for a one-off request.

Named-invocation override: if the user invokes this skill by name (for example `$system-wright` or `/system-wright`), always run Layer 1 first — the Idea Diagnostic, an explicit routing decision (reusable system vs one-off artifact), and the Confirmation Gate — before doing task work, even inside a larger or messy multi-goal session, and even if the routing conclusion is "one-off." An explicit invocation is itself a request to systematize; the one-off off-ramp above must never swallow it, and this override takes priority over the output-weight rule in step 4.

Light path for a clearly-trivial one-off: when a named invocation routes to "one-off" and the deliverable is a single short artifact with no reusable method worth capturing (a toast, a one-line note, a single email), replace the full ceremony with a three-line routing acknowledgement — name the real job, state "routing: one-off, no reusable system here," and ask the single most load-bearing question only if one truly exists — then deliver the artifact and offer in one optional line to build the full system later. Skip the four-layer Work System Card and the Trial Run; with no Work System Card there is nothing for the verification gate to review. Layer 1 still ran and the routing stays visible. Keep the full track whenever a reusable method exists — a repeatable collect-analyze-present pipeline is a system, a wedding toast is not.

Artifact-and-system, not either-or: when the user wants a concrete deliverable (a page, a document, a dataset) and invokes this skill, produce both — a Work System Card for the reusable method (slim if the work is mostly one-off), then the artifact. Naming the skill signals they want the repeatable system, not only the output.

Decision rule tying these three: a reusable method present → a full or slim Work System Card (the artifact-and-system path); no reusable method → the light path, which is the only case that omits the Work System Card and folds the Idea Diagnostic and Confirmation Gate into the three-line acknowledgement. Layer 1 routing stays visible either way.

### 1. Layer 1: Idea Refinement

Produce an "Idea Diagnostic" before designing any system.

Core fields (always include):

- Raw idea: repeat the user's idea in plain language.
- Real job: what work the user is actually trying to get done.
- Decision level: one-off answer, reusable prompt, context pack, harness, loop, MCP, orchestrator, or organization routine.
- Missing decisions: only ask questions that change the system design.
- Load-bearing assumption: name the single assumption the whole design depends on, and carry that same assumption into the Confirmation Gate as the one explicit question.

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

Scope boundary: if the goal is mainly about emotions, mental or physical health, or personal relationships rather than a work output, name that plainly. Do not pretend a loop can fix a feeling. At most, after the user confirms, offer one narrow, optional slice of the work surface around it.

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

Even when proceeding on assumptions, surface the single most load-bearing assumption — the one the whole design depends on — as an explicit question. Never silently default it.

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
- Harness layer: tools, permissions, environment, guardrails, verification commands (use the verification ladder — cheapest sufficient check first, deterministic before human; completion means checkable evidence, not the agent's say-so; put every action on a permission tier and keep real-world writes behind approval — see `references/four-layer-framework.md`)
- Loop layer: repeat cycle, review cadence, feedback capture, memory, next-round improvement, and forbidden means (what the system must never do to satisfy the completion check, so it improves the real goal instead of gaming the metric); name which of the four loop types apply and set stop condition, escalation, budget, and observability (see `references/four-layer-framework.md` and `references/failure-modes.md`)
- Top runtime failure modes: the 2-3 most likely for this system, named from `references/failure-modes.md`, each with a mitigation
- Human judgment gates: what the human must decide (self-check: does this design make the user surrender judgment they should keep — comprehension debt or cognitive surrender?)
- MCP decision: needed or not, MCP primitive, control model, auth/data scope, read/write side effects, approval gate, fallback without MCP
- Orchestrator decision: needed or not, orchestrator type, roles, stages, quality gates, fallback without orchestrator
- Skill decision: whether the final workflow itself should become a reusable skill
- Minimal first version
- Expansion path

Match the output weight to the Decision level. For a `reusable prompt` or `context pack`, drop the MCP, Orchestrator, and Trial-Run sections and just return the prompt or context template — reserve the full Work System Card for harness, loop, MCP, or orchestrator-level work.

Never let the minimal first version perform an external real-world write — send, publish, pay, delete, or modify production. Auto-send and auto-publish must start as draft-for-approval and only escalate after trust is established. Any MCP write primitive keeps its approval gate; it is not optional.

Use `references/four-layer-framework.md` for definitions and fit rules, and `references/failure-modes.md` for the runtime failure modes to design against.

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

- Trial mode: real 实测 / partial / design-consistency dry-run
- Test input
- Assumptions
- First output
- Verification or critique
- Revision
- Observed capability
- Observed limitation

The trial run must test whether the system clarifies the goal and produces a usable next action, not merely whether the text sounds good.

### 7. Verification Gate and Final Handoff

Before handing off, review the design with something other than the agent that wrote it (maker-checker):

- On a host that supports subagents (Codex, Claude Code), spawn one independent checker subagent to score the Work System Card and Trial Run against the rubric in `references/verification-rubric.md`; it returns shippable or a fix list.
- On a host without subagents, run the same rubric as an explicit self-check checklist before handoff.

Never skip the gate; only downgrade its mechanism by host. A miss on routing, a missing Work System Card with visible Prompt / Context / Harness / Loop layers, or a v1 external real-world write blocks the handoff — fix it before continuing. On a light-path one-off there is no Work System Card or Trial Run to review, so the gate is satisfied by the visible routing acknowledgement plus the delivered artifact — nothing to block on there. If the skill was invoked by name, confirm Layer 1 was actually run rather than skipped.

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
- It puts each action on a permission tier and never lets the minimal first version do an external real-world write without approval.
- It names concrete verification as a ladder (cheapest sufficient check first), not a vague sentence.
- It surfaces the single most load-bearing assumption instead of silently defaulting it.
- If the goal is emotional, health-related, or relational rather than a work output, it says so instead of forcing a productivity loop.
- If the skill was invoked by name, it ran Layer 1 (routing made visible) before task work, and produced a Work System Card alongside any requested artifact — unless routing found a clearly-trivial one-off with no reusable method, where the light path applies.
- It passed the verification gate — an independent checker subagent, or the self-check fallback — before handoff; on a light-path one-off, the routing acknowledgement plus the delivered artifact are the handoff and there is nothing for the gate to review.
- It includes a trial-run path or performs a small trial run.
- A non-technical user can understand the system in ordinary work terms.

## References

- `references/four-layer-framework.md`: definitions and decision rules for Prompt, Context, Harness, Loop, MCP, Orchestrator, and Skill, plus the verification ladder, permission tiers, the four loop types, observability, and maker-checker.
- `references/failure-modes.md`: the eight runtime failure modes (goal, context, tool, verification, loop-control, memory, human-collaboration, economic) and their fixes; read when designing the Loop and Harness layers.
- `references/verification-rubric.md`: the maker-checker verification gate — the review rubric, the checker-subagent prompt, and the self-check fallback for hosts without subagents; use before the Final Handoff.
- `references/design-playbook.md`: detailed diagnostic questions, templates, and trial-run protocol.
- `references/test-scenarios.md`: should-trigger and should-not-trigger examples and pass criteria; consult when routing a borderline request or checking for over-design.
- `references/daily-use-protocol.md`: read when producing copyable prompts, plain-language handoffs, daily protocols, or record templates.
- `references/research-notes.md`: audit/background only; read when reviewing the skill against the Agent Skills standard and other external specifications.
