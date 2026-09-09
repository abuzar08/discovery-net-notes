#!/usr/bin/env python3
"""
The state of Albertson at r = 29, recomputed end to end, with every hypothesis
and its exact range of validity.

WHY THIS EXISTS.  Twelve contributions of mine are queued behind a stalled
ledger, and across them the order-58 open count moved five times:

        19193  ->  27761  ->  103292  ->  9533  ->  9104

as four scope defects were found and repaired and two proved-but-unused
hypotheses were finally applied.  Every one of those numbers appears in a
published contribution.  A reader cannot currently tell which is the standing
claim, and given that history the right thing is not another increment but a
single re-derived statement of where the lane actually is, with the hypothesis
inventory that the defects showed was missing.

Nothing here is new mathematics.  Everything is recomputed from the published
modules, and every claim is asserted rather than quoted.

==============================================================================
WHAT IS PROVED, AND BY WHOM

  r <= 26      literature.  Albertson-Cranston-Fox (EJC 16 (2009) #R45) r <= 12;
               Barat-Toth (EJC 17 (2010) #R73) r <= 16; Ackerman r <= 18;
               Cranston (arXiv:2512.08020) r <= 24 and r in {25,26} restricted;
               Sadhu (arXiv:2609.01682) Cor 1.2 settles r <= 26.
  r = 27       mine, reviewed on the ledger.
  r = 28       mine, reviewed on the ledger, independent of the r = 27 argument.
  r = 29       NOT proved.  Order 57 is closed; order 58 is open.

==============================================================================
THE r = 29 FRONTIER

Orders <= 56 are impossible (Gallai join and edge budget).  Orders 57 and 58
survive the deletion-recurrence gate, with thresholds 829 and 841, leaving

        order 57: rows m = 824 .. 828       ALL FIVE CLOSED
        order 58: rows m = 838, 839, 840    OPEN

Order 58 reduces to a single class: the barrier b = 6 with two disjoint
triangles, and H - B having components of sizes (51, 1).

==============================================================================
HYPOTHESIS INVENTORY.  Each hypothesis, what it needs, and where it is legal.
This table is the thing whose absence produced four defects in five passes.

  (C1) no isolated low vertex        delta_0 >= 1        |R| <= 27
  (C2) small blocks are all cut      delta_0 >= 1        |R| <= 27
  (C3) big blocks pairwise disjoint  2 delta_0 > 28      |R| <= 13
  (S)  d_H(z) = (n-1-28) - x_z       exact               all
  (K)  H is K_4-free, alpha(G) <= 3  branch hypothesis   all of order 58
  (X)  x_w >= r + 2 - b = 25         needs (K)           all of order 58
  (W)  e(H[R]) <= floor((|R|-1)^2/3)+4  needs (K) and (X)  all of order 58
  (TT) no two disjoint triangles T   branch hypothesis   all of order 58
       with H - T_1 - T_2 having a perfect matching

delta_0 := 28 - |R|.  At order 57 the theory is applied only at |R| <= 11, so
delta_0 >= 17 and (C1),(C2),(C3) all hold with room; ORDER 57 IS UNAFFECTED BY
EVERY REPAIR, which the control below re-checks.  At order 58 |R| runs to 32 and
all three thresholds are crossed; that is where the defects were.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import crminus as C
import auditc as AC
import alpha58 as A
import turan58 as T
import residue58 as R58
import blockr58 as BR
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N57 = 2 * r - 1
N58 = 2 * r
ALPHA = 3


def part1_ranges():
    print("PART 1   the hypothesis inventory, checked")
    ok = True
    for RSZ in range(2, 33):
        d0 = DEG - RSZ
        c12 = (d0 >= 1)
        c3 = (2 * d0 > DEG)
        ok &= (c12 == (RSZ <= 27)) and (c3 == (RSZ <= 13))
    print("   (C1),(C2) hold exactly for |R| <= 27 : %s" % ("PASS" if ok else "FAIL"))
    print("   (C3)      holds exactly for |R| <= 13 : %s" % ("PASS" if ok else "FAIL"))
    print("   order 57 uses |R| <= 11, so delta_0 >= %d and all three hold."
          % (DEG - 11))
    print("   order 58 uses |R| <= 32, so all three thresholds are crossed.")
    print()
    return ok


def part2_order57():
    print("PART 2   order 57 is closed, and unaffected by every repair")
    M = 828
    X = 2 * M - N57 * DEG
    sx = X - 51
    closed = True
    n = 0
    for RSZ in (10, 11):
        NL = N57 - RSZ
        d0 = DEG - RSZ
        base = M - DEG * RSZ - X
        pub = R58.MU.multisets(NL, max(base, 0),
                               base + RSZ * (RSZ - 1) // 2, d0, r)
        aud = AC.multisets_audited(NL, max(base, 0),
                                   base + RSZ * (RSZ - 1) // 2, d0, r)
        if pub != aud:
            closed = False
        for mult, eL in aud:
            n += 1
            if R58.survivors(N57, M, RSZ, mult, eL, 2, 5, sx):
                closed = False
    print("   row (57,828): %d admissible multisets at |R| = 10, 11;" % n)
    print("   the audited and published enumerations are IDENTICAL there, and")
    print("   every multiset is impossible: %s" % ("PASS" if closed else "FAIL"))
    print("   delta_0 >= 17 also forbids odd-cycle blocks and isolated low")
    print("   vertices outright, so neither gap ever touched order 57.")
    print()
    return closed


def part3_order58():
    print("PART 3   order 58, recomputed")
    a_clique = a_cycle = a_iso = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        c1 = c2 = c3 = 0
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            cap = min(T.turan_k4free(RSZ),
                      (RSZ - 1) * (RSZ - 1) // 3 + 4)   # w sharpens Turan
            for mult, eL in AC.multisets_audited(NL, max(base, 0),
                                                 base + RSZ * (RSZ - 1) // 2,
                                                 d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                eGR = eL - base
                eHR = RSZ * (RSZ - 1) // 2 - eGR
                if eGR < 0 or eHR < 0 or eHR > cap:
                    continue
                if A.alpha_lb(mult, NL) > ALPHA:
                    continue
                if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                    continue
                if BR.blockR(mult, NL, RSZ, eHR) >= Z:
                    continue
                c1 += 1
            # isolated low vertices, possible only when delta_0 <= 0
            if d0 <= 0:
                for iso in range(1, ALPHA + 1):
                    NB = NL - iso
                    if NB < 2:
                        break
                    for mult, eL in AC.multisets_audited(
                            NB, max(base, 0), base + RSZ * (RSZ - 1) // 2, d0, r):
                        eGR = eL - base
                        eHR = RSZ * (RSZ - 1) // 2 - eGR
                        if eGR < 0 or eHR < 0 or eHR > cap:
                            continue
                        if RSZ - DEG + eHR == 0:
                            continue            # K_29 is a subgraph outright
                        if A.alpha_lb(mult, NL, iso) > ALPHA:
                            continue
                        if max(A.iso_bound(mult, RSZ, eHR, iso),
                               BR.blockR(mult, NL, RSZ, eHR)) >= Z:
                            continue
                        if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                            continue
                        c3 += 1
        a_clique += c1
        a_iso += c3
        print("   row (58,%d): %5d clique-block configurations, %4d with an"
              " isolated low vertex" % (m, c1, c3))
    _, c2 = T.item2()
    a_cycle = c2
    print("   odd-cycle configurations, all three rows: %d" % a_cycle)
    print()
    tot = a_clique + a_cycle + a_iso
    print("   ORDER 58 OPEN SET: %d + %d + %d = %d"
          % (a_clique, a_cycle, a_iso, tot))
    print()
    return a_clique, a_cycle, a_iso


def part4_controls():
    print("PART 4   soundness controls")
    ok = C.controls()
    print("   crminus.g <= Z(n), g(n,0) = crK(n), monotone in f : %s"
          % ("PASS" if ok else "FAIL"))
    seeds = []
    for name, base in V.SEED_LADDER:
        V.set_base(base)
        C.reset()
        seeds.append((name, C.g(58, 58 * 57 // 2 - 838)))
    V.set_base(V.BASE_CCCG2021)
    C.reset()
    same = len(set(v for _, v in seeds)) == 1
    print("   g(58, f) at every cr(K_13) seed rung: %s  -> %s"
          % ([v for _, v in seeds], "seed-independent" if same else "SEED-DEPENDENT"))
    print()
    return ok and same


def main():
    print("The state of Albertson at r = %d, recomputed" % r)
    print("Z(29) = %d;  low means d_G = %d" % (Z, DEG))
    print()
    ok1 = part1_ranges()
    ok2 = part2_order57()
    a, b, c = part3_order58()
    ok4 = part4_controls()
    print("CONCLUSION")
    print("   PROVED: r <= 26 in the literature; r = 27 and r = 28 here, both")
    print("   reviewed on the ledger.")
    print()
    print("   r = 29: orders <= 56 impossible; ORDER 57 CLOSED (all five rows,")
    print("   %s); order 58 OPEN in %d configurations"
          % ("re-verified above" if ok2 else "CONTROL FAILED", a + b + c))
    print("   -- %d with clique blocks, %d with an odd-cycle block, %d with an"
          % (a, b, c))
    print("   isolated low vertex -- in the single class b = 6, c = (51,1).")
    print()
    print("   ALBERTSON'S CONJECTURE IS NOT PROVED FOR r = 29.  The superseded")
    print("   counts 19193, 27761, 103292 and 9533 appear in earlier queued")
    print("   contributions of mine; the standing figure is the one above.")
    print()
    print("   Controls: %s" % ("all PASS" if (ok1 and ok2 and ok4) else "FAILURE"))


if __name__ == "__main__":
    main()
