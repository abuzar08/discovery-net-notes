#!/usr/bin/env python3
"""
Barrier dichotomy for r-critical Albertson counterexamples of order 2r-1.

Exact integer verification of the finite case analysis described in README.md.
No floating point, no randomness, no solver.  Standard library only.

Setting.  G is r-critical, n = |G| = 2r-1, complement H := comp(G) connected,
cr(G) < cr(K_r).  Then (Stehlik 2003) H is factor-critical, and
  chi(G) = theta(H) = r   (theta = clique cover number),
  Delta(H) <= n-1-delta(G) <= n-1-(r-1) = r-1,
  X := sum_v ((r-1) - d_H(v)) = n(r-1) - 2 e(H) = 2m - n(r-1),  where m = e(G).

If H has a triangle T then H - V(T) has no perfect matching (else theta(H)<=r-1),
so Tutte-Berge + factor-criticality give a BARRIER B (V(T) subset of B) with
  o(H-B) = |B| - 1 =: q,  and every component C of H-B satisfies, for v in C,
  d_H(v) <= |C|-1+|B|,  hence  x_v := (r-1)-d_H(v) >= r-|C|-|B|.

This script enumerates, for each barrier size b, every multiset of component sizes
of H-B with (i) at least b-1 odd components, (ii) sizes summing to n-b, and applies
four exact exclusions (see README.md):
  1. degree deficiency          sum_C |C|*max(0,r-|C|-b) <= X
  2. crossing number            Kleitman bound for the forced K_{a,|D|-a} <= Z(r)
  3. D-B edge count             lower bound from delta(G) <= exact upper bound
  4. forced K_r subdivision     complete multipartite part contains K_r or K_r-e
It then reports, for each surviving barrier size, the forced max_v x_v and the
forced clique size omega(G) >= (number of components).
"""
# ---------------------------------------------------------------- crossing bounds
def Z(n):
    """Hill/Zarankiewicz number: the best known upper bound for cr(K_n)."""
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4

