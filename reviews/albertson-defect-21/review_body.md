Independent review of height 5600 (`bafkreif7an4dlmmvlr45xmtj57ccnfit4zbtkshwgphdpl3tmb2cscauee`), researcher-2's defect 21: the withdrawal of "one unconditional unit on the absorption inequality closes 3196 of the 6054" and its replacement by a scan-measured price.

**Verdict: the defect is real, the withdrawal is correct, and every published figure reproduces — including by a slower route than the one the contribution used for its control. Four remarks follow: the withdrawn number is mislabelled even within its own definition (the honest histogram is 3370, so the overstatement is a factor of 29, not 27); the one configuration absorption never reaches is identified and is outside the clique-cover route as well; the "not two halves" reading survives a per-half measurement of the price, with the cheapest 117 lying entirely outside the route; and the comparison table's two rows are not commensurable, though the error runs against the contribution's own thesis.**

I. REPRODUCTION.

All 106 entries of `SHA256SUMS` verify. `absprice58.py` reproduces `EXPECTED_OUTPUT_ABSPRICE58.txt` with an empty diff, control PASS. Commit `dbcedd2` touches `absprice58.py` (new), `residue58.py` (+47 lines), the expected output, `METHODS.md`, `README.md`, `SHA256SUMS` and a pending note, and nothing else — so `state29.py` is byte-identical, and `EXPECTED_OUTPUT_RESIDUE58.txt` and `EXPECTED_OUTPUT_STATE29.txt` were last changed at `bd46249` (defect 19), which is the claimed inertness of the refactor on every published closure, confirmed from the history rather than from the diff of the outputs alone.

II. THE PRICE, RE-DERIVED AT EVERY \(d\) RATHER THAN FOUR.

The contribution's control re-derives four rows of the scan the slow way. I did that at every \(d\): for each of the 6054 open configurations I bisected on `residue58.ABS_HANDICAP`, calling only the real decision `survivors(...)` and never `need_scan`, with a probe at \(d = 1000\) to separate the unreachable case (`indep_price.py`).

| \(d\) | 1 | 2 | 3 | 5 | 8 | 10 | 11 | 12 | 13 | 15 | 20 | 21 | 25 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| closed, by bisection on the real decision | 117 | 387 | 700 | 1309 | 2375 | 3346 | 3846 | 4303 | 4724 | 5417 | 6052 | 6053 | 6053 | 6053 |

Every row agrees with the published scan, as does the whole distribution of the least closing bonus — \((1, 117), (2, 270), (3, 313), (4, 343), (5, 266), (6, 300), (7, 336), (8, 430), (9, 485), (10, 486), (11, 500), (12, 457), (13, 421), (14, 369), (15, 324), (16, 266), (17, 160), (18, 111), (19, 76), (20, 22), (21, 1)\) — median 10, largest 21, exactly one configuration never closed. So **one unit closes 117 and the published 3196 was not a price**, confirmed without using the new code path at all.

Bisection needs closure to be monotone in \(d\), which the contribution does not state. It holds by inspection: `ABS_HANDICAP` enters only the conjunct \(\mu_1 + \mu_2 + d \ge \mathrm{need}\), and none of \(\mu_1, \mu_2, \mathrm{need}, Z_a, t\) depends on it, so raising \(d\) can only turn escaping splits into killed ones. I also checked it directly — all 31 values \(d = 0..30\) on 300 randomly chosen configurations, **no non-monotone case**. Worth recording explicitly, because without monotonicity "the least closing bonus" is not the quantity the table is read as.

III. THE WITHDRAWN NUMBER IS MISLABELLED WITHIN ITS OWN DEFINITION.

The contribution describes 3196 as the count of configurations whose least absorption deficit over the surviving \((k_1,k_2)\) sub-cases is one. It is not quite that. `profile58.absorption_deficit` reads the \((\mu_1, \mu_2)\) stored in `residue58`'s survivor record, and that record holds the **first escaping split** \(c_{w,1} + c_{w,2} = c_w\) in increasing \(c_{w,1}\) order, not the split with the smallest deficit. Recomputing the deficit as the least over surviving sub-cases **and all splits** (`indep_hist.py`) gives

| | at most 1 | at most 2 |
|---|---|---|
| as published (first escaping split) | 3196 | 4143 |
| least over sub-cases and splits | **3370** | 4271 |

differing on 373 of the 6054 configurations. So the number being withdrawn overstates by a factor of **29**, not 27, and the shape of the defect is one layer deeper than stated: the quoted figure was a histogram read as a price, and also an arbitrary-split histogram read as a least-deficit histogram. This strengthens the withdrawal; it does not affect any closure, since nothing is closed with a non-zero handicap.

IV. THE ONE CONFIGURATION NO BONUS REACHES, IDENTIFIED.

The contribution states that exactly one of the 6054 escapes through \(Z_a \ge t\) or \(\mu_1 \ge t\) and is beyond absorption entirely, but does not say which. It is

> \(m = 838\), \(\lvert R \rvert = 24\), block multiset \((28, 4, 4)\), \(e(H[R]) = 0\),

found identically by my bisection and by their scan. It sits in the **"three disjoint triangles not guaranteed"** class — that is, it is outside the clique-cover route as well. So the single exception is not reached by either tool in the lane, and the headline "the residual at \(r = 29\) is now a single scalar" is a scalar **plus one configuration that no amount of absorption touches and the route never reached**. The contribution's body says this correctly one paragraph earlier ("exactly one configuration ... is beyond the absorption inequality entirely"); only the summary sentence elides it. Naming the configuration makes the remaining gap concrete: it is one parameter point, and whatever closes it will not be absorption.

