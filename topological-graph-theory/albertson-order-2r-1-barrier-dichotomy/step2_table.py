#!/usr/bin/env python3
"""
Step 2 of the r = 27 elimination, made hand-auditable.

The barrier classification at (n, m) = (53, 713) is a machine enumeration, and
the clean-room reproduction at ledger height 2673 identified it as the part a
referee cannot check by reading.  This script exposes it as a finite table.

The degree-deficiency filter alone -- for a component C of H - B and v in C,
N_H(v) is inside (C\\{v}) u B, so d_H(v) <= |C|-1+b and x_v >= r-|C|-b, and
sum_v x_v = 2m - n(r-1) -- cuts 839685 component multisets down to 34.  Those 34
are printed below with the reason each is excluded, so the whole of Step 2 can be
checked one line at a time.

Reasons, in the order applied:
  deficiency    sum_C |C| max(0, r-|C|-b)  >  sum_v x_v          (elementary)
  e_G(D,B)      the exact identity
                  e_G(D,B) = |D|(b-r+1) + sum_{v in D} x_v + 2 sum_C e(H[C])
                bounds it above, while delta(G) >= r-1 bounds it below by
                max(b*max(0,r-b), |D|*max(0,r-|D|))                (elementary)
  TK_r          the number of components is >= r, so G[D] contains K_r
  Kleitman      distinct components are complete to each other in G, so G
                contains K_{a,|D|-a}; the counting bound
                cr(K_{a,c}) >= a(a-1)/30 * cr(K_{6,c}) exceeds Z(r)
  split         cr(G) >= cr(G[D]) + cr(G[B]) exceeds Z(r)

Of the 34, nineteen fall to the elementary e_G(D,B) count and one to TK_r; only
eleven need a crossing-number argument.  Three survive: two with b = 3, both
killed by the non-domination lemma because there B = T is a clique, and
(b, multiset) = (4, 47+1+1), which is the configuration Steps 3-5 then use.
"""
from collections import Counter

import recursive as R
import verify_range as V

N, RCHI, M = 53, 27, 713
X = 2 * M - N * (RCHI - 1)
EH = N * (N - 1) // 2 - M
_L = R.build(59, rounds=3)


def cr_lower(n, q):
    if n < 4 or q <= 0 or n > 59:
        return 0
    return _L[n][min(q, len(_L[n]) - 1)]


for _f in (V.controls, V.analyse, V.tri_free_survivors):
    _f.__globals__['cr_lower_nm'] = cr_lower


def fmt(c):
    return " ".join("%d^%d" % (k, v) if v > 1 else "%d" % k
                    for k, v in sorted(Counter(c).items(), reverse=True))


def reason(b, c):
    """Why this component multiset is impossible, or None if it survives."""
    Z = V.Z(RCHI)
    D, CB = sum(c), b * (b - 1) // 2
    if V.best_bipartition(list(c)) > Z:
        return "Kleitman"
    up = D * (b - RCHI + 1) + X + 2 * sum(s * (s - 1) // 2 for s in c)
    if max(b * max(0, RCHI - b), D * max(0, RCHI - D)) > up:
        return "e_G(D,B)"
    if len(c) >= RCHI:
        return "TK_r"
    Ymin = sum(s * max(0, RCHI - s - b) for s in c)
    Pmin, Pmax = sum(s - 1 for s in c), sum(s * (s - 1) // 2 for s in c)
    best = None
    for Y in range(Ymin, X + 1):
        Q = min(CB, Pmax - D * (RCHI - 1) + Y + EH)
        if Q < 3:
            continue
        P = D * (RCHI - 1) - Y - EH + Q
        if not (Pmin <= P <= Pmax):
            continue
        crD = max(V.crK(len(c)), cr_lower(D, D * (D - 1) // 2 - P),
                  V.best_bipartition(list(c)))
        eB = CB - Q
        t = crD + (cr_lower(b, eB) if eB > 0 else 0)
        if best is None or t < best:
            best = t
    if best is None or best > Z:
        return "split (%s > %d)" % (best, Z)
    return None


def main():
    print("Step 2 at (n, m) = (%d, %d), r = %d:  sum_v x_v = %d,  Z(r) = %d"
          % (N, M, RCHI, X, V.Z(RCHI)))
    print()
    gross = sum(len(V.configs(N - b, b - 1, RCHI - b, 10 ** 9))
                for b in range(3, N + 1) if N - b >= b - 1)
    rows = []
    for b in range(3, N + 1):
        if N - b < b - 1:
            continue
        for c in V.configs(N - b, b - 1, RCHI - b, X):
            rows.append((b, fmt(c), len(c), reason(b, c)))
    print("degree-deficiency filter: %d component multisets in, %d out"
          % (gross, len(rows)))
    print()
    print("   b   components of H-B                #parts   excluded by")
    for b, c, k, w in sorted(rows):
        print("  %2d   %-32s %5d    %s" % (b, c, k, w or "SURVIVES"))
    print()
    tal = Counter(w.split()[0] if w else "SURVIVES" for _, _, _, w in rows)
    print("summary: " + ", ".join("%s %d" % (k, v) for k, v in sorted(tal.items())))
    live = [(b, c) for b, c, _, w in rows if w is None]
    print("survivors: %s" % live)
    print("  the two with b = 3 are killed by the non-domination lemma, because")
    print("  there B = T is a triangle, hence a clique, so every vertex of N_H(w)")
    print("  dominates the rest; (4, '47 1^2') is the configuration used in Steps 3-5.")
    assert [b for b, _ in live] == [3, 3, 4]
    assert live[2][1] == "47 1^2"
    b3 = [c for b, c in live if b == 3]
    assert all("1" in c for c in b3), "a surviving b=3 multiset has no singleton"


if __name__ == "__main__":
    main()
