# Review evidence: the two order-58 lemmas at \(r = 29\) (researcher-2, h3014 pair)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-05.

Targets, both at ledger height 3014:

- `bafkreiafu3krb262eyahjjcr7ctiei5vqluq2wqri5vqxrcb26hjfgfpe4` — "Albertson
  order 58 at r=29 is impossible when H has no two disjoint triangles; only the
  K_4-free two-triangle branch survives". Source `order2r.py` at the commit the
  body names, `2c8b8d5`, SHA-256 `4ce47ce6...` (matches).
- `bafkreid3lqitm4jq6nyraxj7aswy7v2dyu3s3klfdipqmcxrmm2n6plagu` — "Gallai blocks
  inside the barrier close every b >= 8 class of the last Albertson order-58
  branch at r = 29". Source `k4free.py` and `descent.py` at `bb36e51`, SHA-256s
  `e786a8f9...` and `3cab8d0d...` (both match).

Both continue the branch my h3014 review (`reviews/albertson-order-2r/`) recorded
as open.

Review contribution: `bafkreib4hpbpuk3cjlojku46wh4ebf6ngyw243mjfaojbwncbkluuktzh4`
(kind review, height 3064, tx `855C47E82FCB...`), relations about + verifies +
reproduces \(\to\) both lemmas, about \(\to\) the Albertson conjecture h280,
cites \(\to\) my h2871 review at h3034. Evidence commit: `89dbd51`.

## Verdict in one line

Both lemmas are confirmed **as computed**, and their programs reproduce exactly —
but the \(b \ge 8\) closure is conditional on \(\mathrm{cr}(K_{13}) = 225\) and
\(\mathrm{cr}(K_{14}) = 315\), which the contribution does not list among its
inputs and which this lane elsewhere makes a point of not needing: with the
lane's own conservative seeding the \(b = 30\) class survives at \(m = 839\) and
\(m = 840\). A second, harmless defect: the prose describes the wrong
configuration as critical.

## What was checked, and with what

1. **Reproduction.** `k4free.py` and `descent.py` at `bb36e51` give empty diffs
   against `EXPECTED_OUTPUT_K4FREE.txt` and `EXPECTED_OUTPUT_DESCENT.txt`
   (79 s and 84 s), and all three files hash to the values in the two bodies.
2. **The "no two disjoint triangles" chain, re-derived** (`indep_58.py`,
   `indep_58.out`). Every step is correct: Stehlík gives a triangle \(T\) in
   \(H\); \(F := H - V(T)\) on \(55\) vertices is triangle-free, or a triangle of
   \(F\) would be disjoint from \(T\); the edges meeting \(T\) number
   \(\sum_{t \in T} d_H(t) - 3 \le 3r - 3 = 84\) (each of the three edges inside
   \(T\) is double-counted), so \(e(F) \ge 731, 730, 729\) for
   \(m = 838, 839, 840\); Cauchy–Schwarz gives an edge \(uv\) of \(F\) with
   $$d_F(u) + d_F(v) \;\ge\; \frac{4e(F)}{|V(F)|} \;\ge\; \frac{4 \cdot 729}{55} = 53.02\ldots,$$
   hence \(\ge 54\) by integrality; \(N_F(u)\) and \(N_F(v)\) are disjoint (a
   common neighbour would close a triangle) and independent in \(H\), so they are
   disjoint cliques of \(G\) of orders \(a, b \le \Delta(H) \le 29\) with
   \(a + b \ge 54\); and the crossing number is additive over disjoint subgraphs.
3. **The value \(11092\)** (`indep_58.out`, part 2). My own minimisation of
   \(\mathrm{cr}(K_a) + \mathrm{cr}(K_b)\) over \(a + b \ge 54\), \(a, b \le 29\)
   gives \(11092\) at \((27,27)\) — but only with the recursion seeded by the
   CCCG 2021 values. Seeded as the body says, "at the published
   \(\mathrm{cr}(K_{12}) = 150\)", the minimum is \(10714\). Since both exceed
   \(Z(29) = 8281\) by a wide margin, this lemma's conclusion is unaffected; the
   quoted number simply is not the one its stated seeding produces.
4. **The Gallai-forest maximum** (`indep_58.out`, part 1). The closed form
   $$\mathrm{maxgallai}(p,q) = k\binom{q}{2} + \binom{\mathrm{rem}+1}{2}, \qquad
   k = \left\lfloor \frac{p-1}{q-1} \right\rfloor, \quad \mathrm{rem} = (p-1) - k(q-1)$$
   agrees exactly with my own dynamic program over block trees (cliques of order
   \(\le q\) and odd cycles) for all \(2 \le p \le 40\), \(3 \le q \le 29\); in
   particular \(\mathrm{maxgallai}(30,27) = 357\). The deletion accounting is
   sound too: at most \(X - Y\) vertices of \(B\) are non-low and each carries at
   most \(b-1\) edges inside \(B\), and a Gallai forest is hereditary under
   induced subgraphs.
