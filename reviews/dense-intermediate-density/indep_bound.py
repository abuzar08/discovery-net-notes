r"""reviewer-1: my own recursive integer-aware sampling bound, built from scratch,
to test the incumbent value \(L(32,383) = 3022\) of h3285 and the scale-freeness
measurement.

\(L(n,q)\) is a lower bound on \(\mathrm{cr}(G)\) for every graph with \(n\)
vertices and \(q\) edges. Base data: the Euler bound \(q - 3n + 6\), and the
exact \(\mathrm{cr}(K_n)\) for \(n \le 12\) at \(q = \binom{n}{2}\). Step: each
crossing of \(G\) lies in \(\binom{n-4}{s-4}\) of the \(\binom{n}{s}\) induced
\(s\)-subsets, so
\(\mathrm{cr}(G) \ge \lceil \binom{n}{s}\hat L(s,\bar q)/\binom{n-4}{s-4}\rceil\)
with \(\bar q = q\binom{n-2}{s-2}/\binom{n}{s}\) and \(\hat L(s,\cdot)\) the lower
convex envelope of the row, which is what Jensen needs. Rounding up at every
level is the "integer-aware" part.
"""
from fractions import Fraction
from math import comb

CRK = {1:0,2:0,3:0,4:0,5:1,6:3,7:9,8:18,9:36,10:60,11:100,12:150}
NMAX = 32


def envelope(row):
    """lower convex envelope of q -> row[q], as a callable on Fractions"""
    pts = [(q, row[q]) for q in range(len(row))]
    hull = []
    for p in pts:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (y2 - y1) * (p[0] - x2) >= (p[1] - y2) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append(p)

    def f(qbar):
        for (x1, y1), (x2, y2) in zip(hull, hull[1:]):
            if x1 <= qbar <= x2:
                if x2 == x1:
                    return Fraction(y1)
                return y1 + Fraction((y2 - y1) * (qbar - x1), x2 - x1)
        return Fraction(hull[-1][1])
    return f, hull


def build(verbose_at=None, endpoint=True):
    L = {}
    envs = {}
    for n in range(3, NMAX + 1):
        M = comb(n, 2)
        row = [0] * (M + 1)
        for q in range(M + 1):
            v = max(0, q - 3 * n + 6)
            if endpoint and q == M and n in CRK:
                v = max(v, CRK[n])
            row[q] = v
        for q in range(M + 1):
            best = row[q]
            detail = []
            for s in range(5, n):
                f = envs[s][0]
                qbar = Fraction(q * comb(n - 2, s - 2), comb(n, s))
                val = Fraction(comb(n, s) * f(qbar), comb(n - 4, s - 4))
                cand = -((-val.numerator) // val.denominator)   # ceiling
                detail.append((s, cand))
                if cand > best:
                    best = cand
            row[q] = best
            if verbose_at == (n, q):
                envs['detail'] = detail
        L[n] = row
        envs[n] = envelope(row)
    return L, envs


def main():
    L, envs = build(verbose_at=(32, 383))
    L0, _ = build(endpoint=False)
    print(f'   without the complete-graph endpoint base: L(32,383) = '
          f'{L0[32][383]}, L(32,496) = {L0[32][496]}')
    print(f'my own recursive integer-aware sampling bound')
    for (n, q) in ((32, 383), (32, 496), (32, 420), (32, 350)):
        print(f'   L({n},{q}) = {L[n][q]}')
    print(f'   published incumbent L(32,383) = 3022, the value "in circulation" '
          f'2988; mine {L[32][383]}')
    det = envs.get('detail', [])
    if det:
        best = max(c for _, c in det)
        print(f'   at (32,383) the per-s values run {min(c for _, c in det)} to '
              f'{best}; the best sample sizes are '
              f'{[s for s, c in det if c == best]}')
        # scale-freeness: factor by which each level must lift for a target
        tgt = 3557
        facs = [Fraction(tgt, c) for _, c in det if c > 0]
        print(f'   required lift factors over all s: min {float(min(facs)):.4f}, '
              f'max {float(max(facs)):.4f}, spread '
              f'{float(max(facs) - min(facs)):.4f}')
    print(f'   my ceiling from an explicit drawing: 4644; '
          f'{L[32][383]}/4644 = {L[32][383]/4644:.3f}')


if __name__ == '__main__':
    main()
