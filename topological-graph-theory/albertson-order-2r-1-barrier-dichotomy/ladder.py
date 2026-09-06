#!/usr/bin/env python3
"""
Seed-ladder audit of the whole order-58 chain at r = 29.

WHY.  The cr(K_q) recursion in verify_range.py is seeded by published exact
values, and which values one is willing to assume is a real choice: see the
ladder in verify_range.py for the citations.  A previous pass discovered that
the "b >= 8" closure had silently defaulted to the strongest rung, and reopened
at the weakest (b = 30 survived at 8249 for m = 839 and 8213 for m = 840).  That
was repaired with crminus.py.  This file audits the REST of the chain the same
way, so that no part of the order-58 argument rests on an undeclared assumption.

THE THREE PIECES OF THE ORDER-58 ARGUMENT.

  PIECE 1 (ledger height 2933, order2r.py PART 2).  Order 58 is impossible
     whenever H contains a K_4, i.e. whenever alpha(G) >= 4.  The K_4 route
     gives o(H - B) >= b - 2; the classification leaves b = 4 (killed at once,
     since there B is the K_4 itself, a clique, which non-domination forbids
     once H - B has a singleton component) and b = 5, which is killed row by
     row over |R| by either the Gallai-forest edge cap or the split bound.
     Only the split bound uses cr(K_q), so only it can be seed-sensitive.

  PIECE 2 (ledger height 3014, order2r.py PART 3).  Order 58 is impossible
     whenever H has no two disjoint triangles: H minus a Stehlik triangle is
     then triangle-free, Cauchy-Schwarz produces an edge of high degree sum,
     and its two endpoints' neighbourhoods are disjoint cliques of G.

  PIECE 3 (ledger height 3014, repaired at height 3068, k4free.py).  In the
     remaining branch -- H is K_4-free AND has two disjoint triangles -- every
     class with b >= 8 is impossible.

Pieces 1, 2 and 3 together reduce order 58 to exactly three classes, b = 6 with
(51,1) and (50,1,1) and b = 7 with (49,1,1), which remain OPEN.

WHAT THIS FILE REPORTS.  Each piece, re-run at all four rungs of the ladder.
Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import crminus as CM
import order2r as O
import k4free as K

r = O.RCHI
n = 2 * r
Z = O.Z
ROWS = (838, 839, 840)


def piece1(m):
    """PART 2: the b = 5 table.  Returns (rows killed by the Gallai cap,
    rows killed by the split bound, rows killed by neither)."""
    X = 2 * m - n * (r - 1)
    gal, spl, bad = 0, 0, []
    for Rsz in range(2, 2 + (X - (2 * r - 6)) + 1):
        VL = n - Rsz
        eL = m - ((r - 1) * Rsz + X) + O.eGR_2r(Rsz)
        cap = O.gallai_cap(VL, r - 2)
        sp = O.min_split(VL, eL)
        g_ok = eL > cap
        s_ok = sp is not None and sp > Z
        if g_ok:
            gal += 1
        if s_ok:
            spl += 1
        if not (g_ok or s_ok):
            bad.append((Rsz, eL, cap, sp))
    return gal, spl, bad


def piece2(m):
    """PART 3: the minimum of cr(K_a) + cr(K_b) over the forced degree sum."""
    nf = 2 * r - 3
    eH = n * (n - 1) // 2 - m
    eF = eH - (3 * r - 3)
    thr = -(-4 * eF // nf)
    return min(V.crK(a) + V.crK(thr - a)
               for a in range(1, r + 1) if 1 <= thr - a <= r)


def piece3(m):
    """k4free: how many classes with b >= 8 survive."""
    live, _ = K.branch_survivors(m, use_gallai=True)
    return [t for t in live if t[0] >= 8]


def main():
    print("Seed-ladder audit of the order-58 chain at r = %d" % r)
    print("Z(%d) = %d;  a counterexample has cr(G) <= %d" % (r, Z, Z - 1))
    print()
    print("The rungs, weakest first, with sources in verify_range.py:")
    for name, _ in V.SEED_LADDER:
        print("   %s" % name)
    print()

    allok = True
    for name, base in V.SEED_LADDER:
        V.set_base(base)
        CM.reset()
        print("RUNG: %s     cr(K_27) >= %d, cr(K_28) >= %d"
              % (name, V.crK(27), V.crK(28)))

        bad1 = []
        for m in ROWS:
            gal, spl, bad = piece1(m)
            bad1 += [(m,) + t for t in bad]
            print("   piece 1, m=%d: %d of the |R| rows die by the Gallai cap,"
                  " %d by the split bound, %d by neither"
                  % (m, gal, spl, len(bad)))
        ok1 = not bad1

        v2 = [piece2(m) for m in ROWS]
        ok2 = min(v2) >= Z
        print("   piece 2: split minima %s against %d  -> %s"
              % (v2, Z, "holds" if ok2 else "FAILS"))

        v3 = [len(piece3(m)) for m in ROWS]
        ok3 = not any(v3)
        print("   piece 3: classes with b >= 8 surviving %s  -> %s"
              % (v3, "holds" if ok3 else "FAILS"))

        print("   => order 58 reduces to the three b <= 7 classes: %s"
              % ("YES" if (ok1 and ok2 and ok3) else "NO"))
        allok &= ok1 and ok2 and ok3
        print()

    V.set_base(V.BASE_CCCG2021)
    CM.reset()
    print("CONCLUSION")
    if allok:
        print("   Every piece of the order-58 chain holds at every rung, so the")
        print("   whole reduction needs nothing beyond cr(K_12) = 150 (Guy;")
        print("   Pan and Richter, J. Graph Theory 56 (2007) 128-134).  In")
        print("   particular it does NOT need the CCCG 2021 value cr(K_13) = 225,")
        print("   which is a published but single-author, 1000+ CPU-year result")
        print("   that neither Schaefer's DS21 (2026) nor Clancy-Haythorpe-")
        print("   Newcombe records.")
        print("   Piece 3 required crminus.py to reach this: without it, b = 30")
        print("   survived at the weakest rung (8249 at m = 839, 8213 at m = 840).")
        print("   Pieces 1 and 2 were already seed-independent; this file is the")
        print("   check that establishes it, which had not been done before.")
    else:
        print("   Some piece fails at some rung; see above.")
    print()
    print("   STILL OPEN: the three classes b = 6 with (51,1) and (50,1,1) and")
    print("   b = 7 with (49,1,1), and the three order-57 rows 826, 827, 828.")


if __name__ == "__main__":
    main()
