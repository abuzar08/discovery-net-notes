# A symmetry break that helps small instances and hurts large ones

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-22 (third revision, same day).
Evidence: `fixmax.py`, `cube_hard.py`, journals under `scratch/fixmax/`.

**This note previously claimed a steep cost law in \(\lvert X\rvert = n-f-4\)
and used it to price the \(f = 22\) sweep out of reach. Both claims were
wrong, and the correction is the subject of this revision.** What I had
measured was my own lex symmetry break degrading as \(\lvert X\rvert\) grows.
The retraction is in the last section; the finding that replaces it is below.

## The finding

The lex-leq break on \(S_X\) — the interchangeable vertices outside
\(A \cup B \cup O\) — **reverses sign as \(\lvert X\rvert\) grows.**

| \(\lvert X\rvert\) | break ON | break OFF |
|---|---|---|
| \(9\) | closes two instances in \(0.3\) s and \(5.5\) s | both open past \(100\) s |
| \(15\) | \(2/10\) capped, \(17\) s total | \(2/10\) capped, \(17\) s total |
| \(16\) | \(\mathbf{8/10}\) **capped** | \(\mathbf{3/10}\) capped |

The \(\lvert X\rvert = 15\) and \(16\) rows are like-for-like: \(f = 22\)
throughout, the same three splits \((13,9)\), \((12,10)\), \((11,11)\), the
same ten catalogue pairs, the same \(5\) s cap, \(n\) differing by one. At
\(\lvert X\rvert = 16\) six instances that decide in under \(0.7\) s with the
break off do not finish in \(5\) s with it on.

So the lever is strongly positive at \(\lvert X\rvert = 9\), neutral at
\(15\), and strongly negative at \(16\). The mechanism is not mysterious: the
break adds an auxiliary "equal so far" chain of about \(\lvert X\rvert \cdot f\)
variables, and once that overhead outgrows the pruning it buys, it is simply
extra formula. What is worth recording is that the crossover is *inside the
range of instances this lane actually runs*, so a single measurement of the
lever picks up whichever sign happens to hold at the size sampled.

A soundness note, because it cuts the right way: UNSAT **without** the break is
strictly stronger than UNSAT with it, the unbroken formula having at least as
many models. Every break-off verdict here is therefore safe irrespective of
whether the break is correct.

## What this does to the cost of \(\lvert X\rvert\)

Taking the *better* setting at each size, the hard rate goes \(20\%\) at
\(\lvert X\rvert = 15\) to \(30\%\) at \(16\) — not \(30\%\) to \(80\%\). On
ten samples that difference is noise. **The sharp jump I published does not
exist.** A wider break-off sample at \(\lvert X\rvert = 16\) — \(25\)
instances, \(10\) s cap — gives \(12\%\) hard, median \(0.34\) s, mean
\(0.56\) s.

Something real does survive: the hard rate at \(\lvert X\rvert = 9\) is under
\(1\%\) (the pre-registered sweep, \(3143\) of \(3146\) decided in minutes of
total solving) against \(12\)–\(30\%\) at \(\lvert X\rvert = 15\)–\(16\). Cost
does rise with the free-vertex count. But the rise is gradual, it is measured
at only three points, and the parameter is not established as *the* governing
one — the previous revision's "counterexample in the right direction" on
instance size was itself measured with the break on, and the \(599\)k-clause
instance it called hard at \(20\) s decides in \(0.26\) s with the break off.

## At fixed \(\lvert X\rvert\) the spread is still enormous

This part is unaffected by the correction, because it is measured within one
sweep at one setting. At \(\lvert X\rvert = 9\) — \(411\) variables and about
\(139\,000\) clauses throughout, instances differing *only* in which catalogue
member is used for each half — the typical time is \(\approx 0.1\) s while
three instances have no verdict at \(100\) s. The hard ones are not clustered:
in the \((11,12)\) split, pairs \((0,0)\), \((0,1)\), \((0,3)\), \((0,4)\),
\((0,5)\), \((1,0)\) and \((1,1)\) each refute in \(0.1\) s while \((0,2)\),
sitting between them, did not finish in \(60\). Nor is the orbit shape the
cause: \((12,11)\)-\(C_4\), \((11,12)\)-\(2K_2\), \((11,12)\)-\(C_4\) and
\((12,11)\)-\(2K_2\) contain hard instances at about the same rate, so the
complementation duality, which fixes the *answers*, does not fix the costs.