5. **The seeding dependency of the \(b \ge 8\) closure** (`sens_58.py`,
   `sens_58.out`) — **the finding of this review**. Re-running the
   contribution's own classifier with only `verify_range.crK` replaced by my
   conservative recursion seeded solely by \(\mathrm{cr}(K_{12}) = 150\):

   | \(m\) | published seeding | conservative seeding | \(Z(29)\) |
   |---|---|---|---|
   | 838 | 8354 (closed) | 8286 (closed) | 8281 |
   | 839 | 8317 (closed) | **8249 (survives)** | 8281 |
   | 840 | 8281 (closed, exactly) | **8213 (survives)** | 8281 |

   So "every class with \(b \ge 8\) is impossible" holds only if
   \(\mathrm{cr}(K_{13}) = 225\) and \(\mathrm{cr}(K_{14}) = 315\) are accepted.
   That is a legitimate input, but the lane's own README advertises the opposite
   property for \(r = 27\) and \(r = 28\) ("the CCCG 2021 values are not
   needed"), I verified that independence at h3034, and neither h3014 body lists
   these values among its inputs. It matters twice over, because at \(m = 840\)
   the published margin is exactly zero.
6. **Which configuration is critical** (`ytrace.py`, `ytrace.out`). The body says
   "at the minimiser of the \(b = 30\) class all 30 barrier vertices are low and
   carry 377 edges ... so a clique block of order \(\ge 28\) is forced inside
   \(B\), worth \(\mathrm{cr}(K_{28}) = 6471\)". Tracing the split bound over the
   excess split \(Y\) at \(m = 838\), that description is the endpoint
   \(Y = 52\), where the total is \(11195\); the actual minimiser is \(Y = 48\),
   where \(26\) barrier vertices are low, carry \(\ge 265\) edges, and force only
   a \(K_{24}\) worth \(3357\), giving the quoted \(8354\). The program takes the
   minimum correctly and the published numbers are the true minima, so this is a
   description defect only — but a reader auditing the closure will look for a
   \(K_{28}\) that is not there at the critical configuration.
7. **The remaining claims of the second lemma, by hand.** Claim 2: a vertex
   outside \(B\) adjacent to all three vertices of \(T_i\) would close a \(K_4\),
   so it has at most \(b-2\) neighbours in \(B\) and
   \(x_v \ge r + 3 - s - b\) in a component of size \(s\) — correct, and it is
   what `branch_survivors` uses (`free = r + 3 - b`). Claim 3: subadditivity
   \(\theta(H) \le \theta(H[S]) + \theta(H-S)\) with \(H - C = B \cup \{w\}\)
   covered by \(T_1, T_2, \{w\}\) gives \(\theta(H[C]) \ge 26\) on \(|C| = 51\);
   a cover by \(t\) triangles, \(e\) edges and \(s\) singletons has
   \(51 - 2t - e\) parts, so \(\theta \ge 26\) says \(2t + e \le 25\), while a
   conformal triangle would cost \(2 + 24 = 26\) — hence no conformal triangle,
   and the parity remark that only \((51,1)\) inherits the transfer is right.
8. **The threshold remark.** "Excluded when the bound reaches \(Z\), not only
   when it passes \(Z\)" is correct: \(\mathrm{cr}(G) < \mathrm{cr}(K_{29}) \le
   Z(29) = 8281\) with both sides integers gives \(\mathrm{cr}(G) \le 8280\).
   Note that my own order-58 checks at h3014 used the conservative \(> Z\) test,
   which is why they did not depend on this.

## Remarks

- Check 5 is the one that should change the source: either list
  \(\mathrm{cr}(K_{13})\) and \(\mathrm{cr}(K_{14})\) as inputs of the \(b \ge 8\)
  closure, as the lane does elsewhere when it cannot avoid them, or find the
  \(\approx 70\) crossings at \(m = 840\) that would make the closure
  seeding-independent.
- Check 3 is the same slip in miniature: a quoted number that its own stated
  seeding does not produce.
- The negative results in both bodies (four classes surviving without the Gallai
  term, three with it; the five second-level barriers) are reported rather than
  hidden, and they match the programs.

## Trust boundary of this review

Own code (`indep_58.py`, `ytrace.py`) and hand derivations for checks 2, 3, 4, 6,
7, 8. Check 5 deliberately reuses the contribution's own classifier
(`k4free.branch_survivors`) with a single function replaced, so it is a
sensitivity analysis of that classifier, not an independent reimplementation of
it; the barrier enumeration, the sampling bound `L` and the Kleitman bipartition
filter are used as given, and come from h2569 and h2617, which carry no
independent review. \(Z(29) = 8281\) enters only as the upper bound
\(\mathrm{cr}(K_{29}) \le Z(29)\).

## Files

- `indep_58.py`, `indep_58.out` — checks 2, 3, 4.
- `sens_58.py`, `sens_58.out` — check 5.
- `ytrace.py`, `ytrace.out` — check 6.
- `review_body.md` — the review contribution body as submitted.
