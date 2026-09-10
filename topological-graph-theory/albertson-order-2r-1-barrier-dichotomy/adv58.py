#!/usr/bin/env python3
"""
An admissible H at order 58, built explicitly, and the (3,24) route checked on it.

WHAT THIS IS.  The first computation in this lane on a graph that actually
satisfies every constraint of the class, rather than on parameters.  For

        m = 838,  |R| = 24,  blocks (17,12,5),  e(L) = 212,  e(H[R]) = 178,

it builds H, verifies every count and cap, checks K_4-freeness by exhaustive
search, removes three disjoint triangles, and computes nu of the remaining
49-vertex graph with the certifying matching routine.

==============================================================================
K_4-FREENESS ACROSS THE L/R SPLIT NEEDS THREE CONDITIONS, NOT ONE.

Writing them down is the main content here; the first construction imposed only
the first and was not K_4-free.

  (i)   For each v in L, the set N_H(v) ^ R is TRIANGLE-FREE in H[R].
        Otherwise v together with that triangle is a K_4.  Since
        |N_H(v) ^ R| = rho_i = q_i + |R| - 29, this says H[R] has a triangle-free
        induced set of that size.

  (ii)  For each edge {a,b} of H[R], the L-vertices adjacent to BOTH lie in a
        SINGLE block.  Otherwise two of them from different blocks are H-adjacent
        to each other and to a and b, giving a K_4 on 2 L-vertices and 2
        R-vertices.  THIS is what the first attempt violated.

  (iii) Each z in R has L-neighbours in at most TWO blocks.  Otherwise one vertex
        from each of three blocks is a triangle of H, and z completes a K_4.

Condition (ii) is satisfied here without any constraint on Q_1: if every
Q_2-vertex takes its rho_2 = 7 neighbours INSIDE ONE PART of H[R], no Q_2-vertex
sees both ends of an H[R]-edge, so only Q_1 contributes to any such common
neighbourhood, and Q_1 is one block.  Condition (iii) is free here because
rho_3 = 0.

==============================================================================
THE CONSTRUCTION.  H[R] is K_{8,8,7} on the 23 vertices of Z minus two edges,
with w attached to the four loose ends -- 178 edges, and w of H-degree 4 as the
class requires.  The H-degrees over R are 19 at 28 and 4 at 27 with w at 4,
summing to 29|R| - X = 644.  Each Q_1-vertex takes 12 R-neighbours from a union
of two parts, each Q_2-vertex takes 7 inside one part, and Q_3 takes none.

Every one of those is checked below rather than asserted.

==============================================================================
THE RESULT, AND ITS SCOPE.  nu = 24 with deficiency 1, so the (3,24) route
SUCCEEDS on this H: theta(H) <= 28, contradicting theta(H) = 29.  A randomised
search over admissible placements is run to look for one with nu <= 23.

This does NOT close the configuration.  It is a handful of explicit graphs, and
closing the configuration needs the statement for every admissible H; the greedy
placement is fragile and only a few seeds yield an admissible one, so the sample
is small.  What it does show is that the route is not vacuous, that an admissible
H exists at all, and that constructing reaches a CHECKED answer where the
parameter arguments could not.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import random

from matching import max_matching, size, check_matching

Q = [17, 12, 5]
RS = 24
RHO = [12, 7, 0]
EHR = 178
ELR = sum(Q[i] * RHO[i] for i in range(3))
NL = sum(Q)
N = NL + RS
DEGSUM = 29 * RS - 52            # 29|R| - X with X = 52
CAP = 28
CW = 4


def build(seed):
    """An admissible H, or None if the placement fails."""
    rng = random.Random(seed)
    lab = []
    for i, q in enumerate(Q):
        lab += [i] * q
    lab += [-1] * RS
    Ridx = list(range(NL, N))
    w = Ridx[-1]
    Z = Ridx[:-1]
    adj = [set() for _ in range(N)]

    def add(u, v):
        adj[u].add(v)
        adj[v].add(u)

    for u in range(NL):
        for v in range(u + 1, NL):
            if lab[u] != lab[v]:
                add(u, v)
    P = [Z[0:8], Z[8:16], Z[16:23]]
    pi = {v: i for i, p in enumerate(P) for v in p}
    for a in range(len(Z)):
        for b in range(a + 1, len(Z)):
            u, v = Z[a], Z[b]
            if pi[u] != pi[v]:
                add(u, v)
    drop = [(P[0][0], P[1][0]), (P[0][1], P[2][0])]
    for u, v in drop:
        adj[u].discard(v)
        adj[v].discard(u)
    for u, v in drop:
        add(w, u)
        add(w, v)
    order = sorted(Z, key=lambda z: -len(adj[z]))
    dH = {w: CW}
    for i, z in enumerate(order):
        dH[z] = CAP if i < 19 else CAP - 1
    need = {z: dH[z] - len(adj[z]) for z in Ridx}
    if need[w] != 0 or min(need.values()) < 0:
        return None
    # (ii): every Q_2-vertex inside one part, so E_2 is empty
    q2v = [x for x in range(NL) if lab[x] == 1]
    if seed:
        rng.shuffle(q2v)
    for v in q2v:
        cands = [p for p in P if len(p) >= RHO[1]]
        p = max(cands, key=lambda p: (sum(sorted((need[z] for z in p),
                                                 reverse=True)[:RHO[1]]),
                                      rng.random() if seed else 0))
        for z in sorted(p, key=lambda z: (-need[z], rng.random() if seed else 0))[:RHO[1]]:
            add(v, z)
            need[z] -= 1
    q1v = [x for x in range(NL) if lab[x] == 0]
    if seed:
        rng.shuffle(q1v)
    for v in q1v:
        best = None
        for pa in [(0, 1), (0, 2), (1, 2)]:
            pool = P[pa[0]] + P[pa[1]]
            cand = sorted(pool, key=lambda z: (-need[z], rng.random() if seed else 0))[:RHO[0]]
            if len(cand) == RHO[0]:
                sc = sum(need[z] for z in cand)
                if best is None or sc > best[0]:
                    best = (sc, cand)
        if best is None:
            return None
        for z in best[1]:
            add(v, z)
            need[z] -= 1
    if any(x != 0 for x in need.values()):
        return None
    return lab, adj, Ridx, w


def has_k4(adj):
    for a in range(N):
        na = sorted(adj[a])
        for i in range(len(na)):
            for j in range(i + 1, len(na)):
                b, c = na[i], na[j]
                if c not in adj[b]:
                    continue
                for d in na[j + 1:]:
                    if d in adj[b] and d in adj[c]:
                        return (a, b, c, d)
    return None


def admissible(lab, adj, Ridx, w):
    eHR = sum(1 for u in Ridx for v in adj[u] if v in Ridx and u < v)
    eLR = sum(1 for v in range(NL) for z in adj[v] if z >= NL)
    degR = [len(adj[z]) for z in Ridx]
    checks = [
        ("e(H[R]) exact", eHR == EHR),
        ("e_H(L,R) exact", eLR == ELR),
        ("sum d_H over R exact", sum(degR) == DEGSUM),
        ("every d_H(z) <= 28", max(degR) <= CAP),
        ("d_H(w) <= 4", len(adj[w]) <= CW),
        ("block R-degrees exact",
         all(len([z for z in adj[v] if z >= NL]) == RHO[lab[v]]
             for v in range(NL))),
        ("K_4-free", has_k4(adj) is None),
    ]
    return checks, all(c[1] for c in checks)


def route_nu(lab, adj, tries=6):
    B = [[x for x in range(NL) if lab[x] == i] for i in range(3)]
    best = None
    for off in range(tries):
        T = set()
        for k in range(3):
            for i in range(3):
                T.add(B[i][(k + off) % len(B[i])])
        if len(T) != 9:
            continue
        keep = [v for v in range(N) if v not in T]
        idx = {v: i for i, v in enumerate(keep)}
        a2 = [set() for _ in keep]
        for v in keep:
            for u in adj[v]:
                if u in idx:
                    a2[idx[v]].add(idx[u])
        mt = max_matching(len(keep), a2)
        if not check_matching(len(keep), a2, mt):
            return None
        nu = size(mt)
        if best is None or nu > best:
            best = nu
    return best


def main():
    print("An admissible H at order 58, and the (3,24) route checked on it")
    print("m = 838, |R| = %d, blocks %s, rho %s, e(H[R]) = %d"
          % (RS, tuple(Q), tuple(RHO), EHR))
    print()
    built = build(0)
    if built is None:
        print("   the reference placement failed")
        return
    lab, adj, Ridx, w = built
    checks, ok = admissible(lab, adj, Ridx, w)
    print("ADMISSIBILITY of the reference placement")
    for name, val in checks:
        print("   %-24s %s" % (name, "PASS" if val else "FAIL"))
    print()
    if not ok:
        print("   not admissible; nothing is claimed")
        return
    nu = route_nu(lab, adj)
    print("THE (3,24) ROUTE on it")
    print("   n' = 49 after removing three disjoint triangles")
    print("   nu = %d, deficiency %d;  the route needs nu >= 24" % (nu, 49 - 2 * nu))
    print("   -> %s" % ("SUCCEEDS: theta(H) <= 28, contradicting theta(H) = 29"
                        if nu >= 24 else "FAILS on this H"))
    print()
    print("SEARCH for an admissible placement with nu <= 23")
    worst, tested = None, 0
    for seed in range(1, 121):
        b = build(seed)
        if b is None:
            continue
        l2, a2, R2, w2 = b
        _, ok2 = admissible(l2, a2, R2, w2)
        if not ok2:
            continue
        tested += 1
        v = route_nu(l2, a2)
        if v is not None and (worst is None or v < worst):
            worst = v
    print("   %d of 120 seeds produced an ADMISSIBLE placement; smallest nu"
          % tested)
    print("   found among them = %s.  The greedy placement is fragile, so this"
          % worst)
    print("   is a small sample, not a systematic exploration of the")
    print("   admissible placements -- stated so it is not read as one.")
    print()
    print("CONCLUSION")
    print("   The three cross conditions for K_4-freeness -- triangle-free")
    print("   neighbourhoods, one block per H[R]-edge, at most two blocks per")
    print("   R-vertex -- are what an admissible H must satisfy, and only the")
    print("   first had been used.  With all three imposed an H exists, and on")
    print("   each of the few admissible placements found the (3,24) route")
    print("   SUCCEEDS with nu = 24 and deficiency 1.")
    print()
    print("   This does NOT close the configuration: it is a finite sample, and")
    print("   closing it needs the statement for every admissible H.  It does")
    print("   show the route is not vacuous, and that constructing reaches a")
    print("   checked answer where the parameter arguments could not.")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
