# \(R(5,5) \le 49\): Lemma 3.1 and Theorem 3.1, certified

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-09.
Subject: McKay and Radziszowski, *Subgraph Counting Identities and Ramsey
Numbers*, **JCTB 69 (1997) 193–209**, §3.
Checker: `mr49.py`. Data: `e45.json`, `r45_24_e132.g6`.

## Why this step, and why it is reachable now and was not in 1995

The \(R(5,5) \le 49\) proof rests on two statements:

> **Lemma 3.1.** Let \(G\) be a \((5,5,49)\)-graph. Then for each vertex \(v\),
> \(G^+_v\) and \(\overline{G^-_v}\) are \((4,5,24,132)\)-graphs, regular of
> degree \(11\).
>
> **Theorem 3.1.** The only two \((4,5,24,132)\)-graphs are \(H_1\) and \(H_2\).

In 1995 Theorem 3.1 required a dedicated search, because the catalogue of
\((4,5,24)\)-graphs was incomplete — McKay and Radziszowski had \(350\,904\)
and the true count \(352\,366\) only arrived with Angeltveit and McKay (2016).
**Given the complete catalogue, Theorem 3.1 becomes a filter**, and Lemma 3.1
becomes arithmetic plus one fact about the two survivors. Both are now
checkable in seconds, which is the same shape as the \(R(5,5) \le 46\) Section 4
work in `AM46-SECTION4.md`: an identity, a window, and inequalities.

## What is checked

**(1) The window forces regularity.** At \(n = 49\), \(R(4,5) = 25\) gives
\(49 - 25 = 24 \le d(v) \le 24\). So \(G\) is \(24\)-regular,
\(v(G^+_v) = 24\) and \(v(G^-_v) = 49 - 1 - 24 = 24\).

**(2) Identity \((I_2)\), re-derived rather than copied.** With
\(g_2(X,n) = v(X)\,(n - 2v(X)) + 2e(X)\), the per-vertex constant is
\(24\,(49 - 48) = 24\), so

$$
\sum_v e(G^-_v) = \tfrac{49 \cdot 24}{2} + \sum_v e(G^+_v) = 588 + \sum_v e(G^+_v).
$$

The paper's \(588\) — **match**.

**(3) The complement step.** \(e(G^-_v) = \binom{24}{2} - e(\overline{G^-_v}) = 276 - e(\overline{G^-_v})\), so

$$
\sum_v \big[\, e(G^+_v) + e(\overline{G^-_v}) \,\big] = 49 \cdot 276 - 588 = 12\,936 .
$$

The paper's \(12\,936\) — **match**.

**(4) The forcing, and it has no slack at all.**
\(12\,936 / 49 = 264\), and each of the two terms is at most
\(E(4,5,24) = 132\) — a value this directory recomputed from the full published
catalogue and cross-checked against Angeltveit–McKay's Table 1. Since
\(264 = 2 \times 132\), **both terms are exactly \(132\) at every vertex.**

This is the load-bearing step and it is worth saying how tight it is: the
argument works because the average lands *exactly* on twice the maximum. One
more edge of headroom anywhere — \(E(4,5,24) = 133\) — and the lemma fails
outright. That is also why the \(d = 24\) row matters so much elsewhere, and why
the loose \([111,133]\) bound flagged in `POSITIVE-CONTROL.md` would have been
useless here.

**(5) Theorem 3.1 as a filter.** Filtering the complete \(352\,366\)-graph
catalogue by \(e = 132\) leaves **exactly two** graphs. Both were decoded by
this directory's own graph6 decoder and re-verified to be genuine
\((4,5)\)-graphs by its own clique search, and both are **\(11\)-regular** —
which is precisely the *"no such graphs with maximum degree greater than 11"*
input the lemma cites, here verified rather than taken on trust.

**(6) The automorphism groups.** Computed here by exhaustive backtracking over
all \(24!\)-consistent adjacency-preserving maps:

| | \(|\mathrm{Aut}|\) | vertex-transitive |
|---|---|---|
| first survivor | \(24\) | yes |
| second survivor | \(48\) | yes |

McKay and Radziszowski state \(|\mathrm{Aut}(H_1)| = 48\),
\(|\mathrm{Aut}(H_2)| = 24\), and that both are vertex-transitive. **The
multiset \(\{24, 48\}\) matches and both are vertex-transitive.** Which of my
two is their \(H_1\) is a labelling question and I make no claim about it.

## Trust boundary

**Verified here:** the degree window; the identity \((I_2)\) and both derived
constants; the forcing; that exactly two catalogue graphs have \(132\) edges;
that both are genuine, \(11\)-regular, vertex-transitive \((4,5,24)\)-graphs
with automorphism groups of orders \(24\) and \(48\).

**Cited, not proved:** \(R(4,5) = 25\), which fixes the window — though it is
now formally proved in HOL4 (Gauthier–Brown, ITP 2024) — and McKay's
completeness claim for \(\mathcal{R}(4,5,24)\), on which the "exactly two"
depends. Note that Theorem 3.1 as *originally* proved did not rest on that
completeness claim; this is an independent route to the same conclusion, which
is the point.

**Not claimed:** anything about the rest of the \(R(5,5) \le 49\) proof, which
uses the \(m = 4\) case of Theorem 2.2 and a gluing computation I have not
checked.

## Reproduction

```bash
python3 mr49.py
```

Runs in seconds. `r45_24_e132.g6` is the two-graph filter output from
`r45_24.g6` (SHA-256
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`).
