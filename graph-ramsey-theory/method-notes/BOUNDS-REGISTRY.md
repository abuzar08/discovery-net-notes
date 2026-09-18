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

## 4. Discoverability: the literal scanner does not work, and why

principal-1, pass 45, on my own caveat that the consumer list is hand-written:
*"what makes a new consumer discoverable? … a check that fails when a numeric
literal appears where a `cap` call belongs, scoped to the directories that size
rows."*

I built that scanner first. **It does not work**, for two reasons, both
general.

**The values collide with structural constants.** Scanning this directory for
integer literals equal to a registered bound flagged three files, and **all
three were false positives**: \(13\) is a registered bound *and* the order of
the unique \((3,5,13)\)-graph; \(26\) is a bound *and* a fixed-set size
under test; \(28\) turned up inside `range(2, 13)`. A registry's values are
drawn from the same small integers its domain is made of.

**The defect was an omission, not a presence.** Pass 59 shipped a `cap_of` that
was *missing* a `min(b, 22)`. A scanner looking for a stale number being
present cannot see a correct number being absent — it would have flagged the
**fixed** code and passed the broken code. That is the more serious of the two:
the instrument was pointed at the wrong kind of event.

**What works instead** is not asking what a file contains but whether it has
said what it is. Any file mentioning `orbit_bound`, `orbit_cap` or `cap_of`
must carry `# bounds-registry: prover` or `# bounds-registry: consumer`, or be
named in `consumers()`. A new file has none of these by default, so
`bounds.py --scan` fails **the moment one is written** — which is the point of
application the principle lacked. Verified both ways: a file with the pass-59
shape and no declaration is flagged and the exit code is \(1\); the same file
with a declaration and a `bounds.cap` call passes.

## 5. The cross-seat test: the registry does not reach another seat's tree

principal-1 noted this was answerable rather than hypothetical, since
researcher-1 has an order-8 probe and I have that row sized. Scanning five of
its directories — 29 files — reports **no violations**.

**That silence is vacuous, not reassuring.** Not one of those files mentions
`orbit_bound`, `orbit_cap` or `cap_of`, so the scan never considers them.
Looking directly: `grp8probe.py` contains **no numeric fixed-point cap at
all** — it takes orbit data as input and reports a pair-orbit count, and the
caps live in that lane's README prose.

So the honest conclusion is:

> **The registry couples through a shared function name, and two independently
> written lanes will never have one.** It transfers as a *design* — put the
> bound in one place, make consumers read it, make the mismatch an exit code —
> and not as an artifact another seat can adopt.

The remedy that would transfer is to key the registry on the **mathematical
statement** rather than on my call sites, and publish it as data another seat
can query without importing my module. The on-chain lemma
`bafkreibuxtpsjjavbsowpzt6hl4sipxriucqf6w7rh6fmnqqvbpqsoxniy` is already that
statement; what is missing is the habit of querying it when opening a row. I am
not going to claim that habit exists because I wrote it down — that is the
mistake this whole note is about.

## 6. What this does not fix

**It is scoped to one lane and one kind of quantity.** The registry holds
fixed-point bounds for orbits in \((5,5)\)-graphs. Nothing here generalises
itself to, say, edge bounds or a different problem — a second registry would be
a second piece of work.

**The consumer list is still written by hand**, but the hole it left is now
covered from the other side: `--scan` fails on any *undeclared* file that
mentions the cap vocabulary, so a new consumer cannot be silently absent from
`consumers()` — it can only be absent from the vocabulary, which is a narrower
and more visible failure. (§4 records the scraper I tried first, and why
scanning for literals is the wrong instrument.)

**The declaration is a convention, not an invariant.** A file that computes
caps under different names — as researcher-1's does — is invisible to `--scan`
for the same reason it is invisible to `check`. §5 is the measurement of that,
and it is a real limit rather than a hypothetical one.

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
