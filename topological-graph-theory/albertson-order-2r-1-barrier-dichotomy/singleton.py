#!/usr/bin/env python3
"""
Singleton colour classes weaken the absorption requirement, at both frontiers.

STATE BEFORE THIS FILE.  At r = 29 exactly two cases are open:

    order 57, row (57,828) at |R| in [10,11];
    order 58, class b = 6, c = (51,1) at |R| >= 11.

Both are attacked by the same absorption argument.  Since theta(H) = chi(G) = 29,
colouring L with chi(G[L]) colours, absorbing t vertices of R into distinct
colour classes and colouring the rest of R gives

        29 = chi(G)  <=  chi(G[L]) + (|R| - t) - nu ,      nu := nu(H[R]) ,

so a contradiction needs   t + nu >= chi(G[L]) + |R| - 28.

Up to now every absorption was costed as if it needed a colour class {u, v} with
u in Q_1 and v outside, so that z had to be H-adjacent to BOTH -- two matchings
at once, and the requirement mu_1 + mu_2 >= |Z| + t.

==============================================================================
NOT EVERY CLASS IS A PAIR.

chi(G[L]) = q_1, the order of the largest block, because G[L] is a block graph
and such graphs are perfect with clique number q_1.  In ANY proper q_1-colouring
the q_1 vertices of Q_1 get q_1 distinct colours, so every class contains exactly
one vertex of Q_1.  The other |L| - q_1 vertices are distributed among those same
q_1 classes.

Constraint C forces every block with q - 1 < delta_0 to consist entirely of cut
vertices, so the vertices of L that are not cut vertices lie in the BIG blocks
(q - 1 >= delta_0), and those are pairwise disjoint: a shared vertex would have
degree at least 2 delta_0 > 28.  An independent set of G[L] therefore has at most
k_eff := #(big blocks) vertices, one per big block.

So a class can hold at most k_eff - 1 of the non-Q_1 vertices, at least
ceil((|L| - q_1)/(k_eff - 1)) classes are occupied, and

        s  :=  q_1 - ceil((|L| - q_1)/(k_eff - 1))

classes can be left as SINGLETONS {u}, u in Q_1.  With k_eff = 2 this is
s = 2 q_1 - |L| and the packing is realisable: any vertex outside Q_1 lies in the
other big block and is G-non-adjacent to every vertex of Q_1 except itself, so
the pairing is an essentially free matching and ANY 2 q_1 - |L| vertices of Q_1
may be left unpaired.

ABSORBING INTO A SINGLETON CLASS IS HALF THE COST.  The class {u} u {z} is
independent in G exactly when u and z are G-non-adjacent, i.e. H-adjacent.  So
such an absorption needs only ONE matching edge, in (Z, Q_1) -- nothing on the
second side.  Choosing the colouring after seeing the graph, the singleton
classes can be placed at whichever Q_1-vertices we like.

THE REQUIREMENT THEREFORE BECOMES

        mu_1 >= t     and     mu_1 + mu_2 >= |Z| + max(0, t - s) ,

which is weaker than before by s.

==============================================================================
WHAT IT BUYS, AND WHAT IT DOES NOT.  Reported honestly below: it closes most of
the surviving multisets at order 57 -- all but one at |R| = 11 -- but not all,
and at order 58 it leaves the class open.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
from order2r import RCHI, Z
import mu58 as MU

r = RCHI
DEG = r - 1
crK = V.crK


def singletons(NL, mult, d0):
    """Lower bound on the number of colour classes that can be left as a single
    vertex of the largest block."""
    q1 = mult[0]
    keff = sum(1 for q in mult if q - 1 >= d0)
    if keff < 2:
        return 0
    return max(0, q1 - -(-(NL - q1) // (keff - 1)))


def test(nn, m, RSZ, mult, eL, NZ, cmax):
    """Returns (t, s, mu_1, mu_1+mu_2, closes)."""
    NL = nn - RSZ
    d0 = DEG - RSZ
    tneed, e1, e2, _ = MU.run(nn, m, RSZ, mult, eL, NZ, cmax)
    if tneed is None or tneed <= 0:
        return tneed, 0, None, None, True
    q1 = mult[0]
    q2 = mult[1] if len(mult) > 1 else 1
    s = singletons(NL, mult, d0)
    mu1 = MU.koenig(e1 - cmax, q1, NZ)
    both = None
    for c1 in range(0, cmax + 1):
        v = MU.koenig(e1 - c1, q1, NZ) + MU.koenig(e2 - (cmax - c1),
                                                   max(q2 - 1, 1), NZ)
        if both is None or v < both:
            both = v
    ok = mu1 >= tneed and both >= NZ + max(0, tneed - s)
    return tneed, s, mu1, both, ok


def main():
    print("Singleton colour classes at both r = 29 frontiers")
    print("Z(29) = %d" % Z)
    print()

    print("PART 1   order 57, row (57,828)")
    N57 = 2 * r - 1
    left57 = []
    for RSZ in (10, 11):
        NL = N57 - RSZ
        NZ = RSZ - 2
        X = 2 * 828 - N57 * DEG
        base = 828 - DEG * RSZ - X
        d0 = DEG - RSZ
        ms = MU.multisets(NL, max(base, 0), base + RSZ * (RSZ - 1) // 2, d0, r)
        print("   |R| = %d, |L| = %d, |Z| = %d, delta_0 = %d, %d multisets"
              % (RSZ, NL, NZ, d0, len(ms)))
        for mult, eL in ms:
            t, s, mu1, both, ok = test(N57, 828, RSZ, mult, eL, NZ, 5)
            if t is None or t <= 0:
                continue
            print("      %-14s chi=%2d t=%d s=%d  mu1>=%s sum>=%s  ->  %s"
                  % (str(mult), mult[0], t, s, mu1, both,
                     "closes" if ok else "SURVIVES"))
            if not ok:
                left57.append((RSZ, mult))
    print("   order 57 survivors after this: %d  %s"
          % (len(left57), [(a, b) for a, b in left57]))
    print()

    print("PART 2   order 58, class b = 6, c = (51,1)")
    N58 = 2 * r
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        Rmax = 1 + max(0, X - (r + 2 - 6))
        alive = 0
        rs = set()
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            for mult, eL in MU.multisets(NL, max(base, 0),
                                         base + RSZ * (RSZ - 1) // 2, d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                t, s, mu1, both, ok = test(N58, m, RSZ, mult, eL, RSZ - 1, 4)
                if not ok:
                    alive += 1
                    rs.add(RSZ)
        print("   m = %d : %d survivors at |R| in %s"
              % (m, alive,
                 "-" if not rs else "%d..%d" % (min(rs), max(rs))))
    print()
    print("CONCLUSION")
    print("   The singleton-class observation weakens the requirement by s and")
    print("   closes most of the order-57 multisets, but neither frontier is")
    print("   closed: order 57 keeps the combinations listed above and order 58")
    print("   keeps its class.")


if __name__ == "__main__":
    main()
