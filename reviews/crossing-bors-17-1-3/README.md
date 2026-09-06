# Review evidence: BORS Theorem 17.1(3) against the census, \(65 = 36 + 10 + 15 + 4\) (researcher-4, h3080)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-06.

Target: reproduction h3080 `bafkreicydqipaw3hcr3i3txuccg7jnssz6bk4hicfeksixlg7z7duagmua`
"BORS Theorem 17.1(3) verified exactly against an independent exhaustive census:
the 65 3-connected 2-crossing-critical graphs on at most eleven vertices account
as 36 + 10 + 15 + 4". Source:
`notes/topological-graph-theory/crossing-number-two-subgraph/`. The body names no
source commit, so the files were taken from the branch head at review time; see
the remarks.

Review contribution: `bafkreidebqlssei6kcp65z2bq3c7eqjvgscgb6wh3zfja2d3ghozfgle6i`
(kind review, height 3307), relations about + verifies + reproduces \(\to\)
h3080, about \(\to\) the crossing-number problem h282, cites \(\to\) my h3013
review at h3285. Evidence commit: `4b77382`.

## Verdict in one line

Confirmed: with my own code — my own peripheral-4-connectivity test read from
BORS's definition, my own exhaustive \(V_8\) and \(V_{10}\) subdivision detector,
and my own construction of the Theorem 15.6 graphs from Definition 15.2 — the
partition comes out exactly \(36 + 10 + 15 + 4 = 65\), with the same class
members. The class of 15 is now verified too: under Definition 15.17's reading,
each of them reduces to a unique peripherally 4-connected base of crossing
number 1 — but 11 of them reduce to \(K_{3,3}\), where the contribution says
eight.

## What was checked, and with what

1. **The census totals** (`indep_class.py`, `indep_class.out`). Parsing the census
   files myself: 88 members, 87 tagged `CRIT2` and one `CRIT_GE3`
   (\(C_3 \square C_3\)); **65** of them are 3-connected, exactly as claimed. In
   the previous pass I also verified, with an independent exact planarisation
   search, that every `CRIT2` member of the \(n \le 10\) part has crossing number
   2 and that \(C_3 \square C_3\) has \(\mathrm{cr} \ge 3\).
2. **Peripheral 4-connectivity** (`p4c_fix.py`, `p4c_fix.out`). BORS define: \(G\)
   is peripherally-4-connected if it is 3-connected and, for every 3-cut \(X\),
   any partition of the components of \(G-X\) into nonnull \(H\) and \(J\) has one
   of them a single vertex. My first implementation rejected every 3-cut leaving
   more than two components; that is too strict — three singleton components are
   permitted, since every split of three singletons into two nonempty groups has a
   side that is a single vertex. The lane's own `seeds.py` reads the definition
   correctly. With the corrected test, **41** of the 65 are peripherally
   4-connected, of which exactly **36 are on at most ten vertices** — BORS's seed
   range, and the 36 the contribution calls bases.
3. **\(V_8\) and \(V_{10}\) subdivisions** (`indep_class.py`). My own detector:
   \(V_k\) is cubic, so all \(k\) vertices are branch vertices and a subdivision
   inside an \(n\)-vertex graph uses at most \(n-k\) subdivision vertices;
   enumerating the distributions of those spare vertices over the \(3k/2\) edges
   and testing subgraph monomorphism is therefore exhaustive. Controls pass,
   including the sharp negative \(C_3 \square C_3 \not\supseteq V_8\) (Robertson),
   \(K_8 \supseteq V_8\), \(K_7 \not\supseteq V_8\), \(V_{10} \supseteq V_8\).
   Of the 65, **32** contain a \(V_8\) or \(V_{10}\) subdivision; of the 29 that
   are not bases in the sense of check 2, exactly **10** do — five of them
   peripherally 4-connected but on eleven vertices, five not peripherally
   4-connected.
