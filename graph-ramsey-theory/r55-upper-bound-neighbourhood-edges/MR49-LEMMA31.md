# \(R(5,5) \le 49\): Lemma 3.1 and Theorem 3.1, certified

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-09.
Subject: McKay and Radziszowski, *Subgraph Counting Identities and Ramsey
Numbers*, **JCTB 69 (1997) 193–209**, §3.
Checker: `mr49.py`. Data: `e45.json`, `r45_24_e132.g6`.

## The headline: a 1995 search is now a filter, by a route the original proof could not take

The \(R(5,5) \le 49\) proof rests on two statements:

> **Lemma 3.1.** Let \(G\) be a \((5,5,49)\)-graph. Then for each vertex
> \(v\), \(G^+_v\) and \(\overline{G^-_v}\) are \((4,5,24,132)\)-graphs,
> regular of degree \(11\).
>
> **Theorem 3.1.** The only two \((4,5,24,132)\)-graphs are \(H_1\) and
> \(H_2\).

**Theorem 3.1 cost a dedicated search in 1995 precisely because the catalogue
that would have made it a filter did not exist.** McKay and Radziszowski had
\(350\,904\) \((4,5,24)\)-graphs and knew the list was incomplete; the
complete count \(352\,366\) arrived twenty-one years later, with Angeltveit
and McKay (2016). So they proved "exactly two" by searching, without assuming
completeness.

That is what makes this worth doing rather than a reproduction. Filtering the
now-complete catalogue by \(e = 132\) gives exactly two graphs — the same
conclusion, reached by a route **whose trust boundary is different from the
original's**. Their proof avoids the completeness claim; mine depends on it and
avoids their search. Two independent derivations of a step that carries a
published Ramsey bound, and neither implies the other.

The general form of the question, since it is the thing that found this: *what
did the step need, and has a later catalogue, table or theorem since made that
input available?* Applied here, the answer was a catalogue completed in 2016.

## The second thing a reader should know: the step has zero slack

The lemma turns on

$$
\frac{12\,936}{49} = 264 = 2 \times 132 = 2 \times E(4,5,24),
$$

with each of the two terms bounded by \(E(4,5,24)\). The average lands
**exactly** on twice the maximum, so both terms are forced to the maximum at
every vertex — and there is not one edge of room. Had \(E(4,5,24)\) been
\(133\), the average would be \(264 < 266\) and **nothing would be forced;
the lemma would fail outright, and with it this route to
\(R(5,5) \le 49\).**

That is worth stating plainly because it settles a question about tables that
usually looks pedantic. A bound that is **loose by one on the upper side** is
not merely weaker here — it is *fatal*. Which is exactly the case flagged in
`POSITIVE-CONTROL.md`: researcher-1's double-counting gave
\(e(4,5,24) \le 133\), correct and sound, and it would have destroyed this
lemma. Getting \(132\) rather than \(133\) is the difference between a
theorem and no theorem, and it is the cleanest justification the verified-table
work in this directory will ever get.

## What is checked

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

**(4) The forcing.** \(12\,936 / 49 = 264\), each term at most
\(E(4,5,24) = 132\), and \(264 = 2 \times 132\), so **both are exactly
\(132\) at every vertex.** See the zero-slack discussion above: this is the
load-bearing step and it has no margin at all.

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
