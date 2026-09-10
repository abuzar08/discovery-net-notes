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
| clique blocks | 6019 |
| one odd-cycle block | 15 |
| an isolated low vertex | 307 |
| **total** | **6341** |

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
| **General Tutte obstruction count** (`tuttegen.py`) | **removes 2294** — and unlike every row above it quantifies over **all admissible \(H\)**, not over parameters |
| \(U\)-degree inequality (6) (`tuttegen.py`) | \(\sum_{z\in R}x_z=X\le56\) makes every \(U\)-vertex nearly of degree 29, while a \(U\)-vertex has no \(A\)-neighbour at all: **a large \(U\) cannot exist**. Worth **+117**, more than the two component-count refinements together. Found by pricing, not by guessing |
| Singleton refinement of \(c_A\) | if \(A\) is not inside one block and \(H[A]\) has two components, one is a **singleton**; \(c_A=2\) then needs an isolated \(A\)-vertex or \(p\ge2\). Worth **+12** |
| Odd-component parity in (1) | \(o\) counts odd components, and the two families have forced parities. **No change at all**: the adversary absorbs it by shifting \(u\) or \(t\) by one |
| \(\rho\)-sum bound on \(e(L\setminus A,U)\), **loose form** | choosing the \(\lvert L\rvert-a\) most expensive slots freely: valid, but **never binds**, 0 change |
| \(\rho\)-sum bound, **exact form** | the same idea taken from the lane's own identity, \(e(L,R)=29\lvert R\rvert-X-2e(H[R])\), so \(e(L\setminus A,U)\le e(L,R)-\sum_i a_i\rho_i\). Combined with charging \(w\) only \(d_H(w)\le4\) inside \(U\): **336 → 1343**. Neither half alone changes the count by one |
| \(c_A\le a\) | every component meeting \(A\) holds a vertex of \(A\). **No change alone** |
| Singleton reach for \(c_A=2\) | the singleton is a \(G\)-neighbour of every other \(A\)-vertex in \(L\), so \(a-1\le D_v\le28\): a bounded knapsack over block sizes. **+11** |
| Singleton reach, **with the fit condition** | \(A\) must also *fit* inside \(v\)'s blocks: a block \(Q_j\) not containing \(v\) keeps \(\ge q_j-\mathrm{extra}\) private vertices of which only \(\mathrm{rem}_j\) are deleted with the triangles, so \(s_L\ge\sum_{j\notin B}\max(0,q_j-\mathrm{extra}-\mathrm{rem}_j)\). Without it the knapsack lets \(v\) reach blocks it cannot cover |
| \(\min(\rho_v,u)\) cap on the \(L\)-budget | an \(L\setminus A\) vertex sends at most \(\min(\rho_v,u)\) edges into \(U\), not \(\rho_v\). In case B the \(q_A-a\) leftover block-mates each lose \(\max(0,\rho_A-u)\); when the blocks partition \(L\) the whole sum is exact block by block. Together with the fit condition: **1343 → 2294** |
| Witness mode in the scan | the surviving points are now collected by `obstructed` itself. A previous pass kept a second copy of the enumeration for this, it drifted out of step with `_ok`, and two runs were wasted on the stale copy |
| Disjoint-neighbourhood inequality (7) | \((c_A-\mathrm{iso})\max(0,\rho_A-s_R)\le\lvert W\rvert\). **0 closures alone**, but it changes the surviving shape, and the shape it exposes is what the exact \(\rho\)-sum bound then kills |
| **Priced sensitivity table** (`slack58.py`) | how strong a sharpening must be. Its rows **move as the other inequalities move**, so it is only ever a statement about the current set; `slack58.py` therefore derives its conclusions from the measured rows rather than asserting them |

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
whose \(R\)-neighbours all lie in \(S_R\) — and seven inequalities hold for
**every** admissible \(H\):

