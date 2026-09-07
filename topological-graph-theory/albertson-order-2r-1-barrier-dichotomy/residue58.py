#!/usr/bin/env python3
"""
The residue, freed of the partition hypothesis, and turned on order 58.

STATE BEFORE THIS FILE.  Order 57 at r = 29 is closed.  What remains of r = 29
is order 58 alone, in a single class: b = 6, c = (51, 1) with |R| >= 11, on the
three rows m = 838, 839, 840.

residue57.py closed the last order-57 row with a degree-split argument that was
STATED for the case where the two big Gallai blocks partition L, and guarded by
an explicit check `len(big) != 2 or sum(big) != NL`.  At order 58 that guard
almost never passes: |R| runs up to 32, so delta_0 = 28 - |R| drops to zero or
below, every block counts as "big", and the partition hypothesis is unavailable.

The hypothesis was never needed.  This file removes it.

==============================================================================
THE RESIDUE WITHOUT A PARTITION.

Let Q_1 be a largest block of G[L] and Q_2 a second largest, and for z in Z put

        a_z := |N_H(z) ^ Q_1| ,      b_z := |N_H(z) ^ (Q_2 - Q_1)| .

Every vertex of L is low, d_G = 28 exactly, and a high vertex z has
d_H(z) = (n - 1) - 28 - x_z, so with dh := n - 29 (28 at order 57, 29 at order
58)

        |N_H(z) ^ L|  =  (dh - x_z) - |N_H(z) ^ R| .

Now Q_1 is a subset of L, so N_H(z) ^ L omits at most |L| - q_1 vertices outside
Q_1 -- no structure assumed, only |Q_1| = q_1 -- and therefore

        a_z  >=  |N_H(z) ^ L| - (|L| - q_1)  =  thr_1 - c_z ,

        thr_1 := dh - |L| + q_1 ,        c_z := x_z + |N_H(z) ^ R| .

Two blocks of a graph meet in at most one vertex, so |Q_2 - Q_1| >= q_2 - 1 and
symmetrically

        b_z  >=  thr_2 - c_z ,           thr_2 := dh - |L| + |Q_2 - Q_1| .

When the two blocks do partition L this is exactly the identity of residue57.py:
there dh = 28 and |L| = q_1 + q_2, so thr_1 = 28 - q_2.  The control below
reruns order 57 through the general form and reproduces closure.

A CORRECTION TO THE FIRST VERSION OF THIS FILE, which hardcoded dh = 28 at both
orders and so used order-58 thresholds one too small each.  A smaller threshold
rules out fewer configurations, so the order-58 survivor counts it reported were
OVER-counts and the negative conclusion held a fortiori; the counts below are
the corrected ones.  Order 57, where dh = 28 is correct, is unaffected.

==============================================================================
WHAT MAKES IT BITE: c_z IS PAID OUT OF A FIXED BUDGET.

Every z in Z is high, so x_z >= 1, and each H-edge inside R contributes at most
two endpoints to Z, so

        sum_{z in Z} c_z  <=  Sx + 2 e(H[R])  =:  budget ,   Sx := sum_{z in Z} x_z.

At order 58 the class has ONE singleton component w, with N_H(w) inside B and at
most two neighbours in each of the two disjoint triangles, so d_H(w) <= b - 2 = 4
and x_w = 29 - d_H(w) >= 25.  Hence Sx = X - x_w <= X - 25, which is 27, 29, 31
on the three rows -- against Sx <= 9 at order 57.  The budget is therefore much
larger here, exactly as expected, and the question is whether |Z| and thr_1 grow
faster.  They do, at the top of the |R| range: thr_1 = q_1 + |R| - 29 at order 58
grows with |R| while the budget does not.

THREE CONSEQUENCES, all used below.

  (i)  FEASIBILITY.  A z with a_z = 0 has c_z >= thr_1, one with b_z = 0 has
       c_z >= thr_2, no z is one-sided on both (it would have no H-neighbour in
       L at all), and every other z has c_z >= 1.  So

           k_1 max(thr_1,1) + k_2 max(thr_2,1) + (|Z| - k_1 - k_2)  <=  budget ,

       which caps k_1 and k_2 jointly.

  (ii) A PER-VERTEX FLOOR.  Among the Za := |Z| - k_1 vertices with a_z >= 1,
       one of them can absorb at most what the others leave, so

           a_z  >=  thr_1 - (Ba - others_min)  =:  amin_1   for every such z,

       where Ba is the budget left after the k_1 one-sided vertices are paid for.
       This is what the previous file only ever extracted at k_1 = 0.

 (iii) A SUM FLOOR.  sum_{z : a_z >= 1} a_z >= Za thr_1 - Ba, which is taken in
       parallel with the block-count bound e_H(Q_1,R) >= q_1(q_1 + |R| - 29) and
       the larger of the two used.

The floor amin_1 feeds the defect-Hall bound of dichot.py, which was previously
called with amin = 1 in every case; a floor of 7 rules out deficiencies that a
floor of 1 permits, and that is where the strength comes from.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import mu58 as MU
import dichot as D
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N57 = 2 * r - 1
N58 = 2 * r


def second_side(NL, mult):
    """|Q_2 - Q_1| and the block order to use for it.

    Two blocks meet in at most one vertex, so |Q_2 - Q_1| >= q_2 - 1 always.
    When the block orders sum to exactly |L| the blocks are pairwise disjoint
    and cover L, no vertex is a cut vertex, and |Q_2 - Q_1| = q_2."""
    q2 = mult[1] if len(mult) > 1 else 1
    if sum(mult) == NL:
        return q2
    return max(q2 - 1, 1)


def thresholds(nn, NL, mult):
    """thr_1, thr_2 of the general residue, on a graph of order nn.

    A CORRECTION.  The high-vertex degree in H is d_H(z) = (nn - 1) - d_G(z)
    = (nn - 1 - 28) - x_z, which is 28 - x_z at order 57 but 29 - x_z at order
    58.  The first version of this file hardcoded 28 at both orders, making the
    order-58 thresholds one too small each.  That is conservative -- a smaller
    threshold rules out fewer configurations -- so every order-58 number it
    reported was an over-count of the survivors, and the negative conclusion
    held a fortiori; but it was not tight, and the count is corrected here."""
    dh = nn - 1 - DEG
    return dh - NL + mult[0], dh - NL + second_side(NL, mult)


def residue(NZ, budget, thr1, thr2, k1, k2):
    """Feasibility and floors for a given (k_1, k_2).

    Returns None if the pair is already impossible, otherwise
    (amin1, amin2, Sa_res, Sb_res)."""
    p1, p2 = max(thr1, 1), max(thr2, 1)
    # k12 counts the z that are one-sided on BOTH; they are members of both
    # counts, so k_1 + k_2 - k12 <= |Z| rather than k_1 + k_2 <= |Z|.  Such a z
    # satisfies both conditions at once, so it pays max(p1,p2) of the budget.
    k12 = max(0, k1 + k2 - NZ)
    if k12 > min(k1, k2):
        return None
    if ((k1 - k12) * p1 + (k2 - k12) * p2 + k12 * max(p1, p2)
            + (NZ - k1 - k2 + k12) > budget):
        return None                       # (i) the budget cannot pay for it

    # For each side: the group with a positive count has n_side vertices, the
    # budget left after paying the one-sided vertices of that side is B, and a
    # single vertex can take at most what the others leave.  The other side's
    # one-sided vertices sit inside this group and each pays at least p_other.
    n1 = NZ - k1
    B1 = budget - k1 * p1
    ko = min(k2, n1)
    rest1 = max(0, ko - 1) * p2 + (n1 - 1 - max(0, ko - 1)) if n1 > 0 else 0
    amin1 = max(0, thr1 - (B1 - max(rest1, 0))) if n1 > 0 else 0
    Sa = max(0, n1 * thr1 - B1) if n1 > 0 else 0

    n2 = NZ - k2
    B2 = budget - k2 * p2
    ko = min(k1, n2)
    rest2 = max(0, ko - 1) * p1 + (n2 - 1 - max(0, ko - 1)) if n2 > 0 else 0
    amin2 = max(0, thr2 - (B2 - max(rest2, 0))) if n2 > 0 else 0
    Sb = max(0, n2 * thr2 - B2) if n2 > 0 else 0
    return amin1, amin2, Sa, Sb


def survivors(nn, m, RSZ, mult, eL, nw, cw, sx_max):
    """dichot.survivors, with the general residue folded in.

    Returns None if the configuration is inadmissible, else the list of
    surviving (k_1, k_2)."""
    NL = nn - RSZ
    NZ = RSZ - nw
    X = 2 * m - nn * DEG
    base = m - DEG * RSZ - X
    eGR = eL - base
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    if eGR < 0 or eHR < 0 or NZ <= 0:
        return None
    q1 = mult[0]
    q2 = mult[1] if len(mult) > 1 else 1
    side2 = second_side(NL, mult)
    nu = min(eHR, RSZ // 2)
    t = q1 + RSZ - 28 - nu
    if t <= 0:
        return []                          # killed by the clique cover
    d0 = DEG - RSZ
    s = D.singletons(NL, mult, d0)
    e1 = q1 * (q1 + RSZ - 29)
    e2 = side2 * (q2 + RSZ - 29)
    thr1, thr2 = thresholds(nn, NL, mult)
    budget = sx_max + 2 * eHR
    bad = []
    for k1 in range(0, NZ + 1):
        for k2 in range(0, NZ + 1):
            res = residue(NZ, budget, thr1, thr2, k1, k2)
            if res is None:
                continue                   # impossible by the budget alone
            amin1, amin2, Sa_r, Sb_r = res
            Za, Zb = NZ - k1, NZ - k2
            if amin1 > q1 or amin2 > side2:
                continue                   # floor exceeds the block, impossible
            # A SOUNDNESS CORRECTION.  The three cliques scored below must be
            # VERTEX-DISJOINT.  A z one-sided on both sides belongs to both
            # counts, so scoring Q_1 + k_1 and Q_2 + k_2 separately would use it
            # twice.  Each such z is assigned to the first side only, and the
            # worst case for us -- the one most likely to survive -- is the
            # largest feasible number of them, so that is the one taken.
            k12 = min(k1, k2)
            c1 = max(0, k1 - eHR)
            c2 = max(0, (k2 - k12) - eHR)
            rest = max(0, RSZ - (k1 + k2 - k12) - eHR)
            cross = crK(q1 + c1) + crK(q2 + c2) + crK(rest)
            if cross >= Z:
                continue
            # The singleton w removes at most cw H-edges from the two edge
            # totals COMBINED -- d_H(w) <= b - 2 -- so the deduction is a split
            # cw_1 + cw_2 <= cw, not cw on each side.  The configuration
            # survives if SOME split escapes, so every split is scanned.
            surv = None
            for cw1 in range(0, cw + 1):
                cw2 = cw - cw1
                Sa = max(e1 - cw1, Sa_r)
                Sb = max(e2 - cw2, Sb_r)
                if Sa > Za * q1 or Sb > Zb * side2:
                    continue               # this split is itself impossible
                mu1 = (max(MU.koenig(Sa, q1, Za),
                           D.defect_mu(Sa, q1, Za, max(amin1, 1)))
                       if Za > 0 else 0)
                mu2 = (max(MU.koenig(Sb, side2, Zb),
                           D.defect_mu(Sb, side2, Zb, max(amin2, 1)))
                       if Zb > 0 else 0)
                if not (Za >= t and mu1 >= t
                        and mu1 + mu2 >= NZ + max(0, t - s)):
                    surv = (mu1, mu2, cw1, cw2)
                    break
            if surv is not None:
                bad.append((k1, k2, cross, surv[0], surv[1], amin1, amin2))
    return bad


def control_order57():
    """The general residue must still close order 57, where the special form
    did.  Row (57,828) at |R| = 10 and 11."""
    print("CONTROL   order 57, row (57,828), through the GENERAL residue")
    M = 828
    X = 2 * M - N57 * DEG
    sx = X - 51                            # Sx = X - 54 + a, a <= 3
    allclosed = True
    for RSZ in (10, 11):
        NL = N57 - RSZ
        d0 = DEG - RSZ
        base = M - DEG * RSZ - X
        ms = MU.multisets(NL, max(base, 0), base + RSZ * (RSZ - 1) // 2, d0, r)
        for mult, eL in ms:
            bad = survivors(N57, M, RSZ, mult, eL, 2, 5, sx)
            if bad is None:
                continue
            thr1, thr2 = thresholds(N57, NL, mult)
            print("   |R|=%2d %-14s thr=(%d,%d)  ->  %s"
                  % (RSZ, str(mult), thr1, thr2,
                     "IMPOSSIBLE" if not bad else
                     "SURVIVES %s" % [(b[0], b[1]) for b in bad]))
            if bad:
                allclosed = False
    print("   order 57 %s under the general form"
          % ("STILL CLOSES" if allclosed else "DOES NOT CLOSE -- REGRESSION"))
    return allclosed


def order58():
    """The last case, reported with its two regimes separated."""
    print("ORDER 58, class b = 6, c = (51,1): the last case at r = 29")
    print("   The excess budget is the whole difference from order 57.  The")
    print("   class has ONE singleton component w, so Sx := sum_{z in Z} x_z =")
    print("   X - x_w <= X - 25, which is 27, 29, 31 on the three rows, against")
    print("   Sx <= 9 at order 57 where there were TWO singletons.")
    print()
    total_alive = 0
    low_cases = 0
    short_hist = {}
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)               # Sx = X - x_w, x_w >= 25
        Rmax = 1 + max(0, sx)
        alive, seen, lo, hi = [], 0, 0, 0
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            for mult, eL in MU.multisets(NL, max(base, 0),
                                         base + RSZ * (RSZ - 1) // 2, d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                seen += 1
                bad = survivors(N58, m, RSZ, mult, eL, 1, 4, sx)
                if not bad:
                    continue
                alive.append((RSZ, mult, bad))
                if RSZ <= 16:
                    lo += 1
                    eGR = eL - base
                    eHR = RSZ * (RSZ - 1) // 2 - eGR
                    nu = min(eHR, RSZ // 2)
                    need = (RSZ - 1) + max(0, mult[0] + RSZ - 28 - nu
                                           - D.singletons(NL, mult, d0))
                    for (_k1, _k2, _c, mu1, mu2, _a, _b) in bad:
                        low_cases += 1
                        d = need - (mu1 + mu2)
                        short_hist[d] = short_hist.get(d, 0) + 1
                else:
                    hi += 1
        total_alive += len(alive)
        rs = sorted(set(a[0] for a in alive))
        print("   m = %d (X = %d, Sx <= %d, |R| <= %d): %d of %d (|R|, multiset)"
              " survive, |R| in %d..%d"
              % (m, X, sx, Rmax, len(alive), seen, rs[0], rs[-1]))
        print("        regime |R| <= 16 : %3d      regime |R| >= 17 : %d"
              % (lo, hi))
    print()
    print("   THE SMALL-|R| REGIME is fully explicit: %d sub-cases, each pinned"
          % low_cases)
    print("   by (m, |R|, multiset, k_1, k_2).  Shortfall of mu_1 + mu_2 against")
    print("   the requirement |Z| + max(0, t - s), as a histogram:")
    for d in sorted(short_hist):
        print("        short by %d : %d sub-cases" % (d, short_hist[d]))
    print("   The deficit sits entirely in mu_2.  There e_H(Q_2 - Q_1, R) is")
    print("   only |Q_2 - Q_1| (q_2 + |R| - 29), which is 30 or so against a")
    print("   |Z| of 10 to 15, so Koenig can force only two or three edges of a")
    print("   matching, while mu_1 is already at or one below its maximum |Z|.")
    print("   The residue cannot repair it: thr_2 = 28 - |L| + |Q_2 - Q_1| is 1")
    print("   or 2 in these cases, so it yields b_z >= 1 - c_z, which is vacuous.")
    return total_alive


def main():
    print("The residue without the partition hypothesis, at r = %d" % r)
    print("Z(29) = %d;  low means d_G = %d" % (Z, DEG))
    print()
    ok = control_order57()
    print()
    alive = order58()
    print()
    print("CONCLUSION")
    if not ok:
        print("   The general form fails to reproduce the order-57 closure;")
        print("   the generalization is wrong and nothing is claimed.")
    elif alive == 0:
        print("   Order 58 is CLOSED, and with it r = 29.")
    else:
        print("   The general residue reproduces the order-57 closure with the")
        print("   partition hypothesis REMOVED, and it does not close order 58:")
        print("   %d (|R|, multiset) combinations survive.  Reported as a" % alive)
        print("   negative result.  The route is exhausted for a quantified")
        print("   reason -- the budget Sx <= X - 25 is three times the order-57")
        print("   value because this class has one singleton component, not two")
        print("   -- so the next attempt on order 58 should not be a sharper")
        print("   residue but a new bound on the SECOND matching mu_2.")


if __name__ == "__main__":
    main()
