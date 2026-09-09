# Independent evidence: review of h2711 (Albertson's conjecture at \(r = 28\))

reviewer-1's own code and outputs for the review of researcher-2's proof attempt
"Albertson's conjecture holds for \(r = 28\), independently of the \(r = 27\)
argument", reviewed at the commit that contribution pins, `d0f0230`.

- `indep_28.py`, `indep_28.out` — Part B from scratch: my own crossing-number
  ladder at both seedings, my own dynamic programme for the maximum edges of a
  Gallai forest with blocks of order at most \(r - 2\), the identity
  \(e(L) = m - 27\lvert R\rvert - \sum_v x_v + e(G[R])\), and my own minimisation
  of \(\sum_i \mathrm{cr}(K_{q_i})\) over admissible block multisets. All eight
  rows at \(n = 55\), \(m \in \{768, 769\}\) are impossible under both seedings;
  the tightest margin over \(Z(28) = 7098\) is 256 under the CCCG 2021 seeding
  and **6** under the bare counting seed \(\mathrm{cr}(K_{12}) = 150\).
- `indep_28A.py`, `indep_28A.out`, `n54_survivor.out` — Part A from scratch: my
  own enumeration of the Gallai join decompositions with the subdivision-transfer
  requirement, under **Kostochka–Yancey floors only**. Six of the seven surviving
  orders admit no decomposition inside the edge budget; only \(n = 54\) needs
  more, and its single survivor is \((1,1) + (27,53)\) with floor 754.
- `indep_28_eGR1.out`, `indep_28_sensitivity.out` — Part B under the weakest
  high-set assumption \(e(G[R]) \ge 1\), and a sweep of that floor on the tight
  row \(m = 769\), \(\lvert R\rvert = 6\): the row dies at exactly
  \(e(G[R]) \ge 6\) and survives at 5, on both seedings.
- `pinned.out`, `run.out` — the pinned tree's run (byte-identical to the
  published expected output) and the current head's run, which differs: head's
  ceilings are stronger and leave only \(n = 54\) for the decomposition stage.

`review_body.md` is the submitted review.
