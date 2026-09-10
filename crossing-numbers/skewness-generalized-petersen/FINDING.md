# DS21's rendering of the Chia–Lee skewness conjecture is false at \(k = 3\)

A fourth discrepancy in DS21, and the most robust of the four: it rests on an
exhaustive computation with a certificate that can be checked by hand, not on
notation or on arithmetic internal to the survey.

## What DS21 states

From the open questions of the skewness entry, Ninth Edition of July 17 2026,
re-extracted at page fidelity and confirmed verbatim:

> ▼Chia and Lee [207] conjectured that \(\mathrm{sk}(GP(4k,k)) = k+2\) for odd
> \(k \ge 3\), where \(GP(n,k)\) is the generalized Petersen graph. The
> conjecture was mostly settled in [208], but cases \(k = 5\) and \(k = 7\)
> remain open.

The symbol is plain \(\mathrm{sk}\) with no diacritic, so the notation hazard
that produced an earlier near-miss in this campaign does not apply here.

## What is true

At \(k = 3\) the statement asserts \(\mathrm{sk}(GP(12,3)) = 5\), and \(k = 3\)
is inside the range DS21 describes as settled.

> **\(\mathrm{sk}(GP(12,3)) = 3\).**

\(GP(12,3)\) is cubic on 24 vertices with 36 edges. Deleting the three edges
$$u_0u_1, \qquad u_3v_3, \qquad u_6v_6$$
leaves a planar graph, and **no set of at most two edges does** — verified by
exhausting all \(1 + 36 + 630 = 667\) such sets.

## The certificate, and how it was checked

The witness is checkable by anyone with a planarity routine, and it was not
taken on the routine's word. For \(H = GP(12,3) - \{u_0u_1, u_3v_3, u_6v_6\}\) a
planar embedding was extracted and its faces traversed:

$$V = 24, \quad E = 33, \quad F = 11, \quad V - E + F = 2,$$

which is Euler's formula for a connected planar graph. The exhaustiveness at
\(r \le 2\) was then re-run in a separate loop written independently of the
search that produced the witness.

The construction was validated before use, on the obvious instance: my
\(GP(5,2)\) is isomorphic to `networkx.petersen_graph()`, and the same routine
returns \(\mathrm{sk} = 2\) for the Petersen graph, its known value.

## What this does and does not claim

**It does claim:** the sentence as printed in DS21 is false at \(k = 3\), and
this is checkable from DS21 together with the certificate above.

**It does not claim** anything about what Chia and Lee actually conjectured.
Reference [207] — *Skewness of generalized Petersen graphs and related graphs*,
Front. Math. China **7**.3 (2012) — is paywalled and has not been read, and the
follow-up [208] returned HTTP 403. Two access attempts, both refused; recorded so
the limit is visible rather than implied.

**One thing the abstract of [207] does say**, and it sharpens the framing without
settling it:

> "In this paper, we determine the skewness of the generalized Petersen graph
> \(P(4k,k)\) and hence a lower bound for the crossing number of \(P(4k,k)\)."

They **determine** it — the word is theirs. DS21 presents the same family's
skewness as a **conjecture** with the value \(k+2\) for odd \(k \ge 3\), and
records \(k = 5\) and \(k = 7\) as open. A determined value and an open
conjecture are different things, so at least one of the following holds, and I
cannot tell which from outside the paywall:

- the range in DS21 is wrong and \(k = 3\) lies outside the conjecture;
- the formula in DS21 is wrong;
- DS21 renders as conjectural something the source states as determined, with
  the open cases belonging to a different question.

**What does not depend on resolving that:** the printed sentence asserts
\(\mathrm{sk}(GP(12,3)) = 5\), and the value is 3. The likeliest explanation
is the pattern already seen twice in this survey: **a family or a side condition
altered in transcription.** Two observations point that way rather than at the
authors:

- \(\mathrm{sk}(GP(4k,k))\) at \(k = 3\) is **3**, which is \(k\), not \(k+2\);
- \(\mathrm{sk}(GP(3k,k))\) is **2** at \(k = 3\) and **4** at \(k = 5\), which is
  \(k - 1\) in both cases.

Neither family gives \(k+2\) at the values reachable here, so a single arithmetic
offset does not reconcile it either.

### Correction: my first observation was itself wrong

I wrote above that \(\mathrm{sk}(GP(4k,k))\) "is \(k\)" on the strength of the
single value at \(k = 3\). **Computing \(k = 4\) refutes that**: it is 5, not 4.
The full picture at every reachable \(k\):

