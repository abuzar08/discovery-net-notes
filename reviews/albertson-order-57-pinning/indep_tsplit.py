r"""reviewer-1: independent check of the pinning lemma (height 3285, researcher-2).

This lemma supplies the configuration that the crossing lemma and the order-57
closure both inherit — \(j = 1\), \(\sigma = 0\), blocks \((24,24)\) — so it is
worth checking on its own terms.  My own code for:

  1. Constraint F, the forced non-edges inside \(R\), and the \(e(L)\) band it
     produces for every \((\text{row}, \lvert R\rvert, j, \sigma)\);
  2. Constraint E, the distinct-block requirement for the low \(T\)-vertices;
  3. the \(j = 0\) impossibility and the \(\lvert R\rvert = 9\) pinning, from my
     own enumeration of block multisets;
  4. the crossing-number arithmetic of the "opening" paragraph, under the lane's
     seeding and under conservative seeding;
  5. the per-row quantities the body states uniformly.

`r29.eGR_min` (the lower end of the band) is inherited from an earlier lemma and
used as given, as is the score column, which comes from the lane's split-bound
machinery.
"""
import itertools
import sys

sys.path.insert(0, '/Users/abuzark/.discovery-research-team/workspaces/'
                   'reviewer-1/notes/topological-graph-theory/'
                   'albertson-order-2r-1-barrier-dichotomy')
import r29

N, DEG, RCHI = 57, 28, 29
CASES = [(827, 9), (828, 9), (828, 10), (828, 11)]


def Z_hill(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def cr_lower(seed):
    cr = dict(seed)
    for q in range(max(seed) + 1, 32):
        cr[q] = -(-q * cr[q - 1] // (q - 4))
    return cr


def amin(m, RSZ):
    """every z in Z is high, so x_z >= 1 and sum_Z x_z = X - (54 - a) >= |Z|"""
    X = 2 * m - N * DEG
    return max(0, RSZ + 52 - X)


def band(m, RSZ, j, sig):
    """Constraint F as an upper bound on e(G[R]), turned into an e(L) band"""
    NL = N - RSZ
    a = amin(m, RSZ)
    forced = j * (j - 1) // 2 + max(0, j - 3 + a) + 2 * sig
    eGR_hi = RSZ * (RSZ - 1) // 2 - forced
    eGR_lo = r29.eGR_min(RSZ)
    # e(G[R]) = m - e(L) - (28|L| - 2 e(L))  =>  e(L) = e(G[R]) + 28|L| - m
    return eGR_lo + DEG * NL - m, eGR_hi + DEG * NL - m, a, forced


def multisets(RSZ, eLo, eHi):
    """my own block multisets: orders q >= 2, sum (q-1) = |L| - c components,
    e(L) = sum C(q,2) in the band, plus the lane's two documented filters"""
    NL = N - RSZ
    d0 = DEG - RSZ
    out = set()

    def rec(rem, cap, edges, blocks):
        if edges > eHi:
            return
        if rem == 0:
            if eLo <= edges <= eHi and blocks:
                big = [q for q in blocks if q - 1 >= d0]
                sb = sum(big)
                if sb <= NL and sum(q * (q - 1) for q in blocks
                                    if q - 1 < d0) >= d0 * (NL - sb):
                    out.add((tuple(sorted(blocks, reverse=True)), edges))
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem - u, u, edges + (u + 1) * u // 2, blocks + [u + 1])

    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return sorted(out)


def constraint_E(RSZ, mult, j):
    """the 3 - j low T-vertices lie in pairwise distinct blocks; a vertex lies in
    at most one big block, and the rest lie outside every big block"""
    NL = N - RSZ
    d0 = DEG - RSZ
    big = [q for q in mult if q - 1 >= d0]
    return 3 - j <= len(big) + (NL - sum(big))


def main():
    print('CONSTRAINT F: the e(L) band for every (row, |R|, j, sigma)')
    print('  row |R|  j sig   a_min forced   my band')
    for (m, RSZ) in CASES:
        for j in range(0, 4):
            for sig in (0, 1):
                lo, hi, a, forced = band(m, RSZ, j, sig)
                print(f'  {m} {RSZ:3d} {j:3d} {sig:3d} {a:7d} {forced:6d}   '
                      f'[{lo},{hi}]')
    print()

    print('CONSTRAINTS E AND F TOGETHER: which multisets survive')
    for (m, RSZ) in CASES:
        for j in range(0, 4):
            for sig in (0, 1):
                lo, hi, a, forced = band(m, RSZ, j, sig)
                ms = [mm for mm in multisets(RSZ, lo, hi)
                      if constraint_E(RSZ, mm[0], j)]
                tag = ('NO admissible multiset' if not ms
                       else f'{len(ms)} multisets: '
                            f'{[mm[0] for mm in ms][:4]}')
                print(f'  m={m} |R|={RSZ} j={j} sigma={sig}: {tag}')
        print()

    print('THE PER-ROW QUANTITIES THE BODY STATES UNIFORMLY')
    for m in (827, 828):
        RSZ, NL = 9, 48
        eL = 2 * (24 * 23 // 2)
        eGR = m - eL - (DEG * NL - 2 * eL)
        eHR = RSZ * (RSZ - 1) // 2 - eGR
        theta_start = 24 + (RSZ - eHR)
        print(f'  m = {m} with blocks (24,24): e(G[R]) = {eGR} '
              f'(= C(9,2) - {36 - eGR}), e(H[R]) = {eHR}, '
              f'theta(H) <= 24 + theta(H[R]) = {theta_start}, so four triangles '
              f'give {theta_start - 4}'
              f'{" < 29" if theta_start - 4 < RCHI else " = 29, no contradiction"}')
    print()

    print('THE CROSSING ARITHMETIC OF THE OPENING PARAGRAPH')
    for name, seed in [('lane seeding (CCCG 2021)', {12: 150, 13: 225, 14: 315}),
                       ('conservative seeding', {12: 150})]:
        cr = cr_lower(seed)
        tot = cr[26] + cr[25]
        print(f'  {name}: cr(K26) + cr(K25) = {cr[26]} + {cr[25]} = {tot} '
              f'{">=" if tot >= Z_hill(RCHI) else "<"} Z(29) = {Z_hill(RCHI)}')


if __name__ == '__main__':
    main()
