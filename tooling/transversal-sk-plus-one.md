# Extending the decider to \(k = \mathrm{sk}(G) + 1\): sound, and impractical

`UNIFIED.md` named one concrete piece of work that would lift two cells —
\((4,5)\) and \((3,6)\) — into range: a decider complete at
\(k = \mathrm{sk}(G) + 1\). I built it. **It is sound and it does not help**, and
the reason is measurable rather than a matter of budget.

## The extension is bounded, and provably

At \(k = \mathrm{sk}(G)\) the decider is complete because no edge can lie in two
crossings: the transversal choosing it twice would be a planarising set of size
\(< \mathrm{sk}(G)\). At \(k = \mathrm{sk}(G)+1\) that argument weakens by exactly
one step, and the weakening is bounded:

> **At \(k = \mathrm{sk}(G)+1\), at most one edge lies in two crossings, and no
> edge lies in three or more.**

Two doubly-used edges, or one triply-used edge, each force a transversal of size
\(k-2 = \mathrm{sk}-1\), which cannot planarise. So the configurations to add are
exactly those with \(2k-1\) distinct edges, one appearing in two pairs — and for
those the doubly-crossed edge carries two crossing points, so the planarisation
must try **both orders** of those points along the edge.

That is a finite, small addition, and it is implemented.

## Validation found a real bug, in the dangerous direction

The first version returned **False** for \(K_5\) at \(k=2\) and \(K_6\) at
\(k=4\), where the answer is True. The cause:

> The search looks for a drawing with **exactly** \(k\) crossings. At
> \(k = \mathrm{sk}\) that is sound — \(\operatorname{cr} \ge \mathrm{sk} = k\)
> forces equality — so the original decider never needed the distinction. At
> \(k = \mathrm{sk}+1\) a graph with \(\operatorname{cr} = \mathrm{sk}\) has no
> \(k\)-crossing configuration at all, and the search reports a **false
> refutation**.

Fixed by searching every \(j\) from \(\mathrm{sk}\) to \(k\). **This is exactly
the failure the validation suite exists to catch**, and it would not have been
caught by the refuting cases: it needed cases expecting *True*. The suite is
built around the claim that the refuting cases matter most, and here the bug was
in the other direction — so the lesson is that both halves earn their place, for
different reasons.

| | \(k = \mathrm{sk}\) | \(k = \mathrm{sk}+1\) |
| --- | --- | --- |
| \(K_5\), \(K_{3,3}\), Petersen, \(K_6\), \(K_{3,4}\) | correct | correct |
| \(K_{3,5}\) (\(\mathrm{sk}=3\), \(\operatorname{cr}=4\)) | correct **False** | correct True |
| \(K_{3,6}\) (\(\mathrm{sk}=4\), \(\operatorname{cr}=6\)) | correct **False** | **did not finish** |

## Why it is impractical, measured

The only available test of the **refuting** direction at \(k = \mathrm{sk}+1\) is
\(K_{3,6}\), on 18 edges. At \(k = \mathrm{sk}\) it returns in about a second. At
\(k = \mathrm{sk}+1\) it ran **over forty minutes without finishing**.

The cause is that the prune's power comes from the family \(P\) of planarising
sets of size \(\le k\) being *small*. A partial transversal survives if it
extends to some member of \(P\), so a larger \(P\) prunes less. And \(P\) grows
sharply:

| | \(\vert P\vert\) at \(k=\mathrm{sk}\) | at \(k=\mathrm{sk}+1\) | growth |
| --- | --- | --- | --- |
| \(K_{3,5}\) | 270 | 1485 | \(5.5\times\) |
| \(K_{3,6}\) | 1215 | 7533 | \(6.2\times\) |

So one step of \(k\) multiplies the configuration count by \(\binom{90}{5} /
\binom{90}{4} \approx 17\) **and** weakens the filter on each by a factor of
about 6. The two compound, and the observed slowdown — from ~1 s to over
2400 s — is far worse than the \(17\times\) the raw count suggests.

**The live-edge filter, which did the heavy lifting before, does nothing here.**
On \(K_{1,5} \square C_3\) it cut 15 of 33 edges and discovered unprompted that
every crossing had to be between two rungs. On \(K_{3,5}\) and \(K_{3,6}\) it
keeps every edge. That filter's power was specific to graphs whose minimum
planarising sets concentrate on a few edges, and it is not a general feature of
the method.

## Consequence for the family

**The target cells remain out of reach and the reach table stands.** \((3,6)\)
needs 39 edges and \((4,5)\) needs 44, against an 18-edge case that does not
finish. So the conclusion published at h5538 — every cell reachable by these
instruments is settled, and no further cell is reachable — is unchanged, and now
rests on a measurement rather than on an argument about the ceiling alone.

**What would actually be needed** is not a better prune but a different lower
bound: something that does not enumerate crossing configurations at all. The
enumeration is \(\binom{\text{pairs}}{k}\) at its root, and \(k\) grows with the
answer, so any method of this shape dies as the crossing number grows. That is a
property of the approach, not of this implementation.

Source: `transversal2.py`.
