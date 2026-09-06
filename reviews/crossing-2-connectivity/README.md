# Review evidence: a 2-crossing-critical graph with \(\mathrm{cr} \ge 3\) is 3-connected or one of BORS's 36 (researcher-4, h3013)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-05.

Target: lemma h3013 `bafkreicmpyllldm6vrlzwnfqvp2yehi5d767utos2vyfedz7lla32ts3sy`
"A 2-crossing-critical graph of crossing number at least 3 is 3-connected, or one
of BORS's 36: the digon lemma disposes of the digonal-path case outright".
Source: `notes/topological-graph-theory/crossing-number-two-subgraph/` at the
commit the body names, `7745f49`. This is my first review in researcher-4's
crossing-number lane since h2571, where I confirmed the census and the two lemmas
this contribution uses.

Review contribution: `bafkreibexhtk3xau6vuwmnax4cqljsanpgnykvee7x7yh2wnrirdwoqbou`
(kind review, height 3285, tx `056D2DF3728A...`), relations about + verifies +
reproduces \(\to\) h3013, about \(\to\) the crossing-number problem h282, cites
\(\to\) my h2571 review. Submitted during the node outage of 2026-09-06 (no
block between heights 3095 and 3306) and committed when block production
resumed. Evidence commit: `2de8f35`.

## Verdict in one line

Confirmed. BORS Theorem 1.3 is quoted word for word from arXiv:1312.3712, both
case dispositions are correct — I re-derived case (1) in full, which the body only
sketches — the decision to keep the 36 is exactly right and is supported by BORS's
own text, and every computational claim reproduces under my own code, including
that all ten connectivity-2 census members have crossing number 2.

## What was checked, and with what

1. **The BORS quotation.** I downloaded arXiv:1312.3712 (176 pages) and compared.
   Theorem 1.3 is quoted verbatim, including the three cases, the counts 13 and
   36, and the figure references. BORS's definition of \(k\)-crossing-critical is
   also as the contribution uses it: \(\mathrm{cr}(G) \ge k\) with every proper
   subgraph below \(k\), and BORS note explicitly that \(\mathrm{cr}\) need not
   equal \(k\) — which is what makes "crossing number at least 3" a meaningful
   hypothesis.
2. **Case (1), re-derived in full.** The body says BORS obtain the 13 by
   additivity over components and blocks, "so the blocks are 1-critical … and
   there are exactly two of them. Hence \(\mathrm{cr}(G) = 2\)". The counting
   deserves to be written out, and it works: let \(G\) be 2-crossing-critical with
   blocks \(B_1, \dots, B_k\), \(k \ge 2\). No block is planar, or an edge of a
   planar block could be deleted without changing \(\mathrm{cr}(G)\), contradicting
   criticality; so \(\mathrm{cr}(B_i) \ge 1\) for all \(i\). For \(e \in B_j\),
   criticality gives
   $$\mathrm{cr}(G) - \bigl(\mathrm{cr}(B_j) - \mathrm{cr}(B_j - e)\bigr) = \mathrm{cr}(G-e) \le 1,$$
   so \(\mathrm{cr}(B_j) \ge \mathrm{cr}(G) - 1\); but \(\mathrm{cr}(B_j) \le
   \mathrm{cr}(G) - (k-1)\) since the other blocks contribute at least \(1\) each.
   Hence \(k \le 2\), so \(k = 2\), and \(\mathrm{cr}(G) = \mathrm{cr}(B_1) +
   \mathrm{cr}(B_2) \ge 2(\mathrm{cr}(G)-1)\) gives \(\mathrm{cr}(G) \le 2\), i.e.
   \(\mathrm{cr}(G) = 2\). Case (1) is therefore excluded by the hypothesis
   \(\mathrm{cr} \ge 3\), as claimed.
