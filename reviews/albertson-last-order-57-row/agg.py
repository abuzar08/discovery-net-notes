r"""reviewer-1: locate the '26 against 145' comparison of h3293.

The per-block value 145 is e_H(Q_1, R) for the multiset (24,22,2) at |R| = 11
ONCE the cut-vertex extra is included: 23 vertices of Q_1 lie only in Q_1 and
have D_v = 23, the 24th also lies in the connector block and has D_v = 24, so
e_H(Q_1,R) = 24(|R| - 28) + (23*23 + 24).  This reports that value and every
natural reading of the aggregate bound it is contrasted with.
"""
from indep_293 import identities, N, DEG, RCHI

for RSZ, mult in [(11, (24, 22, 2)), (11, (24, 22)), (10, (24, 23, 2)),
                  (10, (24, 23))]:
    NL, NZ = N - RSZ, RSZ - 2
    eL = sum(q * (q - 1) // 2 for q in mult)
    I = identities(RSZ, eL)
    maxq = max(mult)
    conn = len(mult) > 2                      # a connector block of order 2
    sumD = (maxq - 1) * (maxq - 1) + (maxq if conn else maxq - 1)
    per_extra = maxq * (RSZ - DEG) + sumD
    per_plain = maxq * (maxq + RSZ - RCHI)
    print(f'|R|={RSZ} {mult}: e(L)={eL}, e_H(L,R)={I["eHLR"]}, '
          f'per-block e_H(Q_1,R) plain {per_plain}, with cut-vertex extra '
          f'{per_extra}')
    for name, val in [
        ('e_H(L,R) - |Z|*|L - Q_1|', I['eHLR'] - NZ * (NL - maxq)),
        ('e_H(L,R) - |Z|*(|L - Q_1| + 1)', I['eHLR'] - NZ * (NL - maxq + 1)),
        ('e_H(L,R) - |R|*|L - Q_1|', I['eHLR'] - RSZ * (NL - maxq)),
        ('(e_H(L,R) - 4) - |Z|*|L - Q_1|', I['eHLR'] - 4 - NZ * (NL - maxq)),
    ]:
        print(f'      aggregate {name:34s} = {val}')
