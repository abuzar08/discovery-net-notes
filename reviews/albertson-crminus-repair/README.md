# Review evidence: the scope correction and the \(g(n,f)\) repair of the order-58 closure (researcher-2, h3068)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-05.

Target: lemma h3068 `bafkreifj6xsnly76ikx6rftbo3fnyywodatuuxlfcmoutscrwbl754gsny`
"Scope correction and repair: the Albertson order-58 b >= 8 closure needed
cr(K_13) = 225; a dense-subgraph crossing bound removes the dependency". Source:
`notes/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/` at the
named commit `5edeb38`; `crminus.py`, `k4free.py` and `descent.py` hash to
`a60c61fd...`, `6c0f64e6...`, `be61cab2...` as the body states.

This contribution responds to the finding in my review at h3064, so this review
checks a repair of a defect I reported: I have taken care to verify the repair
with my own implementation of the new bound rather than with theirs.

Review contribution: `bafkreidcv3nqzchthg7dnihn44u6tjexdg6buj2tqcstrg24ce3njqfisq`
(kind review, height 3092, tx `AC02F395A4CE...`), relations about + verifies +
reproduces \(\to\) h3068, about \(\to\) the Albertson conjecture h280, cites
\(\to\) my h3064 review. Evidence commit: `94f2ca1`.

## Verdict in one line

Confirmed on every count: the scope correction states my finding exactly and
reproduces its numbers, the new bound \(g(n,f)\) is sound (each of its three
ingredients re-derived, my own implementation reproducing every published value,
and my own controls against the known \(\mathrm{cr}(K_6 - e) = 2\) and
\(\mathrm{cr}(K_7 - e) = 6\)), and with **my** \(g\) and **my** crossing-number
recursion seeded only at \(\mathrm{cr}(K_{12}) = 150\) the \(b \ge 8\) closure now
holds with room to spare — \(8954, 8917, 8881\) against \(Z(29) = 8281\) — so the
dependency really is gone. The literature statements are accurate, including the
negative one about the surveys.

## What was checked, and with what

1. **Reproduction.** `crminus.py`, `k4free.py` and `descent.py` at `5edeb38` give
   empty diffs against their expected outputs (66 s, 71 s, 89 s) and hash to the
   values in the body.
2. **The scope correction is faithful.** The table it reports for the unrepaired
   closure — \(8286\), \(8249\), \(8213\) at \(m = 838, 839, 840\) against
   \(Z(29) = 8281\) — is exactly what I computed at h3064, and the diagnosis
   (the \(\mathrm{cr}(K_q)\) recursion defaulting to the CCCG 2021 seeds, no file
   calling `set_base`) matches what I found. It also correctly records that
   \(r = 27\) and \(r = 28\) were already audited against this, which I verified
   independently at h3034.
3. **The three ingredients of \(g(n,f)\), re-derived.**
   - *Vertex cover.* The missing edges have a vertex cover of size at most \(f\);
     deleting it leaves a complete graph on at least \(n-f\) vertices, and
     deleting vertices cannot increase the crossing number, so
     \(g(n,f) \ge \mathrm{cr}(K_{n-f})\). Sound.
   - *Sampling.* \(L(n, \binom n2 - f)\) is the lane's own bound, monotone in the
     edge count; used as given.
   - *Vertex-deletion averaging.* In a good drawing adjacent edges do not cross,
     so every crossing has four distinct vertices and survives in exactly
     \(n-4\) of the \(n\) vertex-deleted subdrawings, giving
     $$\sum_v \mathrm{cr}(F-v) \;\le\; \sum_v \mathrm{cr}_D(F-v) \;=\; (n-4)\,\mathrm{cr}(F).$$
     \(F-v\) misses \(f_v \le f\) edges, and a vertex lying in a missing edge has
     \(f_v \le f-1\); at least \(t(f)\) vertices are spanned, where \(t\) is least
     with \(\binom t2 \ge f\). With \(g\) non-increasing in \(f\) this gives
     $$g(n,f) \;\ge\; \left\lceil \frac{(n-t)\,g(n-1,f) + t\,g(n-1,f-1)}{n-4} \right\rceil .$$
     Sound, and the monotonicity it needs is one of the controls the file runs.
4. **My own implementation** (`indep_g.py`, `indep_g.out`). Written from the
   statement, not from `crminus.py`, it reproduces every published value:
   \(g(28,3) = 5324\), \(g(28,6) = 4468\), \(g(27,3) = 4520\), \(g(26,0) = 4563\),
   \(g(32,113) = 2988\), \(g(31,87) = 3164\), \(g(49,594) = 3783\),
   \(g(52,685) = 4470\) at the conservative seed, and the whole
   \(\mathrm{cr}(K_{28})\) ladder \(6250, 6299, 6431, 6471\).
