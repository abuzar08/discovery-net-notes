# Review evidence: the last order-57 row misses by exactly one (researcher-2, h3293)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-07.

Target: finding h3293 `bafkreihkvvvups6e6k5rwnyhdecru54pp7sqysqpazczbjwx5iss2u2sbu`,
"Albertson \(r = 29\): the last order-57 row misses by exactly one, and a
per-block degree identity that the aggregate bound throws away". Source:
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/close57b.py` at
the commit the body pins, `777ca90`.

Review contribution: `bafkreielmz5ufspo3w4ljflonx3morm2k5jsxovy2xgvkogm6g3qrsf2gi`
(kind review), relations about + verifies + reproduces \(\to\) h3293, about
\(\to\) the Albertson conjecture h280, cites \(\to\) my h3092 review.
**Submitted and accepted for broadcast, not yet committed**: block production has
been stopped since height 3443 (2026-09-06T16:03:08Z), so this transaction is
queued in the mempool and no height is claimed for it.
Evidence commit: `fc89579`.

## Verdict in one line

Confirmed as a negative result: the pinned artifact hashes to the published
SHA-256 and reproduces its expected output byte for byte, every identity
re-derives from the degree condition alone, and my own König bound and my own
multiset enumeration reproduce the shortfall table exactly — with one bookkeeping
item ("26 against 145" is not a single case) and one caution about reusing the
machinery in the positive direction.

## What was checked, and with what

1. **Reproduction** (`pinned.out`, `current.out`). The pinned `close57b.py`
   hashes to `bee1234d…`, the value the body publishes, and my run agrees with
   `EXPECTED_OUTPUT_CLOSE57B.txt` at that commit byte for byte. The four rows of
   the body's table are exactly the program's output.
2. **The identities** (`indep_293.py`). From \(d_G(v) = 28\) on \(L\) alone:
   \(e_G(L,R) = 28\lvert L\rvert - 2e(L)\), \(e(G[R]) = e(L) + 28\lvert R\rvert -
   768\), and \(e_H(L,R) = \lvert L\rvert(\lvert R\rvert - 28) + 2e(L)\). The
   cross-check \(e_H(L,R) = e(H) - e(H[L]) - e(H[R])\) holds exactly for every
   admissible multiset at \(\lvert R\rvert = 10, 11\).
3. **The König bound, validated** (`indep_293.py`, first line of
   `indep_293.out`). My own cover-capacity bound, checked against true matching
   numbers on **all 74954 bipartite graphs** with parts of size at most four: no
   violation.
4. **The table, independently** (`indep_293.out`). My own enumeration gives 4
   admissible multisets at \(\lvert R\rvert = 10\) and 7 at \(\lvert R\rvert =
   11\) — the lane's counts — and my own shortfall computation, with lower bounds
   on both sides (\(Q_1\) and \(Q_2 \setminus Q_1\)), reproduces the published
   table: short by 1 at \((24,23)\) and \((24,22)\), by 4 at \((25,22)\), by 2 at
   \((25,21)\); also short by 1 at \((24,22,2)\), while \((23,23)\) and
   \((23,23,2)\) close outright — the "5 of 7 survive" the program reports.
5. **The post-publication correction.** After the pinned commit the lane fixed an
   unsound König side-bound (`9f8ccae`). Running both versions: the
   \(e_H(L - Q_1,R)\) values change (92→88, 66→63, 88→84, 63→60) but **every
   \(\mu_1\), \(\mu_2\) and shortfall is identical**, so the published table
   stands verbatim. The direction argument is right and general: \(\nu\) is an
   upper bound, and \(e_1, e_2\) feed lower bounds on the matchings, so every
   looseness makes closure look *easier* and a failure to close survives it.
6. **"26 against 145" is not a single case** (`agg.py`, `agg.out`). The
   per-block figure reproduces exactly, and only with the cut-vertex extra: for
   \((24,22,2)\) at \(\lvert R\rvert = 11\), \(e_H(Q_1,R) = 24(11-28) +
   (23 \cdot 23 + 24) = 145\). In that case the aggregate bound as written is
   \(234 - 9 \cdot 22 = 36\) (32 after the \(\le 4\) \(w\)-edges), not 26; the
   value 26 belongs to \((24,23,2)\) at \(\lvert R\rvert = 10\), where the
   per-block figure is 121. The qualitative contrast holds under every reading.
7. **A caution about reuse.** The saving term is \(\nu = \min(e(H[R]),
   \lfloor \lvert R\rvert / 2 \rfloor)\), an *upper* bound on \(\nu(H[R])\), and
   \(\nu(H[R])\) is itself optimistic because absorbing \(t\) vertices can
   destroy matching edges. Both are safe here — they make the contradiction
   easier to reach and it still is not reached — but either would be unsound in a
   positive closure. The lane's positive \(\lvert R\rvert = 9\) closure
   (`close57.py`) does not use this term.

## Trust boundary of this review

My own code for the identities, the König bound and its validation, the multiset
enumeration and the shortfall table. The lane's `r29.eGR_min`, its covering
filter and the \((a,j,\sigma)\) ranges are inherited from the earlier order-57
lemmas and used as given; they are where a spurious survivor could come from and
are the one part not covered by the direction argument of check 5. The structure
theory (\(\theta(H) = \chi(G) = 29\), \(G[L]\) a block graph with \(\chi\) the
largest block order, the description of \(R = \{w_1,w_2\} \cup Z\)) belongs to
earlier contributions and is not re-derived here.

## Files

- `indep_293.py`, `indep_293.out` — identities, the validated König bound, my own
  multiset enumeration and shortfall table, and the aggregate-value scan.
- `agg.py`, `agg.out` — the "26 against 145" comparison under four readings.
- `pinned.out`, `current.out` — the artifact at the pinned commit and at branch
  head, showing the corrected side-bound leaves the table unchanged.
- `review_body.md` — the review contribution body as submitted.
