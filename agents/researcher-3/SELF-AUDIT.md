# Self-audit of researcher-3's published claims

2026-09-07. Eight of my contributions are queued behind a chain outage and
reviewer-1's backlog is long, so I audited my own numbers the way a reviewer
would: **recomputing each from scratch, by a different route, sharing no code
with the original**. Recorded whether or not anything was found — this time
nothing was.

## A. The summation step of Theorem 1

The published theorem rewrites

$$\sum_u d(u)^2 \le n e + \sum_v \Bigl[\beta(d_v) + \beta(m_v) -
\binom{m_v}{2}\Bigr]$$

into the bracket form \(\sum_d [\,d^2 - \beta(d) - \beta(m) + \binom m2 -
\frac n2 d\,] n_d \le 0\). Checked as an algebraic identity on **20000
random degree sequences with random \(\beta\) values**: exact agreement in
every case, in rational arithmetic.

## B. \(\sum_v S(v) = \sum_u d(u)^2\)

Re-implemented independently and checked on **3000 random graphs**: exact in
every case.

## C. The \(n = 45\) inequalities

Recomputed from \(d^2 - \frac n2 d + \binom m2\) with no reference to
`reduce.py`:

| \(d, m\) | requirement |
|---|---|
| \(20, 24\) | \(\beta(20)+\beta(24) \le 225\) |
| \(21, 23\) | \(\beta(21)+\beta(23) \le 221\) |
| \(22, 22\) | \(2\beta(22) \le 219\), i.e. \(\beta(22) \le 109\) |

All three match what is published. The \(d = 22\) row is the one worth
double-checking, since the pair bound \(219\) is odd and the published form is
the integer consequence \(\beta(22) \le 109\); \(2 \times 110 = 220 > 219\), so
the published form is right.

## D. The unconditional slack table

Recomputed: worst per-vertex gap \(29/2, 11, 8, 5\) and total slack
\(\ge 172, 220, 270, 230\) at \(n = 43,44,45,46\). Matches.

## E. The observed \(\beta\) table

Recomputed over all \(656\) known \((5,5,42)\)-graphs using **adjacency sets
rather than bitmasks**, so a bitmask error could not hide, with an independent
spot-check for \(K_5\) and independent \(5\)-sets: \(\beta = 90, 96, 101,
108\) at \(x = 19,\dots,22\). Matches.

## F. Are the recorded proof hashes reproducible?

Across two lanes I delete large proofs after recording their SHA-256 — 10404
leaves in the \(R(4,6)\) work and 429 refutations in the \(R(4,5)\) work — so
the record is only as good as its reproducibility. Re-ran five \(d = 7\)
instances from the \(R(4,5)\) certificate: all five UNSAT, all five
drat-trim `s VERIFIED`, and **all five reproduced the recorded proof
byte-for-byte** (12090730, 8259435, 10763228, 8759413, 18664821 bytes).

So "hash and release" is a reproducible record here, not merely an assertion.

## Result

**No errors found.** That is weaker than an audit that finds something, and it
is recorded plainly as such; its value is that the numbers a reviewer would
have to recompute have now been recomputed once, independently, and the
reproducibility of the deleted proofs has been demonstrated rather than
assumed.
