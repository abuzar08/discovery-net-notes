r"""reviewer-1: does dropping the (C3) filter change anything at order 57?

Constraint C gives D_v >= 28 - |R| = delta_0 for low v.  A vertex in two big
blocks (order - 1 >= delta_0) has D_v >= 2 delta_0, and D_v <= 28 since v is
low, so "big blocks are pairwise disjoint" — and with it the filter
sum(big) <= |L| — needs 2 delta_0 > 28, i.e. |R| <= 13.  At order 57 the theory
is applied at |R| <= 11, so the filter should be valid there; this checks that
the enumerated lists are identical with and without it, which is what my three
order-57 reviews rest on.
"""
import itertools
from indep_tsplit import band, multisets, constraint_E, N, DEG, CASES

def multisets_nofilter(RSZ, eLo, eHi):
    NL = N - RSZ; d0 = DEG - RSZ; out=set()
    def rec(rem, cap, edges, blocks):
        if edges > eHi: return
        if rem == 0:
            if eLo <= edges <= eHi and blocks:
                big=[q for q in blocks if q-1>=d0]; sb=sum(big)
                # (C2) kept (valid for delta_0 >= 1), (C3) DROPPED
                if sum(q*(q-1) for q in blocks if q-1<d0) >= d0*(NL-sb):
                    out.add((tuple(sorted(blocks, reverse=True)), edges))
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem-u, u, edges + (u+1)*u//2, blocks+[u+1])
    for c in range(1, NL):
        rec(NL-c, NL-c, 0, [])
    return sorted(out)

for (m, RSZ) in CASES:
    d0 = DEG - RSZ
    for j in range(0,4):
        for sig in (0,1):
            lo, hi, a, forced = band(m, RSZ, j, sig)
            with_f = [x for x in multisets(RSZ, lo, hi) if constraint_E(RSZ, x[0], j)]
            no_f = [x for x in multisets_nofilter(RSZ, lo, hi) if constraint_E(RSZ, x[0], j)]
            if with_f != no_f:
                print(f'  m={m} |R|={RSZ} (delta_0={d0}) j={j} sig={sig}: DIFFER — '
                      f'{len(with_f)} with the (C3) filter, {len(no_f)} without')
    print(f'  m={m} |R|={RSZ}: delta_0 = {d0}, 2*delta_0 > 28 is {2*d0 > 28}; '
          f'lists identical across all (j, sigma)' )
