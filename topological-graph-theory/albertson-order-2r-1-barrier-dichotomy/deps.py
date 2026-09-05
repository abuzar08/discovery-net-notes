#!/usr/bin/env python3
"""
The r = 27 chain does not need Sadhu Theorem 1.3, and Barat-Toth Corollary 5
simplifies the r = 28 order reduction.

Exact integer / Fraction arithmetic only; no floating-point value enters any
comparison.  Imports recursive.py and verify_range.py.

--------------------------------------------------------------------------
THE TWO BARAT-TOTH BOUNDS, read verbatim from the EJC PDF of

    J. Barat and G. Toth, "Towards the Albertson conjecture",
    Electronic Journal of Combinatorics 17 (2010) #R73.

  Corollary 5.  "Let r, p be integers, r >= 4 and 2 <= p <= r-1.  If G is an
    r-critical graph with n vertices and m edges, where n = r+p, and G does not
    contain a topological K_r, then 2m >= (r-1)n + p(r-p) - 1."
    (The paper calls this the Gallai bound.)

  Corollary 7.  "Let r be a positive integer, r >= 4, and let G be an r-critical
    graph.  If G does not contain a topological K_r, then 2m >= (r-1)n + (2r-6)."
    (The paper calls this the Kostochka, Stiebitz bound.  No restriction on n.
    This is exactly the inequality Cranston quotes as his Lemma E and Sadhu as
    Lemma 2.5, so those three citations are one result.)

  Corollary 11.  "Any r-critical graph on at most r+4 vertices satisfy the Hajos
    conjecture."  (Hence it contains a topological K_r; this is Cranston's
    Lemma C.)

All three are journal-published, so the edge floors and the small-order
exclusion do not rest on a preprint.

--------------------------------------------------------------------------
PART 1 -- the r = 27 order reduction without Sadhu Theorem 1.3.

Sadhu Thm 1.3 (a 2026 preprint) was the one input of the r = 27 chain that was
both essential and preprint-only: it supplied |G| in {53,54} together with the
connected complement that Stehlik needs.  It can be dropped.

  n <= r+4 = 31          Barat-Toth Corollary 11: G has a topological K_27.
  32 <= n <= 54          floor max(Kostochka-Yancey, BT Cor 7, BT Cor 5) against
                         the recursive integer-aware sampling ceiling: only
                         n = 52 and n = 53 survive.
  55 <= n <= 171         the single-level sampled bound already exceeds Z(27) at
                         the floor, so every such order is excluded.
  n >= 77                Cranston's band |G| >= 2.82r for a minimum
                         counterexample.  (Overlaps the previous line, so the
                         two together cover every n; Cranston is now used only
                         far from where it is tight.)

PART 2 -- both surviving orders.

  n = 52 = 2r-2:  Gallai (Sadhu Lemma 2.8) makes the complement disconnected, so
                  the Gallai join decomposition applies.  No decomposition fits
                  the edge budget, so the order is impossible.
  n = 53 = 2r-1:  if the complement is disconnected the same join argument
                  applies and again nothing fits; if it is connected, Stehlik
                  applies and the chain of r27.py finishes the job.
  So the connected-complement hypothesis is now derived, not assumed.

In the join step the Kostochka-Yancey floor is used for every part, and the
stronger no-topological-clique floor max(BT Cor 5, BT Cor 7) for ONE part only:
if every part contained a topological K_{r_i}, joining those subdivisions would
give a topological K_r in G, so at least one part contains none.  Parts with
r_j <= 3 always contain one, so the stronger floor is attributed to a part with
r_j >= 4.

PART 3 -- Corollary 5 simplifies the r = 28 order reduction: it alone closes
orders 33, 34, 50, 51, 52 and 53, so the join argument is needed only at n = 54.
--------------------------------------------------------------------------
"""
import recursive as R
import verify_range as V

NMAX = 80
_L = R.build(NMAX, rounds=3)


