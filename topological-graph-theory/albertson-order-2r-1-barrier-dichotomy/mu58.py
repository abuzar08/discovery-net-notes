#!/usr/bin/env python3
"""
A sound two-sided Koenig bound, and its effect on the two surviving cases.

Order 57 row (57,828) at |R| = 10, 11 and order 58 class b = 6, c = (51,1) at
|R| >= 11 are the only cases left at r = 29.  Both are attacked by the same
absorption argument, and both need a lower bound on two matchings mu_1, mu_2 of
the high set against two DISJOINT parts of L.

==============================================================================
A SOUNDNESS CORRECTION TO close57b.py.

That file took the second side to be L - Q_1 and gave it the edge total

        e2 := e_H(L,R) - e1,        e1 := q_1(q_1 + |R| - 29),

where e1 is a valid LOWER bound for e_H(Q_1,R).  But then

        e2 = e_H(L,R) - e1  >=  e_H(L,R) - e_H(Q_1,R) = e_H(L - Q_1, R),

so e2 is an UPPER bound on the true edge total of the second side, and feeding
an upper bound into a Koenig lower bound overstates mu_2.  Checking it, the
overstatement is one full unit for the multisets carrying a connector block:

        |R| = 10, (24,23,2):  mu_2 = 5 claimed, 4 sound
        |R| = 11, (24,22,2):  mu_2 = 5 claimed, 4 sound

The conclusion of close57b.py is unaffected, and unaffected *a fortiori*: it
reported that the row does NOT close, and an overstated mu only makes closure
look more likely.  The tightest multisets it quoted, (24,23) at |R| = 10 and
(24,22) at |R| = 11, are ones where the sound and unsound values agree, so the
published "short by exactly one" also stands.  Still, the inference was invalid
and is replaced here.

THE SOUND VERSION.  Take the second side to be Q_2 - Q_1, where Q_2 is the
second largest block.  Two blocks of a graph meet in at most one vertex, so
|Q_2 - Q_1| >= q_2 - 1, every vertex of it has D_v >= q_2 - 1, and

        e_H(Q_2 - Q_1, R)  >=  (q_2 - 1)(q_2 + |R| - 29).

Q_1 and Q_2 - Q_1 are disjoint by construction, and a colour class of G[L] holds
at most one vertex of each (both are cliques), so a class {u, v} with u in Q_1
and v in Q_2 - Q_1 is exactly what an absorption needs.

==============================================================================
THE TEST.  With t := chi(G[L]) + |R| - 28 - nu absorptions needed and Z the high
vertices other than the singleton w, a contradiction follows once

        mu_1 + mu_2  >=  |Z| + t .

At order 58 the singleton w of the class c = (51,1) has N_H(w) inside B with at
most two neighbours per triangle, so d_H(w) <= b - 2 = 4 and its deduction from
the two edge totals is at most 4, split adversarially.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
from order2r import RCHI, Z

r = RCHI
DEG = r - 1          # 28
crK = V.crK


def koenig(edge_total, side, nz):
    """Least k for which a vertex cover of size k could carry `edge_total`
    edges between parts of sizes nz and `side`."""
    if edge_total <= 0:
        return 0
    for k in range(0, nz + 1):
        best = max(side * cz + (nz - cz) * min(k - cz, side)
                   for cz in range(0, min(k, nz) + 1))
        if best >= edge_total:
            return k
    return nz + 1


def multisets(NL, eLo, eHi, d0, cap):
    out = []

    def rec(rem, capb, edges, blocks):
        if rem == 0:
            if eLo <= edges <= eHi:
                if sum(blocks) - NL < 0:
                    return
                big = [q for q in blocks if q - 1 >= d0]
                if sum(big) > NL:
                    return
                if sum(q * (q - 1) for q in blocks if q - 1 < d0) \
                        < d0 * (NL - sum(big)):
                    return
                out.append((tuple(sorted(blocks, reverse=True)), edges))
            return
        hi, r2, c2 = edges, rem, capb
        while r2 > 0:
            t = min(c2, r2)
            hi += t * (t + 1) // 2
            r2 -= t
        if hi < eLo or edges > eHi:
            return
        for u in range(min(capb, rem), 0, -1):
            if u + 1 > cap:
                continue
            rec(rem - u, u, edges + u * (u + 1) // 2, blocks + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, blocks)
    for c in range(1, NL + 1):
        rec(NL - c, NL - c, 0, [])
    return sorted(set(out))


def run(nn, m, RSZ, mult, eL, NZ, cmax):
    """Sound two-sided test.  Returns (t needed, mu_1, mu_2, closes)."""
    NL = nn - RSZ
    X = 2 * m - nn * DEG
    base = m - DEG * RSZ - X
    eGR = eL - base
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    maxq = max(mult)
    nu = min(eHR, RSZ // 2)
    tneed = maxq + RSZ - 28 - nu
    if tneed <= 0:
        return tneed, None, None, True
    q1 = mult[0]
    q2 = mult[1] if len(mult) > 1 else 1
    e1 = q1 * (q1 + RSZ - 29)
    e2 = (q2 - 1) * (q2 + RSZ - 29)
    best = None
    for c1 in range(0, cmax + 1):
        s = koenig(e1 - c1, q1, NZ) + koenig(e2 - (cmax - c1), max(q2 - 1, 1), NZ)
        if best is None or s < best:
            best = s
    return tneed, e1, e2, best >= NZ + tneed


def main():
    print("A sound two-sided Koenig bound at r = %d" % r)
    print()

    print("PART 1   order 57, row (57,828): the corrected numbers")
    N57 = 2 * r - 1
    for RSZ in (10, 11):
        NL = N57 - RSZ
        X = 2 * 828 - N57 * DEG
        base = 828 - DEG * RSZ - X
        d0 = DEG - RSZ
        ms = multisets(NL, max(base, 0), base + RSZ * (RSZ - 1) // 2, d0, r)
        worst = None
        for mult, eL in ms:
            tneed, e1, e2, ok = run(N57, 828, RSZ, mult, eL, RSZ - 2, 5)
            if not ok:
                short = (RSZ - 2 + tneed) - (koenig(e1 - 0, mult[0], RSZ - 2)
                                             + koenig(e2 - 5, max(mult[1] - 1, 1)
                                                      if len(mult) > 1 else 1,
                                                      RSZ - 2))
                if worst is None or short > worst[1]:
                    worst = (mult, short, tneed)
        print("   |R| = %d : %d multisets, none closes; largest shortfall %d at %s"
              % (RSZ, len(ms), worst[1] if worst else 0,
                 str(worst[0]) if worst else "-"))
    print("   (unchanged from close57b.py, which was safe a fortiori)")
    print()

    print("PART 2   order 58, class b = 6, c = (51,1), the last order-58 case")
    N58 = 2 * r
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        Rmax = 1 + max(0, X - (r + 2 - 6))
        alive = []
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            for mult, eL in multisets(NL, max(base, 0),
                                      base + RSZ * (RSZ - 1) // 2, d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                tneed, e1, e2, ok = run(N58, m, RSZ, mult, eL, RSZ - 1, 4)
                if not ok:
                    alive.append((RSZ, mult, tneed))
        if not alive:
            print("   m = %d : |R| in [11, %d], NOTHING survives  ->  IMPOSSIBLE"
                  % (m, Rmax))
        else:
            rs = sorted(set(a[0] for a in alive))
            print("   m = %d : |R| in [11, %d], %d survivors at |R| in %s"
                  % (m, Rmax, len(alive), "%d..%d" % (rs[0], rs[-1])))
            for a in alive[:3]:
                print("        |R|=%d %s t>=%d" % (a[0], str(a[1])[:26], a[2]))


if __name__ == "__main__":
    main()
