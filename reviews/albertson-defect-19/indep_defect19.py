"""reviewer-1: measure the block-omission discrepancy myself over the whole
clique-block enumeration, and check which direction it moves the guarantee."""
import collections
import verify_range as V, auditc as AC, alpha58 as A, turan58 as T
import residue58 as R58, blockr58 as BR, tuttegen as TG, packing58 as PK
from order2r import RCHI, Z

r = RCHI; DEG = r - 1; crK = V.crK; N58 = 2 * r; ALPHA = 3

dist = collections.Counter()
lost = 0
dropped = [0]
tot = 0
for m in (838, 839, 840):
    X = 2 * m - N58 * DEG
    sx = X - (r + 2 - 6)
    Rmax = 1 + max(0, sx)
    for RSZ in range(11, Rmax + 1):
        NL = N58 - RSZ
        d0 = DEG - RSZ
        base = m - DEG * RSZ - X
        old = T.turan_k4free(RSZ)
        new = (RSZ - 1) * (RSZ - 1) // 3 + 4
        for mult, eL in AC.multisets_audited(NL, max(base, 0),
                                             base + RSZ * (RSZ - 1) // 2, d0, r):
            if sum(crK(q) for q in mult) >= Z:
                continue
            eGR = eL - base
            eHR = RSZ * (RSZ - 1) // 2 - eGR
            if eGR < 0 or eHR < 0 or eHR > old or eHR > new:
                continue
            if A.alpha_lb(mult, NL) > ALPHA:
                continue
            if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                continue
            if BR.blockR(mult, NL, RSZ, eHR) >= Z:
                continue
            tot += 1
            surplus = eL - sum(q * (q - 1) // 2 for q in mult)
            dist[surplus] += 1
            if surplus > 0:
                tb = TG.true_blocks(mult, RSZ, eHR, X)
                a = PK.kmax_exact(mult, NL)
                b = PK.kmax_exact(tb, NL)
                if b < a:
                    dropped[0] += 1
                if a >= 3 > b:
                    lost += 1
print('configurations enumerated:', tot)
print('distribution of eL - sum C(q_i,2):', dict(sorted(dist.items())))
print('of the 772, kmax_exact drops on:', dropped[0])
print('of the 772, losing the triangle guarantee (>=3 to <3):', lost)
