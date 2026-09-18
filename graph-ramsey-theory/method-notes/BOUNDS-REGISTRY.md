# Making "use your own strongest result" a step that runs instead of a rule you remember

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-18.
Status: method note. Implementation: `bounds.py`, `BOUNDS.json` in
`../r55-upper-bound-neighbourhood-edges/`.

principal-1, pass 44:

> *"recording that your first version ignored your own \(\le 22\) theorem — the
> exact failure you diagnosed in another lane two passes earlier — is worth
> more than the caps table, because it establishes that the rule does not
> self-apply and needs to be a step in a procedure rather than a principle in a
> note. Work out what that step looks like concretely."*

This is that step.

## 1. The failure, stated mechanically rather than morally

At pass 53 I wrote, about researcher-1's lane:

> *a lane's own tools are the easiest prior art to miss, because they are filed
> under the case they were first used on.*

At pass 59 I opened the order-8 row and used the arithmetic value \(26\) at
orbit size \(4\), ignoring the \(22\) this lane had proved **one pass
earlier**. I had written the rule, published it, had it praised, and then broke
it at the first opportunity.

The useful reading is not that I was careless. It is that the rule **has no
point of application**. It says "remember something" at a moment — opening a new
row — that feels like starting fresh. Stated as a principle it can only fire if
you happen to think of it, and the situation where it matters is exactly the
situation where you are thinking about something else.

Mechanically, the defect is a **broken link**: a bound is proved in artifact A,
and code written later for row B hard-codes whatever value was current when B
was written. Nothing connects A to B. When A improves, B keeps the old number
and sizes its row too loosely — silently, because a loose bound produces a
larger case list, and a larger case list looks like more work rather than like
an error.

## 2. The step

Three parts, none of which require anyone to remember anything.

**A registry.** `BOUNDS.json` holds every bound this lane has proved, each with
its scope — orbit size, the group induced on the orbit, the graph order it is
proved at — plus its source artifact and what it supersedes.

**Consumers read it.** Code calls `bounds.cap(orbit_size, group, n)` instead of
writing a literal. `cap` returns the **minimum** over all applicable entries, so
adding a better bound tightens every consumer at once rather than only the
artifact that proved it.

**A check that fails.** `python3 bounds.py` compares each consumer's *effective*
cap — obtained by calling it, not by reading its source — against the registry,
and **exits non-zero** if any consumer is weaker. It is a check, not a report
someone has to read correctly. Same design as `ledger_audit.py`: the failure
mode is an exit code.

## 3. The check is tested against the defect that actually shipped

A check that cannot fail proves nothing, so `bounds.py --mutate` reinstates the
exact pass-59 defect — `cap_of` returning the raw orbit-lemma value with the
registry lookup removed — and requires the check to catch it:

| | check passes |
|---|---|
| unmutated | **yes** |
| with the pass-59 defect reinstated | **no** — caught |
| after restoring | **yes** |

Note what is *not* tested: deleting a registry entry and observing that the
lookup changes. That would be a test of `cap`, not of the check, and it would
pass whether or not the check works.

## 4. What this does not fix

**It is scoped to one lane and one kind of quantity.** The registry holds
fixed-point bounds for orbits in \((5,5)\)-graphs. Nothing here generalises
itself to, say, edge bounds or a different problem — a second registry would be
a second piece of work.

**The consumer list is written by hand.** `consumers()` names which files use
which bound at which scope. A new file that hard-codes a literal and is never
added to that list is invisible to the check. That is a real hole, and the
honest description of what has been achieved is: **the bounds this lane has
already connected cannot drift apart again**, not "drift is now impossible". A
stronger version would scrape the source for integer literals near the relevant
call sites and flag any that match a registry value — worth doing if this
happens a third time.

**It does not stop the general failure**, which is broader than bounds: any
result filed under the row it was proved for can fail to reach a new row. What
the registry shows is the *shape* of a fix — make the later consumer read from a
single place, and make the mismatch an exit code — and that shape should
transfer to the next quantity that has the same problem.

## 5. The transferable part

> **When you catch yourself failing to apply your own result, do not write the
> rule down again. Find the link that was missing and make something read it.**

The test of whether a rule has been turned into a step is simple: *can it fire
when nobody is thinking about it?* A note cannot. An exit code can.
