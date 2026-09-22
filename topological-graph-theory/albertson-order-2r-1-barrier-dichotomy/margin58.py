#!/usr/bin/env python3
"""
Which inequality is TIGHT at a surviving point, and three probes that are not.

WHY.  slack58.py prices a sharpening by handicapping an inequality and re-running
the whole scan -- the right question when asking "how strong would a theorem have
to be".  This file asks the complementary and cheaper one: at the points that
actually survive, WHICH inequality is closest to failing?  The two are not the
same, and defect 13 was caused by confusing them, so the count inequality is
excluded from the ranking here: the scan hands the adversary t at the minimum
inequality (1) allows, so (1) is met with equality BY CONSTRUCTION and its slack
measures the search order rather than the mathematics.

The slacks are read from tuttegen.LAST_SLACK, recorded by _ok at the moment it
accepts a point, rather than recomputed here.  A previous pass kept a second copy
of that arithmetic and wasted two runs on a stale one.

==============================================================================
THREE PROBES THAT DO NOT BITE, RECORDED SO THEY ARE NOT RE-DERIVED.

At a case-B surviving point with W = 0 and u = t, the structure is rigid enough
to read off a subgraph of G directly:

  * A lies inside one block, so A is a CLIQUE of G;
  * u = t makes every U-component a singleton, so U is independent in H[R] and
    is therefore a CLIQUE of G;
  * A has no H-neighbour in U, so every A-U pair is a G-edge.

  (P1) A u U is a clique of G of size a + u.  More generally, one vertex per
       U-component extends A, so a + t <= omega(G) in case B at every point.
       And omega(G) <= 28: G is 29-critical on 58 vertices, so a K_29 subgraph
       would be a PROPER subgraph of chromatic number 29, contradicting
       criticality.  (The lane's table had only omega(G) <= 29.)
       MEASURED: a + t never exceeds 26.  Does not bite.

  (P2) On A u U u S_R -- which is a + |R| vertices when W = 0 -- the G-edges
       missing are exactly the H-edges inside, and those are
            e_H(A) + e_H(A,U) + e_H(A,S_R) + e_H(U) + e_H(U,S_R) + e_H(S_R)
          =    0    +    0     +   rsum    +   0    +        e(H[R])
       so G contains K_{a+|R|} minus exactly rsum + e(H[R]) edges, and
       cr(G) >= g(a + |R|, rsum + e(H[R])) with the lane's crminus.g.
       MEASURED: the best value obtained is about half of Z(29) = 8281,
       because removing roughly half the edges of K_43 costs most of its
       crossing number.  The exact figure is printed by main rather than
       quoted here.  Does not bite.

  (P4) COMPONENT SPREAD, inequality (8) in tuttegen.py.  A vertex of W lies in
       one component of H' - S and all of its A-neighbours lie in that same
       component, so with alpha_j, omega_j the A- and W-parts of the c_A
       components,
            e(A,W) <= sum_j alpha_j omega_j <= (a - c_A + 1)|W| ,
       while e(A,W) = e(A,R) - e(A,S_R) >= sum_i a_i rho_i - a s_R.  Where
       inequality (4) is TIGHT this forces c_A = 1: the adversary cannot have
       every vertex of R - U see all of A and still keep A spread over many
       components.  Since (4) is the tightest inequality at most surviving
       points, that looked like the lever.
       MEASURED: it fires on ZERO points, and the reason is sharper than the
       count -- the two conditions it needs are DISJOINT on the surviving set.
       Part 4 below measures that.  Does not bite.

  (P3) R - U is triangle-free whenever some A-vertex sees all of it, since
       N_H(v) ^ R must be triangle-free or v closes a K_4.  That replaces the
       K_4-free Turan cap by Mantel on that part.  MEASURED on the tight points:
       slack 78 where it applies.  Does not bite.

Each is valid.  None of them closes a configuration, and the reason is the same
in all three: the surviving points are tight in the SMALL counts -- spread, the
U-degree -- and slack in everything that scales with |R|.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import pickle
import sys

import crminus as C
import packing58 as P
import tuttegen as G
from order2r import Z

NAMES = ("2 degree", "3 turan", "4 spread", "5 S_R-deg", "6 U-deg",
         "7 disjoint")


def undecided(cfgs):
    out = []
    for m, RSZ, mult, eHR in cfgs:
        NL, X = G.N58 - RSZ, 2 * m - G.N58 * G.DEG
        # true_blocks, not mult: the enumerator does not list every block, and
        # the guarantee computed from the raw multiset is too LARGE (defect 19).
        if P.kmax_exact(G.true_blocks(mult, RSZ, eHR, X), NL) < 3:
            continue
        if G.route_closed(RSZ, list(mult), eHR, X)[0]:
            continue
        out.append((m, RSZ, mult, eHR))
    return out


def points(m, RSZ, mult, eHR):
    NL, X = G.N58 - RSZ, 2 * m - G.N58 * G.DEG
    for k in range(3, P.kmax_exact(G.true_blocks(mult, RSZ, eHR, X), NL) + 1):
        w = []
        G.obstructed(RSZ, list(mult), eHR, k, NL, None, X, w)
        if not w:
            return
        for x in w:
            yield k, x


def main():
    print("Which inequality is tight at a surviving point")
    print()
    cfgs = (pickle.load(open(sys.argv[1], "rb")) if len(sys.argv) > 1
            else G.configurations())
    und = undecided(cfgs)
    print("   in scope and undecided: %d" % len(und))

    tight, mins, npts = {}, {}, 0
    clique_max, clique_bad = 0, 0
    probe2 = []
    t4 = wpos = both = fires = 0
    for m, RSZ, mult, eHR in und:
        for k, x in points(m, RSZ, mult, eHR):
            npts += 1
            sl = x["slack"]
            cand = [(v, n) for n, v in sl.items() if not n.startswith("1")]
            v, n = min(cand)
            tight[n] = tight.get(n, 0) + 1
            mins[min(v, 10)] = mins.get(min(v, 10), 0) + 1
            if sl["4 spread"] == 0:
                t4 += 1
            if x["W"] >= 1:
                wpos += 1
            if sl["4 spread"] == 0 and x["W"] >= 1:
                both += 1
            if (x.get("rsum", 0) - x["a"] * x["sR"]
                    > (x["a"] - x["cA"] + 1) * x["W"]):
                fires += 1
            if x["case"] == "B":
                s = x["a"] + x["t"]
                clique_max = max(clique_max, s)
                if s > 28:
                    clique_bad += 1
                if x["W"] == 0 and x["u"] == x["t"] and len(probe2) < 400:
                    probe2.append((x["a"] + RSZ, x["rsum"] + eHR))
    print("   surviving points: %d" % npts)
    print()
    print("   tightest inequality at a surviving point (inequality (1) excluded,")
    print("   since the scan pins it to equality by construction):")
    for n in sorted(tight, key=lambda n: -tight[n]):
        print("      %-12s %8d" % (n, tight[n]))
    print()
    print("   distribution of that minimum slack (capped at 10): %s"
          % sorted(mins.items()))
    z = mins.get(0, 0)
    print("   points clearing every inequality by EXACTLY ZERO somewhere: %d of %d"
          % (z, npts))
    print()

    print("PROBE 1   a + t <= omega(G) <= 28 in case B")
    print("   largest a + t over case-B points: %d" % clique_max)
    print("   points violating it: %d  ->  %s"
          % (clique_bad, "does not bite" if clique_bad == 0 else "CLOSES SOME"))
    print()

    print("PROBE 2   G contains K_{a+|R|} minus rsum + e(H[R]) edges")
    vals = sorted({(n, f) for n, f in probe2})[:400]
    best = 0
    for n, f in vals:
        v = C.g(n, f)
        best = max(best, v)
    print("   distinct (n, f) pairs scored: %d" % len(vals))
    print("   best crossing bound obtained: %d against Z(29) = %d" % (best, Z))
    print("   ->  %s" % ("does not bite" if best < Z else "CLOSES SOME"))
    print()

    print("PROBE 4   component spread: why inequality (8) cannot fire")
    print("   (8) forces c_A = 1 where (4) is tight, but it needs W >= 1 too.")
    print("   points with (4) slack 0          : %d" % t4)
    print("   points with W >= 1               : %d" % wpos)
    print("   points with BOTH                 : %d" % both)
    print("   points (8) rejects               : %d" % fires)
    print("   -> the two conditions are %s on the surviving set, which is why"
          % ("DISJOINT" if both == 0 else "overlapping"))
    print("   (8) is vacuous: where (4) is tight the adversary always takes")
    print("   W = 0, and there its consequence is already inequality (5).")
    print()
    print("CONCLUSION")
    rank = sorted(tight, key=lambda n: -tight[n])
    print("   The surviving points are tight in the SMALL counts and slack in")
    print("   everything that scales with |R|.  Ranked by how often each is the")
    print("   tightest: %s." % ", ".join("%s %d" % (n, tight[n]) for n in rank))
    print("   Probe 2 reaches %d of the %d it needs, a shortfall of %d (%d%%);"
          % (best, Z, Z - best, 100 * (Z - best) // Z))
    print("   probe 1 reaches %d of its cap of 28." % clique_max)
    print("   Everything in this file is derived from the measurement rather")
    print("   than asserted, because the prose form of exactly such a summary")
    print("   went stale between passes once already (defect 14).")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
