"""LP(5,5,42) at level m=2: what the counting can and cannot do.

The method is McKay and Radziszowski's, `Subgraph Counting Identities and
Ramsey Numbers`, JCTB 69 (1997) 193-209, which defines LP(s,t,n) with exactly
these inputs -- the degree window, the e-extremes for (s-1,t,i)- and
(s,t-1,i)-graphs, and (at level 3) triangle bounds.  Their identity (I2) is the
edge equation; their LP(4,6,41) is infeasible, which is R(4,6) <= 41.

At n = 42 no LP of valid inequalities can be infeasible, because (5,5,42)-graphs
exist and satisfy all of them.  The only thing it could do is exclude ONE
degree.  This file settles level 2: it excludes none.

    python3 lp55.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
N = 42


def main():
    with open(os.path.join(HERE, "e45.json")) as fh:
        d = json.load(fh)
    emin = {int(k): v for k, v in d["emin"].items()}
    emax = {int(k): v for k, v in d["emax"].items()}

    lo_d, hi_d = N - 25, 24                      # R(4,5) = 25 both ways
    print(f"degree window at n = {N}: [{lo_d}, {hi_d}]")
    print("\nper-vertex contribution c(d) = e(G^-_v) - e(G^+_v) + d^2 - 21d, "
          "with sum_v c = 0 (identity I2)\n")
    print("   d   m=41-d   c_min   c_max   0 in range?")
    rng = {}
    for dd in range(lo_d, hi_d + 1):
        m = N - 1 - dd
        C = m * (m - 1) // 2
        cmin = C - emax[m] - emax[dd] + dd * dd - 21 * dd
        cmax = C - emin[m] - emin[dd] + dd * dd - 21 * dd
        rng[dd] = (cmin, cmax)
        print(f"  {dd:2d}   {m:6d}   {cmin:5d}   {cmax:5d}   "
              f"{'yes' if cmin <= 0 <= cmax else 'NO'}")

    excluded = [dd for dd, (a, b) in rng.items() if not (a <= 0 <= b)]
    print(f"\ndegrees whose interval excludes 0: {excluded or 'none'}")

    print("\nforcing n_d >= 1 and testing feasibility of the identity:")
    gmin = min(a for a, _ in rng.values())
    gmax = max(b for _, b in rng.values())
    any_infeasible = False
    for dd in range(lo_d, hi_d + 1):
        lo = rng[dd][0] + (N - 1) * gmin
        hi = rng[dd][1] + (N - 1) * gmax
        ok = lo <= 0 <= hi
        any_infeasible |= not ok
        print(f"   d = {dd:2d}: achievable sum in [{lo:6d}, {hi:6d}]  ->  "
              f"{'FEASIBLE' if ok else 'INFEASIBLE'}")
    if any_infeasible:
        print("\nA degree is excluded -- that would be a new bound.")
        return 0
    print("\nLevel 2 excludes no degree.  It is one linear equation in "
          "intervals that all contain")
    print("zero, and the intervals are symmetric under d <-> 41-d.  See "
          "DEGREE-WINDOW.md for the")
    print("aggregate version, which is worse: it reduces to the tautology "
          "sum_v S(v) = sum_u d(u)^2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
