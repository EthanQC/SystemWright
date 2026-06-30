# Four-Layer Framework

This reference defines the design vocabulary used by the SystemWright skill.

## Plain-Language Definitions

Prompt:
What you ask the AI to do. A prompt is the instruction layer. It should describe the role, task, constraints, decision rules, and output format.

Context:
What the AI needs to know. Context includes files, examples, data, memory, project rules, user preferences, schemas, brand rules, prior decisions, and source-of-truth boundaries.

Harness:
Where and how the AI is allowed to act. Harness includes the agentic IDE, CLI, browser, filesystem, APIs, permissions, safety rails, verification commands, tests, and rollback strategy.

Loop:
How the work improves over time. Loop includes repeated execution, checks, feedback, review, memory, metrics, and next-round updates.

Human judgment:
What the human must decide because it involves taste, risk, priority, ethics, brand, tradeoffs, or business intent.

## The Key Distinction

Skill:
A reusable procedure that teaches an agent how to run a workflow.

MCP:
A connector to external systems, data, tools, or APIs. It is useful only when the designed work system needs live access or tool execution outside the agent's default environment.

MCP primitive:
The specific kind of capability an MCP server exposes. Use tool/resource/prompt as the decision vocabulary:

- tool: model-controlled action for APIs, databases, computations, or write operations.
- resource: application-driven context such as files, schemas, records, or app-specific data.
- prompt: user-controlled reusable workflow template exposed by a server.

MCP control model:
Who controls invocation:

- model-controlled: the model can discover and call a tool, so approval gates and side-effect checks matter.
- application-driven: the host application selects or inserts resources.
- user-controlled: the user explicitly invokes a prompt/template.

Orchestrator:
A coordination pattern for multiple roles, agents, stages, approvals, or quality gates.

Orchestrator type:

- manual/staged workflow / subagent / application orchestrator
- manual/staged workflow: one agent follows staged steps and review gates without a separate orchestrator runtime.
- subagent: spawned subagents (where the host supports them, e.g. Codex/Claude Code) handle independent work slices.
- application orchestrator: app code or an agent runtime owns state, handoffs, tool execution, approvals, and observability.

Loop:
A work system that keeps turning inputs, actions, checks, feedback, and memory into better future outputs.

The current skill is not an MCP and not an orchestrator. It can design MCPs, orchestrators, prompts, context packs, harnesses, loops, and other skills as outputs.

## Fit Rules

Use a prompt when:

- the task is simple, one-off, and low-risk
- the user can manually provide all needed context
- no verification, persistent memory, or tool execution is needed

Use a context pack when:

- the task recurs and depends on stable facts
- examples, style, project rules, or schemas matter
- wrong background information would cause failure

Use a harness when:

- files, code, browser actions, API calls, shell commands, or inspections are needed
- permissions and verification matter
- the AI must act inside a bounded environment

Use a loop when:

- the task repeats
- quality improves through review and feedback
- memory, metrics, or retrospectives should affect the next run
- the user wants a durable way of working, not a single answer

Use MCP when:

- the designed system needs live app data or actions
- manual copy-paste would be too slow or error-prone
- the external system has an API or tool surface worth formalizing
- the task needs reliable read/write access to a service
- the design can name the MCP primitive, control model, auth/data scope, read/write side effects, approval gate, and fallback

Use an orchestrator when:

- multiple specialist roles are required
- stages must be sequenced and reviewed
- parallel work needs coordination
- approvals and quality gates are part of the work
- the design can choose between a staged workflow, subagent workflow, or application-level orchestrator

Use a skill when:

- the user wants to repeat the same AI-assisted workflow
- the workflow contains reusable judgment, process, and output standards
- the workflow should be invoked from an agentic IDE

## Four-Layer Design Checklist

Prompt layer:

- What is the AI's role?
- What is the task?
- What should it not do?
- What format should it return?
- What decisions can it make alone?
- What decisions require human approval?

Context layer:

- What source material is required?
- Which source is authoritative?
- What examples define good and bad output?
- What memory should carry across runs?
- What context should be excluded?

Harness layer:

- Where does the system run?
- What tools are allowed?
- What permissions are needed?
- What verification is required?
- What can be changed, and what must stay read-only?
- How can mistakes be detected or reversed?

Loop layer:

- What triggers a run?
- What is the repeated cycle?
- What gets checked each time?
- How does the user give feedback?
- What gets written back into memory or templates?
- What must the loop never do to hit its target (forbidden means)?
- When does the loop stop, escalate, or redesign itself?
