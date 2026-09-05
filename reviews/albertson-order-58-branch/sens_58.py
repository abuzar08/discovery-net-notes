"""reviewer-1: sensitivity of the b >= 8 closure of h3014 to the crossing-number
seeding.  The classifier is the target's own (k4free.branch_survivors); only
verify_range.crK is replaced, by my conservative recursion seeded solely by
cr(K_12) = 150 (Guy; Pan-Richter 2007), so that the CCCG 2021 values
cr(K_13) = 225 and cr(K_14) = 315 are not used anywhere."""
from functools import lru_cache
import verify_range as V

CR12 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}

@lru_cache(maxsize=None)
def crK12(q):
    if q in CR12:
        return CR12[q]
    return -(-q * crK12(q - 1) // (q - 4))

import k4free as K

for label, patch in (('as published (cr(K_14) = 315)', False),
                     ('conservative (cr(K_12) = 150 only)', True)):
    if patch:
        V.crK = crK12
        K.V.crK = crK12
    print(f'--- {label}: cr(K_24) = {V.crK(24)}, cr(K_26) = {V.crK(26)}, cr(K_28) = {V.crK(28)}')
    for m in (838, 839, 840):
        live, detail = K.branch_survivors(m, use_gallai=True, verbose_b=30)
        big = [t for t in live if t[0] >= 8]
        d30 = [d for d in detail if d[0] == 30]
        best30 = min((d[2] for d in d30), default=None)
        print(f'    m={m}: {len(live)} surviving classes, of which b >= 8: {len(big)}'
              + (f'  {[(t[0], t[2]) for t in big][:4]}' if big else '')
              + (f'; tightest b=30 split bound {best30} vs Z = {K.Z}' if best30 is not None else ''))