1. **count**, \(c_A^{\mathrm{odd}}+t^{\mathrm{odd}}\ge s_L+s_R+D\);
2. **degree**, \(\sum_i a_i\rho_i+e(H[R])-\mathrm{tur}(u-t+1)\le 28(\lvert R\rvert-u)\);
3. **Turán**, \(e(H[R])\le\binom{\lvert R\rvert}{2}-\binom{\lvert R\rvert-s_R}{2}+\mathrm{tur}\bigl((\lvert R\rvert-s_R)-(t+p)+1\bigr)\);
4. **spread**, \(\sum_i a_i\rho_i\le a(\lvert R\rvert-u)\);
5. **\(S_R\)-degree**, \(\max\bigl(0,\sum_i a_i\rho_i-(a-\mathrm{iso})\lvert W\rvert\bigr)+e(H[R])-\mathrm{tur}(\lvert W\rvert-p+1)-\mathrm{tur}(u-t+1)\le 28s_R\);
6. **\(U\)-degree**, with \(u'=u-[\,w\in U\,]\),
   \[28u+\lvert R\rvert-X+24\,[\,w\notin U\,]\ \le\ \min\bigl(u'(s_L+3k),\ e(L,R)-\textstyle\sum_i a_i\rho_i\bigr)+u's_R+2\,\mathrm{tur}(u-t+1)+4\,[\,w\in U\,];\]
7. **disjoint neighbourhoods**, \((c_A-\mathrm{iso})\max(0,\rho_A-s_R)\le\lvert W\rvert\).

Inequality 5 bites because isolating many vertices of \(A\) drives their whole
\(R\)-neighbourhood into \(S_R\), and \(S_R\) must then also carry nearly every
edge of \(H[R]\), which its degree cap forbids. **Inequality 6 is the strongest
of the six**: since \(x_z\ge1\) for every \(z\in R\) and
\(\sum_{z\in R}x_z=X=2m-1624\le56\), the vertices of \(U\) each carry nearly the
full degree 29 — but a vertex of \(U\) has **no neighbour in \(A\) at all**, so its
\(L\)-neighbours lie in \(S_L\) or among the \(3k\) deleted triangle vertices and
its \(H[R]\)-neighbours in its own component or \(S_R\). A large \(U\) cannot
exist: its vertices are too high-degree to be cut off. Since \(x_w\ge25\), any
degree cap over a set containing \(w\) is 24 smaller, and the adversary's best
placement of \(w\) is scanned in 2, 5 and 6 alike.

These are **necessary** conditions, so an infeasible scan is a proof and a
feasible scan proves nothing. That direction is the whole risk, so it is
measured, not trusted: the explicit admissible \(H\) of `adv58.py` has its
Gallai–Edmonds set read off and checked against all five, and a negative control
re-runs the scan at \(D=1\), where an obstruction provably exists because
\(n'=49\) is odd — a scan reporting infeasible there would prove an inequality
false.

**Result: 1343 configurations closed for every admissible \(H\)** — 903 at
\(k=3\) and 440 at \(k=4\) — so order 58 falls from 8635 to **7292**. Of the
6970 remaining, 2369 admit a parameter point the counts cannot rule out — which is not the same as an obstruction existing —
and 4601 are ones for which **three disjoint triangles are not guaranteed**.

**A correction to the previous pass.** That count was published as "4601 have no
three disjoint triangles at all". That overstates it. The test is a *sufficient*
condition — private vertices of three distinct blocks always form a triangle,
and at most \(\mathrm{extra}=\sum_iq_i-\lvert L\rvert\) vertices of any block
fail to be private — so its failure means *not guaranteed for every block
forest*, not *non-existent*. For two large blocks joined by a bridge \(H[L]\)
genuinely is triangle-free, which is where the wrong generalisation came from.
The closure count is unaffected either way, since the test is only ever used to
decide whether a route is available; only the description of the residual was
wrong. Recorded as defect 12.

## How strong would a sharpening have to be? (`slack58.py`)

Rather than guess which inequality to sharpen, each one is **priced**: subtract
\(d\) from its right-hand side unconditionally, re-run the whole closure scan,
and count what falls.

| handicap | \(d=1\) | \(d=5\) | \(d=25\) | \(d=50\) |
|---|---|---|---|---|
| (1) count | **3712** | 3712 | 3712 | 3712 |
| (2) degree | 2294 | 2294 | 2323 | 2720 |
| (3) Turán | 2299 | 2324 | 2538 | 2689 |
| (4) spread | **2937** | 2937 | 2937 | 2937 |
| (5) \(S_R\)-degree | 2299 | 2324 | 2588 | 3259 |

Baseline 2294; the route reaches 3712 configurations in all. **One unit off the
count inequality still closes every one of them**, and the precise target remains
a theorem \(o(H'-S)\le c_A+t-1\) holding unconditionally.

**The table moves when the inequalities move, and this is worth stating.** On the six-inequality scan two passes ago the spread inequality was *inert at
every handicap*; it is now worth **+643** at one unit, having been **+1528** one
pass ago — the same row, three different verdicts, purely because the rest of
the set moved. A pricing table is only
ever a statement about the current set, so `slack58.py` now derives its
conclusions from the measured rows instead of asserting them in prose — the
prose form went stale the moment the inequalities changed underneath it, which is
the same shape as defects 13 and 14.

## The two halves of inequality 6, and a lesson about non-binding bounds

Inequality 6 as first published charged every vertex of \(U\) a full degree 28
and bounded the \(L\)-side by \(u(s_L+3k)\). Both are loose:

- \(w\) lies in \(U\) in the surviving configurations, and \(d_H(w)\le4\), so it
  must be charged 4 and not 28;
- every \(A\)–\(R\) edge lands outside \(U\), so
  \(e(L\setminus A,U)\le e(L,R)-e(A,R)\), and \(e(L,R)\) is **exact** from the
  lane's own identity \(e(L,R)=\sum_{z\in R}d_H(z)-2e(H[R])=29\lvert R\rvert-X-2e(H[R])\).

Applied separately, **neither changes the closure count by a single
configuration**. Applied together they take it from 336 to **1343**.

That is a correction to a published methodological claim. A loose form of the
\(\rho\)-sum bound — choosing the \(\lvert L\rvert-a\) most expensive slots
freely, rather than reading \(e(L,R)\) off the identity — was implemented last
pass, measured, found never to bind, and removed with the note "0 change at three
times the runtime". That measurement was true of what was implemented, and the
inference drawn from it, that the idea was worthless, was wrong twice over: the
bound was in its loose form, and it was being asked to work alone. **Measuring a
weak form of a constraint and concluding the constraint does not matter is a
trap**, and it is the same shape as defect 13. Recorded as defect 14.

The identity itself is checked independently rather than trusted: at
\(\lvert R\rvert=24\), blocks \((17,12,5)\), \(e(H[R])=178\) it gives
\(e(L,R)=288\), which is exactly the \(L\)–\(R\) edge count of the explicitly
constructed admissible \(H\) in `adv58.py`.

**A framing that was wrong, and is withdrawn.** The first version of this
measurement reported, for each surviving parameter point, the slack
\(\mathrm{RHS}_j-\mathrm{LHS}_j\), and found it identically zero for
inequality 1. That is an artefact: the scan hands the adversary \(t\) at the
minimum inequality 1 allows, so 1 is met with equality *by construction*, and a
slack of zero there measures the search order rather than the mathematics. Two
genuine strengthenings of the component count were implemented on the strength
of that reading — the singleton refinement of \(c_A\) and the odd-component
parity — and they moved the closure count by **12 and 0**. The handicap table
above is the honest form of the question, and it is what located inequality 6,
worth **+117**.

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

Fourteen items were found, eleven of one family, all of the same shape — *a step verified on
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
| 12 | "4601 have no three disjoint triangles at all" | **published overstatement** | corrected above; a sufficient test read as a census. Counts unaffected |
| 13 | slack-at-surviving-points as a sharpening guide | mis-framed a measurement | withdrawn; cost two refinements worth 12 and 0 |
| 14 | "the \(\rho\)-sum bound never binds" | **published, misleading** | true of the loose form measured alone; the exact form, paired with the \(w\) charge, is worth 336 → 1343 |

Order 57 is unaffected by all ten: \(\delta_0\ge17\) there, and its enumeration
is identical under the audited filters.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 state29.py   | diff -u EXPECTED_OUTPUT_STATE29.txt -
shasum -a 256 -c SHA256SUMS
```

plus `tuttegen.py`, `blockcut.py` and `slack58.py` against their own expected
outputs.

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
> to widen it. The sensitivity table above says where: **not** in the edge
> counts, which are inert or need improvements of 50, but in the component
> bound, where a single unconditional unit closes every configuration the route
> reaches. Separately, 4601 survivors have no *guaranteed* three disjoint
> triangles and need either a sharper triangle-packing guarantee or a different
> family of the seventy.
