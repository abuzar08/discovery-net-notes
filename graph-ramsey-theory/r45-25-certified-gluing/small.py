"""A machine-checked derivation of the small Ramsey numbers this work cites.

Both of my Ramsey directories cite R(3,4) = 9, R(3,5) = 14, R(4,4) = 18 and
R(4,5) = 25 for their degree windows.  The first three are small enough to
certify outright, which shortens the "cited, not proved" list to R(4,5) alone.

The chain, with nothing quoted:

  R(2,k) = k                        proved directly
  R(3,3) = 6                        upper by EXHAUSTIVE search over all 2^15
                                    graphs on 6 vertices; lower by C_5
  R(3,4) = 9                        upper by the Erdos-Szekeres bound with the
                                    parity refinement; lower by a witness.
                                    Cross-checked a second way, by extension
                                    from every (3,4,8)-graph
  R(3,5) = 14                       upper by Erdos-Szekeres; lower by witness
  R(4,4) = 18                       upper by Erdos-Szekeres; lower by witness

Lemma (Erdos-Szekeres, with parity).  If G is an (s,t,n)-graph then for every
vertex v, G[N(v)] is an (s-1,t)-graph and G[V \\ N[v]] is an (s,t-1)-graph, so

    d(v) <= R(s-1,t) - 1     and     n - 1 - d(v) <= R(s,t-1) - 1,

hence n <= R(s-1,t) + R(s,t-1) - 1, i.e. R(s,t) <= R(s-1,t) + R(s,t-1).
If moreover both R(s-1,t) and R(s,t-1) are even, then at n = R(s-1,t) +
R(s,t-1) - 1 both inequalities are tight for every v, so G is regular of
degree R(s-1,t) - 1, which is odd, on an odd number n of vertices -- and the
degree sum is odd, a contradiction.  So the bound improves by one.
"""
import itertools as it
import sys

import r45bounds as R


def exhaustive_none(n, s, t):
    """True iff there is NO (s,t,n)-graph, by trying every labelled graph."""
    pairs = list(it.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        adj = [0] * n
        for i, (a, b) in enumerate(pairs):
            if (mask >> i) & 1:
                adj[a] |= 1 << b
                adj[b] |= 1 << a
        if R.is_good(n, adj, s, t):
            return False, adj
    return True, None


def es_bound(Rst_1, Rs_1t):
    """R(s,t) <= R(s-1,t) + R(s,t-1), minus one when both are even."""
    b = Rs_1t + Rst_1
    return b - 1 if (Rs_1t % 2 == 0 and Rst_1 % 2 == 0) else b


def extends(n, adj, s, t):
    """Is there a way to add one vertex to an (s,t,n)-graph keeping it good?"""
    for sub in range(1 << n):
        a2 = list(adj) + [sub]
        for u in range(n):
            if (sub >> u) & 1:
                a2[u] |= 1 << n
        if R.is_good(n + 1, a2, s, t):
            return True, a2
    return False, None


def canon(n, adj):
    """Canonical form by brute force over all n! relabellings.  Small n only."""
    best = None
    for p in it.permutations(range(n)):
        code = 0
        bit = 0
        for a in range(n):
            for b in range(a + 1, n):
                if (adj[p[a]] >> p[b]) & 1:
                    code |= 1 << bit
                bit += 1
        best = code if best is None else min(best, code)
    return best


def generate(s, t, upto):
    """All (s,t,n)-graphs up to isomorphism, by iterated one-vertex extension."""
    levels = {0: [[]]}
    for n in range(1, upto + 1):
        seen = {}
        for adj in levels[n - 1]:
            for sub in range(1 << (n - 1)):
                a2 = list(adj) + [sub]
                for u in range(n - 1):
                    if (sub >> u) & 1:
                        a2[u] |= 1 << (n - 1)
                if R.is_good(n, a2, s, t):
                    c = canon(n, a2)
                    if c not in seen:
                        seen[c] = a2
        levels[n] = list(seen.values())
    return levels


def main():
    print("R(2,k) = k: an independent k-set or a single edge; no search needed.")

    none6, _ = exhaustive_none(6, 3, 3)
    ok5, w5 = exhaustive_none(5, 3, 3)
    print(f"R(3,3): no (3,3,6)-graph among all 2^15 labelled graphs: {none6}; "
          f"a (3,3,5)-graph exists: {not ok5}")
    R33 = 6
    assert none6 and not ok5

    b34 = es_bound(R33, 4)          # R(3,4) <= R(2,4) + R(3,3), both even
    print(f"R(3,4) <= R(2,4) + R(3,3) = 4 + 6 = 10, both even so <= {b34}")
    lv = generate(3, 4, 8)
    counts = {n: len(v) for n, v in lv.items() if n >= 5}
    print(f"   (3,4,n)-graphs up to isomorphism, generated here: {counts}")
    ext = [adj for adj in lv[8] if extends(8, adj, 3, 4)[0]]
    print(f"   independent cross-check: of the {len(lv[8])} (3,4,8)-graphs, "
          f"{len(ext)} extend to 9 vertices -> R(3,4) <= 9 confirmed a second way")
    R34 = 9
    assert b34 == 9 and not ext and lv[8]

    b35 = es_bound(R34, 5)          # R(3,5) <= R(2,5) + R(3,4) = 5 + 9
    print(f"R(3,5) <= R(2,5) + R(3,4) = 5 + 9 = {b35}")
    R35 = 14

    b44 = es_bound(R34, R34)        # R(4,4) <= R(3,4) + R(4,3) = 9 + 9
    print(f"R(4,4) <= R(3,4) + R(4,3) = 9 + 9 = {b44}")
    R44 = 18

    # lower bounds from explicit witnesses, re-verified here
    for name, path, n, s, t in (("R(3,5) > 13", "r35_13.g6", 13, 3, 5),
                                ("R(4,4) > 17", "r44_17.g6", 17, 4, 4)):
        o, adj = R.g6_decode(open(path).readline())
        good = (o == n and R.is_good(n, adj, s, t))
        print(f"{name}: witness on {n} vertices verified as a genuine "
              f"({s},{t})-graph: {good}")
        assert good
    print()
    print(f"CERTIFIED: R(3,3) = {R33}, R(3,4) = {R34}, R(3,5) = {R35}, "
          f"R(4,4) = {R44}")
    print("Still cited, not proved: R(4,5) = 25 (McKay-Radziszowski 1995).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
