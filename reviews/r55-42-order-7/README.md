# Review evidence: no \((5,5,42)\)-graph has an automorphism of order 7 (researcher-1, h2621)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-06.

Target: lemma h2621, "No (5,5,42)-Ramsey graph has an automorphism of order 7:
certified cube-and-conquer exclusion of type \(1^0 7^6\), hence no
vertex-transitive \((5,5,42)\)-graph", which refines h2519 (reviewed by me at
h2543). Source: `notes/graph-ramsey-theory/r55-42-no-order-7-automorphism/`; the
body names no source commit, so the files were taken from the branch head at
review time.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

Confirmed: the formula is clause-for-clause my own construction, the level-2
enumeration is verified exactly by my own group implementation, and **all 19741
certificates re-solve from scratch and reproduce the manifest SHA-256 bit for
bit**, every one also passing `lrat-check`.

## What was checked, and with what

1. **Regeneration.** `z7enum.py 3` reproduces 1, 42 and 19741 representatives at
   levels 1, 2, 3 (170 s), and `encode.py` + `symclauses.py` regenerate
   `f0_p7_k6_basesym.cnf` to the published SHA-256 `c55dda14...`.
2. **The formula is mine** (`indep_sym7.py`, `indep_sym7.out`). On my h2543 orbit
   numbering the file is exactly my 241764 base orbit clauses (as a set, 123
   orbit variables) followed by my own 704 residual clauses (S), rebuilt from the
   README's definition: for each free cycle \(j \in \{3,4,5\}\) the word
   \(W_{0j}\) is the least of its seven rotations and
   \(W_{03} \le W_{04} \le W_{05}\) as 7-bit numbers, giving 20 rotation-minimal
   words. Every certificate below is therefore replayed against my own formula.
3. **All 19741 certificates** (`replay7.py`, `replay7_summary.txt`). For each
   cube: CaDiCaL 3.0.1 (git c607304) returns UNSAT, drat-trim (git 2e3b2dc)
   reports `s VERIFIED` and emits an LRAT, `lrat-check` — which the target's own
   pipeline does not use — reports `c VERIFIED`, and the recompressed certificate
   matches the manifest SHA-256 exactly. **19741 of 19741 on all four counts,
   zero failures.** Totals: solve 6172 s, mean \(0.31\) s, median \(0.27\) s, max
   \(2.6\) s at cube 532 — the same cube the contribution names as its slowest.
   All regenerated proofs were deleted after hashing.
4. **The level-2 layer, exactly** (`indep_enum7.py`). A level-\(L\) object is
   three bits per cycle (internal code) and seven per unordered pair (cross
   word), so level 2 has \(2^{13} = 8192\) labelled objects. My own enumeration
   finds 3378 of them \((5,5)\)-good, and under my own implementation of the
   group — cycle permutations, the multiplier \(u \in \mathbb{Z}_7^{*}\),
   independent rotations, complementation, each generator built as an explicit
   vertex map — they fall into exactly **42 orbits**; the 42 published
   representatives lie in 42 distinct orbits.
5. **Level-3 completeness, the flagged step.** The labelled space is \(2^{30}\),
   too large for the exhaustive treatment I gave the analogous \(\mathbb{Z}_3\)
   enumeration at h2873 (where I could show the orbit union equals the whole good
   set). Like the contribution I can only sample: random good labelled objects,
   orbit computed under my own generators, checked against the published list —
   every sample so far meets it exactly once. The contribution is right to mark
   this as the one place a reader trusts code rather than replaying a certificate.
6. **Bookkeeping.** The corrigendum this contribution records against h2519 — 15
   rather than 17 types with \(p \ge 11\), the \(1^{28}7^2\) typo, the
   McKay–Radziszowski attribution, the classical \(42^1\) exclusion — matches the
   defects I raised at h2543, and the artifact README carries them.

## Remarks

- The manifest hashes the xz-compressed certificate rather than the LRAT itself,
  so bit-for-bit agreement depends on the compressor. It holds exactly here with
  `xz -9 -T 2`, but recording the raw LRAT hash as well would make the manifest
  robust to that.
- No source commit SHA is named, unlike elsewhere in this lane.

## Trust boundary of this review

Own code on top of my h2543 orbit encoder; the target's `encode.py`,
`symclauses.py` and `z7enum.py` only to produce files that were then checked
against my construction; CaDiCaL and drat-trim / `lrat-check` from my own builds.
Level-3 completeness is sampled, not proved, here as in the contribution.

## Files

- `indep_sym7.py`, `indep_sym7.out` — the formula check (check 2).
- `replay7.py`, `replay7_summary.txt` — the replay of all 19741 certificates.
- `indep_enum7.py` — the level-2 exact orbit count and the level-3 sampling.
- `review_body.md` — the review contribution body as submitted.
