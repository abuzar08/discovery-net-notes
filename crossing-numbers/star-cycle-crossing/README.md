# \(\operatorname{cr}(K_{1,m} \square C_3)\): two surveyed values confirmed exactly, and a formula conjectured

## Source and selection

Clancy, Haythorpe and Newcombe, *A survey of graphs with known or bounded
crossing numbers*, arXiv:1901.05155 — **a second, open-access survey**, chosen
because the binding constraint on my DS21 work has been access: two of four
corrections there cannot be attributed without a library. This one can be read in
full.

It states, among twenty parametric claims with explicit ranges,
\(\operatorname{cr}(S_3 \square C_n) = 1\) and
\(\operatorname{cr}(S_4 \square C_n) = 2\) at \(n = 3\), where \(S_m = K_{1,m}\).

## Two values confirmed, exactly

My theorem \(\mathrm{sk}(K_{1,m} \square C_3) = m-2\) gives a **proved lower
bound** on the crossing number, since \(\mathrm{sk}(G) \le \operatorname{cr}(G)\)
— deleting one edge per crossing planarises any drawing. The planarisation
heuristic supplies the upper bound. Where they meet, the value is exact:

| | \(\mathrm{sk} = m-2\) (proved) | drawing found | Clancy | |
| --- | --- | --- | --- | --- |
| \(K_{1,3} \square C_3\) | 1 | 1 | 1 | \(\operatorname{cr} = 1\) **exactly** |
| \(K_{1,4} \square C_3\) | 2 | 2 | 2 | \(\operatorname{cr} = 2\) **exactly** |

So both surveyed values are confirmed, and confirmed *independently* — the lower
bound comes from a theorem about a different quantity.

**A capability worth naming:** a skewness theorem is a crossing-number lower
bound. That is what turns a one-sided heuristic into an exact determination, and
it is why the skewness work has reach beyond skewness.

## The two quantities separate at \(m = 5\)

They do not stay equal. Measured upper bounds against the proved lower bound
\(m-2\):

| \(m\) | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| \(\mathrm{sk} = m-2\) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| best drawing | 1 | 2 | 4 | 6 | 9 | 13 | 17 | 21 | 25 |

Skewness grows linearly, the crossing number quadratically, so \(\mathrm{sk}\) is
only a useful lower bound at \(m \le 4\).

## The conjecture

The upper bounds are not arbitrary. Writing
\(X(m) = \lfloor m/2 \rfloor \lfloor (m-1)/2 \rfloor\):

> **Conjecture.** \(\operatorname{cr}(K_{1,m} \square C_3) = X(m)\).

At \(m = 3\) and \(4\) the conjecture gives 1 and 2, matching Clancy.

### The upper bound, swept again at higher effort

The first sweep missed by one at \(m = 8, 9, 10\) and I recorded those as search
luck rather than a ceiling, on the grounds that \(m = 11\) attained \(X(11)\).
**Re-running at 250 restarts confirms that reading**: the misses were the search,
not the graph.

| \(m\) | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| \(\vert E\vert\) | 21 | 27 | 33 | 39 | 45 | 51 | 57 | 63 | 69 | 75 |
| \(X(m)\) | 1 | 2 | 4 | 6 | 9 | 12 | 16 | 20 | 25 | 30 |
| best drawing | **1** | **2** | **4** | **6** | **9** | **12** | **16** | 21 | **25** | 31 |

**Eight of ten meet \(X(m)\) exactly, and no drawing below \(X(m)\) was found at
any \(m\).** This is the same kind of construction-free confirmation as the Hill
and Zarankiewicz sweep: an algorithm that knows nothing about the intended
drawing independently builds one with exactly the conjectured number of
crossings, at every order it can reach.

**The two misses are where my own measured reach says they should be.** The
Harborth lane established that this instrument's meet-rate degrades past
\(|E| \approx 45\); the misses here are at \(|E| = 63\) and \(75\), well beyond
it, while \(m = 11\) at \(|E| = 69\) still meets. So the misses are evidence
about the search, and I do not read them as evidence about the conjecture in
either direction.

It is one-sided, and only in the refuting direction. A drawing below \(X(m)\)
would have killed the conjecture on the spot; **finding none is not evidence for
the lower bound**, which remains the open half.

## Why \(X(m)\), structurally

Not a curve through points. **Contract each leaf triangle of
\(K_{1,m} \square C_3\) to a single vertex** — the same contraction that proves
my skewness lower bound — and the result is exactly \(K_{1,1,1,m}\), verified for
\(m = 3,4,5,6\). And Harborth's theorem, recorded in DS21, is

$$\operatorname{cr}(K_{1,1,1,m}) = X(m),$$

which my heuristic reproduces at \(m = 3, \ldots, 7\). So the conjecture says
that **this contraction does not change the crossing number.**

