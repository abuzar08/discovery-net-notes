#!/usr/bin/env python3
"""
The singleton w sharpens the Turan cap on H[R], and removes 310 configurations.

HOW THIS WAS FOUND.  The plan was to build an ADMISSIBLE adversarial H for one
configuration in the 2116 -- m = 838, |R| = 21, mult = (21,8,8), e(H[R]) = 142 --
and compute nu(H - T_1 - T_2 - T_3) with the certifying matching routine.  The
construction could not be completed, and the reason it could not is a theorem.

==============================================================================
THE ARGUMENT.

The class has a singleton component {w} of H - B with N_H(w) inside B and at most
two neighbours in each of the two disjoint triangles, so

        d_H(w)  <=  b - 2  =  4 ,

and x_w = 29 - d_H(w) >= 25 puts w in R.  Therefore d_{H[R]}(w) <= 4 as well, and

        e(H[R])  =  e(H[R] - w) + d_{H[R]}(w)  <=  e(H[R] - w) + 4 .

Now H is K_4-free, so H[R] - w is a K_4-free graph on |R| - 1 vertices, and
Turan's theorem caps it exactly:

        e(H[R] - w)  <=  floor( (|R| - 1)^2 / 3 ) .

Hence

        e(H[R])  <=  floor( (|R| - 1)^2 / 3 )  +  4 ,

which is strictly stronger than the cap floor(|R|^2 / 3) used until now -- by 3
at |R| = 11 and by 17 at |R| = 32.  The gap is about (2|R| - 1)/3 - 4, so it
grows with |R|, which is exactly where the surviving configurations sit.

THE CONFIGURATION THAT EXPOSED IT.  At |R| = 21 the old cap is 147 and the new
one is 137, while the configuration asks for e(H[R]) = 142.  Deleting w leaves
138 edges on 20 vertices against a K_4-free maximum of 133, so H[R] - w contains
a K_4 and so does H.  The configuration is impossible, and no adversarial H for
it exists -- which is why the construction stalled.

==============================================================================
WHAT IT REMOVES.  310 of the 8623 surviving clique-block configurations.  The
isolated-vertex configurations are unaffected: all 307 already satisfy the
sharper cap, as do the 15 with an odd-cycle block.  Order 58 falls from 8945 to
8635.

Note that this did not come from sharpening an argument.  It came from trying to
exhibit an object and failing, which is a different and in this lane a more
reliable way to find things: the previous nine defects were all found by
re-deriving arguments, and three of them only after they had been published.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import auditc as AC
import alpha58 as A
import turan58 as T
import residue58 as R58
import blockr58 as BR
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N58 = 2 * r
ALPHA = 3
CW = 4                      # d_H(w) <= b - 2 = 4


def cap_w(RSZ):
    """floor((|R|-1)^2/3) + 4, the sharpened K_4-free cap on e(H[R])."""
    return (RSZ - 1) * (RSZ - 1) // 3 + CW


def part1():
    print("PART 1   the sharpened cap against the old one")
    print("   |R|    old floor(|R|^2/3)    new floor((|R|-1)^2/3)+4    gain")
    for RSZ in (11, 16, 21, 26, 32):
        print("   %3d %18d %26d %8d"
              % (RSZ, T.turan_k4free(RSZ), cap_w(RSZ),
                 T.turan_k4free(RSZ) - cap_w(RSZ)))
    print()
    print("   The configuration that exposed it: |R| = 21 with e(H[R]) = 142.")
    print("   Deleting w leaves %d edges on 20 vertices against a K_4-free"
          % (142 - CW))
    print("   maximum of %d, so H[R] - w contains a K_4 and so does H."
          % T.turan_k4free(20))
    print()


def part2():
    print("PART 2   what the sharpened cap removes")
    tot = alive = 0
    iso_tot = iso_alive = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        t = a = 0
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            old, new = T.turan_k4free(RSZ), cap_w(RSZ)
            for mult, eL in AC.multisets_audited(NL, max(base, 0),
                                                 base + RSZ * (RSZ - 1) // 2,
                                                 d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                eGR = eL - base
                eHR = RSZ * (RSZ - 1) // 2 - eGR
                if eGR < 0 or eHR < 0 or eHR > old:
                    continue
                if A.alpha_lb(mult, NL) > ALPHA:
                    continue
                if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                    continue
                if BR.blockR(mult, NL, RSZ, eHR) >= Z:
                    continue
                t += 1
                if eHR <= new:
                    a += 1
            if d0 <= 0:
                for iso in range(1, ALPHA + 1):
                    NB = NL - iso
                    if NB < 2:
                        break
                    for mult, eL in AC.multisets_audited(
                            NB, max(base, 0), base + RSZ * (RSZ - 1) // 2,
                            d0, r):
                        eGR = eL - base
                        eHR = RSZ * (RSZ - 1) // 2 - eGR
                        if eGR < 0 or eHR < 0 or eHR > old:
                            continue
                        if RSZ - DEG + eHR == 0:
                            continue
                        if A.alpha_lb(mult, NL, iso) > ALPHA:
                            continue
                        if max(A.iso_bound(mult, RSZ, eHR, iso),
                               BR.blockR(mult, NL, RSZ, eHR)) >= Z:
                            continue
                        if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                            continue
                        iso_tot += 1
                        if eHR <= new:
                            iso_alive += 1
        tot += t
        alive += a
        print("   row (58,%d): %5d clique-block survivors, %5d within the"
              " sharper cap" % (m, t, a))
    print("   clique-block: %d -> %d  (removed %d)" % (tot, alive, tot - alive))
    print("   isolated-vertex: %d -> %d  (removed %d)"
          % (iso_tot, iso_alive, iso_tot - iso_alive))
    print()
    return tot, alive, iso_alive


def main():
    print("The singleton w sharpens the Turan cap on H[R], at r = %d" % r)
    print("Z(29) = %d;  d_H(w) <= b - 2 = %d puts w in R with small H[R]-degree"
          % (Z, CW))
    print()
    part1()
    tot, alive, iso_alive = part2()
    print("CONCLUSION")
    print("   e(H[R]) <= floor((|R|-1)^2/3) + 4, because deleting w from H[R]")
    print("   leaves a K_4-free graph on |R| - 1 vertices and w carries at most")
    print("   four edges.  Strictly stronger than floor(|R|^2/3) at every |R| in")
    print("   the range, by 3 at |R| = 11 rising to 17 at |R| = 32.")
    print()
    print("   Order 58 at r = 29: %d + 15 + %d = %d configurations, against"
          % (alive, iso_alive, alive + 15 + iso_alive))
    print("   8945 before.  Order 57 is untouched -- w is a feature of the")
    print("   order-58 class only.")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
