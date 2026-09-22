"""Audit of the vertex-disjointness bookkeeping inside residue58.survivors.

In the survivor loop a sub-case (k_1, k_2) is discarded as impossible when

    cross = crK(q1 + c1) + crK(q2 + c2) + crK(rest)  >=  Z,

with the overlap count k12 -- the number of z one-sided on BOTH sides -- fixed
at min(k1, k2), the comment justifying that as "the largest feasible number,
which is the worst case for us".

But k12 is not determined by (k1, k2): counting forces only

    max(0, k1 + k2 - NZ)  <=  k12  <=  min(k1, k2),

and cross is not monotone in k12, since raising k12 shrinks the second clique
(c2 = max(0, k2 - k12 - eHR)) while growing the third (rest), and crK is
convex.  The conservative test is therefore the MINIMUM of cross over the
feasible range; discarding the sub-case is justified only if even that minimum
reaches Z.

This script re-runs the whole survivor loop with cross replaced by that
minimum and reports (a) how often the two differ, (b) how often the code's
single choice discards a sub-case the conservative reading keeps, and (c)
whether any configuration's CLOSURE STATUS flips as a result.
"""
import sys

import dichot as D
import mu58 as MU
import residue58 as R58
import tuttegen as G
from order2r import Z

crK = R58.crK
DEG = R58.DEG
NW, CW = 1, 4

STATS = {"subcases": 0, "differ": 0, "rescued": 0}


def cross_values(q1, q2, RSZ, eHR, k1, k2, NZ):
    """cross at the code's k12, and the minimum over all feasible k12."""
    lo = max(0, k1 + k2 - NZ)
    hi = min(k1, k2)
    vals = {}
    for k12 in range(lo, hi + 1):
        c1 = max(0, k1 - eHR)
        c2 = max(0, (k2 - k12) - eHR)
        rest = max(0, RSZ - (k1 + k2 - k12) - eHR)
        vals[k12] = crK(q1 + c1) + crK(q2 + c2) + crK(rest)
    return vals[hi], min(vals.values())


def survivors_conservative(nn, m, RSZ, mult, eL, nw, cw, sx_max):
    """residue58.survivors, with cross minimised over the feasible overlap."""
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
    side2 = R58.second_side(NL, mult)
    nu = min(eHR, RSZ // 2)
    t = q1 + RSZ - 28 - nu
    if t <= 0:
        return []
    d0 = DEG - RSZ
    s = D.singletons(NL, mult, d0)
    e1 = q1 * (q1 + RSZ - 29)
    e2 = R58.second_edges(NL, mult, RSZ)
    c1c, c2c = R58.side_caps(nn, NL, RSZ, mult, m, eHR, eL)
    e1 = max(e1, c1c)
    e2 = max(e2, c2c)
    thr1, thr2 = R58.thresholds(nn, NL, mult)
    budget = sx_max + 2 * eHR
    need = NZ + max(0, t - s)
    bad = []
    for k1 in range(0, NZ + 1):
        for k2 in range(0, NZ + 1):
            res = R58.residue(NZ, budget, thr1, thr2, k1, k2)
            if res is None:
                continue
            amin1, amin2, Sa_r, Sb_r = res
            Za, Zb = NZ - k1, NZ - k2
            if amin1 > q1 or amin2 > side2:
                continue
            code_cross, min_cross = cross_values(q1, q2, RSZ, eHR, k1, k2, NZ)
            STATS["subcases"] += 1
            if code_cross != min_cross:
                STATS["differ"] += 1
            if code_cross >= Z and min_cross < Z:
                STATS["rescued"] += 1
            if min_cross >= Z:
                continue
            surv = None
            for cw1 in range(0, cw + 1):
                cw2 = cw - cw1
                Sa = max(e1 - cw1, Sa_r)
                Sb = max(e2 - cw2, Sb_r)
                if Sa > Za * q1 or Sb > Zb * side2:
                    continue
                mu1 = (max(MU.koenig(Sa, q1, Za),
                           D.defect_mu(Sa, q1, Za, max(amin1, 1)))
                       if Za > 0 else 0)
                mu2 = (max(MU.koenig(Sb, side2, Zb),
                           D.defect_mu(Sb, side2, Zb, max(amin2, 1)))
                       if Zb > 0 else 0)
                if not (Za >= t and mu1 >= t and mu1 + mu2 >= need):
                    surv = (mu1, mu2, cw1, cw2)
                    break
            if surv is not None:
                bad.append((k1, k2))
    return bad


def parts(m, RSZ, eHR):
    X = 2 * m - G.N58 * G.DEG
    sx = X - (G.RCHI + 2 - 6)
    base = m - G.DEG * RSZ - X
    eL = base + RSZ * (RSZ - 1) // 2 - eHR
    return X, sx, eL


def main():
    cfgs = G.configurations()
    print("all clique-block configurations at order 58: %d" % len(cfgs))
    flips, checked, cover = 0, 0, 0
    for m, RSZ, mult, eHR in cfgs:
        X, sx, eL = parts(m, RSZ, eHR)
        if G.route_closed(RSZ, list(mult), eHR, X)[0]:
            cover += 1
            continue
        a = R58.survivors(G.N58, m, RSZ, list(mult), eL, NW, CW, sx)
        b = survivors_conservative(G.N58, m, RSZ, list(mult), eL, NW, CW, sx)
        if a is None or b is None:
            continue
        checked += 1
        if (not a) != (not b):
            flips += 1
            print("   CLOSURE FLIP m=%d |R|=%d mult=%s eHR=%d: code %s, "
                  "conservative %s"
                  % (m, RSZ, list(mult), eHR,
                     "closed" if not a else "open",
                     "closed" if not b else "open"))
    print("closed by the clique cover, not examined here: %d" % cover)
    print("configurations re-decided: %d" % checked)
    print("sub-cases reached: %d" % STATS["subcases"])
    print("sub-cases where the code's k12 = min(k1,k2) is not the minimising "
          "overlap: %d" % STATS["differ"])
    print("sub-cases the code discards but the conservative reading keeps: %d"
          % STATS["rescued"])
    print("configurations whose closure status flips: %d" % flips)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
