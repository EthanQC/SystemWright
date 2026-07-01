# Research Notes

These notes summarize the external references used to design this skill.

## Official and Primary Standards

## OpenAI Codex Skills

Source:
https://developers.openai.com/codex/skills

Relevant takeaways:

- A skill packages instructions, resources, and optional scripts so Codex can follow a task-specific workflow reliably.
- Codex uses progressive disclosure: it first sees the skill name, description, and file path, then opens `SKILL.md` only when the skill is relevant.
- A skill directory contains `SKILL.md` and optional `scripts/`, `references/`, `assets/`, and Codex display metadata in `openai.yaml` at the skill root (as this repo ships it).
- Skills are suitable for reusable workflows and conventions, while plugins are a distribution unit when shipping broader bundles.

Design implication:
This project should be a skill because the product is a reusable decision and design workflow invoked inside an agentic IDE.

## OpenAI API Skills

Source:
https://developers.openai.com/api/docs/guides/tools-skills

Relevant takeaways:

- Skills are versioned bundles with a `SKILL.md` manifest.
- They codify processes, conventions, and reusable task instructions.
- Validation requires a clear skill structure and exactly one `SKILL.md` per skill directory.

Design implication:
The core logic belongs in `SKILL.md`; deeper material belongs in references so the skill stays lightweight.

## Agent Skills Specification

Source:
https://agentskills.io/specification

Relevant takeaways:

- A skill is a directory with `SKILL.md` plus optional resources.
- Progressive disclosure separates metadata, instructions, and resources.
- The main skill file should remain focused and should not become an oversized manual.

Design implication:
This skill uses a concise main workflow and places detailed definitions, question banks, and design notes in `references/`.

## Anthropic Agent Skills Best Practices

Source:
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Relevant takeaways:

- `SKILL.md` should act like an overview that points to detailed materials as needed.
- Skill authors should keep the main file under 500 lines and split detailed material into separate files.
- Effective skills use concrete examples, consistent terminology, clear workflow steps, feedback loops, and real usage evaluations.

Design implication:
This skill should keep the main file concise, keep detailed templates in references, and include at least three real trial outputs.

## Claude Code Skills

Source:
https://docs.anthropic.com/en/docs/claude-code/skills

Relevant takeaways:

- Claude Code skills extend Claude with `SKILL.md` instructions and optional supporting files.
- Claude can use skills when relevant or the user can invoke one directly.
- Skills are useful when the user repeatedly pastes the same instructions, checklist, or multi-step procedure into chat.
- Per Anthropic's docs, Claude Code skills follow the Agent Skills open standard and add host features such as invocation control, subagent execution, and dynamic context injection.

Design implication:
This skill is suitable for any Agent Skills host — Codex, Claude Code, Gemini CLI, Cursor, and Claude-Code-compatible model backends such as Kimi (Moonshot) and GLM (Zhipu) — but reference-loading conditions must stay clear.

## Model Context Protocol

Source:
https://modelcontextprotocol.io/docs/getting-started/intro

Relevant takeaways:

- MCP connects AI applications to external systems, data, tools, and workflows.
- MCP is useful when an AI system needs live access or controlled actions across external services.

Design implication:
MCP is not required for the idea-refinement skill itself. It is a possible output when the designed work system needs live external-system access.

## MCP Tools

Source:
https://modelcontextprotocol.io/specification/2025-06-18/server/tools

Relevant takeaways:

- MCP tools are model-controlled capabilities for external systems such as APIs, databases, computations, or actions.
- Tool invocations can have side effects, so applications should make exposed tools visible and keep a human in the loop for confirmation.

Design implication:
When this skill designs an MCP tool, it must name read/write side effects, approval gates, and fallback behavior.

## MCP Resources

Source:
https://modelcontextprotocol.io/specification/2025-06-18/server/resources

Relevant takeaways:

- MCP resources expose context such as files, schemas, records, or application-specific information.
- Resources are application-driven: the host application decides how to expose or include them.

Design implication:
When the work system only needs reliable context access, the output should recommend a resource rather than an action tool.

## MCP Prompts

Source:
https://modelcontextprotocol.io/specification/2025-06-18/server/prompts

Relevant takeaways:

- MCP prompts expose structured prompt templates and instructions to clients.
- Prompts are user-controlled and are usually explicitly selected by the user.

Design implication:
If the user needs a reusable external workflow template rather than live data or actions, the output should recommend an MCP prompt.

## OpenAI Agents SDK Orchestration

Source:
https://openai.github.io/openai-agents-python/multi_agent/

Relevant takeaways:

- Orchestration is the flow of agents in an app: which agents run, in what order, and how they decide what happens next.
- Orchestration can be LLM-driven, code-driven, or mixed.

Design implication:
Do not call every staged workflow an application orchestrator. Reserve application-level orchestration for systems where app/runtime code owns flow, state, handoffs, tools, approvals, and observability.

## Codex Subagents

Source:
https://developers.openai.com/codex/subagents

Relevant takeaways:

- Codex can spawn specialized agents in parallel and collect their results.
- Subagents are useful for complex tasks that can be split into independent work, such as codebase exploration or multi-step implementation.
- Codex only spawns subagents when the user explicitly asks, and subagent workflows consume more tokens than single-agent runs.

Design implication:
Subagents are not the same as the product skill and should only be recommended when the designed work system has independent slices worth parallelizing.