def ky(r, n):
    if r <= 1:
        return 0
    if r == 2:
        return 1
    return -(-((r + 1) * (r - 2) * n - r * (r - 3)) // (2 * (r - 1)))


def cor7(r, n):
    return -(-(n * (r - 1) + 2 * (r - 3)) // 2)


def cor5(r, n):
    p = n - r
    if not (2 <= p <= r - 1):
        return 0
    return -(-((r - 1) * n + p * (r - p) - 1) // 2)


def floor_of(r, n):
    return max(ky(r, n), cor7(r, n), cor5(r, n))


def ceiling_of(r, n):
    Z = V.Z(r)
    return max([q for q in range(len(_L[n])) if _L[n][q] < Z], default=-1)


def single_level_ok(r, n):
    """True if the single-level integer-aware sampled bound at the edge floor
    already reaches Z(r), so the order is excluded without the recursive table."""
    m = floor_of(r, n)
    Z = V.Z(r)
    return any(V.sample_bound(m, n, k) >= Z for k in range(4, min(n, 60) + 1))


def join_survivors(r, n, mhi):
    live = []

    def rec(rrem, vrem, minr, cur):
        if rrem == 0:
            if vrem != 0 or len(cur) < 2:
                return
            eM = (n * n - sum(v * v for _, v in cur)) // 2
            kys = sum(ky(ri, vi) for ri, vi in cur)
            deep = [(rj, vj) for rj, vj in cur if rj >= 4]
            if not deep:
                return
            need = min(eM + kys - ky(rj, vj) + max(ky(rj, vj), floor_of(rj, vj))
                       for rj, vj in deep)
            if need <= mhi:
                live.append((sorted(cur, reverse=True), eM, need))
            return
        for ri in range(minr, rrem + 1):
            if ri == 2:
                continue
            if ri == 1:
                if vrem >= 1:
                    rec(rrem - 1, vrem - 1, 1, cur + [(1, 1)])
                continue
            for vi in range(2 * ri - 1, vrem + 1):
                if ky(ri, vi) > mhi:
                    break
                rec(rrem - ri, vrem - vi, ri, cur + [(ri, vi)])
    rec(r, n, 1, [])
    return live


def main():
    print("Dependency reduction for the Albertson r = 27 and r = 28 chains")
    print("Exact arithmetic; no floating-point value enters any comparison.")
    print()

    r = 27
    print("PART 1   r = 27 orders, WITHOUT Sadhu Thm 1.3 and without Cranston's bands")
    print("   n <= %d: Barat-Toth Corollary 11 (a topological K_%d)" % (r + 4, r))
    surv = []
    for n in range(r + 5, NMAX + 1):
        lo, hi = floor_of(r, n), ceiling_of(r, n)
        if lo <= hi:
            surv.append((n, lo, hi))
    print("   %d <= n <= %d, recursive ceiling: surviving orders %s"
          % (r + 5, NMAX, [t[0] for t in surv]))
    for n, lo, hi in surv:
        print("        n=%d: m in [%d, %d]  (%d row%s)"
              % (n, lo, hi, hi - lo + 1, "" if hi == lo else "s"))
    assert [t[0] for t in surv] == [52, 53]
    bad = [n for n in range(55, 172) if not single_level_ok(r, n)]
    print("   55 <= n <= 171, single-level sampled bound at the floor: %s"
          % ("every order excluded" if not bad else "FAILS at %s" % bad))
    assert not bad
    print("   n >= 77: Cranston's band, which covers everything beyond 171 too.")
    print()

    print("PART 2   the two surviving r = 27 orders")
    for n, lo, hi in surv:
        live = join_survivors(r, n, hi)
        tag = ("2r-2, so Gallai forces a disconnected complement"
               if n == 2 * r - 2 else "2r-1, so the complement may be connected")
        print("   n=%d (= %s):" % (n, tag))
        print("      join decompositions fitting the edge budget m <= %d: %d %s"
              % (hi, len(live), "-> the disconnected case is impossible"
                 if not live else live[:2]))
        assert not live
    print("   n=52 is therefore impossible outright; at n=53 the complement must be")
    print("   connected, which is exactly the hypothesis Stehlik needs, and r27.py")
    print("   closes the single remaining row (53, 713).")
    print()

    print("PART 3   Corollary 5 at r = 28")
    r = 28
    for n in (33, 34, 50, 51, 52, 53, 54, 55):
        a, b, c = ky(r, n), cor7(r, n), cor5(r, n)
        hi = ceiling_of(r, n)
        old, new = max(a, b), max(a, b, c)
        print("   n=%2d  KY %4d  Cor7 %4d  Cor5 %4d  ceiling %4d   rows %2d -> %d%s"
              % (n, a, b, c, hi, max(0, hi - old + 1), max(0, hi - new + 1),
                 "   <- closed by Corollary 5" if old <= hi < new else ""))
    print("   so only n = 54 and n = 55 survive, and the join argument is needed")
    print("   only at n = 54.")


if __name__ == "__main__":
    main()
