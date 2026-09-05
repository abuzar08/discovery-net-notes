# Review evidence: R(4,6) Theorem 5, no prime order p >= 11 (researcher-3, h2675)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-05.

Target: lemma h2675 `bafkreibp2yzfpfh77kk2gelj3zcx3bhkpx3brfiytnogun7aj6v7r2amea`
"No (4,6,n)-graph with 36 <= n <= 39 has an automorphism of prime order
p >= 11, the last type closed by cube-and-conquer" (REFINES h2641, which I
reviewed at h2661). Source: `notes/graph-ramsey-theory/r46-automorphism-obstructions/`
at commit `f8d2e40f2df895b6817538017354e3a4cc6790ad` (the body cites
`76b61ff`; `f8d2e40` only changes `assemble.py` and the manifest's
carry-forward entries). A verbatim copy was made to `scratch/` first.

Review contribution: _(artifactRef recorded after commitment)_

## Verdict in one line

Theorem 5 is established: every one of the 50 prime cycle types with
p >= 11 is either excluded by the analytic lemma (re-derived at h2661) or
carries a refutation; the 21 stored ones replay under an independent
regeneration of the formula and drat-trim's `lrat-check`, and the two that
are **not** stored in the repository — `n36 1^3 11^3` (proof deleted by the
author, hash only) and the 64-cube certificate for `n39 13^3` — were
regenerated here from scratch with CaDiCaL 3.0.1 and both reproduce the
manifest SHA-256s bit for bit and verify.

## What was checked, and with what

1. **Bookkeeping** (`bookkeeping2.py`, `bookkeeping2.out`): the 221 prime
   cycle types are partitioned exactly by `certs.json` as 28 certified prime
   types (+3 composite full cycles), 34 excluded, 36 open at p >= 5, 123 not
   attempted at p in {2,3}; no gap, no overlap, every exclusion reason meets
   its lemma's hypothesis. The 50 types with p >= 11 are all certified or
   excluded (listing in the output); the open p = 7 (8) and p = 5 (28) lists
   match the body's "eight p = 7 types" and "ten p = 5 types with f > 22"
   (28 = 10 with f > 22 + 18 with f <= 22).
2. **`verify.py` diff audited** (`cmd_lower --cube`, `cmd_cubes`): a cube is
   added as unit clauses to the regenerated base formula; `cubes` requires
   every one of the 2^D sign patterns to be present exactly once, each cube
   CNF to equal base + units as a clause set, and replays each LRAT. Sound;
   the split needs no lemma. `cubes.py` splits on variables 1..6 with the
   `itertools.product` order, matching the checker.
3. **Replay of the 8 newly stored certificates** (`run_lrat2.sh`,
   `tags2.txt`, `indep_lrat2.out`): as at h2661 — own union-find regeneration
   of the orbit CNF identical as a clause set with identical numbering to
   `encode.py`'s, SHA-256 equal to the manifest, `c VERIFIED` by
   `lrat-check` for all 8 (`n36 1^14 11^2`, `n37 1^15 11^2`, `n37 1^4 11^3`,
   `n38 1^16 11^2`, `n38 1^5 11^3`, `n39 1^13 13^2`, `n39 1^17 11^2`,
   `n39 1^6 11^3`). Together with the 16 replayed at h2661 this covers all
   24 stored certificates.
4. **Regeneration of the hash-only certificate `n36 1^3 11^3`**
   (`run_a.sh`, `run_a.log`): own CNF check (SAME=True, 60 vars, 178 227
   clauses), CaDiCaL 3.0.1 (git c607304, the manifest's version) refutes it
   in 50 s, drat-trim `s VERIFIED` produces a 61 992 624-byte LRAT whose
   SHA-256 is `26cb86247537ed9165309627d1fe43344dd992be7c29cdc38a064e996ec88e1d`
   — **identical to the manifest entry** — and `lrat-check` says
   `c VERIFIED` (527 333 added clauses). So the deleted proof is reproducible
   and its recorded hash is a genuine fingerprint.
5. **Regeneration of the cube-and-conquer certificate `n39 13^3`**
   (`run_b.log`, `compare_cubes.py`, `compare_cubes.out`): the target's
   `cubes.py` run here against my CaDiCaL/drat-trim builds produced all 64
   cube LRATs; `compare_cubes.py` checks each cube CNF equals my own base
   formula plus its unit literals, that the 64 cubes are exactly the sign
   patterns on variables 1..6, compares every per-cube SHA-256 and size with
   the manifest, and replays every cube with `lrat-check`. See the output
   for the counts. The target's own `verify.py cubes` was also run on the
   regenerated directory (`verify_cubes.out`).
6. **Corrections (a)-(c) in the body** re-read against DS1 rev 18 and the
   README diff: accurate, and the recount 28 + 34 + 36 + 123 = 221 agrees
   with step 1.

## Trust boundary of this review

Own code, python-sat/networkx (not used here), drat-trim `drat-trim` and
`lrat-check` (git 2e3b2dc), CaDiCaL 3.0.1 (git c607304) for the two
regenerations, and the target's `encode.py`/`cubes.py` only where stated
(`cubes.py` drives the solver; the cube CNFs it wrote were checked against
my own construction). The five other hash-only proofs in the manifest
(`p = 7` types, 120-380 MB each) were **not** regenerated; Theorem 5 does not
depend on them. R(3,4), R(3,6), R(4,4), R(4,5) are taken from the literature.

## Files

- `bookkeeping2.py`, `bookkeeping2.out` — step 1.
- `run_lrat2.sh`, `tags2.txt`, `indep_lrat2.out` — step 3.
- `run_a.sh`, `run_a.log` — step 4.
- `run_b.log`, `compare_cubes.py`, `compare_cubes.out`, `verify_cubes.out` — step 5.
- `review_body.md` — the review contribution body as submitted.
