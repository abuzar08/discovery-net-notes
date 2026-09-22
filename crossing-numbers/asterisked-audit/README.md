# Auditing the results the survey itself says cannot be relied upon

Clancy, Haythorpe and Newcombe mark certain results with an asterisk. Their
reason, verbatim:

> "some of these journals impose no peer review, or that which does occur is
> inadequate. As such, the results contained within cannot be relied upon, either
> in their own right, [or] ... where the proofs are either incorrect, or
> incomplete. To address this, we have marked all results appearing within such
> journals with an asterisk. ... marking results in this way is not intended to
> disparage the authors, but rather to highlight results which should be
> revisited and submitted to thorough peer review."

**That is a stated open task in an open-access source**, and it is exactly what
this instrument set does: decide individual crossing numbers independently of any
published proof. The gate from the previous pass says which asterisked claims are
reachable.

## Result: 21 exact values across 5 asterisked results, zero disagreements

### Theorem 2.26\* (Yang and Zhao, 2001) — confirmed at all 14 values tested

> \(\operatorname{cr}(Ci_n(\{1, \lfloor n/2 \rfloor\})) = 1\) for \(n \ge 6\).

The claim \(\operatorname{cr} = 1\) forces \(\mathrm{sk} = 1\), which is a
one-edge check — so this claim is unusually cheap to attack. **But
\(\mathrm{sk} = 1\) does not give \(\operatorname{cr} \le 1\)**: re-inserting the
deleted edge into a planar embedding may need more than one crossing. Both halves
were therefore decided:

- \(\mathrm{sk} = 1\) exactly, for every \(n = 6, \ldots, 19\) — so
  \(\operatorname{cr} \ge 1\);
- the transversal test at \(k = \mathrm{sk} = 1\), where it is **complete**,
  returns \(\operatorname{cr} \le 1\) at every one.

Hence \(\operatorname{cr} = 1\) **exactly at \(n = 6,\ldots,19\)**. The even cases
are the Möbius ladder and already follow from Guy and Harary; the **odd** cases
are the asterisked content, and they are confirmed.

### Theorem 2.33\* (Wang and Huang, 2008), and Conjecture 2.34

> \(m \le \operatorname{cr}(Ci_{3m-1}(\{1,m\})) \le m+1\) for \(m \ge 3\), with
> the companion conjecture that the value is \(m+1\).

At the smallest admissible \(m = 3\), i.e. \(Ci_8(\{1,3\})\) on 8 vertices and 16
edges: \(\mathrm{sk} = 4\) and a drawing with 4 crossings exists, so

> \(\operatorname{cr}(Ci_8(\{1,3\})) = 4\), **exactly.**

This confirms the asterisked bounds *and* **settles Conjecture 2.34 at its
smallest admissible parameter**, where \(m+1 = 4\).

### Theorem 2.10\* (He and Huang, 2007)

\(\operatorname{cr}(K_{1,2,2,n}) = 4X(n) + n + \lfloor n/2 \rfloor\). Confirmed
exactly at \(n = 1\) (\(\operatorname{cr} = 1\)) and \(n = 2\)
(\(\operatorname{cr} = 3\)).

### Theorem 2.9\* (Shanthini and Babujee, 2016)

\(\operatorname{cr}(K_{1,1,m,n}) = \operatorname{cr}(K_{m+2,n+2}) + \lfloor m/2
\rfloor \lfloor n/2 \rfloor - mn\). Confirmed exactly at \((m,n) = (2,3)\):
\(\operatorname{cr}(K_{1,1,2,3}) = 3\). At \((3,3)\) the gap is 4 and the cell is
outside the gate.

### Theorem 2.14\* (He et al., 2011)

\(\operatorname{cr}(K_{3,n} \setminus e) = X(n) - \lfloor (n-1)/2 \rfloor\).
Confirmed exactly at \(n = 4, 5, 6\) — values 1, 2, 4. At \(n = 7\) the gap is 2
and the cell is outside the gate.

### Theorems 3.15\* and 3.17\* — upper bound reproduced, not decided

\(\operatorname{cr}(P_n \square Ci_7(1,2)) = 8n\) and
\(\operatorname{cr}(P_n \square Ci_8(1,4)) = 9n-1\). At \(n = 1\) both claim 8,
and the planarisation heuristic **finds drawings with exactly 8 crossings** in
each. Since the heuristic only overestimates, a drawing below 8 would have
refuted them; none was found, and the construction is reproduced independently.
The lower half is out of reach — these have 35 and 32 edges with
\(\mathrm{sk}\) well above the gate.