def cr_K6n(n):
    """Kleitman (1970): cr(K_{6,n}) = 6*floor(n/2)*floor((n-1)/2)."""
    return 6 * (n // 2) * ((n - 1) // 2)

def kleitman_bipartite(a, c):
    """Counting bound  cr(K_{a,c}) >= C(a,6)/C(a-2,4) * cr(K_{6,c}) = a(a-1)/30 * cr(K_{6,c}).

    Every crossing of a drawing of K_{a,c} uses two vertices of the a-side; each of the
    C(a,6) induced K_{6,c} subdrawings has >= cr(K_{6,c}) crossings and each crossing is
    counted C(a-2,4) times.  Returns an exact integer lower bound (floor).
    Valid for a >= 6; symmetric in (a,c), so we take the better of the two orientations.
    """
    best = 0
    for x, y in ((a, c), (c, a)):
        if x >= 6:
            best = max(best, (x * (x - 1) * cr_K6n(y)) // 30)
    return best

def best_bipartition(parts):
    """Max over 2-colourings of `parts` of the Kleitman bound for the induced K_{a,c}."""
    reach = {0}
    for p in parts:
        reach |= {s + p for s in reach}
    tot = sum(parts)
    return max(kleitman_bipartite(s, tot - s) for s in reach)

# ---------------------------------------------------------------- configurations
def configs(total, nodd, free, budget):
    """Yield sorted-descending component-size multisets: sizes >= 1 summing to `total`,
    at least `nodd` of them odd, forced deficiency sum(s*max(0,free-s)) <= budget.
    Any number of components is allowed (>= nodd)."""
    def cost(s):
        return s * max(0, free - s)

    out = []
    def rec(rem, maxsz, cur, c):
        if rem == 0:
            if sum(1 for s in cur if s % 2) >= nodd:
                out.append(tuple(cur))
            return
        for s in range(min(maxsz, rem), 0, -1):
            nc = c + cost(s)
            if nc > budget:
                continue
            # optimistic completion: remaining rem-s vertices cost >= 0
            rec(rem - s, s, cur + [s], nc)
    rec(total, total, [], 0)
    return out

def analyse(r, m, verbose=True):
    """Return (X, Z(r), branches) where each surviving branch is
    (barrier size b, forced max_v x_v, forced omega(G), upper bound on e_G(D,B))."""
    n = 2 * r - 1
    X = 2 * m - n * (r - 1)           # total degree deficiency budget in H
    eH = n * (n - 1) // 2 - m
    target = Z(r)                     # cr(K_r) <= Z(r); we must beat this to contradict
    if verbose:
        print("r=%d  n=%d  m=%d  e(H)=%d  deficiency budget X=%d  Z(r)=%d"
              % (r, n, m, eH, X, target))
        print("   b  q=b-1  #cfg  #survive   min forced max_v x_v   min omega   note")
    branches = []
    for b in range(3, n + 1):
        q = b - 1
        if n - b < q:                 # not enough vertices for q components
            continue
        free = r - b                  # sizes >= free have zero forced deficiency
        cfgs = configs(n - b, q, free, X)
        if not cfgs:
            if verbose:
                print("  %2d  %5d  %4d  %8d   %20s   %9s   excluded: degree deficiency"
                      % (b, q, 0, 0, "-", "-"))
            continue
        # (i) crossing-number exclusion; (ii) edge-count exclusion between D and B.
        def eGDB_upper(c):
            # e_G(D,B) = |D|(b-r+1) + sum_{v in D} x_v + 2 sum_C e(H[C])
            return sum(c) * (b - r + 1) + X + 2 * sum(s * (s - 1) // 2 for s in c)

        def eGDB_lower(c):
            # delta(G) >= r-1.  u in B: d_G(u) <= (b-1) + e_G(u,D)  => e_G(u,D) >= r-b.
            # v in C:  d_G(v) = (|D|-|C|) + deg_{G[C]}(v) + e_G(v,B) <= |D|-1 + e_G(v,B)
            #          => e_G(v,B) >= r-|D|.
            D = sum(c)
            fromB = b * max(0, r - b)
            fromD = D * max(0, r - D)
            return max(fromB, fromD)

        def has_TKr(c):
            """G[D] is the complete multipartite graph with parts the components of H-B.
            (a) |c| >= r  =>  K_r subset of G[D].
            (b) |c| = r-1 with exactly one part of size 2 and the rest singletons
                =>  G[D] = K_r - e.  Both endpoints x,y of the missing edge have
                d_G >= r-1 and only r-2 neighbours inside D, so each has a neighbour
                in B; if G[B] is connected we get an x-y path through B, i.e. TK_r.
                G[B] is connected because  e(G[B]) >= (b(r-1) - eGDB_upper)/2  exceeds
                the maximum C(b-1,2) of a disconnected graph on b vertices."""
            if len(c) >= r:
                return "K_%d subgraph" % r
            if len(c) == r - 1 and sorted(c) == [1] * (r - 2) + [2]:
                eGB = -(-(b * (r - 1) - eGDB_upper(c)) // 2)     # ceil
                if eGB > (b - 1) * (b - 2) // 2:
                    return "TK_%d (K_%d-e plus connected G[B]: e(G[B])>=%d > %d)" % (
                        r, r, eGB, (b - 1) * (b - 2) // 2)
            return None

        live = [c for c in cfgs
                if best_bipartition(list(c)) <= target
                and eGDB_lower(c) <= eGDB_upper(c)
                and has_TKr(c) is None]
        if not live:
            if verbose:
                print("  %2d  %5d  %4d  %8d   %20s   %9s   excluded (all %d configs)"
                      % (b, q, len(cfgs), 0, "-", "-", len(cfgs)))
            continue
        # forced max_v x_v for a configuration: the smallest component is the tightest
        fx = min(max(max(0, r - s - b) for s in c) for c in live)
        oq = min(len(c) for c in live)          # omega(G) >= number of components
        # G-edges between the component union D and the barrier B:
        #   e_G(D,B) = |D|(b-r+1) + sum_{v in D} x_v + 2 sum_C e(H[C])
        #            <= |D|(b-r+1) + X + 2 sum_C C(|C|,2)
        eb = max(eGDB_upper(c) for c in live)
        branches.append((b, fx, oq, eb))
        if verbose:
            print("  %2d  %5d  %4d  %8d   %20d   %9d   e_G(D,B)<=%d  cfgs=%s"
                  % (b, q, len(cfgs), len(live), fx, oq, eb,
                     [tuple(x) for x in live][:3]))
    return X, target, branches

def report(r, rows):
    print("=" * 78)
    print("Albertson barrier dichotomy at order n = 2r-1, r = %d" % r)
    print("=" * 78)
    aes = (2 * (2 * r - 1)) // 5      # Andrasfai-Erdos-Sos: delta > 2n/5 => bipartite
    tf = (2 * r - 2 - aes) - (r - 1)  # forced max_v x_v in the triangle-free branch
    out = []
    for m in rows:
        X, target, branches = analyse(r, m)
        # dichotomy: max_v x_v >= tf   OR   omega(G) >= B,
        # where B is forced by every barrier branch that does not already give x >= tf.
        weak = [br for br in branches if br[1] < tf]
        B = min([br[2] for br in weak]) if weak else None
        print("  -> surviving barrier sizes b: %s" % ([br[0] for br in branches],))
        print("  -> branches with forced max_v x_v < %d: b in %s, each forcing omega(G) >= %s"
              % (tf, [br[0] for br in weak], B))
        out.append((m, tf, B))
        print()
    print("Triangle-free branch detail (Andrasfai-Erdos-Sos, n = %d):" % (2 * r - 1))
    print("  delta(H) > 2n/5 = %d forces H bipartite; a factor-critical graph of odd" % aes)
    print("  order is never bipartite, so delta(H) <= %d, i.e. max_v d_G(v) >= %d,"
          % (aes, 2 * r - 2 - aes))
    print("  i.e. max_v x_v >= %d." % tf)
    print()
    for m, a, b in out:
        print("RESULT r=%d n=%d m=%d:  max_v (d_G(v)-(r-1)) >= %d   OR   omega(G) >= %d"
              % (r, 2 * r - 1, m, a, b))
    print()

if __name__ == "__main__":
    report(28, [768, 769])
    report(27, [713, 714, 715, 716])
