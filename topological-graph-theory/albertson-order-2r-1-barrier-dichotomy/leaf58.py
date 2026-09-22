#!/usr/bin/env python3
"""
The leaf-block lemma: a new admissibility filter, and what it costs |R| - q_1.

WHY.  capacity58.py showed the order-58 absorption deficit is missing CAPACITY,
not slack -- mu_1 and mu_2 sit at ceilings no matching can pass -- and that the
deficit tracks |R| - q_1, the gap between the high set and the largest Gallai
block.  So the only lever left is a theorem about that gap.  This file does two
things: it proves and applies one such constraint, and it prices the general
programme honestly, including what makes it impossible to push far.

==============================================================================
THE LEMMA.

G[L] is a Gallai forest (Gallai's theorem on the low vertices of a k-critical
graph), so every block is a complete graph or an odd cycle.  Every v in L has
d_G(v) = 28 and at most |R| neighbours outside L, so its degree INSIDE L is

        D_v  >=  d_0 := 28 - |R| .

Let B be a LEAF block -- a block containing at most one cut vertex of its
component.  B has at least two vertices, so it has a vertex v that is not a cut
vertex, and such a v lies in no block but B.  Hence N_{G[L]}(v) is contained in
B and

        D_v  =  deg_B(v)  =  q_B - 1   (B a clique)    or    2   (B an odd cycle).

        THEREFORE, IF d_0 >= 3: no leaf block is an odd cycle, and every leaf
        block is a clique with q_B >= d_0 + 1 = 29 - |R|.

Every component of a forest of blocks has at least one leaf block, and at least
two if it has at least two blocks, so this is a real constraint on the block
multiset -- and it is NOT implied by the Constraint-C filters of auditc.py,
which only bound degree SUMS.

d_0 >= 3 IS THE EXACT VALIDITY THRESHOLD, and the caller enforces it.  At
d_0 <= 2 an odd-cycle leaf block has degree 2 >= d_0 and satisfies the floor,
so the lemma says nothing; PART 5 measures what applying it there anyway would
have wrongly bought, so that the threshold is visible rather than asserted.

WHAT IS APPLIED.  Not the weak corollary "some block is big", but the exact
test: does SOME realisable assignment of cut vertices leave every leaf block of
size at least d_0 + 1?  If none does, no Gallai forest on that multiset can
occur and the configuration is impossible.  packing58.forests already
enumerates exactly those assignments -- the same enumeration the triangle
guarantee is built on.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import packing58 as PK
import tuttegen as G

# adv58.py's explicitly constructed admissible H, for the positive control.
ADV_BLOCKS, ADV_R = (17, 12, 5), 24


def killed(cfgs):
    """The configurations the lemma rules out, with their parameters."""
    out = []
    for m, RSZ, mult, eHR in cfgs:
        d0 = G.DEG - RSZ
        if d0 < 3:
            continue
        X = 2 * m - G.N58 * G.DEG
        tb = G.true_blocks(mult, RSZ, eHR, X)
        if not PK.leaf_feasible(tb, G.N58 - RSZ, d0):
            out.append((m, RSZ, mult, eHR))
    return out


def main():
    print("The leaf-block lemma at order 58")
    print()
    before = G.configurations(leaf=False)
    after = G.configurations(leaf=True)
    print("PART 1   what it removes from the enumeration")
    print("   configurations before the filter: %d" % len(before))
    print("   configurations after:             %d" % len(after))
    dead = killed(before)
    print("   removed: %d" % len(dead))
    byR = {}
    for _m, RSZ, _mu, _e in dead:
        byR[RSZ] = byR.get(RSZ, 0) + 1
    print("   by |R|: %s" % sorted(byR.items()))
    newly = sum(1 for m, RSZ, mult, eHR in dead
                if not G.route_closed(RSZ, list(mult), eHR,
                                      2 * m - G.N58 * G.DEG)[0])
    print("   of those, OPEN under every previous filter -- NEW CLOSURES: %d"
          % newly)
    print()

    print("PART 2   positive control: the one explicitly constructed H")
    d0 = G.DEG - ADV_R
    NL = G.N58 - ADV_R
    ok = PK.leaf_feasible(ADV_BLOCKS, NL, d0)
    print("   adv58.py builds an admissible H with |R| = %d, blocks %s"
          % (ADV_R, str(ADV_BLOCKS)))
    print("   d_0 = %d, so every leaf block needs q >= %d; smallest block is %d"
          % (d0, d0 + 1, min(ADV_BLOCKS)))
    print("   lemma accepts it: %s   %s" % (ok, "PASS" if ok else "**FAIL**"))
    print("   -- and with margin ZERO, which is the useful part: the filter is")
    print("      tight against the only admissible H anyone here has built.")
    print()

    print("PART 3   completeness of the enumeration the filter rests on")
    worst, empty, lim = 0, 0, 0
    for m, RSZ, mult, eHR in before:
        d0 = G.DEG - RSZ
        if d0 < 3:
            continue
        X = 2 * m - G.N58 * G.DEG
        tb = G.true_blocks(mult, RSZ, eHR, X)
        extra = sum(tb) - (G.N58 - RSZ)
        if extra < 0:
            continue
        fs = PK.forests(list(tb), extra)
        worst = max(worst, len(fs))
        if not fs:
            empty += 1
        if len(fs) >= 200000:
            lim += 1
    print("   most realisable forests on any one multiset: %d" % worst)
    print("   calls that hit the 200000 cap: %d" % lim)
    print("   multisets with no realisable forest at all: %d" % empty)
    print("   %s -- a rejection is 'no forest is admissible', never"
          % ("PASS" if lim == 0 else "**FAIL**"))
    print("   'the enumeration gave up'.")
    print()

    print("PART 4   the validity threshold is load-bearing, not decorative")
    would = 0
    for m, RSZ, mult, eHR in before:
        d0 = G.DEG - RSZ
        if d0 >= 3 or d0 < -100:
            continue
        X = 2 * m - G.N58 * G.DEG
        tb = G.true_blocks(mult, RSZ, eHR, X)
        if not PK.leaf_feasible(tb, G.N58 - RSZ, max(d0, 3)):
            would += 1
    print("   applied at d_0 <= 2, where an odd-cycle leaf block is permitted,")
    print("   the same test would remove a further %d configurations." % would)
    print("   THEY ARE NOT CLAIMED.  This is the number the lane would have")
    print("   over-claimed by if the threshold had been asserted instead of")
    print("   derived -- the failure auditc.py exists to prevent for (C1)-(C3).")
    print()

    print("PART 5   pricing the general programme: a theorem q_1 >= |R| - k")
    gaps = sorted(RSZ - max(G.true_blocks(mult, RSZ, eHR,
                                          2 * m - G.N58 * G.DEG))
                  for m, RSZ, mult, eHR in after
                  if not G.route_closed(RSZ, list(mult), eHR,
                                        2 * m - G.N58 * G.DEG)[0])
    n = len(gaps)
    print("   open configurations: %d;  |R| - q_1 runs %d .. %d"
          % (n, gaps[0], gaps[-1]))
    print("   %-6s %-12s %s" % ("k", "eliminated", "left open"))
    for k in (-2, 0, 2, 3, 5, 7, 8, 10, 12, 15):
        elim = sum(1 for g in gaps if g > k)
        print("   %-6d %-12d %d" % (k, elim, n - elim))
    print()
    advgap = ADV_R - max(ADV_BLOCKS)
    print("   THE CEILING ON THIS PROGRAMME.  adv58.py's admissible H has")
    print("   |R| - q_1 = %d, so no theorem q_1 >= |R| - k with k < %d follows"
          % (advgap, advgap))
    print("   from admissibility alone -- there is an admissible object that")
    print("   violates it.  At the best value that survives that object,")
    reach = sum(1 for g in gaps if g > advgap)
    print("   k = %d, the programme eliminates %d of the %d open configurations"
          % (advgap, reach, n))
    print("   and leaves %d.  That is the honest ceiling: the largest single"
          % (n - reach))
    print("   lever identified in this lane, and it is not a closure of order")
    print("   58 on its own.")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
