# Independent evidence: review of the four-connected-hamiltonicity lane

reviewer-1's own code and outputs.

- `indep_ham4.py` — my own filters: graph6 decoding, 4-connectivity by
  exhaustive cut enumeration, Hamiltonicity by an exact subset dynamic
  programme, independence number, and the skewness lower bound
  \(\mathrm{cr} \ge \mathrm{sk}\) implemented as "no three edges planarise it".
- `indep_n9.out` — the \(n = 9\) layer, which the lane's range omits: 11260
  candidates, 10331 four-connected, **9** four-connected non-Hamiltonian, all
  with \(\alpha = 5\) and all with \(\mathrm{cr} \ge 4\).
- `indep_kab.out` — the containment behind the lemma: all nine \(n = 9\)
  survivors contain a spanning \(K_{4,5}\) (so \(\mathrm{cr} \ge 8\)), and all
  seven \(n = 10\) survivors with \(\alpha = 6\) contain \(K_{4,6}\) (so
  \(\mathrm{cr} \ge 12\)).
- `run_n10.sh`, `indep_n10.out`, `n10_survivors.txt` — my complete \(n = 10\)
  census: 705929 read (acceptance criterion fixed before aggregation, passed),
  672249 four-connected, **48** four-connected non-Hamiltonian, every one with
  skewness at least 4 and therefore \(\mathrm{cr} \ge 4\). No counterexample at
  \(n = 10\).

`review_body.md` is the submitted review.
