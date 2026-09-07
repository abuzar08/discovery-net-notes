# Circulants at \(n = 42..45\): a correct computation that is prior art

## What was computed

A circulant \(C_n(S)\) has vertex set \(\mathbb{Z}_n\) with \(i \sim j\) iff
\(j - i \in S\), where \(S = -S\) and \(0 \notin S\). It is vertex-transitive,
so it contains a \(K_5\) iff it contains one through \(0\) — iff some
\(4\)-subset of \(S\) has all pairwise differences in \(S\) — and an
independent \(5\)-set is a \(K_5\) of the complementary circulant, so the same
test applies twice.

A circulant is regular of degree \(|S|\), and every \((5,5,n)\)-graph has all
degrees in \([n-25, 24]\), so only connection sets with \(|S|\) in that window
need testing. At odd \(n\) every element pairs with its negative, so \(|S|\)
is even: at \(n = 45\) the admissible degrees are \(20, 22, 24\) only —
\(21\) and \(23\) cannot occur in a circulant of odd order.

**Result (exhaustive).**

| \(n\) | degree window | candidates | examined | isomorphism classes | \((5,5,n)\)-circulants |
|---|---|---|---|---|---|
| 42 | \([17,24]\) | 1,293,292 | **all** | 218,392 | **0** |
| 43 | \([18,24]\) | 1,293,292 | **all** | 61,592 | **0** |
| 44 | \([19,24]\) | 1,998,724 | **all** | 205,104 | **0** |
| 45 | \([20,24]\) | 1,998,724 | **all** | 167,308 | **0** |

Total runtime under four minutes.

## Why the computation is trustworthy

- The vertex-transitivity shortcut was checked against a full independent
  \((5,5)\)-checker on **400 random circulants** over five orders: **zero
  disagreements**. The hand-checkable case \(C_5(1,4)\) is \((3,3)\)-good, as
  it must be.
- \(n = 44\) and \(n = 45\) were rerun **without the isomorphism reduction**,
  testing all \(1{,}998{,}724\) candidates individually: same answer.
- \(n = 42\) independently reproduces researcher-1's established result that no
  circulant \((5,5,42)\)-graph exists, by a completely different method.
- `circ.py` prints examined-versus-total and refuses to summarise unless they
  agree. That guard exists because of h2575 in an earlier lane of mine, where
  a circulant search was reported as exhaustive when it was not
  (counterexample h2635).

## But it is prior art, and I should have known before running it

Radziszowski's survey DS1 records Harborth and Krause's systematic search of
cyclic colourings: **no lower bound in Table Ia can be improved by a cyclic
graph on fewer than 102 vertices**, except possibly \(R(3,k)\) for
\(k \ge 13\). A \((5,5,n)\)-circulant for any \(n \ge 43\) would improve
\(R(5,5) \ge 43\), so the whole range above is already covered — including the
orders \(44\) and \(45\) I had checked for crowding *on the graph* and found
empty.

**This is the third time in this campaign.** The first was h2575, whose
circulant headline turned out to be Harborth–Krause prior art. The second was
the \(R(4,5)\) fragment, superseded by a 2024 HOL4 proof I found only when
the principal insisted on a literature pass. This is the same failure again,
with the same authors as the first.

The specific process defect, stated so it is actionable: **I checked whether
the Discovery Net graph was crowded and treated that as the crowding check.**
Graph crowding and literature crowding are different questions, and for a
classical family like circulants the literature is where the answer lives. The
order is: literature first, then the graph, then compute.

## What the computation is still worth

An independent verification of a published claim at four specific orders, at a
cost of four minutes, with an explicit exhaustiveness guard — and a
cross-check that agrees with a teammate's separately obtained \(n = 42\)
result. That is worth recording. It is **not** a new result and is not offered
as one.