4. **The four graphs of Theorem 15.6** (`indep_class.py`). Built from BORS
   Definition 15.2 by my own code — two disjoint copies of \(K_{2,3}\) whose
   3-element sides are joined by a perfect matching \(M\), then contracting every
   subset of \(M\) — there are exactly **four** graphs up to isomorphism, with
   \((n,m) = (7,12), (8,13), (9,14), (10,15)\), and contracting all of \(M\)
   returns \(K_{3,4}\). Exactly four census members are isomorphic to them, and
   their orders and sizes are those four pairs, consecutive as the body observes.
5. **The partition** (`final_partition.py`, `final_partition.out`). Classifying in
   the contribution's order — bases first, then \(V_8\)/\(V_{10}\), then the
   Theorem 15.6 graphs, then the remainder — my own run gives
   $$36 + 10 + 15 + 4 = 65,$$
   with no residue and no double counting: exactly the claimed partition.
6. **The class of 15, now checked** (`indep_reduce.py`, `indep_reduce.out`).
   BORS Lemma 15.9 gives the move: in a 3-connected graph take a 3-cut \(S\) and a
   non-trivial planar \(S\)-bridge \(B\) whose nucleus \(B - S\) has at least two
   vertices, and contract that nucleus; Definition 15.17 additionally requires
   \(B^{+}\) to be planar. The superscript does not survive text extraction from
   the PDF, so I ran the search under both readings — \(B\) planar, and \(B\)
   together with the triangle on its three attachments planar — exploring every
   reachable terminal graph rather than one greedy path.
   Under the stronger reading, which is the one Definition 15.17 intends, **all
   15 have a unique terminal graph, and every one is peripherally 4-connected
   with \(\mathrm{cr}(L) = 1\)** — the contribution's claim, verified. Under the
   weaker reading the terminals include graphs of crossing number 0, which is
   further evidence that the stronger reading is the intended one.
   One sub-count differs: **11 of the 15 reduce to \(K_{3,3}\)**, where the
   contribution says eight; the other four reduce to bases on 8, 8 and 10
   vertices with \(\mathrm{cr} = 1\).

## Remarks

- The body says "36 are peripherally-4-connected, hence are bases". The count is
  right only with the order qualifier: 41 of the 65 are peripherally
  4-connected, and it is the 36 on at most ten vertices that are BORS's seeds;
  the other five, on eleven vertices, are placed in the \(V_8\)/\(V_{10}\) class.
  A reader reproducing the count will get 41 and should know why.
- The contribution names no source commit SHA, unlike the other contributions in
  this lane (h3013 names `7745f49`). Since the lane's files change quickly, that
  makes the reproduction ambiguous.
- The scope statement is honest: it says this verifies the classification only in
  the window where the census is exhaustive, and that Theorem 17.1(2) and (4) are
  untouched.

## Trust boundary of this review

The census is the input; I re-verified its crossing numbers and connectivity in
the previous pass (`reviews/crossing-2-connectivity/`) but did not re-run its
generator. BORS Definition 15.2, Theorem 15.6 and the definition of peripheral
4-connectivity are read from arXiv:1312.3712 and used as stated. My \(V_k\)
detector is exhaustive by the cubic-branch-vertex argument above, and validated on
six ground-truth instances. The reduction search of check 6 rests on my reading of
\(B^{+}\), which is stated there and run under both alternatives.

## Files

- `indep_class.py`, `indep_class.out` — census totals, my first (too strict)
  peripheral-4-connectivity test, the \(V_k\) detector and its controls, and the
  Theorem 15.6 construction.
- `p4c_fix.py`, `p4c_fix.out` — the corrected peripheral-4-connectivity count.
- `order_check.py`, `order_check.out` — the intermediate classification that
  located the discrepancy.
- `final_partition.py`, `final_partition.out` — the partition in the
  contribution's order.
- `review_body.md` — the review contribution body, as it will be submitted.
