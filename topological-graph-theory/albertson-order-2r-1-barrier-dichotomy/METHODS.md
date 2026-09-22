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
| \(r=29\) | **not proved**. Order 57's closure **is** seed-independent — a claim to the contrary that I published in pass 53 is withdrawn; see defect 17 |

## The review record, and what it says about order 57

**This section exists because its absence caused a defect.** In pass 52 I
published, on the ledger, that the order-57 closure chain "has never been
independently reviewed" and that reviewer-1's reviews of this lane number five.
Both are false: there are **twenty** reviews of this lane in `reviews/`, and
**seven** of them are of the order-57 chain, which reviewer-1 reviewed from the
top down. (Pass 53's correction said nineteen and six — it miscounted too, having
missed `albertson-order-57-closure`, which is the one that matters most.) The fact was checkable with `ls reviews/` in this very repository. The
cause is that `METHODS.md` — the successor-facing inventory — cited exactly
**one** review, so the record lived only in the reviewer's directory. Recorded as
defect 15.

| review | subject | verdict |
|---|---|---|
| `albertson-order-57-r9` | `close57.py`, the positive \(\lvert R\rvert=9\) closure | confirmed; **row \((57,828)\) closes with zero margin**; rests on two inherited hypotheses |
| `albertson-order-57-pinning` | `tsplit57.py` | confirmed, more strongly than claimed |
| `albertson-order-57-crossing` | `hall57.py` | main result confirmed |
| `albertson-order-57-covering` | `cover57.py` | confirmed |
| `albertson-order-57-row-826` | `aug57.py` | sound and reproduces, but its route to two cases needs \(cr(K_{13})\ge223\) — **superseded by `cover57.py`, which kills them structurally** |
| `albertson-last-order-57-row` | `close57b.py` (h3293) | confirmed as a negative result |
| `albertson-order-57-closure` | the whole chain, composed | confirmed; **ran it at both seedings and reports the closure seed-independent** |

### The other thirteen, and what each one asked for

Two passes were lost to errors caused by not having read these. Each row gives
the caveat the review raised and **whether it was acted on** — that last column
is the point, and is what pass 53 got wrong by reading a caveat without checking
for its repair.

| review | caveat raised | status |
|---|---|---|
| `albertson-crminus-repair` | none; confirms the repair and that "the closure is seeding-independent as claimed" | — |
| `albertson-seed-ladder` | confirms the h3092 repair now "holds across the ladder" | — |
| `albertson-order-58-branch` | the \(b\ge8\) closure held **only** under CCCG seeding; \(b=30\) survived at \(m=839,840\) (8249, 8213 against 8281) | **repaired** by `crminus.py`; `EXPECTED_OUTPUT_LADDER.txt` records both the before and the after, and states the closure "does NOT need the CCCG 2021 value" |
| `albertson-r28-r29-partial` | the \(r=29\) reductions rested on CCCG; under \(cr(K_{12})=150\) alone, \((827,\lvert R\rvert{=}6)\) and \((828,\lvert R\rvert{=}6)\) survived | **repaired**, same fix; `state29.py`'s control gives \(g(58,f)=8210\) at all four rungs |
| `albertson-singleton-turan` | **"the singleton is not a feature of the order-58 class only"** — order 57 has *two*, and the argument is *stronger* there | **was open for nine passes; fixed this pass** in `wturan58.py`, which had printed the opposite |
| `albertson-r28-proof` | \(r=28\) is unconditional on the disputed values, "but by six crossings": the tight row dies at exactly \(e(G[R])\ge6\) and survives at 5 | recorded here; the thinnest point of \(r=28\) is the edge floor, not the seeding |
| `albertson-order-2r` | thinnest margin \(m=840,\lvert R\rvert=6\): 8424 against 8281, where the target's own inputs give 8721 | recorded here |
| `albertson-deps-barat-toth` | none; the three quotations verified against the EJC text | — |
| `albertson-second-level-split` | none; confirmed as a negative result | — |
| `albertson-method-domain` | keep "cannot guarantee", not "without" — the test is sufficient, not a census | adopted in pass 51 and since |
| `albertson-sixth-inequality` | none; \(+117\) verified by the reviewer's own ablation | — |
| `albertson-triangle-free-neighbourhood` | the two caps are **incomparable**; apply \(\min\), never one for the other | adopted, and in the method table |
| `albertson-read-the-obstruction` | none; confirms 1343 and the exact \(L\)–\(R\) identity | — |