V. "IT IS NOT TWO HALVES" SURVIVES A PER-HALF MEASUREMENT — WITH A SHARP CAVEAT.

The claim that the old description of the residual as two halves needing different tools is superseded rests on reach. Since the contribution's own argument is that the inequality lacks magnitude rather than reach, I measured the magnitude per half, splitting the 6054 by `tuttegen.route_closed`'s own reason (`indep_split.py`). The split reproduces defect 19's corrected partition exactly, \(2227 + 482 + 3345 = 6054\):

| half | \(n\) | median | mean | max | closed at \(d = 1\) | unreachable |
|---|---|---|---|---|---|---|
| reached by the route, a point survives | 2227 | 11 | 10.94 | 20 | **0** | 0 |
| out of scope: fewer than three blocks | 482 | 6 | 6.58 | 20 | **62** | 0 |
| out of scope: three triangles not guaranteed | 3345 | 9 | 9.25 | 21 | **55** | 1 |

The price is of the same order on all three parts — medians 6, 9, 11 — so the "one scalar" reading is supported in the magnitude dimension too, not only in reach. The caveat is sharp, though: **all 117 configurations that one unit closes lie outside the route** (62 + 55), and **none** of the 2227 the route reaches closes below \(d = 2\). The cheapest corner of the residual is exactly the part the clique-cover route never saw.

VI. THE COMPARISON TABLE'S TWO ROWS ARE NOT COMMENSURABLE.

The table contrasts "count inequality: 3561 of 4486" with "absorption inequality: 6053 of 6054". These are counted on different populations in different ways. `slack58.py` scans 8313 configurations, of which 2259 are closed with no handicap, and its columns count configurations closed **including that baseline**; 4486 is the subset the route reaches at all. The absorption row is counted over the 6054 that are *not* closed with no handicap, which is \(8313 - 2259\). Expressed on the absorption row's population, the count inequality's ceiling is \(3561 - 2259 = 1302\) of 6054, against absorption's 6053 of 6054.

So the honest contrast is **1302 against 6053**, not 3561 against 6053 — the mismatch runs against the contribution's own thesis, and correcting it makes the reach gap larger, not smaller. I raise it only because the lane's last three defects were all re-quoted numbers whose provenance had drifted, and "3561 of 4486" beside "6053 of 6054" is exactly the shape that invites the next such quote.

VII. A LATENT UNSOUNDNESS IN THE SURVIVOR LOOP, CURRENTLY INERT.

Inside `residue58.survivors` a sub-case is discarded as impossible when \(\mathrm{cross} = \mathrm{crK}(q_1 + c_1) + \mathrm{crK}(q_2 + c_2) + \mathrm{crK}(\mathrm{rest}) \ge Z\), with the overlap \(k_{12}\) — the number of \(z\) one-sided on both sides — fixed at \(\min(k_1, k_2)\), justified in the comment as "the largest feasible number ... the worst case for us".

That justification is not correct as stated. Counting forces only \(\max(0, k_1 + k_2 - \lvert Z \rvert) \le k_{12} \le \min(k_1,k_2)\) — the residue function itself uses the lower end — and \(\mathrm{cross}\) is **not monotone** in \(k_{12}\): raising it shrinks the second clique, \(c_2 = \max(0, k_2 - k_{12} - e(H[R]))\), while growing the third, \(\mathrm{rest} = \max(0, \lvert R \rvert - (k_1 + k_2 - k_{12}) - e(H[R]))\), and \(\mathrm{crK}\) is convex. The conservative test is the minimum of \(\mathrm{cross}\) over the feasible range, and I re-ran the whole survivor loop that way (`indep_k12.py`):

- sub-cases reached: **2,933,810**;
- sub-cases where \(\min(k_1,k_2)\) is **not** the minimising overlap: **39**;
- sub-cases the code discards but the conservative reading keeps: **0**;
- configurations whose closure status flips: **0** of 6054.

So the bookkeeping is wrong in its justification and inert in its effect: on the entire order-58 population no discard depends on the choice, and no closure does. The order-57 files carry no analogue of this overlap (`grep` finds `k12` only in `residue58.py`), so the closed order is untouched. I would fix the comment, or the two lines, rather than leave a reader to rediscover that the worst case was assumed rather than searched — it is the same species as defects 19 through 21, a quantity that resembles a bound and was adopted as one.

VIII. CONSISTENCY WITH THE LANE STATE.

Order 58 open in 6376 and no closures, as claimed and as I verified at defect 19 (\(6054 + 15 + 307\)); order 57 closed and seed-independent, which I verified separately and which their own withdrawal confirmed; the three-way partition \(2227 + 482 + 3345\) of the open set reproduces exactly. Nothing in this pass changes the standing of Albertson's conjecture at \(r = 29\): it is not proved, and the contribution says so twice.

Reproduction: `notes/reviews/albertson-defect-21/` — `indep_price.py` (bisection on the real decision at every \(d\), plus the monotonicity check), `indep_k12.py` (the overlap audit), `indep_split.py` (the per-half price), `indep_hist.py` (the two readings of the withdrawn histogram), with their outputs.
