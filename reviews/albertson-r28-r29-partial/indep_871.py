"""reviewer-1: independent checks of h2871 (researcher-2), rebuilt from the
mathematics rather than from r28.py / r29.py.

Order n = 2r-1, G r-critical with cr(G) < cr(K_r), H = complement connected and
(by Stehlik/Gallai) factor-critical.  Then d_G(v)+d_H(v) = 2r-2 and
x_v = d_G(v)-(r-1) = r-1-d_H(v) >= 0, X := sum_v x_v = 2m - n(r-1).
In the unique surviving configuration B = T u {s} (T an H-triangle),
H - B = C u {w1} u {w2}, A_i := N_T(w_i) with A_1, A_2 disjoint, so
d_H(w_i) <= |A_i|+1 and x_{w1}+x_{w2} >= 2(r-1) - 5 = 2r-7, giving
|R| <= 2 + (X - (2r-7)) for the set R of vertices of positive excess.

  (1) the e(G[R]) floor of section 3 of h2871, re-derived and brute-forced;
  (2) the row tables: e(L) >= m - ((r-1)|R| + X) + floor(|R|), against my own
      Gallai cap (blocks are cliques of order <= r-2 or odd cycles) and my own
      split bound (crossing number is additive over blocks), with cr(K_q)
      seeded either by cr(K_14) = 315 or only by cr(K_12) = 150;
  (3) the exact integer order bands of section 1.

usage: python3 indep_871.py
"""
from functools import lru_cache
from itertools import product

CR12 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}
CR14 = {**CR12, 13: 225, 14: 315}


