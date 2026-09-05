#!/usr/bin/env python3
"""
Matching-barrier dichotomy for Albertson counterexamples of order n = 2r-1,
over the whole edge range that published results leave open.

Self-contained superset of verify.py.  Exact integer / Fraction arithmetic only:
no floating point, no randomness, no solver, no external data, no imported
campaign code.

--------------------------------------------------------------------------
Setting.  G is r-critical, n = |G| = 2r-1, H := complement(G) is connected, and
cr(G) < cr(K_r).  Then
  chi(G) = theta(H)  (clique cover number of H), so theta(H) = r;
  delta(G) >= r-1, so Delta(H) <= n-1-(r-1) = r-1;
  x_v := (r-1) - d_H(v) = d_G(v) - (r-1) >= 0  and  X := sum_v x_v = 2m - n(r-1).
Stehlik (JCTB 89 (2003) 189-194): a k-critical graph with connected complement
has, for every vertex x, a (k-1)-colouring of G-x with all classes of size >= 2.
At n = 2k-1 all classes then have size exactly 2, so H-x has a perfect matching
for every x, i.e. H is factor-critical.

Barrier step.  If H has a triangle T then H-V(T) has no perfect matching (else
V(T) together with that matching covers V(H) by r-1 cliques and theta(H) <= r-1).
Tutte-Berge gives S with o(H-V(T)-S) >= |S|+2.  Put B := S u V(T), b := |B|.
Then
        o(H - B) >= b - 1.
(Factor-criticality additionally gives o(H-B) <= b+1 by Berge's formula, so in
fact o(H-B) is b-1 or b+1; only the lower bound "o(H-B) >= b-1" is used below,
and every enumeration here ranges over ALL component multisets with at least
b-1 odd components, so both cases are covered.)

Edge range.  Both endpoints are recomputed here from published results only:
  lower  Kostochka-Yancey (Sadhu Lemma 2.4): 2m >= ((r+1)(r-2)n - r(r-3))/(r-1);
  upper  Sadhu Lemma 2.1  cr(G) >= 5m - (203/9)(n-2)  pushed through the standard
         induced-sampling average over k-subsets:
             cr(G) >= [ 5m k(k-1)/(n(n-1)) - (203/9)(k-2) ] * (n)_4/(k)_4,
         since each crossing of an optimal drawing has 4 distinct vertices and
         survives a random k-subset with probability (k)_4/(n)_4.  The largest m
         for which no k makes this reach Z(r) >= cr(K_r) is the upper endpoint.
No fleet-internal recurrence, no r=27 chain, and no unpublished bound is used.
--------------------------------------------------------------------------
"""
from fractions import Fraction as F
from functools import lru_cache

# ------------------------------------------------------------------ constants
def Z(n):
    """Hill's number: cr(K_n) <= Z(n).  Only this UPPER bound on the target is
    used, so nothing here depends on the Harary-Hill conjecture."""
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4