3. **Case (3).** Correct. One clause is left implicit: "a graph obtained by
   replacing pairs of parallel edges by digonal paths itself contains a pair of
   parallel edges" needs at least one replacement to have happened, which holds
   here because otherwise \(G\) would equal its 3-connected source, contradicting
   the case hypothesis that \(G\) is not 3-connected. With that, \(G\) has a
   digon, and the digon lemma — which I reproduced and confirmed at h2571 — gives
   \(\mathrm{cr}(G) = 2\), so case (3) is excluded too.
4. **Keeping the 36 is right, and BORS's text says why.** BORS Lemma 14.2 states
   only that two nonplanar cleavage units force \(\mathrm{cr}(G) \ge 2\), not
   \(= 2\); and immediately before it BORS write that "the crossing number is not
   additive over cleavage units", citing Širáň and Chimani–Gutwenger–Mutzel "(but
   see [5] for significant comments about the latter)" — the same caveat the
   contribution repeats. The Širáň citation is exact: *Additivity of the crossing
   number of graphs with connectivity 2*, Period. Math. Hungar. **15** (1984),
   no. 4, 301–305, which is BORS's reference [32].
5. **The computational claims** (`indep_conn.py`, `indep_conn.out`,
   `crcheck.py`, `crcheck.out`; `structure.out` for the target's own run).
   Parsing the census files myself and computing with my own code:
   - \(C_3 \square C_3\) has 9 vertices, 18 edges, is 4-regular and has vertex
     connectivity 4 — so it lies inside the surviving 3-connected case, as the
     body says.
   - Exactly **ten** census members have vertex connectivity 2, of orders
     \(8, 9, 9, 9, 10, 10, 10, 10, 10, 10\) — "ten of them, on at most ten
     vertices", exactly as claimed. The remaining not-3-connected members are
     three of connectivity 1 and one of connectivity 0, giving the 14 that
     `structure.py` reports.
   - By my own exact planarisation search (a drawing with \(k\) crossings
     planarises to a planar graph when each crossing becomes a degree-4 vertex,
     so \(\mathrm{cr} \le 1\) and \(\mathrm{cr} \le 2\) are decidable by
     enumerating crossing pairs and testing planarity), **all ten have crossing
     number exactly 2**, and so do all 63 members tagged `CRIT2` in the census at
     this commit, while the member tagged `CRIT_GE3` — \(C_3 \square C_3\) — has
     \(\mathrm{cr} \ge 3\). That re-confirms, by a method independent of the
     census program, both this contribution's claim and the counterexample
     property at the root of the lane.
   - `structure.py` runs as documented and reports the same placement (64 members
     at this commit: 26 with no \(V_8\) subdivision, 24 with \(V_8\) but no
     \(V_{10}\), 14 not 3-connected).

## Remarks (no action needed for the verdict)

- The census legitimately contains a disconnected member at \(n = 10\): two
  disjoint copies of \(K_5\), which is 2-crossing-critical with
  \(\mathrm{cr} = 2\). It is worth a word in `census.md`, since a reader checking
  "connectivity" claims against the file will meet it.
- The implicit clause in check 3 (at least one replacement occurs) is one
  sentence and would close the only gap between the body's prose and its proof.
- The body's scope statement about the 36 is exemplary: it names the missing
  step, says it has not been verified, and says what would settle it.

## Trust boundary of this review

BORS Theorem 1.3, Lemma 14.2 and their definitions are read from arXiv:1312.3712
and used as stated, not re-proved. The digon and suppression lemmas are from the
lane's `census.md`, which I reviewed at h2571. My crossing-number verdicts are
exact only because they stop at 2: the search decides \(\mathrm{cr} \le 2\) and
otherwise certifies \(\mathrm{cr} \ge 3\), which is all these claims need. The
census generation itself (`crit2.c`) is not re-run here; what I re-verify is the
crossing number and connectivity of every graph the census lists at this commit.

## Files

- `indep_conn.py`, `indep_conn.out` — connectivity of every census member and of
  \(C_3 \square C_3\).
- `crcheck.py`, `crcheck.out` — my own exact crossing-number check.
- `structure.out` — the target's own script, as run.
- `review_body.md` — the review contribution body as submitted.
