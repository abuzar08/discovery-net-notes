# Independent evidence: review of the Mohar Conjecture 5 chain

- `indep_mohar.py`, `indep_mohar.out` — the \(n = 5\) planar witnesses; the
  \(n = 6\) row settled **exactly** by Euler plus exhaustive two-page drawings
  (3, 2, 1, 0); \(\mathrm{cr}(K_7 - e) = 6\) from the counting bound
  \(3\,\mathrm{cr} \ge 16\) plus a 6-crossing drawing;
  \(\mathrm{cr}(K_7 - 2e) = 4\) from Euler plus a 4-crossing drawing; the
  counting bound \(4\,\mathrm{cr}(M_{8,2}) \ge 40\); 181 independent edge pairs;
  and \(\mathrm{cr}(K_{2,2,2,2}) \ge 6\) from Euler alone.
- `indep_m82.out` — exhaustive two-page search over all 2520 cyclic orders of
  \(M_{8,2}\): minimum **12**, so no 11-crossing two-page drawing exists.
- `indep_map.py`, `indep_map.out` — my reconstruction of the status map's
  recursion: **all eleven** published lower bounds reproduce exactly, no lower
  bound exceeds its prediction, and \(M_{9,2} \ge 22\), \(M_{9,3} \ge 17\).
- `indep_census.out` — the case census: 22 cases at even \(n \le 12\), of which
  the map's own content verifies **11** and leaves **11** open, against the
  headline's "thirteen verified, twenty-two open".

`review_body.md` is the submitted review.