def cr_K6n(n):
    """Kleitman (1970): cr(K_{6,n}) = 6*floor(n/2)*floor((n-1)/2)."""
    return 6 * (n // 2) * ((n - 1) // 2)

def falling(n, k):
    p = 1
    for i in range(k):
        p *= (n - i)
    return p

# ------------------------------------------------------------------ edge range
def ky_floor(r, n):
    """ceil of ((r+1)(r-2)n - r(r-3)) / (2(r-1))."""
    num = (r + 1) * (r - 2) * n - r * (r - 3)
    den = 2 * (r - 1)
    return -(-num // den)

@lru_cache(maxsize=None)
def sample_bound(m, n, k):
    inner = F(5 * m * k * (k - 1), n * (n - 1)) - F(203 * (k - 2), 9)
    return inner * F(falling(n, 4), falling(k, 4))

def edge_range(r):
    n = 2 * r - 1
    lo = ky_floor(r, n)
    target = Z(r)
    hi = n * (n - 1) // 2
    for m in range(lo, hi + 1):
        if any(sample_bound(m, n, k) >= target for k in range(4, n + 1)):
            hi = m - 1
            break
    return lo, hi

# ------------------------------------------------------------ crossing bounds
def kleitman_bipartite(a, c):
    """cr(K_{a,c}) >= C(a,6)/C(a-2,4) * cr(K_{6,c}) = a(a-1)/30 * cr(K_{6,c}).
    Each crossing uses two vertices of the a-side, so it lies in C(a-2,4) of the
    C(a,6) induced K_{6,c} sub-drawings.  Exact integer floor; symmetric."""
    best = 0
    for x, y in ((a, c), (c, a)):
        if x >= 6:
            best = max(best, (x * (x - 1) * cr_K6n(y)) // 30)
    return best

# Exact crossing numbers of small complete graphs.
#   through K_12: Guy; Pan-Richter 2007 gives cr(K_11)=100, whence cr(K_12)=150.
#   K_13 = 225 and K_14 = 315: McQuillan-Pan-Richter (JCTB 2015) bounded cr(K_13),
#   settled as 225 (and cr(K_14)=315) by the CCCG 2021 computation
#   "Another Small but Long Step for Crossing Numbers: cr(13)=225 and cr(14)=315".
BASE_CONSERVATIVE = {5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}
BASE_CCCG2021 = {**BASE_CONSERVATIVE, 13: 225, 14: 315}
_CRK = {q: 0 for q in range(0, 5)}
_CRK.update(BASE_CCCG2021)

def set_base(base):
    """Choose which published exact values seed the cr(K_q) recursion."""
    _CRK.clear()
    _CRK.update({q: 0 for q in range(0, 5)})
    _CRK.update(base)
    cr_lower_nm.cache_clear()

def crK(q):
    """Lower bound for cr(K_q): exact values above, then the standard counting
    recursion cr(K_q) >= ceil(q/(q-4) * cr(K_{q-1})) -- each of the q induced
    K_{q-1} sub-drawings has >= cr(K_{q-1}) crossings and each crossing, having
    4 distinct vertices, is counted q-4 times."""
    if q in _CRK:
        return _CRK[q]
    v = -(-q * crK(q - 1) // (q - 4))
    _CRK[q] = v
    return v

@lru_cache(maxsize=None)
def cr_lower_nm(n2, m2):
    """Lower bound for cr(F) valid for EVERY graph F with n2 vertices and m2 edges:
    Sadhu Lemma 2.1 (cr >= 5m - (203/9)(n-2)) averaged over random k-subsets."""
    if n2 < 4 or m2 <= 0:
        return 0
    best = 0
    for k in range(4, n2 + 1):
        b = sample_bound(m2, n2, k)
        if b > best:
            best = b
    return max(0, int(best))          # floor of an exact Fraction

def best_bipartition(parts):
    reach = {0}
    for p in parts:
        reach |= {s + p for s in reach}
    tot = sum(parts)
    return max(kleitman_bipartite(s, tot - s) for s in reach)

# ------------------------------------------------------------ configurations
def configs(total, nodd, free, budget):
    """All multisets of component sizes: parts >= 1 summing to `total`, at least
    `nodd` of them odd, and forced deficiency sum(s*max(0,free-s)) <= budget."""
    out = []
    def rec(rem, maxsz, cur, c):
        if rem == 0:
            if sum(1 for s in cur if s % 2) >= nodd:
                out.append(tuple(cur))
            return
        for s in range(min(maxsz, rem), 0, -1):
            nc = c + s * max(0, free - s)
            if nc > budget:
                continue
            rec(rem - s, s, cur + [s], nc)
    rec(total, total, [], 0)
    return out

# ------------------------------------------------------------------- analysis
def analyse(r, m):
    """Return the list of surviving branches (b, forced max_v x_v, forced omega)."""
    n = 2 * r - 1
    X = 2 * m - n * (r - 1)
    eH = n * (n - 1) // 2 - m
    target = Z(r)
    branches = []
    for b in range(3, n + 1):
        q = b - 1
        if n - b < q:
            continue
        free = r - b
        cfgs = configs(n - b, q, free, X)
        if not cfgs:
            continue

        def eGDB_upper(c):
            # exact identity  e_G(D,B) = |D|(b-r+1) + sum_{v in D} x_v + 2 sum_C e(H[C])
            return sum(c) * (b - r + 1) + X + 2 * sum(s * (s - 1) // 2 for s in c)

        def eGDB_lower(c):
            # delta(G) >= r-1.  u in B: d_G(u) <= (b-1) + e_G(u,D)  => e_G(u,D) >= r-b.
            # v in C:  d_G(v) <= (|D|-1) + e_G(v,B)                 => e_G(v,B) >= r-|D|.
            D = sum(c)
            return max(b * max(0, r - b), D * max(0, r - D))

        def has_TKr(c):
            # G[D] is complete multipartite with the components as parts.
            if len(c) >= r:
                return True                       # K_r  subset of  G[D]
            if len(c) == r - 1 and sorted(c) == [1] * (r - 2) + [2]:
                # G[D] = K_r - e; route the missing edge xy through B.
                eGB = -(-(b * (r - 1) - eGDB_upper(c)) // 2)
                return eGB > (b - 1) * (b - 2) // 2   # forces G[B] connected
            return False

        def split_bound(c):
            """cr(G) >= cr(G[D]) + cr(G[B]).  D and B are disjoint, so G[D] u G[B]
            is a subgraph of G and the crossing number of a disjoint union is the
            sum of the crossing numbers.

            Write Y = sum_{v in D} x_v, P = sum_C e(H[C]) = e(H[D]), Q = e(H[B]).
            Counting d_H over D gives  e_H(D,B) + 2P = |D|(r-1) - Y, and
            e(H) = Q + e_H(D,B) + P, so the exact identity

                P = |D|(r-1) - Y - e(H) + Q.

            Hence e(G[D]) = C(|D|,2) - P and e(G[B]) = C(b,2) - Q.  Both crD and crB
            are non-increasing in Q, so for each admissible Y the worst case is Q
            maximal; Y itself is scanned over its whole admissible range.
            Feasibility: Y >= the forced deficiency inside D and Y <= X;
            sum_C (|C|-1) <= P (components are connected) and P <= sum_C C(|C|,2);
            3 <= Q <= C(b,2), since the triangle T that produced B lies inside B.
            If no (Y,Q) is admissible the configuration itself is impossible, which
            we signal with an infinite bound."""
            D = sum(c)
            CD, CB = D * (D - 1) // 2, b * (b - 1) // 2
            Ymin = sum(s * max(0, r - s - b) for s in c)
            Pmin, Pmax = sum(s - 1 for s in c), sum(s * (s - 1) // 2 for s in c)
            best = None
            for Y in range(Ymin, X + 1):
                Q = min(CB, Pmax - D * (r - 1) + Y + eH)
                if Q < 3:
                    continue
                P = D * (r - 1) - Y - eH + Q
                if not (Pmin <= P <= Pmax):
                    continue
                crD = max(crK(len(c)), cr_lower_nm(D, CD - P),
                          best_bipartition(list(c)))
                eB = CB - Q
                tot = crD + (cr_lower_nm(b, eB) if eB > 0 else 0)
                if best is None or tot < best:
                    best = tot
            return best if best is not None else target + 1

        live = [c for c in cfgs
                if best_bipartition(list(c)) <= target
                and eGDB_lower(c) <= eGDB_upper(c)
                and not has_TKr(c)
                and split_bound(c) <= target]
        if live:
            fx = min(max(max(0, r - s - b) for s in c) for c in live)
            oq = min(len(c) for c in live)
            branches.append((b, fx, oq, max(eGDB_upper(c) for c in live)))
    return branches

def tri_free_survivors(r, m):
    """Case A: H triangle-free.  Then for a vertex v of maximum H-degree
    q = Delta(H) = (r-1) - min_v x_v, the set Q = N_H(v) is independent in H, hence
    a clique K_q in G, and e(H[Q]) = 0.  With R = V \\ Q (which contains v):
        sum_{u in Q} d_H(u) = e_H(Q,R) = q(r-1) - sum_Q x_u >= q(r-1) - X,
        e(H[R]) = e(H) - e_H(Q,R) <= e(H) - q(r-1) + X,
        e(G[R]) = C(n-q,2) - e(H[R]) >= C(n-q,2) - e(H) + q(r-1) - X.
    Q and R are disjoint, so cr(G) >= cr(K_q) + cr(G[R]).  Returns the list of
    min_v x_v values not excluded by this."""
    n = 2 * r - 1
    X = 2 * m - n * (r - 1)
    eH = n * (n - 1) // 2 - m
    out = []
    for s_ in range(0, r):
        if n * s_ > X:                       # sum_v x_v >= n * min_v x_v
            break
        q = (r - 1) - s_
        eGR = (n - q) * (n - q - 1) // 2 - (eH - q * (r - 1) + X)
        tot = crK(q) + (cr_lower_nm(n - q, eGR) if eGR > 0 else 0)
        if tot <= Z(r):
            out.append((s_, tot))
    return out

def controls():
    """Soundness controls: every lower bound produced here must stay below a
    known upper bound on the same quantity."""
    def Zb(a, b):
        return (a // 2) * ((a - 1) // 2) * (b // 2) * ((b - 1) // 2)
    ok = True
    for n in range(5, 61):
        ok &= crK(n) <= Z(n) and cr_lower_nm(n, n * (n - 1) // 2) <= Z(n)
    for a in range(3, 31):
        for b in range(3, 31):
            ok &= cr_lower_nm(a + b, a * b) <= Zb(a, b)
            ok &= kleitman_bipartite(a, b) <= Zb(a, b)
    for n in range(5, 61):
        for m in range(1, 3 * n - 6):
            ok &= cr_lower_nm(n, m) == 0          # such a graph may be planar
    return ok

def run(r, verbose=True):
    n = 2 * r - 1
    lo, hi = edge_range(r)
    aes = (2 * n) // 5
    tf = (r - 1) - aes
    worst, surviveA, allb = None, [], {}
    for m in range(lo, hi + 1):
        a = tri_free_survivors(r, m)
        bs = analyse(r, m)
        if a:
            surviveA.append((m, [x[0] for x in a]))
        cand = ([tf] if a else []) + ([min(br[1] for br in bs)] if bs else [])
        if cand:
            row = min(cand)
            worst = row if worst is None else min(worst, row)
        for br in bs:
            allb.setdefault(br[0], []).append((m, br[1]))
    if verbose:
        print("r = %d,  n = 2r-1 = %d,  Z(r) = %d,  open edge range m in [%d, %d]"
              % (r, n, Z(r), lo, hi))
        print("   Case A (complement triangle-free): Andrasfai-Erdos-Sos would give "
              "max_v x_v >= %d;" % tf)
        print("      surviving rows: %s" % (surviveA if surviveA else "NONE - case A is impossible"))
        print("   Case B (complement has a triangle): surviving barrier sizes")
        for b in sorted(allb):
            print("      b=%2d  %2d of %2d rows (m=%d..%d), forced max_v x_v >= %d"
                  % (b, len(allb[b]), hi - lo + 1, allb[b][0][0], allb[b][-1][0],
                     min(x[1] for x in allb[b])))
        print("   RESULT  max_v (d_G(v)-(r-1)) >= %d   =>   Delta(G) >= %d, "
              "delta(complement) <= %d" % (worst, (r - 1) + worst, (r - 1) - worst))
        print()
    return lo, hi, worst

def main():
    print("Albertson counterexamples of order n = 2r-1: a forced high-degree vertex")
    print("Exact integer/Fraction arithmetic; published inputs only; no solver,")
    print("no floating point, no randomness, no external data.")
    print()
    for label, base in (("cr(K_12)=150 (Pan-Richter 2007)", BASE_CONSERVATIVE),
                        ("cr(K_14)=315 (CCCG 2021)", BASE_CCCG2021)):
        set_base(base)
        print("#" * 76)
        print("# recursion base: %s" % label)
        print("#" * 76)
        print("SOUNDNESS CONTROLS: %s" % ("PASS" if controls() else "FAIL"))
        print()
        summary = []
        for r in (27, 28, 29, 30):
            lo, hi, w = run(r)
            summary.append((r, lo, hi, w))
        for r, lo, hi, w in summary:
            print("SUMMARY base=%s  r=%d  n=%d  m in [%d,%d]:  Delta(G) >= %d"
                  % (label.split()[0], r, 2 * r - 1, lo, hi, (r - 1) + w))
        print()

if __name__ == "__main__":
    main()
