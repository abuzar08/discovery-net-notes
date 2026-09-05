#!/usr/bin/env python3
"""
Two things at r = 29:

PART 1 -- an independent reproduction of the eight-row r = 29 frontier, from
published inputs plus the Gallai join/edge-budget argument.

PART 2 -- a first attempt at the order-2r barrier machinery, the one structural
gap left by the order-(2r-1) theory.

--------------------------------------------------------------------------
ORDER 2r.  Let G be r-critical of order n = 2r with connected complement H and
cr(G) < cr(K_r).  Then delta(G) >= r-1, so Delta(H) <= r, and with
x_v := d_G(v) - (r-1) = r - d_H(v) >= 0 we have sum_v x_v = 2m - 2r(r-1).
theta(H) = r, so no clique partition of V(H) into r-1 parts: sizes summing to 2r
over r-1 parts would give savings r+1.  Two consequences used here:

  (K4)  For every K_4 Q of H, H - Q has no perfect matching: otherwise
        Q together with that matching is a partition into 1 + (r-2) = r-1
        cliques with savings 3 + (r-2) = r+1.
  (TT)  For every pair of disjoint triangles T1, T2 with H - T1 - T2 having a
        perfect matching, the same count gives savings 2+2+(r-3) = r+1.

(K4) plus Tutte-Berge gives, whenever H contains a K_4, a set B = Q u S with
b = |B| = |S| + 4 and

        o(H - B) >= |S| + 2 = b - 2,

which is the order-2r analogue of the o(H-B) >= b-1 used at order 2r-1 -- one
weaker.  The same five filters then apply to the component multiset of H - B:
degree deficiency, the Kleitman bound on the complete bipartite subgraph forced
by the complete-multipartite part G[D], the exact e_G(D,B) identity against
delta(G) >= r-1, a forced K_r, and the split bound.

If H has no K_4 at all then alpha(G) <= 3; that branch is NOT handled here and is
reported separately.

NON-DOMINATION AT ORDER 2r (new; the analogue of the order-2r-1 lemma).

  Let H have theta(H) = r on 2r vertices with Stehlik's property, and let {w} be
  a component of H - B.  Then no vertex a of N_H(w) is adjacent to every other
  vertex of N_H(w).

  Proof.  Suppose a dominates N_H(w).  Take Stehlik's cover of H - a: one
  triangle T_a and r-2 edges, r-1 parts, every part of size >= 2.  The part
  containing w consists of w together with vertices of N_H(w) minus {a}, all adjacent
  to a by assumption.
    * If that part is an edge {w,u}, then {w,a,u} is a triangle, and replacing
      {w,u} by it gives a cover of H by T_a, that triangle and the remaining r-3
      edges: r-1 parts covering 3 + 3 + 2(r-3) = 2r vertices with savings
      2 + 2 + (r-3) = r+1, so theta(H) <= r-1.
    * If that part is the triangle T_a = {w,y,z}, then y,z are adjacent to a and
      to each other, so {w,y,z,a} is a K_4; with the r-2 edges it is a cover by
      r-1 parts covering 4 + 2(r-2) = 2r vertices with savings 3 + (r-2) = r+1.
  Either way theta(H) <= r-1, a contradiction.  QED

  Two consequences.  First, delta(H) >= 2: a vertex of degree 1 could not be put
  in any part of size >= 2 of the cover of H minus its neighbour.  Second, when
  B is a CLIQUE the lemma is immediately contradictory, because then every vertex
  of N_H(w) dominates the rest.  So the barrier size b = 4, where B is the K_4
  itself, is impossible whenever H - B has a singleton component.
--------------------------------------------------------------------------
"""
import recursive as R
import verify_range as V

RCHI = 29
Z = V.Z(RCHI)
NMAX = 80
_L = R.build(NMAX, rounds=3)


def L(n, q):
    if n < 4 or q <= 0 or n not in _L:
        return 0
    return _L[n][min(q, len(_L[n]) - 1)]


