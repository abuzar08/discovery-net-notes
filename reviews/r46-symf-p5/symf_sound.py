"""reviewer-1: own exhaustive soundness test of the fixed-vertex lex-leader (L)
as used by h2919 — the counterpart of the target's symftest.py, written here.

For small (n, f, p, k) it enumerates ALL sigma-invariant graphs (one bit per
orbit of pairs, my own union-find numbering) and checks

  (A) descent: whenever (L) fails at rows u, u+1, swapping the two fixed vertices
      strictly decreases the key (profile columns, then G[F] row by row) — so the
      lexicographically least relabelling satisfies (L);
  (B) no solution lost: every S_f-orbit of graphs contains at least one member
      satisfying (L) — reported both over all graphs and over the (s,t)-good ones,
      and the (s,t)-goodness of a graph is checked to be invariant under S_f.

usage: python3 symf_sound.py n s t f p k
"""
import sys, itertools
from indep_symf import orbit_numbering


def main():
    n, s, t, f, p, k = map(int, sys.argv[1:7])
    var, nv = orbit_numbering(n, f, p, k)
    assert nv <= 22, f'{nv} orbit variables is too many to enumerate'
    x = lambda val, a, b: (val >> (var[(a, b) if a < b else (b, a)] - 1)) & 1

    cols = lambda u: [f + j * p for j in range(k)] + [w for w in range(f) if w not in (u, u + 1)]
    colsets = [cols(u) for u in range(f - 1)]

    def rows_ok(val):
        for u in range(f - 1):
            c = colsets[u]
            if [x(val, u, w) for w in c] > [x(val, u + 1, w) for w in c]:
                return False
        return True

    def relabel(val, pi):
        """apply the permutation pi of the fixed vertices"""
        out = 0
        seen = {}
        for (a, b), v in var.items():
            aa = pi[a] if a < f else a
            bb = pi[b] if b < f else b
            w = var[(aa, bb) if aa < bb else (bb, aa)]
            bit = (val >> (v - 1)) & 1
            assert seen.get(w, bit) == bit
            seen[w] = bit
            if bit:
                out |= 1 << (w - 1)
        return out

    def key(val):
        return (tuple(tuple(x(val, u, f + j * p) for j in range(k)) for u in range(f)),
                tuple(tuple(x(val, u, w) if u != w else 0 for w in range(f)) for u in range(f)))

    def good(val):
        for S in itertools.combinations(range(n), s):
            if all(x(val, a, b) for a, b in itertools.combinations(S, 2)):
                return False
        for T in itertools.combinations(range(n), t):
            if not any(x(val, a, b) for a, b in itertools.combinations(T, 2)):
                return False
        return True

    perms = list(itertools.permutations(range(f)))
    total = 1 << nv
    viol = 0
    seen = set()
    orbits = orbits_ok = 0
    goodorbits = goodorbits_ok = 0
    for val in range(total):
        # (A) descent
        for u in range(f - 1):
            c = colsets[u]
            if [x(val, u, w) for w in c] > [x(val, u + 1, w) for w in c]:
                viol += 1
                pi = list(range(f)); pi[u], pi[u + 1] = u + 1, u
                assert key(relabel(val, pi)) < key(val), f'descent fails at {val}, u={u}'
        # (B) orbits
        if val in seen:
            continue
        orb = {relabel(val, list(pi)) for pi in perms}
        seen |= orb
        orbits += 1
        ok = any(rows_ok(v) for v in orb)
        orbits_ok += ok
        assert ok, f'orbit of {val} has no (L)-member'
        gs = {good(v) for v in orb}
        assert len(gs) == 1, f'({s},{t})-goodness is not S_{f}-invariant on the orbit of {val}'
        if gs.pop():
            goodorbits += 1
            goodorbits_ok += ok
    print(f'n={n} ({s},{t}) 1^{f} {p}^{k}: {nv} orbit vars, {total} sigma-invariant graphs; '
          f'(A) {viol} (graph,u) violations, every one repaired by a strictly descending swap; '
          f'(B) {orbits} S_{f}-orbits, all with an (L)-member ({orbits_ok}); '
          f'{goodorbits} of them ({s},{t})-good, all with an (L)-member ({goodorbits_ok})')


if __name__ == '__main__':
    main()