| \(k\) | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- |
| \(\mathrm{sk}(GP(4k,k))\) | 0 | **3** | **5** | \(\ge 5\) |
| \(k+2\) | 4 | 5 | 6 | 7 |

\(k = 2\) is planar, consistent with the known classification that \(GP(n,k)\)
is planar exactly when \(k = 1\), or \(k = 2\) with \(n\) even — an
independent check on the construction. \(k = 2\) and \(k = 4\) are outside the
conjecture's stated range of odd \(k\), so neither bears on its truth; they are
reported because they bear on **which formula was intended**.

### A hypothesis, with the measurement that would kill it

\(3\) and \(5\) at \(k = 3, 4\) fit \(\mathbf{2k-3}\) exactly. That
predicts \(\mathrm{sk}(GP(20,5)) = 7\) — which happens to **agree with the
conjectured \(k+2\) at \(k = 5\) alone**, the two formulas coinciding only
there, and to disagree at \(k = 7\) where \(2k-3 = 11\) against \(k+2 = 9\).

If it holds, the natural reading is that DS21's range is wrong rather than its
formula — that the conjecture belongs to odd \(k \ge 5\) and \(k = 3\) was
swept in — which is the same dropped-side-condition pattern as Finding 1 of the
main audit.

**This is a two-point fit and is stated as a hypothesis, not a result.** A
two-point trend elsewhere in this campaign failed its first test, so the fit is
recorded together with the computation that decides it: \(\mathrm{sk}(GP(20,5))\)
is running, \(r \le 4\) is already exhausted, and \(2k-3\) requires that
\(r = 5\) and \(r = 6\) **both** fail.

## Consequence for the open cases

DS21 records \(k = 5\) and \(k = 7\) as the remaining open cases. **If the
statement is false at \(k = 3\), that framing needs revisiting**: what is open is
not "two remaining values of a conjecture verified elsewhere" but the conjecture's
correct statement.

### Progress on the open case \(k = 5\)

> **\(6 \le \mathrm{sk}(GP(20,5)) \le 7\).**

**Lower bound**, by exhaustion: no set of at most 5 edges planarises
\(GP(20,5)\), verified over all
\(1 + 60 + 1{,}770 + 34{,}220 + 487{,}635 + 5{,}461{,}512 = 5{,}985{,}198\)
sets, taking 56 minutes.

**Upper bound**, by an explicit witness. The certificates at \(k = 3\) and
\(k = 4\) share a shape — one outer edge together with spokes — so rather than
enumerate \(\binom{60}{7}\) sets, search that shape alone, fixing the outer
edge by the vertex-transitivity of the outer cycle. **Found in 24 seconds:**
deleting
$$u_0u_1, \qquad u_3v_3,\; u_4v_4,\; u_5v_5,\; u_8v_8,\; u_9v_9,\; u_{10}v_{10}$$
leaves a planar graph — 7 edges.

Verified the same way as the \(k=3\) certificate: \(V = 40\), \(E = 53\),
\(F = 15\), \(V - E + F = 2\).

**So the open case is confined to two values, with a hand-checkable certificate
for the upper one.** Deciding between them needs the exhaustion at \(r = 6\):
\(\binom{60}{6} = 50{,}063{,}860\) sets, about **8.6 core-hours** at the
measured 1,626 sets per second. That is cheap against everything else this seat
has priced — the \(n = 13\) crossing-critical census cost 124 core-hours and
settled an entire order — and it decides a case DS21 records as open, either way.
It is running.

**Both outcomes are worth having.** \(\mathrm{sk} = 7\) confirms the
conjectured \(k+2\) at \(k = 5\) and, with \(k = 3\) false, points at
DS21's *range* rather than its formula. \(\mathrm{sk} = 6\) refutes the
conjecture at \(k = 5\) as well, and refutes the \(2k-3\) fit with it.

## The witnesses have a pattern, and it predicts

The certificates at \(k = 3, 4, 5\) are not merely "one outer edge plus spokes".
The spokes are **two runs of \(k-2\) consecutive indices, offset by \(k\)**,
starting at 3:

| \(k\) | spokes deleted | total edges |
| --- | --- | --- |
| 3 | \(\{3\},\ \{6\}\) | 3 |
| 4 | \(\{3,4\},\ \{7,8\}\) | 5 |
| 5 | \(\{3,4,5\},\ \{8,9,10\}\) | 7 |

which is \(1 + 2(k-2) = 2k-3\) edges — the fit recorded above, now with a
construction behind it rather than a curve through two points.

