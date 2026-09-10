r"""reviewer-1: independent checks on the involution bound and the order-4 sizing
of the r55-42 automorphism census.
"""
import itertools
import sys
from collections import Counter

sys.path.insert(0, '../r55o9')
from indep_o9 import perm_from_type, pair_orbits

N = 42
FMAX = 36


def z4_types():
    out = []
    for c4 in range(1, N // 4 + 1):
        for c2 in range((N - 4 * c4) // 2 + 1):
            c1 = N - 4 * c4 - 2 * c2
            if c1 < 0:
                continue
            if c1 + 2 * c2 > FMAX:          # sigma^2 is an involution
                continue
            out.append((c1, c2, c4))
    return out


def z2z2_actions(ordered=True):
    out = []
    for n4 in range(N // 4 + 1):
        rest = N - 4 * n4
        for na in range(rest // 2 + 1):
            for nb in range((rest - 2 * na) // 2 + 1):
                for nc in range((rest - 2 * na - 2 * nb) // 2 + 1):
                    n1 = rest - 2 * (na + nb + nc)
                    if n1 < 0:
                        continue
                    fs = (n1 + 2 * na, n1 + 2 * nb, n1 + 2 * nc)
                    if max(fs) > FMAX:
                        continue
                    key = (n1, tuple(sorted((na, nb, nc))), n4)
                    out.append((n1, na, nb, nc, n4) if ordered else key)
    return out if ordered else sorted(set(out))


def orbits_of(cycles):
    p = perm_from_type(cycles)
    return pair_orbits(p)[1]


def main():
    print('(1) the involution bound, and what the pair-orbit count does')
    lo = hi = None
    for k in range(1, N // 2 + 1):
        f = N - 2 * k
        if f > FMAX:
            continue
        o = orbits_of([1] * f + [2] * k)
        lo = o if lo is None else min(lo, o)
        hi = o if hi is None else max(hi, o)
    print(f'    involutions with f <= {FMAX}: pair orbits range {lo} to {hi} '
          f'(published 441 to 747: '
          f'{"match" if (lo, hi) == (441, 747) else "DIFFER"})')
    print(f'    closed form C(f,2) + fk + 2C(k,2) + k at the endpoints: '
          f'f=0,k=21 -> {2*210+21}, f=36,k=3 -> {36*35//2 + 108 + 2*3 + 3}')
    print()
    print('(2) the Z_4 enumeration')
    ts = z4_types()
    print(f'    cycle types with c_4 >= 1 and c_1 + 2c_2 <= {FMAX}: {len(ts)} '
          f'(published 90: {"match" if len(ts) == 90 else "DIFFER"})')
    os_ = [(orbits_of([1] * a + [2] * b + [4] * c), (a, b, c)) for a, b, c in ts]
    os_.sort()
    print(f'    pair orbits range {os_[0][0]} to {os_[-1][0]} '
          f'(published 221 to 637: '
          f'{"match" if (os_[0][0], os_[-1][0]) == (221, 637) else "DIFFER"})')
    print(f'    the smallest is type 1^{os_[0][1][0]} 2^{os_[0][1][1]} '
          f'4^{os_[0][1][2]} with {os_[0][0]} orbits '
          f'(published smallest: 1^0 2^1 4^10 with 221)')
    print()
    print('(3) the Z_2 x Z_2 enumeration')
    a1 = z2z2_actions(ordered=True)
    a2 = z2z2_actions(ordered=False)
    print(f'    orbit-structure tuples (n_1, n_a, n_b, n_c, n_4) with every '
          f'involution at f <= {FMAX}: {len(a1)} ordered, {len(a2)} up to '
          f'relabelling the three subgroups')
    print(f'    published 1347 -> '
          f'{"matches the ordered count" if len(a1) == 1347 else ("matches the unordered count" if len(a2) == 1347 else "matches neither (%d / %d)" % (len(a1), len(a2)))}')


if __name__ == '__main__':
    main()
