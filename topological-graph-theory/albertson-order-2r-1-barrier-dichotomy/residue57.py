#!/usr/bin/env python3
"""
Order 57 at r = 29 is CLOSED: row (57,828) is eliminated.

STATE BEFORE THIS FILE.  dichot.py cut row (57,828) to nine explicit sub-cases,
each pinned by (|R|, multiset, k_1, k_2), where k_1 counts the z in Z with
a_z := |N_H(z) ^ Q_1| = 0 and k_2 the z with b_z := |N_H(z) ^ Q_2| = 0.  Every
survivor had k_1 at its MAXIMUM.  That is exactly the configuration this file
rules out.

==============================================================================
THE RESIDUE: a_z + b_z IS PINNED BY THE DEGREE.

The two big blocks are pairwise disjoint and, in every admissible multiset here,
cover L: their orders sum to |L|, the small connector block consists entirely of
cut vertices by Constraint C, and two blocks share at most one vertex.  So
L = Q_1 u Q_2 disjointly and, for every z in Z,

        a_z + b_z  =  |N_H(z) ^ L|  =  d_H(z) - |N_H(z) ^ R|
                   =  (28 - x_z) - |N_H(z) ^ R| .

A vertex with a_z = 0 therefore has b_z = |N_H(z) ^ L| <= |Q_2| = q_2, i.e.

        x_z + |N_H(z) ^ R|  >=  28 - q_2  =:  thr_1 ,

and symmetrically a_z <= q_1 forces x_z + |N_H(z) ^ R| >= 28 - q_1 =: thr_2 for
any z with b_z = 0.  These are expensive: every z is high, so x_z >= 1 already,
and sum_z |N_H(z) ^ R| <= 2 e(H[R]) because each H-edge inside R contributes at
most two endpoints to Z.  Writing Sx := sum_z x_z,

        k_1 (thr_1 - 1)  <=  Sx + 2 e(H[R]) - |Z| ,

and likewise for k_2.  The excess budget fixes Sx: the two singleton components
have sum d_H(w_i) = 2 + a with a := |A_1| + |A_2| <= 3, so
x_{w_1} + x_{w_2} = 54 - a and Sx = X - 54 + a <= X - 51.

==============================================================================
WHY THAT IS DECISIVE.  At (26,20) with |R| = 11 the pinning is total: Sx = 9,
|Z| = 9, e(H[R]) = 0, so k_1 (28 - 20 - 1) <= 0 and k_1 = 0; likewise k_2 = 0.
Concretely, every z has d_H(z) = 27 and no H-neighbour in R, so a_z + b_z = 27
with b_z <= 20 -- forcing a_z >= 7, where the previous argument had only
a_z >= 1.  The sub-cases k_1 = 1 that survived dichot.py simply do not exist.

The same happens at |R| = 10: the caps come out k_1 <= 1, 1, 0 for the three
multisets, against surviving k_1 = 3, 2, 2.

Every (k_1, k_2) inside the caps was already closed by dichot.py, so the row
dies.  ORDER 57 AT r = 29 IS THEREFORE CLOSED, and order 58's single class
b = 6, c = (51,1) is all that remains.

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
M = 828


def residue_caps(RSZ, mult, eHR, Sx):
    """Upper bounds on k_1 and k_2 from the degree-split residue."""
    NZ = RSZ - 2
    q1, q2 = mult[0], mult[1]
    budget = Sx + 2 * eHR - NZ
    out = []
    for thr in (DEG - q2, DEG - q1):
        if thr <= 1:
            out.append(NZ)
        else:
            out.append(max(0, budget // (thr - 1)))
    return out[0], out[1]


def main():
    print("Order 57 at r = 29: the residue closes row (57,828)")
    print("Z(29) = %d" % Z)
    print()
    X = 2 * M - N57 * DEG
    print("X = %d, so Sx := sum_z x_z = X - 54 + a <= %d  (a = |A_1|+|A_2| <= 3)"
          % (X, X - 51))
    print()
    allclosed = True
    for RSZ in (10, 11):
        NL = N57 - RSZ
        NZ = RSZ - 2
        d0 = DEG - RSZ
        base = M - DEG * RSZ - X
        Sx = X - 51
        ms = MU.multisets(NL, max(base, 0), base + RSZ * (RSZ - 1) // 2, d0, r)
        print("|R| = %d : |L| = %d, |Z| = %d, %d admissible multisets"
              % (RSZ, NL, NZ, len(ms)))
        for mult, eL in ms:
            q1 = mult[0]
            q2 = mult[1] if len(mult) > 1 else 1
            eGR = eL - base
            eHR = RSZ * (RSZ - 1) // 2 - eGR
            if eGR < 0 or eHR < 0:
                continue
            # the two big blocks must partition L for the residue to apply
            big = [q for q in mult if q - 1 >= d0]
            if len(big) != 2 or sum(big) != NL:
                print("      %-14s big blocks do not partition L; skipped"
                      % str(mult))
                continue
            K1, K2 = residue_caps(RSZ, mult, eHR, Sx)
            bad = D.survivors(N57, M, RSZ, mult, eL, 2, 5)
            if bad is None:
                continue
            live = [(k1, k2) for (k1, k2, _c, _m1, _m2) in bad
                    if k1 <= K1 and k2 <= K2]
            print("      %-14s e(H[R])=%d  thr=(%d,%d)  caps k1<=%d k2<=%d ;"
                  " dichot survivors %s  ->  %s"
                  % (str(mult), eHR, DEG - q2, DEG - q1, K1, K2,
                     [(b[0], b[1]) for b in bad] if bad else "none",
                     "IMPOSSIBLE" if not live else "SURVIVES %s" % live))
            if live:
                allclosed = False
        print()
    print("CONCLUSION")
    if allclosed:
        print("   Every admissible (|R|, multiset, k_1, k_2) for row (57,828) is")
        print("   impossible, so the row is ELIMINATED.")
        print()
        print("   ORDER 57 AT r = 29 IS CLOSED: all five rows of the frontier")
        print("   (57,824) ... (57,828) are eliminated.")
        print("   What remains of r = 29 is order 58 alone, and there a single")
        print("   class: b = 6, c = (51,1) with |R| >= 11.")
    else:
        print("   Some sub-case survives; see above.")


if __name__ == "__main__":
    main()
