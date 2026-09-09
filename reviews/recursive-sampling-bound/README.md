# Independent evidence: review of h2713 (the recursive integer-aware sampling bound)

reviewer-1's own code and outputs.

- `indep_2713.py`, `indep_2713.out` — my own implementation of the bound from
  the lemma statement alone (base, lower convex envelope, recursion, exact
  arithmetic), built bottom-up to \(n = 54\). All seven worked values agree, as
  do \(L(5,10) = 1\), \(L(6,15) = 3\) and \(73335\) at \(K_{54}\); it also gives
  \(L(32,383) = 3022\) and \(L(32,496) = 8336\), the incumbent values of the
  height-3285 lane. Includes my own soundness suite (complete, complete
  bipartite against Zarankiewicz, \(K_a\) plus isolates, disjoint unions,
  monotonicity, vanishing below \(3n-6\)) — all pass.
- `indep_adv.py`, `indep_adv.out` — a soundness family the published suite does
  not contain: explicit two-page drawings at 36 pairs \((n,q)\) spanning
  densities 0.55 to 1.0 for \(n\) up to 32, which is where the bound is actually
  used. No violation.
- `indep_arith.out` — the stated coincidences checked exactly: both
  Büngener–Kaufmann bounds equal \(1474/9\) at \((24,132)\), the amplification
  factors \(16450/759\) and \(27/25\), and the telescoping identity.

`review_body.md` is the submitted review.
