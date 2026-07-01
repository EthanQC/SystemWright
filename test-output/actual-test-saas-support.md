# Actual Test: saas-support Triage Work System Design

This run records the "yes, build it" path: a case where the honest answer is MCP = yes with live
connectors, not "not yet." It exists so the repo has a positive MCP example, and so the routing that
reaches MCP=yes with full primitive / control-model / side-effect / approval / fallback detail has a
regression anchor.

## Test Input

I run a small SaaS. Every day I manually triage support tickets that live in our Postgres DB and
Intercom: decide bug vs question vs billing, draft replies, and escalate anything urgent. I want to stop
doing this by hand and set up an AI system for it. I'm technical, have API access, and don't want just a
prompt — design the actual work system.

## Idea Diagnostic

Raw idea:
Turn daily manual support-ticket triage into an AI work system that reads real tickets, classifies them,
drafts replies, and flags the urgent ones — instead of the owner doing it by hand every morning.

Real job:
Keep a reliable daily triage loop over live tickets: classify (bug / question / billing), draft a reply,
and surface the few that need a human now — without the owner reading every ticket.

Decision level:
Loop + Harness + MCP. The task recurs, needs verification and memory (loop), needs to act inside a
bounded environment over live data (harness), and needs live read/write access to Postgres and Intercom
(MCP). Orchestrator is not yet needed for a one-person v1.

Missing decisions:
Whether v1 may auto-send any reply (default: no), the daily ticket volume, the "urgent" definition, and
whether classification labels already exist in the tools or must be created.

User role: owner/operator of the SaaS.
Success signal: the owner reads only the escalations and a short triage summary, and trusts the labels.
Failure risk: a wrong auto-send to a customer, a missed urgent ticket, or a fabricated fact in a draft.
Working assumptions: v1 is draft-only (no auto-send), a few dozen tickets/day, "urgent" = billing
failure / churn risk / explicit anger or deadline. Labelled as assumptions, not confirmed.

## Confirmation

- Outcome: every new ticket is classified and gets a drafted reply; urgent ones are flagged for the owner.
- Main user: the SaaS owner/operator.
- Recurring task: daily triage — classify, draft, escalate.
- Available context: Postgres tickets table, Intercom conversations, past resolved tickets, product docs.
- Tools allowed: read Postgres and Intercom; write only Intercom draft notes (never send) in v1.
- Human approval points: any reply sent to a customer, any escalation action, any label written back.
- What I will not automate yet: sending replies, closing tickets, refunds, or any customer-facing write.

Load-bearing assumption surfaced as a question (not silently defaulted): **may v1 draft replies as
private internal notes only, with zero customer-facing sends until you've reviewed a week of drafts?**
The whole safety design depends on this being "yes."

## Plain-Language Brief

What this helps with:
Doing your morning ticket triage for you — reading every new ticket, sorting it, drafting a reply, and
telling you only the ones you need to handle personally.

What the user gives it:
Read access to your ticket database and Intercom, a few example replies you like, and your rule for what
counts as urgent.

What the AI does:
Reads new tickets, labels each (bug / question / billing), drafts a reply as an internal note, checks the
draft against facts and rules, and posts a short list of the urgent ones for you.

What the human still decides:
Whether to send each reply, how to handle escalations, and whether a label rule should change.

How to check whether it worked:
Each run leaves labelled tickets, internal-note drafts, an escalation list, and a log — and never sends
anything to a customer on its own.

What gets saved for next time:
Approved reply patterns, corrected labels, the urgent-definition rule, and misclassification cases.

First task:
Run one manual pass over yesterday's tickets with read-only access and drafts as notes; send nothing.

## Work System Card

System name:
saas-support Triage Loop

Intended user:
The SaaS owner/operator (technical, has API access).

Job-to-be-done:
Classify, draft, and escalate live support tickets daily without the owner reading every ticket.

Trigger:
Scheduled (each morning) plus on-demand; later, event-driven on new-ticket webhooks.

Inputs:
New/updated tickets (Postgres), Intercom conversations, approved example replies, product docs,
urgent-definition rule.

Outputs:
A label per ticket, a drafted reply stored as an internal note, an escalation list, and a run log. No
customer-facing sends in v1.

Prompt layer:
Role is a support-triage agent plus a separate checker. Task is classify → draft → check → escalate.
Constraints: never invent facts, never send to a customer, never promise refunds/timelines without a
human. Output format: per-ticket label + confidence, draft note, risk flags, and an escalation reason.
Decision rules: unknown/low-confidence → escalate; anything money/legal/churn → escalate.