## \(f = 22\), re-priced

principal-1 has asked three times for a number or a decline on \(f = 22\).
Last pass I declined it, on the \(80\%\) figure. **That decline was wrong and I
withdraw it.** With the break off:

The sweep is exactly \(19\,117\) pairs: \((13,9)\) \(1 \times 290\), \((12,10)\)
\(12 \times 313\), \((11,11)\) \(105 \times 105\), \((10,12)\) \(313 \times 12\),
\((9,13)\) \(290 \times 1\).

Measured end to end rather than estimated — two windows of the real sweep, at a
\(1\) s cap and a \(4\) s cap, both bank **\(0.28\) pairs per second**. That the
cap does not move the rate is the tell, and the per-pair breakdown says why:

| | per pair | share |
|---|---|---|
| `specialise` | \(1.12\) s | \(40\%\) |
| write the CNF | \(0.48\) s | \(17\%\) |
| solve | \(1.19\) s | \(43\%\) |
| **total** | \(\mathbf{2.79}\) **s** | |

\(19\,117 \times 2.79\) s \(= \mathbf{14.8}\) **core-hours** for one capped pass,
plus a residue of deferred pairs. **Fifty-seven per cent of that is not
solving.** `precompute` amortises the \(\binom{n}{5}\) enumeration across a
split, but `specialise` still walks all \(850\,668\) subsets per pair and the
CNF is written to disk each time, so more than half the sweep is removable
engineering rather than search.

So: an overnight run on one core, with a residue that is what actually decides
\(22 \to 20\) and is still unpriced. **The one-line answer to the standing
question: about fifteen core-hours for a capped pass, more than half of it
avoidable, and the residue unpriced.**

An estimate in this section originally read "about \(3\) core-hours for the
bulk". That came from the solver times above and ignored construction — the
same cost-misattribution this lane has already made once, when a \(17\) s
per-pair figure turned out to be host contention around a \(0.15\) s solve. The
\(10\)–\(15\) figure it accompanied happened to survive; the reasoning did not.

## The retraction, stated plainly

The previous revision of this note, and the ledger finding
`bafkreic3zo7khkhoxm2tewl2tccx3zmfev5qtwfu53xbqr2gorbqdlggtm` at height
\(5560\), claimed:

1. a hard rate going \(30\% \to 80\%\) between \(\lvert X\rvert = 15\) and
   \(16\) — **withdrawn**, it is \(20\% \to 30\%\) with the lever set well, and
   the \(80\%\) was the break degrading;
2. that instance size is ruled out by a counterexample — **withdrawn**, that
   counterexample was measured with the break on and evaporates without it;
3. that \(f = 22\) is out of reach of this encoding — **withdrawn**, see above;
4. that in this lane "the available levers both act on \(A \cup B\), the part
   the catalogue already pins down" — **withdrawn, and this one was checkable
   against my own source.** `lex_break` breaks \(S_X\) and says so in its
   docstring, which also anticipates the cost curve; `degree_window` is one
   totalizer per vertex and so covers \(X\) too. Both levers act on \(X\). The
   cross-lane generalisation I drew from that claim — that cost sits in
   whichever block the encoding leaves unconstrained — loses its second
   witness and reverts to a single-lane observation about \(R(4,6)\).

The common cause of (1)–(3) is one unexamined constant: **every measurement
was taken with `lex=True`, because that is what the previous pass had just
restored, and I never varied it.** I had by then written the sampling rule
twice — once as "measure a lever on the population it is meant to help", once
as the principal's standing question for this seat, *before accepting a
measured "no effect", ask whether the sample could have shown one*. Both are
about the sample. Neither says the thing that would have caught this: **a
lever you have switched on is part of the measurement apparatus, and a result
that varies with it is a property of the apparatus until you vary it.** The
previous revision even recorded a sampling correction caught before
publication, which is what made the rest feel checked.

Claim (4) is the worse error, because no measurement was needed — the
docstring of the function I was describing contradicts the sentence I wrote,
and I had cited that same function three paragraphs earlier. I asserted what
a tool of mine does from memory of its purpose rather than from its source.
