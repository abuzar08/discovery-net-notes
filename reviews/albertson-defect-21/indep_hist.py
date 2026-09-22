"""Is the withdrawn 3196 even the histogram it is described as?

profile58.absorption_deficit takes, per surviving sub-case, the (mu_1, mu_2)
stored in residue58's survivor record.  That record holds the FIRST escaping
split cw_1 + cw_2 = cw found, in increasing cw_1 order -- not the split with
the smallest absorption deficit.  So the published figure is the least deficit
over sub-cases of an arbitrarily chosen split, not the least deficit over
sub-cases and splits.

This script recomputes the deficit map both ways and compares the two counts
at one unit, to see whether the number being withdrawn was also mislabelled
within its own definition.
"""
import sys

import dichot as D
import mu58 as MU
import profile58 as PF
import residue58 as R58
import tuttegen as G
from order2r import Z

NW, CW = 1, 4


def parts(m, RSZ, eHR):
    X = 2 * m - G.N58 * G.DEG
    sx = X - (G.RCHI + 2 - 6)
    base = m - G.DEG * RSZ - X
    eL = base + RSZ * (RSZ - 1) // 2 - eHR
    return X, sx, eL


def deficit_all_splits(nn, m, RSZ, mult, eL, nw, cw, sx_max):
    """Least need - (mu_1 + mu_2) over surviving sub-cases AND all splits."""
    NL = nn - RSZ
    NZ = RSZ - nw
    X = 2 * m - nn * R58.DEG
    base = m - R58.DEG * RSZ - X
    eGR = eL - base
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    if eGR < 0 or eHR < 0 or NZ <= 0:
        return None
    q1 = mult[0]
    side2 = R58.second_side(NL, mult)
    nu = min(eHR, RSZ // 2)
    t = q1 + RSZ - 28 - nu
    if t <= 0:
        return 0
    d0 = R58.DEG - RSZ
    s = D.singletons(NL, mult, d0)
    e1 = q1 * (q1 + RSZ - 29)
    e2 = R58.second_edges(NL, mult, RSZ)
    c1c, c2c = R58.side_caps(nn, NL, RSZ, mult, m, eHR, eL)
    e1, e2 = max(e1, c1c), max(e2, c2c)
    thr1, thr2 = R58.thresholds(nn, NL, mult)
    budget = sx_max + 2 * eHR
    need = NZ + max(0, t - s)
    best = None
    for k1 in range(0, NZ + 1):
        for k2 in range(0, NZ + 1):
            res = R58.residue(NZ, budget, thr1, thr2, k1, k2)
            if res is None:
                continue
            amin1, amin2, Sa_r, Sb_r = res
            Za, Zb = NZ - k1, NZ - k2
            if amin1 > q1 or amin2 > side2:
                continue
            k12 = min(k1, k2)
            c1 = max(0, k1 - eHR)
            c2 = max(0, (k2 - k12) - eHR)
            rest = max(0, RSZ - (k1 + k2 - k12) - eHR)
            q2 = mult[1] if len(mult) > 1 else 1
            if R58.crK(q1 + c1) + R58.crK(q2 + c2) + R58.crK(rest) >= Z:
                continue
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
                    d = need - (mu1 + mu2)
                    if best is None or d < best:
                        best = d
    return best if best is not None else 0


def main():
    pub, alt = [], []
    for m, RSZ, mult, eHR in G.configurations():
        X, sx, eL = parts(m, RSZ, eHR)
        if G.route_closed(RSZ, list(mult), eHR, X)[0]:
            continue
        bad = R58.survivors(G.N58, m, RSZ, list(mult), eL, NW, CW, sx)
        if bad is None:
            continue
        pub.append(PF.absorption_deficit(G.N58, m, RSZ, list(mult), eL, sx, bad))
        alt.append(deficit_all_splits(G.N58, m, RSZ, list(mult), eL, NW, CW, sx))
    for name, vals in (("as published (first escaping split)", pub),
                       ("least over sub-cases AND splits", alt)):
        fin = [v for v in vals if v is not None]
        print("%-38s n = %d  at most 1: %d  at most 2: %d"
              % (name, len(fin), sum(1 for v in fin if v <= 1),
                 sum(1 for v in fin if v <= 2)))
    diff = sum(1 for a, b in zip(pub, alt) if a != b)
    print("configurations where the two differ: %d" % diff)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
