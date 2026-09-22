"""reviewer-1: the hitting-tail distribution recomputed over the CORRECTED
out-of-scope population, with the unlisted block restored."""
import collections
import verify_range as V, auditc as AC, alpha58 as A, turan58 as T
import residue58 as R58, blockr58 as BR, tuttegen as TG, packing58 as PK
from order2r import RCHI, Z

r = RCHI; DEG = r - 1; crK = V.crK; N58 = 2 * r; ALPHA = 3

old_pop = collections.Counter()
new_pop = collections.Counter()
scope_old = scope_new = 0
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
            tb = TG.true_blocks(mult, RSZ, eHR, X)
            k_old = PK.kmax_exact(list(mult), NL)
            k_new = PK.kmax_exact(tb, NL)
            if k_old < 3:
                scope_old += 1
                old_pop[PK.hitting_tail(list(mult), NL)] += 1
            if k_new < 3:
                scope_new += 1
                new_pop[PK.hitting_tail(list(tb), NL)] += 1
print('out of scope on the uncorrected multiset:', scope_old,
      '  tails', dict(sorted(old_pop.items())))
print('out of scope on the corrected multiset  :', scope_new,
      '  tails', dict(sorted(new_pop.items())))
print('a tail of 7 or more, which would certify nu_tri >= 3:',
      sum(v for k, v in new_pop.items() if k >= 7))
