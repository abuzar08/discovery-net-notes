"""reviewer-1: verify the repair of h3068 with my own bound and my own crK.

The classifier is the contribution's own (k4free.branch_survivors); both
crossing-number inputs are replaced by mine: verify_range.crK by my conservative
recursion (seeded only at cr(K_12) = 150, so cr(K_13) >= 217 comes from counting
alone) and crminus.g by my own implementation of the three ingredients."""
import verify_range as V
import crminus as C
import indep_g as I

mine_crK, mine_g = I.make({})          # bare counting seed
V.crK = mine_crK
C.g = mine_g
import k4free as K
K.V.crK = mine_crK
K.CM.g = mine_g

print(f'my crK(13) = {mine_crK(13)}, crK(28) = {mine_crK(28)}, g(28,3) = {mine_g(28,3)}')
for m in (838, 839, 840):
    live, detail = K.branch_survivors(m, use_gallai=True, verbose_b=30)
    big = [t for t in live if t[0] >= 8]
    b30 = min((d[2] for d in detail if d[0] == 30), default=None)
    print(f'  m={m}: {len(live)} classes survive, of which b >= 8: {len(big)}'
          + (f' {[(t[0], t[2]) for t in big]}' if big else '')
          + (f'; tightest b=30 split bound {b30} vs Z = {K.Z}' if b30 is not None else ''))