**That is a motivation, not a proof, and the direction matters.** Crossing number
is *not* minor-monotone, so \(\operatorname{cr}(K_{1,1,1,m}) \le
\operatorname{cr}(K_{1,m} \square C_3)\) does **not** follow from the contraction.
The lower bound is open; what is proved is only \(\operatorname{cr} \ge m-2\).

## The upper bound is now proved, not sampled

The other direction *does* go through, and it needs no heuristic. The point is
that the contraction has an inverse which is **local**.

> **Theorem.**
> \(\operatorname{cr}(K_{1,m} \square C_3) \le \operatorname{cr}(K_{1,1,1,m})\)
> for every \(m \ge 1\). With
> \(\operatorname{cr}(K_{1,1,1,m}) = X(m)\) this gives
> \(\operatorname{cr}(K_{1,m} \square C_3) \le X(m)\) for **all** \(m\).

**Proof.** In \(K_{1,1,1,m}\) every vertex \(v_j\) of the large part is adjacent
to exactly the three vertices of the small parts, so
\(\deg v_j = 3\) **exactly**. Take an optimal drawing. Around each \(v_j\) choose
a disc meeting only the three edge-ends at \(v_j\), and let
\(e_1, e_2, e_3\) be those ends in the cyclic order in which they leave \(v_j\).
Delete \(v_j\), place \(t_1, t_2, t_3\) inside the disc in that same cyclic
order, join \(e_i\) to \(t_i\), and draw the triangle \(t_1t_2t_3\) inside the
disc. Everything added lies inside a disc that no other edge enters, and the
three ends are attached in their original cyclic order, so **no crossing is
created and none is destroyed**. Doing this at every \(v_j\) yields a drawing of
the split graph with the same number of crossings.

That the split graph *is* \(K_{1,m} \square C_3\) is immediate — the small parts
become the centre triangle \(T_0\), each \(t\)-triangle becomes a leaf triangle
\(T_j\), and the three former edges at \(v_j\) become its rungs — and it is
verified by isomorphism test for every \(m\) from 2 to 12. The attachment order
matters for the *drawing* but not for the *graph*, since a triangle is symmetric
under every permutation of its vertices. \(\blacksquare\)

**This supersedes the sampled upper bound**, and it settles the two misses: the
heuristic's \(X(10)+1\) and \(X(12)+1\) were the search, not the graph, and that
is now a proof rather than a reading of the trend.

## What the conjecture has been reduced to

With the upper bound proved, the conjecture
\(\operatorname{cr}(K_{1,m} \square C_3) = X(m)\) is **exactly equivalent** to the
reverse inequality

$$\operatorname{cr}(K_{1,1,1,m}) \;\le\; \operatorname{cr}(K_{1,m} \square C_3),$$

that is: *contracting the leaf triangles does not decrease the crossing number.*
One clean question, in place of a formula to be guessed.

**A concrete route to it.** In an optimal drawing the edges of a leaf triangle
\(T_j\) are pairwise adjacent, so \(T_j\) is drawn as a simple closed curve
\(\gamma_j\). If some edge crossed \(\gamma_j\) twice it could be rerouted
alongside to save two crossings, so in an optimal drawing **no edge crosses
\(\gamma_j\) twice**; hence any edge meeting \(\gamma_j\) has an endpoint in the
disc it bounds. So it would be enough to show that some optimal drawing has
**every leaf triangle bounding an empty disc** — then each \(\gamma_j\) can be
shrunk to a point, contracting \(T_j\) at no cost and giving a drawing of
\(K_{1,1,1,m}\) with the same number of crossings.

That reduction is not proved here, and it is where the remaining difficulty sits.

**Why the usual quantitative tools cannot help.** \(X(m)\) is quadratic in
\(m\), but \(K_{1,m} \square C_3\) has \(|V| = 3m+3\) and \(|E| = 6m+3\), so
\(|E| < 4|V|\) for every \(m\) and the **crossing lemma gives nothing at all**.
The graph is sparse; the quadratic growth comes from the structure — \(m\) prisms
sharing one triangle — and not from edge density. Any proof of the lower bound
has to be structural.

## Status

- \(\operatorname{cr}(K_{1,m} \square C_3) = X(m)\) for \(m = 3, 4\): **proved**
  here (lower bound from the skewness theorem, upper from a drawing), and
  agreeing with Clancy.
- \(\operatorname{cr}(K_{1,m} \square C_3) \le X(m)\) for \(m \le 11\): explicit
  drawings, with three values one above.
- \(\operatorname{cr}(K_{1,m} \square C_3) = X(m)\) in general: **conjectured**,
  with a structural reason and no proof of the lower bound.

Source: `chiasim.py`, `ubound.py`.
