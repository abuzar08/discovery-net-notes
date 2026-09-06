#!/usr/bin/env python3
"""
The last order-57 row at r = 29: row (57, 828) at |R| = 10 and 11.

STATE BEFORE THIS FILE.  close57.py eliminated row (57, 827) and both |R| = 9
cases, leaving row (57, 828) at |R| in [10, 11] as the only open order-57 cases.

The machinery transfers, but two things change and both have to be redone
exactly rather than reused.

==============================================================================
THE PER-BLOCK IDENTITY.  Every vertex of L is low, so d_G(v) = 28 exactly, and
its G-neighbours inside L are exactly the union of its blocks minus itself:
D_v := sum_{blocks ni v} (|Q| - 1).  Hence v has 28 - D_v G-neighbours in R and

        |N_H(v) ^ R|  =  |R| - 28 + D_v ,

so for any block Q of order q,

        e_H(Q, R)  =  q(|R| - 28) + sum_{v in Q} D_v ,

and summing over the blocks, e_H(L, R) = |L|(|R| - 28) + 2 e(L), an identity
that cross-checks against e(H) - e(H[L]) - e(H[R]).

At |R| = 9 the blocks were (24, 24), every D_v was 23, and the count came out
uniform.  Here the multiset has a small connector block whose vertices are all
cut vertices (Constraint C), so D_v is larger for those and the per-block totals
are NOT uniform.  Using the crude bound
sum_z a_z >= e_H(L,R) - |Z| * |L - Q_1| throws almost everything away -- it gives
26 where the truth is 145.  The per-block identity is what must be used.

==============================================================================
WHAT HAS TO BE PROVED.  theta(H) = chi(G) = 29.  Colouring L with chi(G[L]) =
max block order colours, absorbing t vertices of R into distinct colour classes,
and colouring the rest of R,

        29 = chi(G)  <=  maxq + (|R| - t) - nu ,      nu := nu(H[R]) ,

so a contradiction needs   t + nu  >=  maxq + |R| - 28.

Absorbing z into a class {u, v} with u in Q_1 and v outside Q_1 needs z to be
H-adjacent to both, i.e. exactly the triangle condition, and t such absorptions
into distinct classes exist as soon as

        mu_1 + mu_2  >=  |Z| + t ,

where mu_1, mu_2 are the maximum matchings of Z against Q_1 and against L - Q_1.
Koenig bounds each below from the corresponding edge total:  a cover of size k
admits at most q*cz + (|Z| - cz)*min(k - cz, q) edges.

==============================================================================
THE w-DEDUCTION IS THE WHOLE FIGHT.  N_H(w_i) lies inside B, so

        c := sum_i |N_H(w_i) ^ L|  =  2(1 - sigma) + (a - j_A),

where a := |A_1| + |A_2|, sigma = 1 if s is high, j := |T ^ R| and j_A is the
number of high T-vertices lying in A_1 u A_2.  That c splits as c_1 + c_2
between Q_1 and L - Q_1, and each part is subtracted from the corresponding edge
total before the Koenig bound.  A single unit moved between c_1 and c_2 can cost
a whole unit of mu, so every split has to be checked.

==============================================================================
A SOUNDNESS CORRECTION.  An earlier version of this file took the second side to
be L - Q_1 with edge total e_H(L,R) - e1.  Since e1 is a LOWER bound for
e_H(Q_1,R), that expression is an UPPER bound on e_H(L - Q_1, R), and feeding an
upper bound into a Koenig lower bound overstates mu_2 -- by one full unit for the
multisets carrying a connector block, (24,23,2) at |R| = 10 and (24,22,2) at
|R| = 11.  The conclusion was unaffected, and unaffected a fortiori, since it was
negative and an overstated mu only makes closure look more likely; and the
tightest multisets quoted, (24,23) and (24,22), are ones where the sound and
unsound values agree, so "short by exactly one" also stands.  The version below
uses the sound bound: second side Q_2 - Q_1, of size at least q_2 - 1, with edge
total at least (q_2 - 1)(q_2 + |R| - 29).

RESULT, REPORTED NEGATIVELY.  The enumeration below runs every admissible block
multiset -- not just the crossing-minimiser -- and every (a, j, sigma) with every
split of c.  Row (57, 828) does NOT close at |R| = 10 or 11.

The deficit is small and uniform.  At the tightest multisets, (24,23) for
|R| = 10 and (24,22) or (24,22,2) for |R| = 11, Koenig gives mu_1 + mu_2 >= 9
resp. 10 where |Z| + t = 10 resp. 11 is needed: short by exactly ONE.  The
multisets with a block of order 25 are further off, by 3 or 4, because
chi(G[L]) = 25 raises the number of absorptions needed faster than the larger
block raises mu_1.

So the |R| = 9 argument does not extend, and the reason is structural rather
than arithmetic: at |R| = 9 the two blocks partitioned L and every z was forced
to be crossing, which is what drove mu_1, mu_2 >= 6.  Here |Z| is larger, |L| is
smaller, and neither is forced.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import r29 as R9

N = R9.N          # 57
DEG = R9.DEG      # 28
M = 828


def koenig_min_mu(edge_total, side, nz):
    """Least k such that a vertex cover of size k could carry `edge_total`
    edges of a bipartite graph with parts of sizes nz and `side`."""
    for k in range(0, nz + 1):
        best = max(side * cz + (nz - cz) * min(k - cz, side)
                   for cz in range(0, min(k, nz) + 1))
        if best >= edge_total:
            return k
    return nz + 1


def multisets(RSZ):
    """Every block multiset admissible for row 828 at this |R|, under the
    filters of cover57.py: the e(L) band, no isolated low vertex, and the
    covering condition on small blocks."""
    NL = N - RSZ
    d0 = DEG - RSZ
    X = 2 * M - N * DEG
    base = M - (DEG * RSZ + X)
    eLo = base + R9.eGR_min(RSZ)
    eHi = base + RSZ * (RSZ - 1) // 2
    out = []

    def rec(rem, cap, edges, blocks):
        if rem == 0:
            if eLo <= edges <= eHi:
                extra = sum(blocks) - NL
                if extra < 0:
                    return
                big = [q for q in blocks if q - 1 >= d0]
                sb = sum(big)
                if sb > NL:
                    return
                if sum(q * (q - 1) for q in blocks if q - 1 < d0) < d0 * (NL - sb):
                    return
                out.append((tuple(sorted(blocks, reverse=True)), edges))
            return
        hi, r2, c2 = edges, rem, cap
        while r2 > 0:
            t = min(c2, r2)
            hi += t * (t + 1) // 2
            r2 -= t
        if hi < eLo or edges > eHi:
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem - u, u, edges + u * (u + 1) // 2, blocks + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, blocks)
    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return sorted(set(out))


def main():
    print("Albertson r = 29, order 57, row (57, %d): the last open cases" % M)
    print()
    X = 2 * M - N * DEG
    for RSZ in (10, 11):
        NL = N - RSZ
        NZ = RSZ - 2
        amin = max(1, NZ - X + 2 * DEG - 2)
        ms = multisets(RSZ)
        print("|R| = %d : |L| = %d, |Z| = %d, a >= %d, %d admissible block"
              " multisets" % (RSZ, NL, NZ, amin, len(ms)))
        survivors = []
        for mult, eL in ms:
            eGR = eL - M + DEG * RSZ + X
            eHR = RSZ * (RSZ - 1) // 2 - eGR
            eHLR = NL * (RSZ - DEG) + 2 * eL
            maxq = max(mult)
            nu = min(eHR, RSZ // 2)
            tneed = maxq + RSZ - 28 - nu
            if tneed <= 0:
                continue                       # already contradictory
            # Sound two-sided bound.  e1 is a lower bound for e_H(Q_1,R).  The
            # SECOND side must also be lower-bounded, so it cannot be taken as
            # e_H(L,R) - e1: that is an UPPER bound on e_H(L - Q_1, R), and
            # feeding an upper bound into a Koenig lower bound overstates mu_2.
            # Instead take the side to be Q_2 - Q_1.  Two blocks meet in at most
            # one vertex, so |Q_2 - Q_1| >= q_2 - 1 and each such vertex has
            # D_v >= q_2 - 1, giving the lower bound below.  Q_1 and Q_2 - Q_1
            # are disjoint, and a colour class holds at most one vertex of each.
            q2 = mult[1] if len(mult) > 1 else 1
            e1 = maxq * (maxq + RSZ - 29)
            e2 = (q2 - 1) * (q2 + RSZ - 29)
            side2 = max(q2 - 1, 1)
            bad = []
            for a in range(amin, 4):
                for j in range(1, 4):
                    for sig in (0, 1):
                        jA = max(0, j + a - 3)
                        c = 2 * (1 - sig) + a - jA
                        if c < 0:
                            continue
                        for c1 in range(0, c + 1):
                            mu1 = koenig_min_mu(e1 - c1, maxq, NZ)
                            mu2 = koenig_min_mu(e2 - (c - c1), side2, NZ)
                            if mu1 + mu2 < NZ + tneed:
                                bad.append((a, j, sig, c1, c - c1, mu1, mu2))
            if bad:
                w = min(bad, key=lambda t: t[5] + t[6])
                survivors.append((mult, eL, eHR, maxq, tneed, e1, e2, w, len(bad)))
        if not survivors:
            print("   every admissible multiset closes  ->  |R| = %d IMPOSSIBLE"
                  % RSZ)
        else:
            print("   %d multisets survive; the worst are" % len(survivors))
            for (mult, eL, eHR, maxq, tneed, e1, e2, w, nb) in survivors[:4]:
                print("      %-16s e(L)=%d e(H[R])=%d chi=%d t>=%d"
                      % (str(mult)[:16], eL, eHR, maxq, tneed))
                print("         e_H(Q_1,R)>=%d, e_H(L-Q_1,R)>=%d ; worst"
                      " a=%d j=%d sig=%d c=(%d,%d): mu_1>=%d mu_2>=%d,"
                      " sum %d < %d"
                      % (e1, e2, w[0], w[1], w[2], w[3], w[4], w[5], w[6],
                         w[5] + w[6], NZ + tneed))
            print("   shortfall at the worst multiset: %d"
                  % (NZ + survivors[0][4] - survivors[0][7][5]
                     - survivors[0][7][6]))
        print()


if __name__ == "__main__":
    main()
