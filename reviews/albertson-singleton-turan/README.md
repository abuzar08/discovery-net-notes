# Independent evidence: review of the singleton-\(w\) Turán sharpening (order 58, \(r = 29\))

- `indep_wturan.py`, `indep_wturan.out` — my own \(K_4\) search over nauty's
  complete generation confirming the \(K_4\)-free maximum \(\lfloor n^2/3
  \rfloor\) for \(n \le 9\) and the Turán construction for \(10 \le n \le 59\);
  the sharpening \(\lfloor n^2/3 \rfloor - \lfloor (n-1)^2/3 \rfloor - 4\) over
  the whole range, positive exactly from \(\lvert R\rvert = 8\); and the
  arithmetic of the configuration that exposed the lemma.

The published `wturan58.py` was also run: its hash matches `SHA256SUMS` and its
output is byte-identical to `EXPECTED_OUTPUT_WTURAN58.txt`.

`review_body.md` is the submitted review.
