# Design Playbook

Use this playbook when the user's idea is broad, vague, emotional, or mixes several possible systems.

## Layer 1: Idea Refinement

The purpose of Layer 1 is to turn "I want to improve something with AI" into a designable work target.

### Diagnostic Sequence

1. Restate the idea in ordinary language.
2. Identify the real job behind the idea.
3. Classify the current request level.
4. Find the recurring work, if any.
5. Identify context and tools already available.
6. Separate what AI can decide from what the human must decide.
7. Confirm the design target.

### Beginner Default Questions

Use this default set (a subset of the at-most-7-questions cap) when the user is non-technical, rushed, or confused:

1. What result do you want to see after one run?
2. How do you do this today?
3. What materials, files, examples, or rules can the AI use?
4. What must the AI never do without asking you first?
5. How will you know the run was useful?

If the answer is still vague, continue with working assumptions instead of blocking the user.

### Request-Level Classifier

One-off answer:
The user wants advice or content now.

Reusable prompt:
The user repeats the same kind of request manually.

Context pack:
The user needs the AI to use stable background information.

Harness:
The user needs the AI to inspect files, run tools, use a browser, call APIs, or verify output.

Loop:
The user needs repeated work with checks, feedback, and memory.

MCP:
The user needs live connection to an external system or service.

Orchestrator:
The user needs multiple roles, stages, approvals, or parallel execution.

Organization routine:
The user needs a team or personal operating rhythm, not just an automation.

### Question Bank

Outcome:

- What result would make this useful within one week?
- What output do you want to see after each run?
- What decision should the system help you make?

Current process:

- How do you do this today?
- Which step is slow, inconsistent, or easy to forget?
- Where does quality drop?

Context:

- Which files, examples, data, rules, or memories should the AI use?
- Which sources are authoritative?
- What should the AI ignore?

Tools and permissions:

- Should the AI only advise, or can it inspect and change files?
- Does it need browser, shell, API, database, or app access?
- What actions need explicit approval?

Review:

- What should be checked before accepting output?
- Who approves risky decisions?
- What counts as a failed run?

Loop:

- How often should this run?
- What feedback should be remembered?
- What should improve each time?

Use at most 7 questions per round. If the user wants direct progress, select the most important assumptions and move on.

## Layer 2: Work-System Design

The purpose of Layer 2 is to convert the confirmed target into a usable AI work system.

### Plain-Language Brief Template

Always produce this before the technical Work System Card:

```text
What this helps with:

What you give it:

What the AI does:

What you still decide:

How to check it worked:

What gets saved for next time:

First task:
```

### Work System Card Template

```text
System name:

Intended user:

Job-to-be-done:

Trigger:

Inputs:

Outputs:

Prompt layer:
- Role:
- Task:
- Constraints:
- Decision rules:
- Output format:

Context layer:
- Required context:
- Source of truth:
- Examples:
- Memory to keep:
- Context to exclude:

Harness layer:
- Runtime:
- Tools:
- Permissions:
- Guardrails:
- Verification:

Loop layer:
- Cycle:
- Review cadence:
- Feedback capture:
- Memory update:
- Next action:
- Forbidden means (what the system must never do to satisfy its own completion check):

Human judgment gates:

MCP decision:

Orchestrator decision:

Skill decision:

Minimal first version:

Expansion path:
```

### MCP Primitive Decision Format

Use this when MCP may be needed. Pick the smallest primitive that matches the job.

```text
MCP needed: yes/no/not yet
Reason:
External system:
MCP primitive: tool/resource/prompt
Control model: model-controlled / application-driven / user-controlled
Auth/data scope:
Read actions:
Write actions:
Read/write side effects:
Approval gate:
Fallback without MCP:
```

Primitive fit:

- tool: the model may call an external action such as API lookup, database query, computation, or write operation.
- resource: the system needs app data, files, schemas, records, or other context selected by the host application.
- prompt: the external system should expose a reusable user-invoked workflow template.

### Orchestrator Type Decision Format

Use this when the work may require coordination beyond a single prompt.

```text
Orchestrator needed: yes/no/not yet
Reason:
Orchestrator type: manual/staged workflow / subagent / application orchestrator
Roles:
Stages:
Quality gates:
Parallel work:
State owner:
Approval points:
Fallback without orchestrator:
```

Type fit:

- manual/staged workflow: one agent follows staged steps, checklists, and review gates without a separate orchestrator runtime.
- subagent: spawned subagents (where the host supports them, e.g. Codex/Claude Code) independently inspect, implement, or review parallel slices.
- application orchestrator: app/runtime code owns agent flow, tools, state, handoffs, approvals, and observability.

### Skill Decision Format

```text
Reusable skill needed: yes/no/not yet
Reason:
Trigger:
Procedure:
References:
Test scenario:
```

## Trial-Run Protocol

Run a tiny version of the designed system.

```text
Test input:

Assumptions:

First output:

Check:

Revision:

Observed capability:

Observed limitation:
```

Good trial runs test whether the system:

- clarifies vague intent
- chooses the right system form
- separates prompt, context, harness, and loop
- avoids unnecessary tooling
- produces a next action the user can actually take

## Common Failure Modes

Over-building:
Designing MCPs, dashboards, or orchestrators before the actual recurring job is known.

Under-building:
Giving a polished prompt when the task really needs context, tool access, checks, and memory.

Hidden context:
Assuming the AI knows the user's business, files, preferences, or project rules.

No loop:
Producing a workflow that has no feedback, review, or memory, so quality does not improve.

Fake automation:
Calling something automated when the human still has to copy, verify, and reconcile everything manually.

No human judgment:
Letting AI decide taste, risk, strategy, or customer-facing actions without approval.