**Applied to \(k = 7\) it works on the first try.** Deleting \(u_0u_1\) and
the spokes \(\{3,4,5,6,7\} \cup \{10,11,12,13,14\}\) planarises
\(GP(28,7)\), so

> \(\mathrm{sk}(GP(28,7)) \le 11\),

obtained from a **single planarity test** rather than a search.

## \(k = 7\) cannot be settled here, and the number says why

DS21 conjectures \(k+2 = 9\), which is *below* the bound above, so 11 does not
test the conjecture. Deciding \(k = 7\) needs the lower bound, and that is out
of range by a wide margin:

$$\sum_{r \le 8} \binom{84}{r} = 48{,}563{,}893{,}286 \ \text{ tests} \ \approx\ \mathbf{8{,}296 \text{ core-hours}}$$

at the measured 1,626 tests per second — **four times** the \(M_{8,3}\) figure
declined earlier in this campaign, and sixty-seven times the \(n = 13\)
crossing-critical census that settled an entire order.

**So \(k = 5\) is decidable here and \(k = 7\) is not.** What remains
reachable at \(k = 7\) is only better upper bounds: a search over the same
structured shape for fewer spokes is running, to see whether 9 is achievable
within it. **A failure there would not be evidence against 9** — it would show
only that 9 is unreachable by deleting one outer edge and spokes, which is one
shape among many.

### The structured search at \(k = 7\): 9 is unreachable in that shape

Exhausted: **no set of one outer edge plus at most 8 spokes planarises
\(GP(28,7)\)** — 5, 6, 7 and 8 spokes all fail, over
\(98{,}280 + 376{,}740 + 1{,}184{,}040 + 3{,}108{,}105 = 4{,}767{,}165\) sets.

**This is not evidence against DS21's conjectured 9**, and it was declared not to
be before the run started. It shows only that 9 is unreachable **by that shape**,
which is one family of edge sets among many, and the true skewness could be 9 by
some set the shape does not contain.

### The shape is provably suboptimal, and this weakens my own \(k = 7\) bound

Tested against the cases DS21 records as **settled**, where the conjectured
\(k+2\) is taken to be the true value:

| \(k\) | graph | shape gives | settled value \(k+2\) |
| --- | --- | --- | --- |
| 9 | \(GP(36,9)\) | 15 | **11** |
| 11 | \(GP(44,11)\) | 19 | **13** |

**The shape overshoots by 4 and 6.** So \(2k-3\) is a property of *this
construction*, not of the skewness function, and the shape's agreement with the
exhaustive answers at \(k = 3\) and \(k = 4\) is a small-case accident rather
than a general pattern.

Three consequences, and I would rather state them against my own results than
leave them implied:

1. **\(\mathrm{sk}(GP(28,7)) \le 11\) is probably loose.** It is still a valid
   upper bound, but a bound from a construction now known to overshoot by 4 at
   the next odd value carries little weight, and **the gap between it and DS21's
   9 is evidence about my shape, not about the conjecture.**
2. **The \(2k-3\) hypothesis is dead as a claim about skewness.** It survives
   only as a description of what this particular family of edge sets achieves.
3. **The exhaustion at \(k = 7\) up to 9 edges says less than it appeared to.**
   It rules out 9 within a shape that is known to be the wrong shape at \(k = 9\)
   and \(k = 11\).

**What is untouched.** \(\mathrm{sk}(GP(12,3)) = 3\) rests on **exhaustive**
enumeration over all sets of at most two edges plus an Euler-verified witness,
not on the shape at all. Finding 4 stands exactly as stated.

### Whether the shape is optimal at \(k = 5\) is about to be tested

The shape gives the exact value at \(k = 3\) (3, matching the exhaustive
answer) and at \(k = 4\) (5, matching). At \(k = 5\) it gives **7**, while
exhaustion has so far shown only \(\mathrm{sk} \ge 6\).

**So the running \(r = 6\) computation tests two things at once.** If it finds a
witness, then \(\mathrm{sk}(GP(20,5)) = 6\) and **the structured shape is not
optimal** — in which case my \(\le 11\) at \(k = 7\) is probably loose too,
and the gap between it and DS21's 9 would be a defect of the shape rather than
evidence about the conjecture. If it finds nothing, \(\mathrm{sk}(GP(20,5)) = 7\),
the shape is optimal at every value tested, and the \(k = 7\) bound of 11 gains
standing.

That is worth saying plainly: **the value of the \(k = 7\) upper bound depends
on a computation about \(k = 5\)**, and neither number should be read on its own.

Source: `gp.py`, `gp28.py`.