def ky(r, n):
    if r <= 1:
        return 0
    if r == 2:
        return 1
    return -(-((r + 1) * (r - 2) * n - r * (r - 3)) // (2 * (r - 1)))


def cor7(r, n):
    return -(-(n * (r - 1) + 2 * (r - 3)) // 2)


def cor5(r, n):
    p = n - r
    if not (2 <= p <= r - 1):
        return 0
    return -(-((r - 1) * n + p * (r - p) - 1) // 2)


def floor_of(r, n):
    return max(ky(r, n), cor7(r, n), cor5(r, n))


def ceiling_of(r, n):
    zz = V.Z(r)
    return max([q for q in range(len(_L[n])) if _L[n][q] < zz], default=-1)


def cranston_excluded(n, r):
    if 50 * n >= 141 * r:
        return True
    return 250 * n >= 307 * r and 125 * n <= 221 * r


def join_survivors(r, n, mhi):
    live = []

    def rec(rrem, vrem, minr, cur):
        if rrem == 0:
            if vrem != 0 or len(cur) < 2:
                return
            eM = (n * n - sum(v * v for _, v in cur)) // 2
            kys = sum(ky(ri, vi) for ri, vi in cur)
            deep = [(rj, vj) for rj, vj in cur if rj >= 4]
            if not deep:
                return
            need = min(eM + kys - ky(rj, vj) + max(ky(rj, vj), floor_of(rj, vj))
                       for rj, vj in deep)
            if need <= mhi:
                live.append((sorted(cur, reverse=True), eM, need))
            return
        for ri in range(minr, rrem + 1):
            if ri == 2:
                continue
            if ri == 1:
                if vrem >= 1:
                    rec(rrem - 1, vrem - 1, 1, cur + [(1, 1)])
                continue
            for vi in range(2 * ri - 1, vrem + 1):
                if ky(ri, vi) > mhi:
                    break
                rec(rrem - ri, vrem - vi, ri, cur + [(ri, vi)])
    rec(r, n, 1, [])
    return live


# ------------------------------------------------------------------ order 2r
def configs(total, nodd, free, budget):
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


def order2r_survivors(r, m):
    """Barrier classification at n = 2r under (K4): o(H-B) >= b-2."""
    n = 2 * r
    X = 2 * m - n * (r - 1)
    eH = n * (n - 1) // 2 - m
    zz = V.Z(r)
    live = []
    for b in range(4, n + 1):
        nodd = b - 2
        if n - b < nodd:
            continue
        # v in C: d_H(v) <= |C|-1+b, and x_v = r - d_H(v), so x_v >= r+1-|C|-b
        free = r + 1 - b
        for c in configs(n - b, nodd, free, X):
            D = sum(c)
            CB = b * (b - 1) // 2
            if V.best_bipartition(list(c)) > zz:
                continue
            # e_G(D,B) = |D|(b-r) + sum_D x_v + 2 sum_C e(H[C])
            up = D * (b - r) + X + 2 * sum(s * (s - 1) // 2 for s in c)
            lo = max(b * max(0, (r - 1) - (b - 1)), D * max(0, (r - 1) - D + 1))
            if lo > up:
                continue
            if len(c) >= r:
                continue
            Ymin = sum(s * max(0, r + 1 - s - b) for s in c)
            Pmin = sum(s - 1 for s in c)
            Pmax = sum(s * (s - 1) // 2 for s in c)
            best = None
            for Y in range(Ymin, X + 1):
                # sum_D d_H = |D| r - Y = e_H(D,B) + 2P  =>  P = (|D| r - Y - e_H(D,B))/2
                # and e(H) = e(H[B]) + e_H(D,B) + P  =>  P = |D| r - Y - e(H) + e(H[B])
                Q = min(CB, Pmax - D * r + Y + eH)
                if Q < 6:                      # B contains a K_4: >= 6 edges
                    continue
                P = D * r - Y - eH + Q
                if not (Pmin <= P <= Pmax):
                    continue
                CD = D * (D - 1) // 2
                crD = max(V.crK(len(c)), L(D, CD - P), V.best_bipartition(list(c)))
                eB = CB - Q
                crB = L(b, eB) if eB > 0 else 0
                t = crD + crB
                if best is None or t < best:
                    best = t
            if best is not None and best <= zz:
                live.append((b, tuple(sorted(c, reverse=True))))
    return live


def main():
    print("Albertson r = %d: independent frontier, and the order-2r attempt" % RCHI)
    print("Z(%d) = %d" % (RCHI, Z))
    print()
    print("PART 1   independent r = 29 order reduction")
    print("   n <= %d: Barat-Toth Corollary 11" % (RCHI + 4))
    surv = []
    for n in range(RCHI + 5, NMAX + 1):
        if cranston_excluded(n, RCHI):
            continue
        lo, hi = floor_of(RCHI, n), ceiling_of(RCHI, n)
        if lo <= hi:
            surv.append((n, lo, hi))
    print("   floors vs recursive ceiling leave: %s" % [t[0] for t in surv])
    for n, lo, hi in surv:
        print("      n=%2d  m in [%d, %d]  (%d rows)%s"
              % (n, lo, hi, hi - lo + 1,
                 "   <- n <= 2r-2, Gallai join applies" if n <= 2 * RCHI - 2 else ""))
    for n, lo, hi in surv:
        if n <= 2 * RCHI - 2:
            live = join_survivors(RCHI, n, hi)
            print("      n=%2d join decompositions within the edge budget: %d %s"
                  % (n, len(live), "-> ORDER IMPOSSIBLE" if not live else live[:2]))
    left = [t for t in surv if t[0] > 2 * RCHI - 2
            or join_survivors(RCHI, t[0], t[2])]
    tot = sum(t[2] - t[1] + 1 for t in left)
    print("   => surviving orders %s, %d rows in total"
          % ([t[0] for t in left], tot))
    print("      (ledger height 2761 reports the same eight rows: orders 57 and 58)")
    print()

    print("PART 2   order 2r = %d, assuming H contains a K_4" % (2 * RCHI))
    print("   barrier classes surviving the five filters:")
    kill4 = True
    for m in (838, 839, 840):
        live = order2r_survivors(RCHI, m)
        for b, c in live:
            note = ""
            if b == 4:
                note = "   killed: B is the K_4 itself, a clique -> non-domination"
                if 1 not in c:
                    kill4 = False
            print("     m=%d  b=%d  %s%s" % (m, b, c, note))
    assert kill4, "a b=4 class has no singleton component"
    print()
    print("   The only class left is b = 5 with H - B = C u {w1} u {w2}, |C| = %d."
          % (2 * RCHI - 7))
    print("   There B = Q u {s} with Q a K_4; non-domination gives w_i ~ s and s")
    print("   adjacent to no vertex of A_i := N_Q(w_i); and A_1, A_2 are disjoint,")
    print("   because otherwise both w_1 and w_2 would have to occupy the part")
    print("   {w_i, s} of the same cover.  Hence d_H(w1)+d_H(w2) <= 2 + |Q| = 6 and")
    print("   x_{w1} + x_{w2} >= 2r - 6 = %d." % (2 * RCHI - 6))
    print()
    print("   m    |R|  |V(L)|  e(L) >=   Gallai cap   split bound   verdict")
    n2 = 2 * RCHI
    for m in (838, 839, 840):
        X = 2 * m - n2 * (RCHI - 1)
        for Rsz in range(2, 2 + (X - (2 * RCHI - 6)) + 1):
            VL = n2 - Rsz
            eL = m - ((RCHI - 1) * Rsz + X) + eGR_2r(Rsz)
            cap = gallai_cap(VL, RCHI - 2)
            sp = min_split(VL, eL)
            ok = eL > cap or (sp is not None and sp > Z)
            print("  %3d   %2d    %3d     %4d       %5d       %6s       %s"
                  % (m, Rsz, VL, eL, cap, sp, "impossible" if ok else "SURVIVES"))
            assert ok
    print()
    print("   => order %d is impossible whenever H contains a K_4," % n2)
    print("      i.e. whenever alpha(G) >= 4.")
    print()
    print("PART 3   what is NOT covered")
    print("   If H has no K_4 (alpha(G) <= 3) the barrier must come instead from two")
    print("   disjoint triangles, giving only o(H-B) >= b-4.  Those classes (b = 6,")
    print("   7 and 30) survive the same filters, so that branch stays open.")


def eGR_2r(Rsz):
    """As at order 2r-1, but with |Q| = 4 rather than |T| = 3."""
    nz = Rsz - 2
    best = None
    for sigma in (0, 1):
        for tA in range(0, 5):
            for tO in range(0, 5 - tA):
                if sigma + tA + tO > nz:
                    continue
                v = 1 + 2 * (nz - sigma - tA - tO) + tA + 2 * tO + sigma * tA
                if best is None or v < best:
                    best = v
    return max(1, best if best is not None else 1)


def gallai_cap(VL, maxblk):
    U = VL - 1
    NEG = -1
    dp = [[NEG, NEG] for _ in range(U + 1)]
    dp[0][1] = 0
    for t in range(U + 1):
        for s in (0, 1):
            if dp[t][s] < 0:
                continue
            for u in range(1, U - t + 1):
                o = []
                if u + 1 <= maxblk - 1:
                    o.append((u * (u + 1) // 2, s))
                elif u + 1 == maxblk and s == 1:
                    o.append((u * (u + 1) // 2, 0))
                if u >= 2 and (u + 1) % 2 == 1:
                    o.append((u + 1, s))
                for e, ns in o:
                    if dp[t][s] + e > dp[t + u][ns]:
                        dp[t + u][ns] = dp[t][s] + e
    return max(dp[U])


def min_split(NL, eL_lo):
    best = [None]

    def rec(rem, cap, edges, cliques):
        if rem == 0:
            if edges >= eL_lo:
                s = sum(V.crK(b) for b in cliques if b >= 15)
                if best[0] is None or s < best[0]:
                    best[0] = s
            return
        hi, rr, c2 = edges, rem, cap
        while rr > 0:
            t = min(c2, rr)
            hi += t * (t + 1) // 2
            rr -= t
        if hi < eL_lo:
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem - u, u, edges + u * (u + 1) // 2, cliques + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, cliques)
    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return best[0]


if __name__ == "__main__":
    main()