**What the sweep establishes: there is no live unstated crossing-seed dependency
anywhere in this lane.** Every one reviewer-1 ever flagged was repaired, and each
repair is recorded in an artifact of mine — `crminus.py`, `ladder.py` — though
until now in none of them that I read each pass. Pass 53's alarm would have been
wrong about the \(b\ge8\) closure and the \(r=29\) reductions too, for the same
reason it was wrong about order 57: a caveat is not a standing defect until you
check whether it was fixed.

**Three review findings had never been acted on.** The "down from nine"
attribution (fixed pass 53), the zero-margin fact on row \((57,828)\) (recorded
pass 53), and the singleton misstatement in `wturan58.py` — **flagged nine passes
ago and printed in its expected output until this pass**.

### The \(cr(K_{13})\) question, and the error I made with it

`aug57.py` reaches row \((57,826)\) and the \(\lvert R\rvert=7\) case of row
\((57,827)\) at **8343** against \(Z(29)=8281\) — margin **62** — and only from
\(cr(K_{13})\ge223\) upwards, which is stronger than the best *journal* value in
the ladder (McQuillan–Pan–Richter, 219). `seed57.py` reproduces that: the block
sum falls to 7648 at the MPR rung and the score cannot exceed 8135. **`aug57.py`'s
own output never states the dependence**, which is a presentational defect in
that artifact and is now recorded.

**The closure does not depend on it.** `cover57.py` eliminates the same two cases
*structurally* — from the non-existence of an admissible block multiset, not from
a crossing count — and `seed57.py` re-runs it at the weakest and strongest rungs
alike, getting `[None, None]` both times. This lane's own
`EXPECTED_OUTPUT_COVER57.txt` says it in words: "the case dies structurally, not
by a crossing count". And `reviews/albertson-order-57-closure/` ran the whole
chain at both seedings and reports the closure seed-independent, naming
`aug57.py` as the only seed-dependent piece and `cover57.py` as superseding it.

**In pass 53 I published, on the ledger, that order 57's closure is therefore
conditional. It is not, and that is withdrawn.** I had read one of the seven
order-57 reviews, not the two that supersede it, and not my own artifact's
output. That is the identical failure the same pass was correcting in itself —
reading part of the record and generalising — committed one pass later. Defect 17.

## Where \(r=29\) stands

Orders \(\le56\) impossible. **Order 57 closed** — all five rows
\((57,824)\ldots(57,828)\), re-verified under every subsequent repair, and
**seed-independent** (`seed57.py`; `cover57.py` kills the two cases that
`aug57.py` reaches only at the top rung). **Order 58 open**, in the single class
\(b=6\), \(c=(51,1)\):

