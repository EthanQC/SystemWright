# Runtime Failure Modes

These are the eight ways a designed work system fails *while it runs* — as opposed to the design-time
mistakes in `design-playbook.md` (over-building, hidden context, no loop, fake automation). Read this
when designing the Loop and Harness layers: for each mode, name the top symptoms the system will show
and put the fix into the design so the loop improves the real goal instead of degrading silently.

Every loop amplifies whatever it runs on — good process and good checks, but also weak verifiers, bad
permissions, and vague goals. So design against these before automating anything.

## 1. Goal failure

Symptoms: goal too big to know what to do first; too abstract to verify; multiple goals conflict; no
written success standard; the stop condition is ignored.

Fix: split into small single-goal loops; write the completion evidence explicitly; make one main goal
per loop.

## 2. Context failure

Symptoms: too little context so the model guesses; too much so it is distracted; stale facts;
instructions conflict with data; prior history pollutes the current task; retrieval returns
surface-relevant but useless material.

Fix: read the index before the body; tier context into must-read / optional / never; clear old memory
on a schedule; keep facts, assumptions, and plans written separately.

## 3. Tool failure

Symptoms: unclear tool descriptions; overlapping tools; noisy returns; errors the agent can't act on;
over-broad permissions; a tool that changed external state while the loop assumed it only read.

Fix: one tool, one job; structured returns; actionable errors; an approval gate before any real write.

## 4. Verification failure

Symptoms: the maker grades its own work; the standard is subjective; only format is checked, not facts;
only the final result is checked, not the key steps; an LLM judge is fooled by fluent prose; tests miss
the real user path.

Fix: use the verification ladder (deterministic > rule > multi-model > human, cheapest sufficient
first); split maker from checker; keep a sample set for critical cases; keep a human as the final judge
on risk.

## 5. Loop-control failure

Symptoms: infinite retries; each failure changes direction so it gets messier; no budget ceiling; no
condition that escalates to a human; the same problem is reprocessed every day; automated output piles
into a new inbox.

Fix: set a max round count and a cost/time budget; write failure reasons into state; escalate to a
human on the third same-class failure; produce nothing when there is no new input.

## 6. Memory failure

Symptoms: a wrong conclusion is saved; a temporary preference is stored as a permanent rule; too much
memory pollutes judgment; the reason a decision was made is not recorded; state drifts out of sync with
the real world.

Fix: give each memory a source, a time, and a scope; only persist rules that recur; re-check memory on a
schedule; keep facts, preferences, decisions, and unverified assumptions separate.

## 7. Human-collaboration failure

Symptoms: the human stops reading the output; the human can't understand what the loop did; the loop
hides all uncertainty; the human hands over responsibility; the system omits risks to look finished.

Fix: every output carries evidence and open questions; high-risk actions require approval; sample-review
on a schedule; treat "uncertain" as a first-class output. Watch two human risks named by the framework:
comprehension debt (the system runs so fast the person no longer understands the current result) and
cognitive surrender (the person hands over judgment and only presses start).

## 8. Economic failure

Symptoms: too many subagents so token cost explodes; event triggers fire too often; every run re-reads
large material; a strong model is used for simple classification; complex verification runs for tiny
gains.

Fix: small model for classification, strong model for judgment; cache stable context; prove value
manually before automating; add a verification loop only on high-value steps.