def make_crK(base):
    @lru_cache(maxsize=None)
    def crK(q):
        if q in base:
            return base[q]
        return -(-q * crK(q - 1) // (q - 4))
    return crK


def Z(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


# ---------------------------------------------------------------- (1) the floor
def egr_floor_formula(Rsz, tsize=3):
    """min of 1 + 2(|Z|-sigma-tA-tO) + tA + 2 tO + sigma*tA over the admissible
    (sigma, tA, tO), which is what section 3 of h2871 minimises"""
    Zs = Rsz - 2
    best = None
    for sigma in (0, 1):
        for tA in range(0, tsize + 1):
            for tO in range(0, tsize + 1 - tA):
                if sigma + tA + tO > Zs:
                    continue
                v = 1 + 2 * (Zs - sigma - tA - tO) + tA + 2 * tO + sigma * tA
                if best is None or v < best:
                    best = v
    return max(1, best if best is not None else 1)


def egr_floor_bruteforce(Rsz, tsize=3):
    """same floor, obtained by enumerating where the |R|-2 further high vertices
    can sit (C, A_1, A_2, T minus A_1 u A_2, or s) and counting the G-edges that
    the structure forces, without using the closed formula"""
    Zs = Rsz - 2
    best = None
    # a high vertex sits in: 'C', 'A1', 'A2', 'T0' (T outside A_1 u A_2), or 's'
    slots = ['C', 'A1', 'A2', 'T0', 's']
    for assign in product(slots, repeat=Zs):
        if assign.count('s') > 1:
            continue
        if assign.count('A1') + assign.count('A2') + assign.count('T0') > tsize:
            continue
        e = 1                                    # w1 w2
        for a in assign:
            if a == 'C':
                e += 2                           # G-adjacent to both w_i
            elif a in ('A1', 'A2'):
                e += 1                           # H-adjacent to one w_i only
            elif a == 'T0':
                e += 2                           # H-adjacent to neither w_i
            # s: H-adjacent to both, contributes nothing to the w's
        if 's' in assign:
            e += assign.count('A1') + assign.count('A2')     # s is G-adjacent to A_1 u A_2
        if best is None or e < best:
            best = e
    return max(1, best if best is not None else 1)


# ------------------------------------------------------- (2) cap and split bound
def gallai_cap(nv, maxblk, at_most_one_max=True):
    U = nv - 1
    dp = [[-1, -1] for _ in range(U + 1)]
    dp[0][1] = 0
    for t in range(U + 1):
        for s in (0, 1):
            if dp[t][s] < 0:
                continue
            for u in range(1, U - t + 1):
                blk = u + 1
                opts = []
                if blk <= maxblk - 1 or (not at_most_one_max and blk <= maxblk):
                    opts.append((u * (u + 1) // 2, s))
                elif blk == maxblk and s == 1:
                    opts.append((u * (u + 1) // 2, 0))
                if u >= 2 and blk % 2 == 1:
                    opts.append((blk, s))
                for e, ns in opts:
                    if dp[t][s] + e > dp[t + u][ns]:
                        dp[t + u][ns] = dp[t][s] + e
    return max(dp[U])


def min_split(nv, e_lo, crK, maxblk=None):
    best = [None]

    def rec(rem, cap, edges, cliques):
        if rem == 0:
            if edges >= e_lo:
                s = sum(crK(b) for b in cliques if b >= 15)
                if best[0] is None or s < best[0]:
                    best[0] = s
            return
        hi, rr, c2 = edges, rem, cap
        while rr > 0:
            t = min(c2, rr)
            hi += t * (t + 1) // 2
            rr -= t
        if hi < e_lo:
            return
        for u in range(min(cap, rem), 0, -1):
            if maxblk is None or u + 1 <= maxblk:
                rec(rem - u, u, edges + u * (u + 1) // 2, cliques + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, cliques)

    for c in range(1, nv):
        rec(nv - c, nv - c, 0, [])
    return best[0]


def rows(r, ms, crK, floors, at_most_one_max=True):
    n = 2 * r - 1
    out = []
    for m in ms:
        X = 2 * m - n * (r - 1)
        hi = 2 + (X - (2 * (r - 1) - 5))
        for Rsz in range(2, hi + 1):
            VL = n - Rsz
            eL = m - ((r - 1) * Rsz + X) + floors[Rsz]
            cap = gallai_cap(VL, r - 2, at_most_one_max)
            sp = min_split(VL, eL, crK, r - 2)
            out.append((m, Rsz, VL, eL, cap, sp,
                        eL > cap or (sp is not None and sp > Z(r))))
    return out


def main():
    floors = {k: egr_floor_formula(k) for k in range(2, 12)}
    brute = {k: egr_floor_bruteforce(k) for k in range(2, 12)}
    print('(1) e(G[R]) floor for |R| = 2..11')
    print('    h2871 claims        : [1, 1, 3, 4, 6, 8, 10, 12, 14, 16]')
    print(f'    my closed form      : {[floors[k] for k in range(2, 12)]}')
    print(f'    my brute force      : {[brute[k] for k in range(2, 12)]}')
    print(f'    agree: {[floors[k] for k in range(2, 12)] == [brute[k] for k in range(2, 12)] == [1, 1, 3, 4, 6, 8, 10, 12, 14, 16]}')
    print()

    for r, ms, label in ((28, (768, 769), 'r = 28, order 55'), (29, (824, 825, 826, 827, 828), 'r = 29, order 57')):
        for base, bname in ((CR14, 'cr(K_14)=315'), (CR12, 'cr(K_12)=150 only')):
            crK = make_crK(base)
            tab = rows(r, ms, crK, floors)
            splits = [t[5] for t in tab if t[5] is not None]
            surv = [(t[0], t[1]) for t in tab if not t[6]]
            print(f'(2) {label}, {bname}: {len(tab)} rows, Z({r}) = {Z(r)}')
            print(f'    split minima: {splits}')
            if splits:
                print(f'    tightest margin over Z({r}): {min(splits) - Z(r)}')
            print(f'    rows not closed: {surv if surv else "none"}')
        print()

    print('(3) exact integer order bands (section 1)')
    for name, dec, exact in (('n >= 2.82 r', (2.82,), (50, 141)),
                             ('n >= 1.228 r', (1.228,), (250, 307)),
                             ('n <= 1.768 r', (1.768,), (125, 221))):
        print(f'    {name}: {exact[1]}/{exact[0]} = {exact[1] / exact[0]} == {dec[0]}: {exact[1] / exact[0] == dec[0]}')
    for r in (28, 29):
        band = [n for n in range(r + 5, 90)
                if not (50 * n >= 141 * r or (250 * n >= 307 * r and 125 * n <= 221 * r))]
        print(f'    r = {r}: orders NOT excluded by the integer bands: {band}')


if __name__ == '__main__':
    main()
