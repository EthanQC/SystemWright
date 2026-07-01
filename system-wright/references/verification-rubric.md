# Verification Rubric and Checker Gate

Run this gate after producing the Work System Card and Trial Run, before the Final Handoff. It is the
maker-checker split made structural: the design must be reviewed by something other than the agent that
wrote it. The gate exists because real use shows the weakest point is not depth but discipline — a design
that is never actually produced, or a workflow skipped under a messy multi-goal session, cannot be caught
by richer templates alone.

## How to run the gate (by host)

- Host supports subagents (Codex, Claude Code): spawn ONE independent checker subagent. Give it the
  produced Work System Card plus Trial Run and the rubric below. It returns SHIPPABLE, or FIX with the
  specific items to redo. The checker must not be the agent that wrote the design.
- Host does not support subagents (some Gemini CLI or Cursor modes): run the same rubric as an explicit
  self-check checklist — score each item out loud before handoff. This is weaker than an independent
  checker, but the review step still happens. Never skip the gate; only downgrade its mechanism.

## The rubric (score each hit / partial / miss with one line of evidence)

1. Routing: the decision level is correct and unneeded sections were dropped for a one-off. If the user
   invoked the skill by name, Layer 1 (Idea Diagnostic, routing decision, Confirmation Gate) was actually
   run before task work.
2. A Work System Card exists with Prompt, Context, Harness, and Loop as visibly separate layers — not a
   stylistic nod while the model just did the task and produced only an artifact.
3. Verification is ordered as a ladder (deterministic > rule > multi-model > human) with at least one
   named deterministic check; completion is defined as checkable evidence, not the agent's say-so.
4. Every action sits on a permission tier; the minimal first version performs no external real-world
   write; any write primitive keeps its approval gate.
5. Stop condition, retry cap, and cost/budget are set; the maker is not the only checker.
6. Observability fields are listed (run time, inputs, actions, failed step, retries, cost, evidence).
7. Loop type(s) are named, and the top 2-3 runtime failure modes (by name, from `failure-modes.md`) each
   have a mitigation.
8. The single most load-bearing assumption is surfaced, not silently defaulted.
9. The Trial Run is labelled by mode (real 实测 / partial / design-consistency dry-run) and promises no
   capability the minimal first version cannot deliver.

A miss on item 1, 2, or 4 blocks the handoff — those are routing, existence, and safety, not polish.

## Checker subagent prompt template

```text
You are an independent checker. You did NOT write the design below. Score it against the 9-item rubric
(hit / partial / miss + one line of evidence each). Then return exactly one verdict:
- SHIPPABLE — items 1, 2, and 4 all hit, and no more than two partials elsewhere.
- FIX: <items, most important first> — anything else.
Design under review:
[paste the Work System Card + Trial Run]
```

## Self-check fallback (hosts without subagents)

Before handoff, walk the same 9 items yourself and write the verdict. If items 1, 2, or 4 are not clean,
do not hand off — go back and produce the missing routing, the missing Work System Card layers, or remove
the unsafe v1 write first.
