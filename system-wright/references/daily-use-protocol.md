# Daily-Use Protocol

Use this reference when the user needs a copyable way to run the designed work system after the design session ends.

## Plain-Language Output

Before technical labels, give the user the plain-language brief shape — the seven fields defined once in
`design-playbook.md` (Plain-Language Brief Template): what this helps with, what you give it, what the AI
does, what you still decide, how to check it worked, what gets saved for next time, and the first task.

## Daily-Use Protocol

```text
1. Paste the raw input.
2. Paste the current goal or project this should connect to.
3. Ask the AI to run the system once.
4. Check the output against the review rule.
5. Decide: execute, revise, defer, or discard.
6. Save only the parts that were verified or useful.
7. Start the next run with the saved rule, example, or correction.
```

## Copyable Starting Prompt

```text
I want to run my AI work system once.

Raw input:
[paste the task, article, notes, project issue, or messy idea]

Current goal:
[what I am trying to improve or decide]

Available context:
[files, examples, rules, project notes, prior attempts, constraints]

Hard boundaries:
[what AI must not do without asking]

Please return:
1. Plain-Language Brief
2. Work System Card
3. First output for this run
4. What I need to approve
5. What should be saved for next time
6. Review Rule result: pass / revise / discard
```

## Markdown Record Template

```markdown
# Work System Run

Date:
System:
Raw input:
Current goal:
Context used:

## Plain-Language Brief

## Output

## Human Decision
- [ ] Execute
- [ ] Revise
- [ ] Defer
- [ ] Discard

Reason:

## Review Rule
Did the output produce a concrete next action, respect boundaries, and identify what to save?

Result: pass / revise / discard

## Memory Update
Save:

Do not save:

Next run should change:
```

## Review Rule

The run passes only if:

- the user can take one concrete next action
- the output uses the provided context rather than generic advice
- risky actions still require human approval
- the system says what to save and what not to save
- the next run has a clear improvement point

If any item fails, revise the workflow before treating the output as reusable.
