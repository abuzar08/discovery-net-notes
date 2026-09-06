"""The neighbourhood-edge reduction for (5,5,n)-graphs, in exact arithmetic.

Everything here is a few lines of counting; the point is that the constants
come from `e45.json`, which was recomputed from primary catalogues rather than
quoted, and that the arithmetic is done in exact rationals so the inequalities
are decided rather than estimated.

    python3 reduce.py            # the reduction at n = 43, 44, 45
    python3 reduce.py --selftest # soundness check on (3,4), where the answer is known
"""
import json
import os
import sys
from fractions import Fraction as F
from math import comb, floor

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    d = json.load(open(os.path.join(HERE, "e45.json")))
    return ({int(k): v for k, v in d["emin"].items()},
            {int(k): v for k, v in d["emax"].items()})


def degree_window(n, R45=25):
    """n - R45 <= d(v) <= R45 - 1 for a (5,5,n)-graph."""
    return n - R45, R45 - 1


def reduction(n, emin, emax):
    """The inequalities on beta whose truth excludes a (5,5,n)-graph.

    For a vertex v of degree d, write m = n-1-d, N = N(v), M = V \\ N[v].
    G[N] is a (4,5,d)-graph and G[M] is a (5,4,m)-graph, so the complement of
    G[M] is a (4,5,m)-graph.  With

        S(v) = sum over u in N(v) of d(u),
        e_M(v) = e + e_N(v) - S(v)        (identity, proved in the README)

    and e_N(v) <= beta(d), e_M(v) >= C(m,2) - beta(m), we get

        S(v) <= e + beta(d) + beta(m) - C(m,2).

    Summing over v and using sum_v S(v) = sum_u d(u)^2 and e = (1/2) sum d(u):

        sum_d [ d^2 - beta(d) - beta(m) + C(m,2) - (n/2) d ] n_d  <=  0.

    Every n_d >= 0 and sum_d n_d = n > 0, so if every bracket is strictly
    positive the graph cannot exist.  The bracket is positive exactly when

        beta(d) + beta(m)  <  d^2 - (n/2) d + C(m,2).
    """
    lo, hi = degree_window(n)
    out = []
    seen = set()
    for d in range(lo, hi + 1):
        m = n - 1 - d
        if d not in emax or m not in emax:
            raise SystemExit(f"n={n}, d={d}: need emax at {d} and {m}")
        key = tuple(sorted((d, m)))
        if key in seen:
            continue
        seen.add(key)
        rhs = F(d * d) - F(n, 2) * d + comb(m, 2)
        strict = floor(rhs) if rhs.denominator != 1 else int(rhs) - 1
        out.append((d, m, int(strict), emax[d] + emax[m]))
    return out


def unconditional_slack(n, emax):
    """How far the unconditional bound (beta = emax) is from a contradiction."""
    lo, hi = degree_window(n)
    worst = None
    for d in range(lo, hi + 1):
        m = n - 1 - d
        gap = F(emax[d] + emax[m] - comb(m, 2)) - (F(d * d) - F(n, 2) * d)
        worst = gap if worst is None else max(worst, gap)
    per_vertex_min = min(
        -(F(d * d) - (emax[d] + emax[n - 1 - d] - comb(n - 1 - d, 2)) - F(n, 2) * d)
        for d in range(lo, hi + 1))
    return worst, per_vertex_min * n


def selftest():
    """Run the identical argument on (3,4), where (3,4,n)-graphs exist iff n <= 8.

    A contradiction reported at any n <= 8 would mean the derivation is wrong.
    """
    import itertools

    def good(m, adj, a, b):
        for S in itertools.combinations(range(m), a):
            if all((adj[x] >> y) & 1 for x, y in itertools.combinations(S, 2)):
                return False
        for S in itertools.combinations(range(m), b):
            if all(not (adj[x] >> y) & 1 for x, y in itertools.combinations(S, 2)):
                return False
        return True

    def bounds(a, b, mmax=6):
        out = {}
        for m in range(mmax + 1):
            pairs = list(itertools.combinations(range(m), 2))
            lo = hi = None
            for mask in range(1 << len(pairs)):
                adj = [0] * m
                for i, (x, y) in enumerate(pairs):
                    if (mask >> i) & 1:
                        adj[x] |= 1 << y
                        adj[y] |= 1 << x
                if good(m, adj, a, b):
                    e = bin(mask).count("1")
                    lo = e if lo is None else min(lo, e)
                    hi = e if hi is None else max(hi, e)
            if lo is not None:
                out[m] = (lo, hi)
        return out

    NB, MB = bounds(2, 4), bounds(3, 3)     # (3,4): N(v) is (2,4), M(v) is (3,3)
    dmax, mmax = max(NB), max(MB)
    bad = []
    for n in range(4, 11):
        ds = [d for d in range(max(0, n - 1 - mmax), dmax + 1)
              if d in NB and (n - 1 - d) in MB]
        if not ds:
            verdict = "excluded (no admissible degree)"
        else:
            cs = {d: F(d * d) - (NB[d][1] + MB[n - 1 - d][1]) - F(n, 2) * d
                  for d in ds}
            verdict = ("CONTRADICTION" if all(c > 0 for c in cs.values())
                       else "no contradiction")
        print(f"  (3,4,{n}): {verdict}")
        if n <= 8 and verdict == "CONTRADICTION":
            bad.append(n)
    print("  (3,4,n)-graphs exist exactly for n <= 8 since R(3,4) = 9.")
    print("  SOUNDNESS:", "FAILED - false exclusion at " + str(bad) if bad
          else "OK - no false exclusion at any n <= 8")
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    emin, emax = load()
    for n in (43, 44, 45):
        lo, hi = degree_window(n)
        worst, total = unconditional_slack(n, emax)
        print(f"=== n = {n}:  {lo} <= d(v) <= {hi} ===")
        print(f"  unconditional (beta = emax): NO contradiction; "
              f"total slack >= {total}, worst per-vertex gap {worst}")
        print(f"  a (5,5,{n})-graph is excluded if all of:")
        for d, m, strict, cur in reduction(n, emin, emax):
            if d == m:
                print(f"    beta({d}) <= {strict // 2}"
                      f"          (unconditionally {cur // 2}; "
                      f"must drop by {cur // 2 - strict // 2})")
            else:
                print(f"    beta({d}) + beta({m}) <= {strict}"
                      f"   (unconditionally {cur}; must drop by {cur - strict})")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