## Second batch: 6 more exact values, and the informative-cell problem resolved

### Theorem 2.14\* part two, and Theorem 4.2\* (Li, 2014)

\(\operatorname{cr}(K_{4,n} \setminus e) = 2X(n) - \lfloor (n-1)/2 \rfloor\):
confirmed exactly at \(n = 3, 4, 5\) — values 1, 3, 6.

Theorem 4.2\* takes \(G = C_4 \cup K_1\) and claims three formulas. Confirmed
exactly: \(\operatorname{cr}(G + D_1) = 0\), \(\operatorname{cr}(G + D_2) = 1\),
\(\operatorname{cr}(G + P_1) = 2\).

**Running total: 27 exact values across 7 asterisked results, zero
disagreements.**

### The tension, stated

An exact decision needs \(V - \mathrm{sk} \le 1\), where \(V\) is the claimed
value. But a transcription defect is *harder to notice* when \(V\) is large and
the graph is big — so **information content grows with \(V - \mathrm{sk}\),
while decidability requires it to be small.** The cells I can decide are the
least informative ones. Measured across this batch:

| cell | \(V\) | \(\mathrm{sk}\) | \(V - \mathrm{sk}\) | decided? |
| --- | --- | --- | --- | --- |
| \(K_{4,4} \setminus e\) | 3 | 3 | 0 | yes |
| \(K_{4,5} \setminus e\) | 6 | 5 | 1 | yes |
| \(K_{4,6} \setminus e\) | 10 | 7 | 3 | no |
| \(G + D_3\) | 5 | 3 | 2 | no |
| \(G + D_4\) | 10 | 6 | 4 | no |
| \(G + C_4\) | 12 | 7 | 5 | no |

### Why it does not matter as much as it looks — the defects have a direction

**All three defects I have ever found are values printed too LARGE**: a planar
graph assigned crossing number 1; a skewness of 3 printed as 5; \(m-2\) printed
as \(2(m-2)\). Not one was a value printed too small.

And a claim that is too large is refuted by the **one-sided** check
\(ub < V\) — a drawing with fewer crossings than claimed. That needs no gate, no
exact decision, and **no bound on \(V - \mathrm{sk}\) at all**, because the
planarisation heuristic only ever overestimates.

So the audit does cover the high-information cells, for the defect mode that has
actually been observed. In **every** undecided cell above the heuristic
independently constructed a drawing with *exactly* the claimed number of
crossings and never fewer:

| cell | claimed | best drawing found |
| --- | --- | --- |
| \(K_{4,6} \setminus e\) | 10 | **10** |
| \(G + D_3\) | 5 | **5** |
| \(G + D_4\) | 10 | **10** |
| \(G + P_2\) | 6 | **6** |
| \(G + P_3\) | 11 | **11** |
| \(G + C_3\) | 7 | **7** |
| \(G + C_4\) | 12 | **12** |

Seven for seven. That is a construction-free reproduction of the upper half of
every claim I could not decide — and the half where the observed defect mode
lives.

**The limit that remains** is a claim printed too *small*, which only a lower
bound can catch and which needs the gate. No instance of that mode has been
observed in this lane, so the exposure is real but unquantified — I record it as
an untested direction rather than a covered one.

## What this says about my own pattern claim

My smallest-parameter claim has been narrowed twice, and stands as: the three
defects I found sit in **DS21's restatements of conjectures and open questions**,
not in stated formulas and not in Clancy's theorems. The asterisked results are a
**third population, and the one where defects should be most likely** — the
survey's own grounds for flagging them is that the proofs may be "incorrect, or
incomplete".

| population | checks at smallest parameter | defects |
| --- | --- | --- |
| DS21, restated **conjectures and questions** | 9 | **3** |
| DS21, stated **formulas** | 9 families | 0 |
| Clancy, stated **theorems** | 6 | 0 |
| Clancy, **asterisked** (unreviewed) results | 5 | **0** |

**The results flagged as unreliable are clean everywhere I can check, while the
defects I found were in a survey's restatements of reliable sources.** That is
evidence for the mechanism I proposed and against the intuitive alternative: the
failure is in *transcription*, not in the underlying mathematics or in the rigour
of the original venue.

It is a small sample and it does not exonerate anything — I could reach only the
smallest parameters, and the asterisked proofs remain unchecked *as proofs*. What
is checked is their values, at the parameters the gate admits.

Source: `aster.py`, `aster2.py`, `aster3.py`, using `transversal.py`, `ubound.py`.
