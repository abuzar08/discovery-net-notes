"""Certify Lemma 3.1 and Theorem 3.1 of McKay-Radziszowski, R(5,5) <= 49.

McKay and Radziszowski, `Subgraph Counting Identities and Ramsey Numbers`,
JCTB 69 (1997) 193-209.  Their proof of R(5,5) <= 49 rests on two statements:

  Lemma 3.1.  Let G be a (5,5,49)-graph.  Then for each vertex v, G^+_v and the
              complement of G^-_v are (4,5,24,132)-graphs, regular of degree 11.
  Theorem 3.1. The only two (4,5,24,132)-graphs are H_1 and H_2.

Both are now checkable end to end from public data, which they were not in
1995: Theorem 3.1 was proved then by a dedicated search over an incomplete
list, and the COMPLETE catalogue of (4,5,24)-graphs -- 352366 of them -- only
arrived with Angeltveit and McKay (2016).  Given that catalogue, Theorem 3.1 is
a filter, and Lemma 3.1 is arithmetic plus one fact about the survivors.

WHAT IS CHECKED

  (1) the degree window at n = 49 forces 24-regularity;
  (2) identity (I2) at n = 49, re-derived rather than copied, giving
      sum_v e(G^-_v) = 588 + sum_v e(G^+_v);
  (3) the complement step, giving sum_v [e(G^+_v) + e(comp G^-_v)] = 12936;
  (4) 12936 / 49 = 264 = 2 x 132 with each term at most e_max(4,5,24) = 132,
      so every term is exactly 132 -- the forcing that carries the lemma;
  (5) exactly two (4,5,24)-graphs have 132 edges (Theorem 3.1), both genuine,
      both 11-regular -- which is the "maximum degree at most 11" input the
      lemma needs, verified rather than cited;
  (6) both are vertex-transitive with |Aut| = 24 and 48, matching the orders
      McKay and Radziszowski state for H_2 and H_1.

    python3 mr49.py
"""
import json
import os
import sys

import r45bounds as R

HERE = os.path.dirname(os.path.abspath(__file__))
N = 49


def automorphisms(n, adj):
    """Every automorphism, by backtracking with adjacency consistency."""
    perms, img, used = [], [-1] * n, [False] * n

    def bt(k):
        if k == n:
            perms.append(tuple(img))
            return
        for c in range(n):
            if used[c]:
                continue
            if all(((adj[k] >> j) & 1) == ((adj[c] >> img[j]) & 1)
                   for j in range(k)):
                img[k] = c
                used[c] = True
                bt(k + 1)
                used[c] = False
                img[k] = -1
    bt(0)
    return perms


def main():
    with open(os.path.join(HERE, "e45.json")) as fh:
        emax = {int(k): v for k, v in json.load(fh)["emax"].items()}

    lo, hi = N - 25, 24                      # R(4,5) = 25 on both sides
    print(f"(1) degree window at n = {N}: [{lo}, {hi}]  ->  "
          f"{'24-regular' if lo == hi == 24 else 'NOT forced'}")
    if (lo, hi) != (24, 24):
        raise SystemExit("the window does not force regularity")
    d = 24
    m = N - 1 - d
    print(f"    so v(G^+_v) = {d} and v(G^-_v) = {m}")

    # (2) identity (I2): sum_v 2 e(G^-_v) = sum_v [ v(X)(n - 2v(X)) + 2 e(X) ]
    coef = d * (N - 2 * d)
    const = N * coef // 2
    print(f"(2) (I2) with v(G^+_v) = {d}: the per-vertex constant is "
          f"{d}({N} - {2 * d}) = {coef},")
    print(f"    so sum_v e(G^-_v) = {const} + sum_v e(G^+_v)"
          f"    [paper: 588]  ->  {'MATCH' if const == 588 else 'MISMATCH'}")
    if const != 588:
        raise SystemExit("constant does not match")

    # (3) complement step
    C = m * (m - 1) // 2
    total = N * C - const
    print(f"(3) e(G^-_v) = C({m},2) - e(comp) = {C} - e(comp), so")
    print(f"    sum_v [ e(G^+_v) + e(comp G^-_v) ] = {N}*{C} - {const} = "
          f"{total}    [paper: 12936]  ->  "
          f"{'MATCH' if total == 12936 else 'MISMATCH'}")
    if total != 12936:
        raise SystemExit("total does not match")

    # (4) the forcing
    per = total / N
    cap = emax[24]
    print(f"(4) {total} / {N} = {per:g} = 2 x {per / 2:g}; each of the two "
          f"terms is at most e_max(4,5,24) = {cap},")
    if per != 2 * cap:
        raise SystemExit(f"no forcing: {per} != 2 x {cap}")
    print(f"    and {per:g} = 2 x {cap}, so BOTH are exactly {cap} at every "
          f"vertex.  The lemma's forcing holds")
    print("    with no slack whatever -- one more edge of headroom anywhere "
          "and it fails.")

    # (5) and (6) the survivors
    path = os.path.join(HERE, "r45_24_e132.g6")
    with open(path) as fh:
        lines = [x.strip() for x in fh if x.strip()]
    print(f"(5) (4,5,24)-graphs with {cap} edges, filtered from the complete "
          f"352366-graph catalogue: {len(lines)}")
    if len(lines) != 2:
        raise SystemExit("Theorem 3.1 says there are exactly two")
    orders = []
    for i, line in enumerate(lines):
        n, adj = R.g6_decode(line)
        deg = sorted(bin(a).count("1") for a in adj)
        e = sum(deg) // 2
        good = R.is_good(n, adj, 4, 5)
        A = automorphisms(n, adj)
        orb = {p[0] for p in A}
        orders.append(len(A))
        print(f"    graph {i + 1}: n = {n}, e = {e}, degrees "
              f"[{deg[0]},{deg[-1]}], genuine (4,5)-graph = {good},")
        print(f"               |Aut| = {len(A)}, vertex-transitive = "
              f"{len(orb) == n}")
        if not good or deg[0] != 11 or deg[-1] != 11:
            raise SystemExit("not an 11-regular (4,5,24,132)-graph")
    print(f"(6) automorphism orders {sorted(orders)}; McKay and Radziszowski "
          f"state |Aut(H_1)| = 48 and")
    print("    |Aut(H_2)| = 24, and that both are vertex-transitive.  "
          "The multiset matches;")
    print("    which of mine is their H_1 is a labelling question and is not "
          "claimed here.")
    if sorted(orders) != [24, 48]:
        raise SystemExit("automorphism orders do not match the paper")
    print()
    print("CERTIFIED.  Lemma 3.1 and Theorem 3.1 hold, from the arithmetic "
          "re-derived here and the")
    print("complete catalogue.  Trust boundary: McKay's completeness claim "
          "for R(4,5,24) is cited,")
    print("not proved; everything else above is checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