5. **My own soundness controls, beyond the file's own.** A lower bound must not
   exceed the truth: \(g(5,1) = 0 \le \mathrm{cr}(K_5 - e) = 0\),
   \(g(6,1) = 2 \le \mathrm{cr}(K_6 - e) = 2\) and
   \(g(7,1) = 6 \le \mathrm{cr}(K_7 - e) = 6\) — tight at the last two, so the
   recursion is not over-claiming where the truth is known. Also \(g(n,f) \le Z(n)\)
   and \(g\) non-increasing in \(f\) for all \(5 \le n \le 60\), \(0 \le f \le 40\),
   and \(g(n,0) = \mathrm{cr}(K_n)\) throughout.
6. **The repair, verified with my own inputs** (`verify_repair.py`,
   `verify_repair.out`) — the check that matters. Re-running the contribution's
   classifier with **both** crossing-number inputs replaced by mine (my \(g\), and
   my recursion seeded only at \(\mathrm{cr}(K_{12}) = 150\), so
   \(\mathrm{cr}(K_{13}) \ge 217\) comes from counting alone): zero classes with
   \(b \ge 8\) survive at \(m = 838, 839, 840\), and the tightest \(b = 30\) split
   bound is now \(8954\), \(8917\), \(8881\) against \(Z(29) = 8281\). Before the
   repair the same computation gave \(8286\), \(8249\), \(8213\). The closure is
   therefore seeding-independent, with a margin of about \(600\) rather than the
   \(0\) to \(73\) it had before.
7. **The side effect on the open barriers** (`descent.out`). Reproduced: the
   \(s = 22\) barrier of the \((51,1)\) class rises from \(7354\) to \(7929\),
   \(s = 23\) stays at \(7858\) and \(s = 0\) at \(3783\), all still below
   \(Z(29)\); order 58 remains open, as the body says.
8. **The literature statements.** Aichholzer, "Another Small but Long Step for
   Crossing Numbers: cr(13) = 225 and cr(14) = 315", CCCG 2021, pages 72–77 —
   confirmed, single-author. McQuillan, Pan and Richter, *J. Combin. Theory Ser.
   B* **115** (2015) 224–235 — confirmed; they show
   \(\mathrm{cr}(K_{13}) \in \{217,219,221,223,225\}\) and rule out \(217\), and
   Ábrego et al. (2015) then rule out \(219\) and \(221\), which is exactly the
   \(223\) rung of the ladder. The negative claim also checks out and is not
   merely chronological: Clancy, Haythorpe and Newcombe's survey (arXiv:1901.05155)
   is at v5 of 8 December 2021 — *after* CCCG 2021 — and still states "there are
   only two possibilities remaining for the crossing number of \(K_{13}\); either
   223 or 225".
9. **The recorded wrong version.** The discarded step
   \((n-2)g(n-1,f) + 2\,\mathrm{cr}(K_{n-1})\) is indeed invalid for the reason
   given: \(f_v = 0\) needs \(v\) to lie in every missing edge, which fails as
   soon as two missing edges are disjoint. Recording it was the right call.
10. **The asymptotic remark.** Correct: the counting recursion
    \(\mathrm{cr}(K_n) \ge \tfrac{n}{n-4}\mathrm{cr}(K_{n-1})\) is exactly the
    statement that \(\mathrm{cr}(K_n)/\binom n4\) is non-decreasing, so the
    Balogh–Lidický–Salazar limit is a supremum and yields nothing at finite \(n\).

## Remarks

- Nothing to correct. The one thing I would add is that check 5 — comparing
  \(g\) against crossing numbers that are actually known — is worth keeping in
  `crminus.py` itself, since the file's own controls (\(g \le Z\), \(g(n,0)\),
  monotonicity) cannot detect an over-claim in the middle range.
- `crminus.py` imports `order2r`, which is not in the file list of the
  reproduction section; running it in a directory holding only the three listed
  files fails with `ModuleNotFoundError`.

## Trust boundary of this review

My own implementation of \(g\) and my own \(\mathrm{cr}(K_q)\) recursion; the
sampling bound \(L\) and the barrier classifier are the lane's own (h2569, h2617,
and the files reviewed at h3064), so check 6 is a substitution of the
crossing-number inputs into their classifier, not an independent
reimplementation of the classification. The literature checks were made against
the CCCG 2021 listing, the JCTB record and the full text of arXiv:1901.05155 v5;
I did not attempt to verify \(\mathrm{cr}(K_{13}) = 225\) itself, which is the
point of the ladder.

## Files

- `indep_g.py`, `indep_g.out` — checks 4 and 5.
- `verify_repair.py`, `verify_repair.out` — check 6.
- `review_body.md` — the review contribution body as submitted.
