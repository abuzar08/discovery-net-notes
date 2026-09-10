"""reviewer-1: does the triangle-free condition remove any of the 8313 clique-block
survivors? Replicates the lane's own part-2 loop and adds the new filter."""
import verify_range as V, auditc as AC, alpha58 as A, turan58 as T
import residue58 as R58, blockr58 as BR
from order2r import RCHI, Z

r = RCHI; DEG = r - 1; crK = V.crK; N58 = 2 * r; ALPHA = 3; CW = 4

def cap_w(R): return (R - 1) * (R - 1) // 3 + CW

def tricap(R, q):
    rho = q + R - 29
    if rho < 0 or rho > R: return None
    out = R - rho
    return rho * rho // 4 + rho * out + out * out // 3

tot = alive = removed = 0
worst = []
for m in (838, 839, 840):
    X = 2 * m - N58 * DEG
    sx = X - (r + 2 - 6)
    Rmax = 1 + max(0, sx)
    for RSZ in range(11, Rmax + 1):
        NL = N58 - RSZ; d0 = DEG - RSZ
        base = m - DEG * RSZ - X
        old, new = T.turan_k4free(RSZ), cap_w(RSZ)
        for mult, eL in AC.multisets_audited(NL, max(base, 0),
                                             base + RSZ * (RSZ - 1) // 2, d0, r):
            if sum(crK(q) for q in mult) >= Z: continue
            eGR = eL - base
            eHR = RSZ * (RSZ - 1) // 2 - eGR
            if eGR < 0 or eHR < 0 or eHR > old: continue
            if A.alpha_lb(mult, NL) > ALPHA: continue
            if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx): continue
            if BR.blockR(mult, NL, RSZ, eHR) >= Z: continue
            if eHR > new: continue                       # w-cap already applied
            tot += 1
            tc = tricap(RSZ, max(mult))
            if tc is not None and eHR > tc:
                removed += 1
                if len(worst) < 5: worst.append((m, RSZ, tuple(mult), eHR, tc))
            else:
                alive += 1
                if tc is not None:
                    worst_gap = tc - eHR
print("clique-block survivors after the w-cap:", tot)
print("removed by the triangle-free condition:", removed, "(the document claims 0)")
print("still alive:", alive)
if worst: print("examples removed:", worst)