Context layer:
Required context: ticket schema, recent resolved tickets, approved reply examples, product docs, the
urgent rule. Source of truth: the live tools (Postgres/Intercom), not the model's memory. Examples: 5-10
good replies and 3 bad ones. Memory to keep: approved patterns and corrected labels. Context to exclude:
unrelated internal chatter and stale docs.

Harness layer:
Runtime: the owner's environment / an agent CLI with connectors. Tools: Postgres (read), Intercom (read
+ draft note). Permissions: read-only on Postgres; read + internal-note-write on Intercom; no send/close.

Permission tier (every action is placed on a tier; real-world writes need approval):
- read-only: query Postgres tickets, read Intercom conversations.
- draft: write a reply as a private internal note in Intercom.
- external-tool / real-world (NOT in v1, human-approved only): send reply, close ticket, refund, label
  write-back.

Verification ladder (cheapest sufficient check first; completion means checkable evidence, not the
agent's say-so):
- deterministic: ticket ID exists, draft references a real order/account number, no promise of a refund
  amount, escalation list is non-empty only when true.
- rule: banned-phrase check (no "guaranteed", no invented SLA), billing keywords force the billing label.
- multi-model / LLM check: a separate checker agent scores the draft against a rubric (maker-checker:
  the drafting agent is never the one that approves its own draft).
- human: the owner approves any send and any escalation action.

Guardrails: no send in v1; every draft is a note; the checker is a distinct agent.

Observability (every run logs): run time, which tickets were read, label + confidence per ticket, which
drafts were written, which checks failed, retries, token cost, and the final evidence (note IDs).

Loop layer:
Cycle: read new tickets → classify → draft note → check (deterministic → rule → checker) → escalate →
log → memory update. Loop types in use: an agent loop (act/observe) wrapped by a verification loop
(check/redo), moving toward an event-driven loop once trusted; a monthly hill-climbing loop reviews
misclassifications to update rules.
Review cadence: daily escalation review; weekly rule review.
Feedback capture: owner corrections on labels and drafts.
Memory update: approved patterns, corrected labels, urgent-rule changes.
Next action: after 10 supervised days, decide whether to allow draft-with-one-click-send.
Stop condition: no new tickets → no output; max 2 retries per ticket then escalate.
Escalation: third same-class failure, any low-confidence label, or any money/legal ticket → human.
Budget / limits: cap tokens per run; small model for classification, strong model only for drafts.
Forbidden means: never mark a ticket "handled" by closing it or sending a canned reply just to clear the
queue; the completion check is a correct label plus a human-reviewable draft, not an empty inbox.

Human judgment gates:
Whether to send each reply, how to act on escalations, refund/legal decisions, and label-rule changes.

MCP decision:
MCP needed: yes.
Reason: the system needs reliable live read of Postgres and Intercom and a controlled draft-write to
Intercom; manual copy-paste would be too slow and error-prone at daily volume.
External system: Postgres (tickets) and Intercom (conversations).
MCP primitive: resource for reading ticket/conversation data and schema; tool for the Intercom
draft-note write; prompt for a reusable triage-review template.
control model: the read resources are application-driven; the draft-note write tool is model-controlled
and must require approval; the review prompt is user-controlled.
auth/data scope: a read-only Postgres role limited to the tickets/customers tables; an Intercom token
scoped to read + write-note only (no send, no close), for the support inbox only.
read actions: query tickets, read conversations and customer records.
write actions: create an internal draft note on a conversation.
read/write side effects: reads can expose customer PII (must stay in-scope); the write creates a visible
internal note but sends nothing to the customer.
approval gate: required before any send/close/refund and before any label write-back — non-optional for
every write primitive.
Fallback without MCP: the owner pastes a batch of tickets and stores the Markdown record by hand.

Orchestrator decision:
Orchestrator needed: not yet for a one-person v1.
Orchestrator type: v1 is a manual/staged workflow (classify → draft → check → escalate) with review
gates, not a separate orchestrator runtime. Subagents (a maker draft agent and a separate checker agent)
handle the maker-checker split. An application orchestrator is only justified later if this becomes a
multi-agent, stateful, approval-queued service.
Roles: classifier, drafter, checker, owner.
Stages: read → classify → draft → check → escalate → log.
Quality gates: verification ladder passes, escalation reasons present, no customer-facing send.
Fallback without orchestrator: run the stages sequentially in one agent with explicit checkpoints.

Skill decision:
Reusable skill needed: yes if this daily triage runs as a standing routine; package it once the label
rules and reply patterns stabilize.

Minimal first version:
Read-only Postgres + Intercom, drafts as internal notes, a separate checker, full run log, zero sends.

Expansion path:
After 10 supervised days with low correction rate, allow draft-with-approval send; later add new-ticket
webhooks for an event-driven loop and a monthly hill-climbing rule review.

## Daily-Use Protocol

1. Trigger the run each morning (or on demand).
2. It reads new tickets and writes labelled drafts as internal notes.
3. Review the escalation list and the drafts.
4. Approve, edit, or send manually; never let v1 send.
5. Save corrected labels and approved patterns; note any rule change.

## Copyable Starting Prompt

```text
Run the saas-support Triage Loop once (read-only + draft notes; never send).

Raw input:
[batch of new tickets, or the connector query for today]

Current goal:
[what a good triage pass looks like today]

Available context:
[ticket schema, approved reply examples, product docs, the urgent rule]

Hard boundaries:
Do not send to customers. Do not invent facts, SLAs, or refunds. Any write beyond an internal draft note
needs my approval. Escalate anything money/legal/low-confidence.

Return: Plain-Language Brief delta if any, per-ticket label + confidence, draft notes, failed checks,
escalation list with reasons, run log, memory-update candidates, and the Review Rule result.
```

## Markdown Record Template

```markdown
# saas-support Triage Run
Date:
Tickets read:

## Labels
Ticket | label | confidence | escalate?

## Drafts (internal notes only)

## Failed checks

## Escalations (reason)

## Run log
Run time / actions / retries / cost / evidence (note IDs)

## Human decision
Sent / edited / escalated:

## Memory update
Save:
Do not save:
```

## First task

Run one supervised pass over yesterday's tickets with read-only access and drafts as internal notes; send
nothing; review the labels and drafts, and record the correction rate.

## Review Rule

Pass only if the run produced a label + confidence per ticket, an internal-note draft, an escalation list
with reasons, and a run log — with zero customer-facing sends and no invented facts.

## Trial Run

This trial has two labelled modes, kept distinct so a design-consistency check is never mis-stated as a
real-data test.

### Mode A — Design-consistency trial (self-authored, synthetic input)

Test input:
Three synthetic tickets: (1) "the export button 500s every time" ; (2) "how do I change my plan?" ;
(3) "you charged me twice this month, refund now or I'm leaving."

Assumptions:
Read-only access; drafts are internal notes; "urgent" = billing failure / churn / anger.

First output:
- Ticket 1 → label: bug (0.9). Draft note: acknowledge, ask for account ID + steps, no fix promised.
- Ticket 2 → label: question (0.85). Draft note: point to the plan-change doc.
- Ticket 3 → label: billing (0.95), ESCALATE (money + churn). Draft note: apologize, confirm we're
  checking; no refund amount or promise.

Verification (maker-checker + ladder):
- deterministic: no refund amount appears in any draft; escalation list = {ticket 3}. Pass.
- rule: banned-phrase check flags a first draft of ticket 3 that said "we'll refund you today" → checker
  rejected it and required the no-promise version. Caught.
- checker agent: confirmed ticket 3 must escalate and must not commit to an outcome.

Revision:
Add an explicit rule: any ticket mentioning a charge/refund is billing + escalate, and drafts may never
state a refund decision.

Observed capability:
On synthetic input the design routes correctly, keeps every action on a permission tier, and the
maker-checker split blocks a dangerous over-promise before it reaches a human.

Observed limitation:
This is a design-consistency demonstration, not proof over real data. It cannot show real-world
classification accuracy, real PII handling, or real cost.

### Mode B — Real 实测 protocol (to run before trusting it)

Replay the last 20 real resolved tickets through the read-only + draft path and measure: per-class label
agreement vs the human's original resolution; zero fabricated facts in any draft; zero missed urgent
tickets; and the token cost per run. Only after this passes on real tickets should draft-with-approval
send be considered. Until Mode B runs, the system is "designed and self-consistent," not "verified."

## Check

The workflow keeps MCP as a designed output with a full primitive/control-model/side-effect/approval/
fallback specification, keeps every write behind an approval gate, splits maker from checker, and refuses
customer-facing sends in v1 — reaching "yes, build it" without becoming fake automation.
