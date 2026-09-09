# Albertson at \(r=29\): what was tried, what it gave, and where it stops

This is the method inventory for the \(r=29\) lane. It is a **stopping point, not
a proof**. `state29.py` recomputes the standing position end to end and asserts
every claim in it; this document records what was attempted around that position,
so that a successor does not repeat it.

## What is proved

| | |
|---|---|
| \(r\le26\) | literature — Albertson–Cranston–Fox (*EJC* **16** (2009) #R45) \(r\le12\); Barát–Tóth (*EJC* **17** (2010) #R73) \(r\le16\); Ackerman \(r\le18\); Cranston (arXiv:2512.08020) \(r\le24\); Sadhu (arXiv:2609.01682) Cor. 1.2 settles \(r\le26\) |
| \(r=27\) | mine, reviewed on the ledger |
| \(r=28\) | mine, reviewed on the ledger, independent of the \(r=27\) argument |
| \(r=29\) | **not proved** |

## Where \(r=29\) stands

Orders \(\le56\) impossible. **Order 57 closed** — all five rows
\((57,824)\ldots(57,828)\), re-verified under every subsequent repair. **Order 58
open**, in the single class \(b=6\), \(c=(51,1)\):

| | count |
|---|---|
| clique blocks | 8313 |
| one odd-cycle block | 15 |
| an isolated low vertex | 307 |
| **total** | **8635** |

## The method inventory

Each row is a method, what it was applied to, and the measured outcome.

| method | outcome |
|---|---|
| Deletion-recurrence gate (`recursive.py`, `crminus.py`) | reduces \(r=29\) to orders 57, 58; thresholds 829, 841. **Seed-independent**: \(g(58,f)=8210\) at every \(cr(K_{13})\) rung |
| Gallai low-vertex blocks + barrier classification | order 58 to one class, \(b=6\), \(c=(51,1)\) |
| Residue \(a_z\ge\mathrm{thr}_1-c_z\) (`residue57.py`, `residue58.py`) | **closes order 57**; at order 58 the budget is \(Sx\le X-25\in[27,31]\) against \(\le9\), and it does not reach |
| Block-plus-\(R\) near-complete bound (`blockr58.py`) | \(v\in Q\) has only \(q+\lvert R\rvert-29\) non-neighbours in \(R\); kills 172 |
| \(\alpha(G)\le3\) applied to the blocks (`alpha58.py`) | private vertices of distinct blocks are independent; **103292 → 9533**, the single largest reduction |
| Turán cap \(e(H[R])\le\lfloor\lvert R\rvert^2/3\rfloor\) (`turan58.py`) | removes 444 |
| Corrected singleton count (`dichot.singletons`) | closes 159; brings 3326 configurations to *one unit* short |
| Widened second side to \(L\setminus Q_1\) (`residue58.second_edges`) | \(\mu_2\) improves for 641 of 1843; closes **none** |
| Matroid intersection on the absorption step (`exhaust58.py`) | closes **1 of 1843**; inclusion–exclusion was never the bottleneck |
| Hall sharpening of \(s\) | **no change at all**, 8623 → 8623 |
| Splitting \(R\) between two blocks | **strictly worse**, by 700–1700; \(g\) grows superlinearly |
| Three-block near-clique decomposition | ~6354 against the two-way bound's 7510; **worse** |
| Degree-aware deletion averaging | **no change**; the sampling bound, not the averaging, is binding at \((58,m)\) |
| Stehlík's partition of \(H-x\) | yields only \(\lvert R\rvert\le61\), \(q_1\le28\); never binding |
| \(\theta(H)\ge\omega(G)\) | gives \(\omega(G)\le29\); never forces a \(K_{30}\) |
| \(L\)/\(R\) split scored by sampling | 6213–6550 against 8281; the block sum beats it twofold |

**Where the two obstructions stand** (`profile58.py`): the absorption shortfall
reaches **1**, with 3326 configurations within one unit; the crossing shortfall
reaches 5 but is long-tailed, most survivors sitting 3000–6000 short. All four
components of the absorption inequality are at their limit (`exhaust58.py`).

## The branch hypothesis is one condition of seventy

\(H\) is \(K_4\)-free, so \(\theta(H)\le28\) holds **iff** some vertex-disjoint
packing has \(2t_3+t_2\ge30\), \(3t_3+2t_2\le58\), \(t_3+t_2\le28\) — **seventy**
\((t_3,t_2)\) families. The branch hypothesis (TT) excludes \((2,26)\) and nothing
else (`routes58.py`).

The next family, \((3,24)\), is available on 6829 configurations, because three
or more Gallai blocks put a complete multipartite graph inside \(H[L]\). Of the
Tutte obstructions to it (`tutte324.py`):

- **isolate a part** — unreachable exactly when every block has order \(>c_w=4\);
  that holds on **2116** configurations and fails on 4713, because of connector
  blocks of order 2;
- **an \(R\)-set cut off from \(L'\)** — unreachable **everywhere**, since it
  would need \(Sx\ge29+\lvert Z\rvert-1\ge38\) against \(Sx\le31\).

## The precise open question

On the 2116 where both decidable families are unreachable, the remaining question
is whether **some other** Tutte set obstructs. It is not decided by
\((\lvert R\rvert,\text{multiset},e(H[R]))\): those fix \(H[L]\) completely
(complete multipartite on the blocks) and fix the *counts* of the \(L\)–\(R\) and
\(R\)–\(R\) edges, but not their **placement**.

Answering it means fixing a placement — building \(H\) — and computing
\(\nu(H-T_1-T_2-T_3)\) on 49 vertices. That needs general (non-bipartite) maximum
matching, which is **not available in this environment** (no `networkx`), so it
needs either a new dependency or a hand-written Blossom implementation. **That is
a decision for the principal, not for me**, which is why this lane stops here
rather than guessing.

## The defect record

Seven items of one family were found, all of the same shape — *a step verified on
the case that happens to be favourable, then generalised without re-deriving*:

| # | item | direction | effect |
|---|---|---|---|
| 1 | \(d_H(z)=28-x_z\) hardcoded at both orders | conservative | counts were over-counts |
| 2 | (C1)/(C2) applied where \(\delta_0\le0\) | excluded cases | 8568 → 47468 |
| 3 | (C3) in the enumeration filter | excluded cases | 479172 multisets |
| 4 | (C3) in the singleton count | **over-claimed** | 198 wrongly closed |
| 5 | \(k_{\mathrm{eff}}\) form with unbalanced blocks | **over-claimed** | latent; 0 wrongly closed |
| 6 | absorption into a triangle colour class | over-claimed | latent; 0 wrongly closed |
| 7 | Tutte obstruction checked only at \(Q_1\) | **over-claimed** | 6829 → 2116 |

Order 57 is unaffected by all seven: \(\delta_0\ge17\) there, and its enumeration
is identical under the audited filters.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 state29.py   | diff -u EXPECTED_OUTPUT_STATE29.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diff, `Controls: all PASS`, and OK for all 81 hashes. The full
per-file reproduction list is in `README.md`.

> **Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed;
> order 58 is open in 8635 configurations, with one named live route and a
> precisely stated question that this method cannot answer.
