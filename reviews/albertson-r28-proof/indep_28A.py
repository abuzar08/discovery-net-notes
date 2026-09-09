r"""reviewer-1: Part A of the r = 28 proof attempt, with Kostochka-Yancey floors
only (Cranston's Lemma E is a preprint I do not have).

For each order n in the published surviving band, enumerate the Gallai join
decompositions: parts with r_i = 1 and v_i = 1, or r_i >= 3 and v_i >= 2r_i - 1,
with sum r_i = 28 and sum v_i = n; require sum over parts of the
Kostochka-Yancey floor, plus the edges of the complete multipartite graph on the
parts, to fit inside the edge budget; and require some part with r_j >= 4 (the
subdivision-transfer constraint).
"""
import itertools, sys
from math import comb

R = 28
BANDS = {33: (471, 494), 34: (484, 509), 50: (700, 712), 51: (714, 724),
         52: (727, 735), 53: (741, 746), 54: (754, 757)}


def ky(r, v):
    """Kostochka-Yancey: an r-critical graph on v vertices has at least
    ceil( ((r+1)(r-2)v - r(r-3)) / (2(r-1)) ) edges"""
    num = (r + 1) * (r - 2) * v - r * (r - 3)
    den = 2 * (r - 1)
    return -(-num // den)


def parts(nleft, rleft, minr, cur, out, n):
    if rleft == 0:
        if nleft == 0:
            out.append(tuple(cur))
        return
    for r in range(minr, rleft + 1):
        if r == 2:
            continue                     # a 2-critical part is K_2, excluded
        vmin = 1 if r == 1 else 2 * r - 1
        for v in range(vmin, nleft + 1):
            if r == 1 and v != 1:
                break
            parts(nleft - v, rleft - r, r, cur + [(r, v)], out, n)


def main():
    for n, (mlo, mhi) in BANDS.items():
        out = []
        parts(n, R, 1, [], out, n)
        ok = []
        for p in out:
            if not any(r >= 4 for r, v in p):
                continue                 # subdivision transfer needs some r>=4
            vs = [v for _, v in p]
            eM = (n * n - sum(v * v for v in vs)) // 2
            floor = eM + sum(ky(r, v) for r, v in p if r >= 3)
            if floor <= mhi:
                ok.append((p, floor))
        print(f'n = {n}: {len(out)} decompositions, {len(ok)} within the edge '
              f'budget [{mlo},{mhi}] under Kostochka-Yancey floors alone'
              + (f'; tightest {min(f for _, f in ok)}' if ok else ''))


if __name__ == '__main__':
    main()
