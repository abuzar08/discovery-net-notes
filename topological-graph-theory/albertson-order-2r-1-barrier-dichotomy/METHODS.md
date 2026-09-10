# Albertson at \(r=29\): what was tried, what it gave, and where it stops

This is the method inventory for the \(r=29\) lane. It is **not a proof**, and it
is no longer a stopping point — see the closing note. `state29.py` recomputes the standing position end to end and asserts
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
| clique blocks | 8117 |
| one odd-cycle block | 15 |
| an isolated low vertex | 307 |
| **total** | **8439** |

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
| **\(w\)-sharpened Turán cap** \(e(H[R])\le\lfloor(\lvert R\rvert-1)^2/3\rfloor+4\) (`wturan58.py`) | removes **310**; found by failing to build an adversary |
| Triangle-free-neighbourhood cap on \(e(H[R])\) | valid — \(N_H(v)\cap R\) must be triangle-free or \(v\) closes a \(K_4\) — but **non-binding**: removes 0. Reviewer-1 (`reviews/albertson-triangle-free-neighbourhood/`) confirms the derivation and the zero-removal on the whole survivor set, and records that this cap and the \(w\)-sharpened cap are **incomparable**: apply \(\min\) of the two, never one in place of the other |
| Block-forest lemma for \(c_A\) (`blockcut.py`) | three low vertices that pairwise share a block share a **common** block, since the block-cut tree is acyclic and two blocks meet in at most one vertex. Hence \(A\) not inside one block \(\Rightarrow\) \(H[A]\) has at most two components. Checked on 6768 Gallai forests and 719597 subsets |
| **General Tutte obstruction count** (`tuttegen.py`) | **removes 196** — and unlike every row above it quantifies over **all admissible \(H\)**, not over parameters |

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

## From "some other Tutte set" to every Tutte set

The question left by `tutte324.py` was whether **some other** Tutte set — outside
the two hand-picked families — obstructs. That question is now answered by a
count rather than by sampling placements, in `tuttegen.py`.

Generalise the family from \((3,24)\) to \((k,30-2k)\): removing \(k\) disjoint
triangles of \(H\) leaves \(n'=58-3k\) vertices needing a matching of \(30-2k\),
i.e. Tutte–Berge deficiency at most \(k-2\). The deficiency has the parity of
\(n'\), which is the parity of \(k\), so an obstruction needs a Tutte set of
deficiency exactly \(D=k\) or more — **a larger \(k\) asks the adversary for
more**, at the cost of deleting more of \(L\).

Now parameterise an arbitrary Tutte set \(S\) by six integers — \(a=\lvert
L'\setminus S\rvert\), \(s_R\), the size \(u\) and number \(t\) of the components
of \(H'-S\) missing \(A\), the number \(p\) of components of \(H[W]\) on the
remaining high vertices, and the number \(\mathrm{iso}\) of vertices of \(A\)
whose \(R\)-neighbours all lie in \(S_R\) — and five inequalities hold for
**every** admissible \(H\):

1. **count**, \(c_A+t\ge s_L+s_R+D\);
2. **degree**, \(\sum_i a_i\rho_i+e(H[R])-\mathrm{tur}(u-t+1)\le 28(\lvert R\rvert-u)\);
3. **Turán**, \(e(H[R])\le\binom{\lvert R\rvert}{2}-\binom{\lvert R\rvert-s_R}{2}+\mathrm{tur}\bigl((\lvert R\rvert-s_R)-(t+p)+1\bigr)\);
4. **spread**, \(\sum_i a_i\rho_i\le a(\lvert R\rvert-u)\);
5. **\(S_R\)-degree**, \(\max\bigl(0,\sum_i a_i\rho_i-(a-\mathrm{iso})\lvert W\rvert\bigr)+e(H[R])-\mathrm{tur}(\lvert W\rvert-p+1)-\mathrm{tur}(u-t+1)\le 28s_R\).

Inequality 5 is the one that bites: isolating many vertices of \(A\) drives their
whole \(R\)-neighbourhood into \(S_R\), and \(S_R\) must then also carry nearly
every edge of \(H[R]\), which its degree cap forbids. Since \(x_w\ge25\), any
degree cap over a set containing \(w\) is 24 smaller, and the adversary's best
placement of \(w\) is scanned.

These are **necessary** conditions, so an infeasible scan is a proof and a
feasible scan proves nothing. That direction is the whole risk, so it is
measured, not trusted: the explicit admissible \(H\) of `adv58.py` has its
Gallai–Edmonds set read off and checked against all five, and a negative control
re-runs the scan at \(D=1\), where an obstruction provably exists because
\(n'=49\) is odd — a scan reporting infeasible there would prove an inequality
false.

**Result: 196 configurations closed for every admissible \(H\)** (193 at
\(k=3\), 3 at \(k=4\)), so order 58 falls from 8635 to 8439. Of the 8117
remaining, 4601 have no three disjoint triangles at all and 3516 admit a
parameter point the counts cannot rule out — which is not the same as an
obstruction existing.

**An earlier version of this document said this needed a new dependency and put
the choice to the principal. That was wrong, and is withdrawn.** Writing a
matching routine is not adding a dependency; `matching.py` provides one, standard
library only, verified against brute force, and both of its answers are
self-certifying — \(\nu\ge k\) by exhibiting \(k\) disjoint edges, \(\nu\le k\)
by a Tutte set. The lane did not need to stop there.

**Constructing has been more productive here than arguing** — every defect below
was found by re-deriving an argument, three of them only after publication,
whereas the \(w\)-sharpened cap, the three cross conditions for \(K_4\)-freeness,
and the errors caught in passes 42–45 all came from a computation disagreeing
with an expectation. The count above is the pay-off: it was reachable only after
building an explicit \(H\) showed what an admissible one has to satisfy.

## The defect record

Eleven items of one family were found, all of the same shape — *a step verified on
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
| 8 | Tutte family C omitted the \(H[R]\)-neighbourhood cost | mis-stated | caught by computation, unpublished |
| 9 | first adversarial \(H\) violated \(d_H(z)\le28\) | inadmissible | caught by computation, unpublished |
| 10 | "needs a dependency" framing of the matching question | mis-framed a decision | withdrawn above |
| 11 | first `tuttegen.py` used \(c_A=1\) where blocks overlap | **would have over-claimed** | caught pre-publication; 6536 of 8313 configurations affected |

Order 57 is unaffected by all ten: \(\delta_0\ge17\) there, and its enumeration
is identical under the audited filters.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 state29.py   | diff -u EXPECTED_OUTPUT_STATE29.txt -
shasum -a 256 -c SHA256SUMS
```

plus `tuttegen.py` and `blockcut.py` against their own expected outputs.

Expected: empty diff, `Controls: all PASS`, `Soundness controls: real Tutte set
PASS; D = 1 negative control PASS`, `VERDICT: all PASS` for the block-forest
lemma, and OK for every hash. The full per-file reproduction list is in
`README.md`.

> **Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed;
> order 58 is open in 8635 configurations, with one named live route and a
> precisely stated question.
>
> This was written as a stopping point and should no longer be read as one. The
> \((k,30-2k)\) routes now have a decision procedure that quantifies over every
> admissible \(H\), and it closes 196 configurations. The concrete next step is
> to widen it: 4601 of the survivors have no three disjoint triangles at all and
> need a different family of the seventy, and on the 3516 the counts do not
> decide the question is which of the five inequalities is slack.