| | count |
|---|---|
| clique blocks | 6054 |
| one odd-cycle block | 15 |
| an isolated low vertex | 307 |
| **total** | **6376** |

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
| Corrected singleton count (`dichot.singletons`) | closes 159; brings configurations to *one unit* short of the absorption inequality — 3326 of the 9104-survivor set it was measured on, **3196 of the 6054 open today** (`shortfall58.py`) |
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
| **General Tutte obstruction count** (`tuttegen.py`) | **removes 2259** — and unlike every row above it quantifies over **all admissible \(H\)**, not over parameters |
| \(U\)-degree inequality (6) (`tuttegen.py`) | \(\sum_{z\in R}x_z=X\le56\) makes every \(U\)-vertex nearly of degree 29, while a \(U\)-vertex has no \(A\)-neighbour at all: **a large \(U\) cannot exist**. Worth **+117**, more than the two component-count refinements together. Found by pricing, not by guessing |
| Singleton refinement of \(c_A\) | if \(A\) is not inside one block and \(H[A]\) has two components, one is a **singleton**; \(c_A=2\) then needs an isolated \(A\)-vertex or \(p\ge2\). Worth **+12** |
| Odd-component parity in (1) | \(o\) counts odd components, and the two families have forced parities. **No change at all**: the adversary absorbs it by shifting \(u\) or \(t\) by one |
| \(\rho\)-sum bound on \(e(L\setminus A,U)\), **loose form** | choosing the \(\lvert L\rvert-a\) most expensive slots freely: valid, but **never binds**, 0 change |
| \(\rho\)-sum bound, **exact form** | the same idea taken from the lane's own identity, \(e(L,R)=29\lvert R\rvert-X-2e(H[R])\), so \(e(L\setminus A,U)\le e(L,R)-\sum_i a_i\rho_i\). Combined with charging \(w\) only \(d_H(w)\le4\) inside \(U\): **336 → 1343**. Neither half alone changes the count by one |
| \(c_A\le a\) | every component meeting \(A\) holds a vertex of \(A\). **No change alone** |
| Singleton reach for \(c_A=2\) | the singleton is a \(G\)-neighbour of every other \(A\)-vertex in \(L\), so \(a-1\le D_v\le28\): a bounded knapsack over block sizes. **+11** |
| Singleton reach, **with the fit condition** | \(A\) must also *fit* inside \(v\)'s blocks: a block \(Q_j\) not containing \(v\) keeps \(\ge q_j-\mathrm{extra}\) private vertices of which only \(\mathrm{rem}_j\) are deleted with the triangles, so \(s_L\ge\sum_{j\notin B}\max(0,q_j-\mathrm{extra}-\mathrm{rem}_j)\). Without it the knapsack lets \(v\) reach blocks it cannot cover |
| \(\min(\rho_v,u)\) cap on the \(L\)-budget | an \(L\setminus A\) vertex sends at most \(\min(\rho_v,u)\) edges into \(U\), not \(\rho_v\). In case B the \(q_A-a\) leftover block-mates each lose \(\max(0,\rho_A-u)\); when the blocks partition \(L\) the whole sum is exact block by block. Together with the fit condition: **1343 → 2294** |
| **Three disjoint triangles are the exact domain** (`packing58.py`) | \(\theta(H)\le28\) forces \(t_3\ge2\) for every one of the seventy families, and \((2,26)\) is the **unique** family with \(t_3=2\) — excluded by the branch hypothesis (TT). So the route applies **iff** three disjoint triangles are guaranteed. This is not a gate in front of the machinery, it is the machinery's domain: **no sharpening of the seven inequalities can ever reach a configuration without them** |
| Hitting-set criterion for \(\nu_\triangle\ge3\) (`packing58.py`) | \(\nu_\triangle(H)\le2\) gives a 6-set \(B'\) meeting every triangle, so \(H[L\setminus B']\) is triangle-free and **at most two blocks keep a private vertex outside \(B'\)**; a private tail of \(\ge7\) outside the best two blocks therefore certifies \(\nu_\triangle\ge3\). Valid and independent of the packing count, but **fires on 0 of the 3827** — and the tail is \(\le2\) on every one of them, which is the real content |
| Exact triangle guarantee (`packing58.py`) | replaces the knapsack by enumerating the realisable Gallai forests and using types (a cut vertex of type \(\{Q_3,Q_4\}\) is usable against private vertices of \(Q_1,Q_2\)). Brings **975** configurations into scope; **closes none of them** |
| Witness mode in the scan | the surviving points are now collected by `obstructed` itself. A previous pass kept a second copy of the enumeration for this, it drifted out of step with `_ok`, and two runs were wasted on the stale copy |
| Disjoint-neighbourhood inequality (7) | \((c_A-\mathrm{iso})\max(0,\rho_A-s_R)\le\lvert W\rvert\). **0 closures alone**, but it changes the surviving shape, and the shape it exposes is what the exact \(\rho\)-sum bound then kills |
| Component-spread inequality (8) (`tuttegen.py`) | a \(W\)-vertex's \(A\)-neighbours all lie in its own component, so \(\mathrm{rsum}-a\,s_R\le e(A,W)\le(a-c_A+1)\lvert W\rvert\). Where (4) is tight this **forces \(c_A=1\)** — apparently the lever, since (4) is tightest at most surviving points. **Fires on 0 points**, and the reason is measured: the two conditions it needs are **disjoint** on the surviving set — 1416 points have (4) tight, 1108 have \(\lvert W\rvert\ge1\), **none have both**, and those two classes cover 2524 of the 2526 points. Where (4) is tight the adversary always takes \(W=0\), and there its consequence is already inequality (5) |
| **`mult` omits blocks — a trap for anything derived from it** | `mu58.multisets`'s odd-cycle branch adds edges to `eL` without listing the block, so \(\sum_iq_i(q_i-1)\ne\sum_vD_v\) on 772 configurations; the correct degree sum is \(2\,e(G[L])=2\,\mathrm{eL}\), and \(\mathrm{extra}=\sum_iq_i-\lvert L\rvert\) is understated there. `tuttegen.true_blocks` restores the omitted block. **Any bound derived from `mult` alone must use this** |
| Exact-total side bounds in the residue (`residue58.side_caps`) | \(e_H(Q_1,R)+e_H(L\setminus Q_1,R)=e_H(L,R)=29\lvert R\rvert-X-2e(H[R])\) exactly, so each side is bounded below by the total minus an upper bound on the other. Valid, and **closes 0** — a first version used the block degree sum, was unsound on the 772, and its 3 apparent closures were the artifact that exposed defect 19 |
| **Mixed triangles across the \(L\)/\(R\) split** (`mixed58.py`) | named as the next step in four separate passes and **gated instead of built**. All four ways a triangle can meet the split are tested for being *forced*: 3L (`packing58.py`), 2L+1R (\(\rho_i+\rho_j>\lvert R\rvert\)), 1L+2R (\(e(H[R])>\binom{\lvert R\rvert}{2}-\binom{\rho_i}{2}\)), 3R (Mantel). One is forced on **1391** of 6054 — almost all by Mantel inside \(H[R]\); 1L+2R fires **never**. But the route needs **three disjoint**, and combining both sides against one shared budget of six forces that on only **183**, **all of which the block route already reaches, and 0 of the 3827**. **The mixed route adds no scope at all** |
| **Margin at a surviving point** (`margin58.py`) | which inequality is *closest to failing* where the scan survives: **(4) spread on 1416 points, (6) \(U\)-degree on 1043, (3) Turán on 67**, and **1536 of 2526 points clear something by exactly zero**. Complementary to the handicap table, not a substitute — confusing the two is defect 13 |
| \(a+t\le\omega(G)\le28\) from criticality | \(A\) is a clique of \(G\) and one vertex per \(U\)-component extends it; and a \(K_{29}\) in a 29-critical graph on 58 vertices would be a **proper** subgraph of chromatic number 29. Sharpens the table's \(\omega\le29\). **Measured: \(a+t\) never exceeds 26 — does not bite** |
| Crossing ladder on the near-complete subgraph | at a case-B point with \(W=0\), \(u=t\): \(G\supseteq K_{a+\lvert R\rvert}\) minus **exactly** \(\sum_ia_i\rho_i+e(H[R])\) edges. **Measured: best bound 4163 against \(Z(29)=8281\), a 49% shortfall — does not bite**, because deleting ~half of \(K_{43}\) costs most of its crossing number |
| **Priced sensitivity table** (`slack58.py`) | how strong a sharpening must be. Its rows **move as the other inequalities move**, so it is only ever a statement about the current set; `slack58.py` therefore derives its conclusions from the measured rows rather than asserting them |

**Where the two obstructions stand** — re-measured on the class that is open
*today* (`shortfall58.py`), because `profile58.py`'s figures are true of the
9104-survivor set that no longer exists:

| | then (9104) | **now (6054)** |
|---|---|---|
| absorption shortfall 1 | 3326 (36.5%) | **3196 (52.8%)** |
| smallest absorption shortfall | 1 | 1 |
| crossing shortfall | long-tailed, thousands | unchanged; only 100 under 500, none at 0 |

**The proportion within one unit has risen**, from 36.5% to 52.8%. **That does
not mean what this document said it meant, and the reading is withdrawn as
defect 21.** The histogram is a *minimum over surviving sub-cases*, and a
configuration closes only when every surviving sub-case dies; the inequality is
also one of three conjuncts, so a sub-case escaping through \(Z_a\ge t\) or
\(\mu_1\ge t\) is untouchable by an absorption bonus of any size.

## What the absorption inequality actually buys (`absprice58.py`)

Priced the way `slack58.py` prices the Tutte inequalities — give it \(d\) more
units unconditionally and re-run the decision. `residue58.survivors` gains a
`need_scan` mode that walks the **same code path** and returns the least bonus
that closes each configuration, so the price cannot drift from the thing priced.

| bonus \(d\) | **scan closes** | histogram predicts | overstatement |
|---|---|---|---|
| 1 | **117** | 3196 | **3079** |
| 2 | 387 | 4143 | 3756 |
| 5 | 1309 | 5436 | 4127 |
| 10 | 3346 | 6022 | 2676 |
| 15 | 5417 | 6052 | 635 |
| 20 | **6052** | 6054 | 2 |
| 25 | 6053 | 6054 | 1 |

Median least closing bonus **10**, largest **21**. Four rows are re-derived the
slow way through the real decision, by setting `residue58.ABS_HANDICAP`: all
**PASS**.

**And the reach, which is the useful half.** Exactly **one** configuration of the
6054 escapes the absorption inequality entirely; the other **6053** close for a
large enough bonus, *including configurations outside the clique-cover route that
nothing else in this lane reaches*. The contrast with the count inequality is now
measured on both sides:

| | reach | strength needed |
|---|---|---|
| count (`slack58.py`) | **3561 of 4486**, unchanged from \(d=1\) to \(d=50\) | 1 unit, and it never gets further |
| absorption (`absprice58.py`) | **6053 of 6054** | median **10**, max **21** |

**So the residual is not two halves needing two tools.** It is one inequality and
one scalar: how many units of absorption can be proved unconditionally. Ten
closes half the class, twenty-one closes all of it but one. That is a harder
target than the one it replaces and a better-founded one.

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
| (1) count | **3561** | 3561 | 3561 | 3561 |
| (2) degree | 2259 | 2259 | 2284 | 2627 |
| (3) Turán | 2264 | 2289 | 2503 | 2654 |
| (4) spread | **2786** | 2786 | 2786 | 2786 |
| (5) \(S_R\)-degree | 2264 | 2289 | 2549 | **3166** |

Baseline 2259; the route reaches **4486** configurations in all.

**A claim this table was read as supporting is withdrawn — defect 20.** Until
pass 60 the reach was computed here by the *superseded* knapsack bound
`kmax_guaranteed` applied to the *raw* multiset, while `route_closed` decides
reach by the exact packing number on the *true* block multiset. The weaker bound
understates reach; the unlisted blocks of defect 19 overstate it. The two errors
did not cancel — they produced **3712**, which coincided **exactly** with the
count row, and the coincidence was published as *"one unconditional unit on the
count inequality closes every configuration the route reaches"*.

It does not. One unit off the count inequality closes **3561 of the 4486** the
route reaches — **925 short** — and **no inequality here is decisive at one
unit**. At \(d=50\) the count row is still the best and still 3561 of 4486 —
it does not move at all — and the best of the others, \(S_R\)-degree, reaches
3166. The
target \(o(H'-S)\le c_A+t-1\) is still the most valuable single theorem in the
table, but it is no longer a *sufficient* one.

**The table moves when the inequalities move, and this is worth stating.** On the six-inequality scan two passes ago the spread inequality was *inert at
every handicap*; it is now worth **+527** at one unit, having been **+643** and
before that **+1528** — the same row, four different verdicts, purely because
the rest of the set moved. A pricing table is only
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

Twenty-one items were found, fifteen of one family, all of the same shape — *a step verified on
the case that happens to be favourable, then generalised without re-deriving*.
**Defects 19, 20 and 21 are one failure in three places** — *a number that resembles a price, adopted as one*: the block multiset that was not the block multiset, the reach denominator computed by a superseded bound, and the shortfall histogram read as a closure count. The first pair in detail: the same unlisted blocks, first corrupting a
guarantee and then, through a second and independent error in the same
direction-blind measurement, corrupting the denominator a published target was
priced against. Two wrong numbers that agreed are the hardest kind to see, and
the only thing that exposed either was refusing to bank a gain I did not
believe:

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
| 15 | "order 57 has never been independently reviewed" | **false, published on the ledger** | **twenty** reviews exist, **seven** on order 57; checkable with `ls reviews/`. Cause: this document cited one of them |
| 16 | `aug57.py` never prints its \(cr(K_{13})\ge223\) dependence | a presentational defect in one artifact | flagged in its review, not carried into the artifact; `seed57.py` now records it |
| 17 | "order 57's closure is conditional on \(cr(K_{13})\ge223\)" | **false, published on the ledger** | withdrawn. `cover57.py` kills those cases structurally at every rung. Made by reading one review of seven — the same failure the same pass was correcting |
| 18 | "\(w\) is a feature of the order-58 class only" (`wturan58.py`) | **false, and printed in its expected output** | order 57 has **two** such singletons and the cap is *stronger* there. Flagged in `reviews/albertson-singleton-turan/` nine passes ago; fixed |
| 19 | the block multiset **does not list every block** | **35 published closures were invalid** | `mu58.multisets` adds odd-cycle blocks' edges to `eL` without appending them to the list, so `extra` was understated on **772** configurations, overstating the triangle guarantee. **151 lose the guarantee; 35 had been closed on it.** Withdrawn: 2294 → 2259, order 58 6341 → **6376** |
| 20 | "one unit on the count inequality closes every configuration the route reaches" | **false, published on the ledger** | `slack58.py` measured the *denominator* with the superseded `kmax_guaranteed` on the *raw* multiset while `route_closed` used the exact guarantee on the true one. Two errors in opposite directions, not cancelling, produced a reach of 3712 that coincided **exactly** with the count row. Corrected: **3561 of 4486, 925 short**, and **no** inequality is decisive at one unit |
| 21 | "one unit on the absorption inequality closes 3196 of the 6054" | **false, published on the ledger** | a *histogram* read as a *price*. The deficit is a minimum over surviving sub-cases, and a configuration closes only when every one dies; the inequality is also one of three conjuncts. Priced by a scan (`absprice58.py`): one unit closes **117**, median **10**, and the same scan shows it **reaches 6053 of 6054** |

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
> to widen it. The mixed-triangle route is now measured out (`mixed58.py`): it
> adds no configurations the block route does not already reach. The sensitivity
> table below says where: **not** in the edge
> counts, which are inert or need improvements of 50, but in the component
> bound, which is worth more at one unit than anything else priced — though
> **not** enough to close everything the route reaches, a claim this note
> carried until pass 60 and which is withdrawn as defect 20. Separately, the
> out-of-scope survivors have no *guaranteed* three disjoint
> triangles and need either a sharper triangle-packing guarantee or a different
> family of the seventy.
