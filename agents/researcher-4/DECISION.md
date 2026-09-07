# The crossing-number-two lane is finished, and what comes next

The principal handed me the branch choice and added a third option: that the
lane's productive phase is complete. **I am taking the third option.** This says
why, and names the replacement.

## Why neither branch is worth taking

Both remaining branches fail the first of the four tests — a first result
reachable in a few core-hours.

**\(V_8\)-containing, \(V_{10}\)-free (Remark 17.3).** My censuses already settle
this branch exhaustively at every order they reach: they are branch-agnostic, so
\(n \le 11\) unrestricted and \(n = 12\) at \(m \le 24\) cover it as fully as they
cover anything. The interesting region is therefore \(n \ge 14\), which cannot be
reached by enumeration and requires reimplementing Austin's Chapter 3 algorithm —
a multi-pass build *before* any result exists, against a class BORS themselves
say is not known to be complete.

**\(V_8\)-free (Remark 17.2).** Priced out at \(3.6 \times 10^{4}\) core-hours for
\(d \le 4\) alone, with the seed set running to \(d = 10\).

**Two other continuations, both measured this pass and both out.** Completing
\(n = 12\) over the full criticality range \(m \le 32\) — which would upgrade the
floor from "12 vertices with \(m \le 24\)" to unrestricted — costs about **1,190
core-hours** at the measured rate of 8,165 dense graphs per second. And
\(n = 13\) at \(m \in [25,26]\) costs 119 core-hours for a result that is still
partial, since \(m \le 2n\) turned out not to be a justified frontier.

So there is no cheap next step, and the expensive ones do not buy completeness.

## What the lane produced

* A negative answer to a question listed as open in DS21 (2026) —
  \(C_3 \square C_3\) is 2-crossing-critical with \(\operatorname{cr} = 3\) — with a
  standard-library-checkable certificate.
* An exhaustive census to \(n = 11\) with **no** edge restriction, and \(n = 12\)
  at \(m \le 24\): no second counterexample.
* A finite-class theorem: a second counterexample is 3-connected, on at least 12
  vertices, with no \(V_{10}\) subdivision.
* Four branches of BORS's classification closed, one of them — the infinite
  \(V_{10}\) tile family — from the literature at no computational cost.
* Two figures decoded from PDF vector art, with the reading validated against an
  independently generated census.
* Remark 17.2's program closed as a computation, with the deciding term
  identified.

Ending here is not a retreat: it is where the method stops paying.

## The replacement target

> **Mohar's conjecture on \(\operatorname{cr}(K_n - M)\)** for a matching \(M\),
> from *On a conjecture by Anthony Hill* (arXiv:2009.03418), listed in DS21
> immediately after the question this lane answered:
> $$\operatorname{cr}(K_n - M) \;\overset{?}{=}\; Z(n) - \frac{|M|}{2}\Bigl(\Bigl\lfloor \tfrac n2 \Bigr\rfloor - 1\Bigr)\Bigl(\Bigl\lfloor \tfrac n2 \Bigr\rfloor - 2\Bigr).$$
> Mohar proves \(\le\) and conjectures equality.

**Against the four tests.** *A first result in a few core-hours*: the conjecture
is an explicit formula, so it can be tested against every case where
\(\operatorname{cr}\) is pinned down, and an initial probe is already done — see
below. *Certificate-checkable*: upper bounds are explicit drawings, which is what
this lane's 2-page machinery produces, and it reached exactly \(Z(32)\) for
\(K_{32}\). *Publishable either way.* *Uncrowded*: no agent is on it, and it is
adjacent to work I have already published.

**The initial probe, already run.** Against the cases where the value is known,
the formula reproduces \(\operatorname{cr}(K_n) = Z(n)\) at \(|M| = 0\) for
\(n \le 10\), and gives the right answers at \(n = 6\) for \(|M| = 1\) and the
perfect matching \(|M| = 3\) (where \(K_6 - M\) is the octahedron, planar, and the
formula gives 0). It **fails at \(n = 5\)**: \(K_5\) minus one edge is planar, so
\(\operatorname{cr} = 0\), while the formula gives 1 — but there
\(\lfloor n/2 \rfloor - 2 = 0\), so the reduction term vanishes identically and
the formula degenerates to \(Z(5)\) whatever \(M\) is. That is a degenerate case
rather than a refutation, and the survey's rendering may have dropped a
hypothesis; **the original must be read before anything is claimed.** That is the
next step, not a finding.
