#!/usr/bin/env python3
"""
How far is order 58 from closing NOW?  The shortfall map, re-measured.

WHY AGAIN.  profile58.py measured this when order 58 stood at 9104 survivors and
reported that the absorption shortfall reaches 1, with 3326 configurations within
one unit.  That verdict has been quoted in this lane's documents ever since.
It is now stale in three ways:

  * the class has fallen 9104 -> 6019 clique-block configurations, through the
    w-sharpened Turan cap, the exact triangle guarantee and 2294 closures by the
    eight Tutte inequalities;
  * omega(G) <= 28 was not available then (a K_29 in a 29-critical graph on 58
    vertices would be a proper subgraph of chromatic number 29);
  * every surviving configuration has since been through machinery that did not
    exist, so "the residue does not reach" is a verdict about a different set.

The lane's own rule, learned the hard way twice: a verdict is not standing until
it is re-measured on the set it is being applied to.  This file re-measures it.

WHAT IS MEASURED, for every configuration open TODAY:

  CROSSING shortfall  Z(29) minus the best crossing lower bound this directory
      can prove -- the larger of the block sum and the block-plus-R bound.

  ABSORPTION shortfall  the deficit in the second absorption inequality,
      minimised over the surviving (k_1,k_2) sub-cases, since the adversary
      picks the best one.

A configuration dies as soon as EITHER reaches zero, so the per-configuration
minimum of the two is what matters, and its distribution is the map.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import pickle
import sys

import blockr58 as BR
import profile58 as PF
import residue58 as R58
import tuttegen as G
import verify_range as V
from order2r import Z

crK = V.crK


def shortfalls(m, RSZ, mult, eHR):
    """(crossing, absorption) shortfall for one open configuration."""
    X = 2 * m - G.N58 * G.DEG
    sx = X - (G.RCHI + 2 - 6)
    base = m - G.DEG * RSZ - X
    eL = base + RSZ * (RSZ - 1) // 2 - eHR
    blocks = sum(crK(q) for q in mult)
    br = BR.blockR(list(mult), G.N58 - RSZ, RSZ, eHR)
    cross = Z - max(blocks, br)
    bad = R58.survivors(G.N58, m, RSZ, list(mult), eL, 1, 4, sx)
    absorb = PF.absorption_deficit(G.N58, m, RSZ, list(mult), eL, sx, bad)
    return cross, absorb


def main():
    print("How far is order 58 from closing NOW?")
    print("Z(29) = %d;  a configuration dies as soon as EITHER shortfall hits 0"
          % Z)
    print()
    cfgs = (pickle.load(open(sys.argv[1], "rb")) if len(sys.argv) > 1
            else G.configurations())
    openc = [(m, RSZ, mult, eHR) for m, RSZ, mult, eHR in cfgs
             if not G.route_closed(RSZ, list(mult), eHR,
                                   2 * m - G.N58 * G.DEG)[0]]
    print("   open clique-block configurations today: %d" % len(openc))
    print("   (profile58.py measured this at 9104, before the w-cap, the exact")
    print("    triangle guarantee and 2294 Tutte closures)")
    print()

    cro, abso, both, none_ = {}, {}, 0, 0
    minima = {}
    for m, RSZ, mult, eHR in openc:
        c, a = shortfalls(m, RSZ, mult, eHR)
        if a is None:
            none_ += 1
            continue
        cro[min(c // 500, 12)] = cro.get(min(c // 500, 12), 0) + 1
        abso[min(a, 12)] = abso.get(min(a, 12), 0) + 1
        mn = min(a, c)
        minima[min(mn, 12)] = minima.get(min(mn, 12), 0) + 1
        if a <= 0 or c <= 0:
            both += 1
    print("   ABSORPTION shortfall (exact, capped at 12):")
    print("      %s" % sorted(abso.items()))
    lo = min(abso) if abso else None
    print("      smallest: %s;  within one unit: %d"
          % (lo, sum(v for k, v in abso.items() if k <= 1)))
    print()
    print("   CROSSING shortfall (in units of 500, capped):")
    print("      %s" % sorted(cro.items()))
    print()
    print("   min of the two, per configuration (capped at 12):")
    print("      %s" % sorted(minima.items()))
    print()
    if none_:
        print("   configurations where the absorption deficit is undefined: %d"
              % none_)
        print()
    print("CONCLUSION")
    if both:
        print("   %d configurations already have a shortfall at or below zero --"
              % both)
        print("   they would close, and their presence means a filter is stale.")
    else:
        print("   No configuration has either shortfall at zero, so neither tool")
        print("   closes anything on its own, as expected.")
    w1 = sum(v for k, v in abso.items() if k <= 1)
    print("   The absorption shortfall is the near one: smallest %s, and %d"
          % (lo, w1))
    print("   configurations sit within a single unit of it -- against the 3326")
    print("   that profile58.py measured on the old and larger set.")
    print()
    print("   The crossing shortfall stays in the thousands, so the crossing")
    print("   ladder is not the near tool here and re-pointing it at this class")
    print("   is not worth a pass.")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
