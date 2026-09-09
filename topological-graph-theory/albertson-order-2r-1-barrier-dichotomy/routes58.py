#!/usr/bin/env python3
"""
The branch hypothesis imposes one of seventy necessary conditions.

WHY THIS EXISTS.  Both arguments the chain has -- crossing and absorption -- are
now measured out at order 58 (exhaust58.py, profile58.py).  What is left is the
branch hypothesis itself, and it turns out to be far weaker than the condition it
is standing in for.  Two findings, one a verification and one a lever.

==============================================================================
THE CLIQUE-COVER ARITHMETIC.

H is K_4-free, so every clique of a cover has at most three vertices.  A cover
built from a vertex-disjoint packing of t_3 triangles and t_2 edges, with the
uncovered vertices as singletons, uses

        58 - (2 t_3 + t_2)   cliques,

so theta(H) <= 28 holds if and only if some vertex-disjoint packing has

        2 t_3 + t_2 >= 30 ,   3 t_3 + 2 t_2 <= 58 ,   t_3 + t_2 <= 28 .

Enumerating those constraints gives SEVENTY admissible (t_3, t_2) families, the
smallest two being

        (t_3, t_2) = (2, 26)   covering all 58 vertices,
        (t_3, t_2) = (3, 24)   covering 57, one vertex left over.

The branch hypothesis (TT) -- "no two disjoint triangles T_1, T_2 with
H - T_1 - T_2 having a perfect matching" -- is exactly the exclusion of the FIRST
family and of nothing else.  The other sixty-nine are equally valid routes to
theta(H) <= 28 and none of them has ever been imposed.

==============================================================================
WHERE THE SECOND ROUTE IS AVAILABLE.

The (3, 24) family needs three pairwise disjoint triangles in H.  The barrier
supplies two, inside B.  A third must avoid B, and the Gallai structure supplies
it: with k >= 3 blocks the blocks are cliques of G, hence independent sets of H,
so H[L] CONTAINS the complete multipartite graph on them, and picking one vertex
from each of three blocks gives a triangle of H.  Disjointly, that is min_i q_i
of them.

So on every surviving configuration with three or more blocks, H has at least
three pairwise disjoint triangles and the (3, 24) route is available: it asks
whether H minus three disjoint triangles -- 49 vertices -- has a matching of 24.
That is a condition the branch never excluded.

Measured below: it applies to 8141 of the 8623 surviving clique-block
configurations, which is 94 per cent of what remains.

==============================================================================
A VERIFICATION: ABSORPTION INTO A TRIANGLE CLASS IS IMPOSSIBLE.

alpha(G[L]) <= 3, so a colour class of G[L] has at most three vertices, and a
class of exactly three is a triangle of H.  Absorbing z into it would need z
H-adjacent to all three, giving a K_4.  So triangle classes CANNOT absorb, and
with t_i classes of size i,

        t_1 + t_2 + t_3 = q_1 ,   t_1 + 2 t_2 + 3 t_3 = |L| ,

the absorbable classes number t_1 + t_2 = q_1 - t_3 while the singletons number
t_1 = 2 q_1 - |L| + t_3.  Raising t_3 buys singletons and costs absorbable
classes, and the chain has been taking s at the value t_3 = q_3 that maximises
singletons while implicitly assuming all q_1 classes can absorb.  That is
inconsistent, and the missing requirement is

        t  <=  q_1 - t_3 .

Checked below: NONE of the 3-or-more-block partition configurations is closed by
the absorption argument at all -- they are open, or killed by the crossing bound
-- so the inconsistency is LATENT rather than active.  No published elimination
rests on it, but it must be fixed in any future use of the argument.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import auditc as AC
import alpha58 as A
import turan58 as T
import residue58 as R58
import blockr58 as BR
import dichot as D
import mu58 as MU
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N58 = 2 * r
ALPHA = 3


def families():
    """All (t_3, t_2) with a packing forcing theta(H) <= 28."""
    out = []
    for t3 in range(0, 25):
        for t2 in range(0, 32):
            if 2 * t3 + t2 >= 30 and 3 * t3 + 2 * t2 <= N58 and t3 + t2 <= 28:
                out.append((t3, t2))
    return sorted(out)


def t3_range(NL, mult):
    q1 = mult[0]
    q3 = mult[2] if len(mult) > 2 else 0
    return max(0, NL - 2 * q1), min(q3, (NL - q1) // 2)


def corrected_ok(NL, mult, t, mu1, mu2, NZ, Za):
    """The absorption test with the triangle-class cap t <= q_1 - t_3."""
    q1 = mult[0]
    lo, hi = t3_range(NL, mult)
    for t3 in range(lo, hi + 1):
        t1 = 2 * q1 - NL + t3
        if t1 < 0 or t > q1 - t3:
            continue
        if Za >= t and mu1 >= t and mu1 + mu2 >= NZ + max(0, t - t1):
            return True
    return False


def main():
    print("How many necessary conditions does the branch hypothesis impose?")
    print("Z(29) = %d;  H is K_4-free, so every cover clique has <= 3 vertices."
          % Z)
    print()
    fam = families()
    print("PART 1   the clique-cover families forcing theta(H) <= 28")
    print("   2 t_3 + t_2 >= 30,  3 t_3 + 2 t_2 <= 58,  t_3 + t_2 <= 28")
    print("   families: %d;  smallest t_3 = %d" % (len(fam), min(f[0] for f in fam)))
    for f in fam[:4]:
        print("        (t_3,t_2) = (%2d,%2d): covers %2d vertices in %2d parts,"
              " savings %d" % (f[0], f[1], 3 * f[0] + 2 * f[1], f[0] + f[1],
                               2 * f[0] + f[1]))
    print("   The branch hypothesis (TT) excludes (2,26) and NOTHING ELSE,")
    print("   so %d of the %d necessary conditions are unimposed."
          % (len(fam) - 1, len(fam)))
    print()

    print("PART 2   where the (3,24) route is available, and the triangle cap")
    tot = three = examined = wrong = 0
    byk = {}
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            cp = T.turan_k4free(RSZ)
            for mult, eL in AC.multisets_audited(NL, max(base, 0),
                                                 base + RSZ * (RSZ - 1) // 2,
                                                 d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                eGR = eL - base
                eHR = RSZ * (RSZ - 1) // 2 - eGR
                if eGR < 0 or eHR < 0 or eHR > cp:
                    continue
                if A.alpha_lb(mult, NL) > ALPHA:
                    continue
                open_here = bool(R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx))
                killed = BR.blockR(mult, NL, RSZ, eHR) >= Z
                if open_here and not killed:
                    tot += 1
                    byk[len(mult)] = byk.get(len(mult), 0) + 1
                    if len(mult) >= 3:
                        three += 1
                # the triangle-class check, on 3+ block partitions the chain closed
                if (not open_here) and (not killed) and sum(mult) == NL \
                        and len(mult) >= 3:
                    NZ = RSZ - 1
                    q1 = mult[0]
                    side2 = R58.second_side(NL, mult)
                    nu = min(eHR, RSZ // 2)
                    t = q1 + RSZ - 28 - nu
                    if t <= 0:
                        continue
                    examined += 1
                    Sa = max(q1 * (q1 + RSZ - 29) - 4, 0)
                    Sb = max(R58.second_edges(NL, mult, RSZ) - 4, 0)
                    mu1 = max(MU.koenig(Sa, q1, NZ), D.defect_mu(Sa, q1, NZ, 1))
                    mu2 = max(MU.koenig(Sb, side2, NZ),
                              D.defect_mu(Sb, side2, NZ, 1))
                    if not corrected_ok(NL, mult, t, mu1, mu2, NZ, NZ):
                        wrong += 1
    print("   surviving clique-block configurations: %d" % tot)
    print("   by block count: %s"
          % ", ".join("%d blocks: %d" % (k, byk[k]) for k in sorted(byk)))
    print("   with >= 3 blocks, so H[L] is complete multipartite and supplies")
    print("   min_i q_i disjoint triangles inside L: %d  (%d%% of the case)"
          % (three, (100 * three) // tot))
    print()
    print("   triangle-class cap t <= q_1 - t_3: %d of the 3-or-more-block"
          % examined)
    print("   partition configurations are closed by the ABSORPTION argument at")
    print("   all -- the rest are open, or killed by the crossing bound -- so")
    print("   the cap has nothing to bite on there and %d must be withdrawn."
          % wrong)
    if examined == 0:
        print("   The inconsistency is therefore latent, not active: it should be")
        print("   fixed in any future use of the argument, but no published")
        print("   elimination rests on it.")
    print()
    print("CONCLUSION")
    print("   The chain's two arguments are exhausted, and the branch hypothesis")
    print("   turns out to impose 1 of %d necessary conditions.  The next one,"
          % len(fam))
    print("   the (3,24) route, is AVAILABLE on %d%% of what remains, because"
          % ((100 * three) // tot))
    print("   three or more Gallai blocks put a complete multipartite graph")
    print("   inside H[L] and hence three pairwise disjoint triangles in H.")
    print("   It asks whether H minus three disjoint triangles, on 49 vertices,")
    print("   has a matching of 24 -- a question about H as a graph, which is")
    print("   why the parameter enumeration in this directory cannot answer it.")
    print()
    print("   Order 58 at r = 29 remains open; r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
