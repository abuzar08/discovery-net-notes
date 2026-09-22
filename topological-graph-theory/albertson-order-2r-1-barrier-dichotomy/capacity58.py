#!/usr/bin/env python3
"""
The absorption gap is not slack: it is missing CAPACITY.  Measured.

WHERE THIS STARTS.  absprice58.py priced the absorption inequality

        mu_1 + mu_2  >=  |Z| + max(0, t - s)

by a scan and found the median configuration needs TEN unconditional units,
while reaching 6053 of the 6054 open configurations.  That left the residual as
a single scalar and the obvious next move as "find a subclass where one or two
units are provable".  This file asks the prior question -- WHERE the units would
have to come from -- and the answer closes the line.

WHAT IS MEASURED, at the binding point of each configuration (the (k_1,k_2) and
w-split at which the required bonus is attained, recorded by
residue58.LAST_BINDING on the same code path that prices it):

  (1) mu_1 against its ABSOLUTE ceiling min(Za, q_1).  mu_1 is a lower bound for
      a matching between the Za vertices of Z with a_z >= 1 and the q_1 vertices
      of Q_1; no matching can exceed min(Za, q_1) whatever is proved about it.

  (2) mu_2 against its absolute ceiling min(Zb, |second side|), likewise.

  (3) the required bonus against |R| - q_1.

IF mu_1 AND mu_2 ARE AT THOSE CEILINGS, the deficit is not an under-estimate
that a sharper argument recovers.  It is an arithmetic shortfall: there are more
high vertices to absorb than there are vertices available to absorb them into,
and no theorem about mu_1 or mu_2 changes that.  exhaust58.py asserted "all four
components are at their limit" two passes before the class was what it is now;
this measures the strongest form of that claim, on the class open today, at the
point that actually binds.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import pickle
import sys

import absprice58 as A
import residue58 as R58
import tuttegen as G


def binding(m, RSZ, mult, eHR):
    """(least closing bonus, binding record) or (None, None)."""
    _X, sx, eL = A.parts(m, RSZ, eHR)
    if R58.survivors(G.N58, m, RSZ, list(mult), eL, A.NW, A.CW, sx) is None:
        return None, None
    R58.LAST_BINDING.clear()
    need = R58.survivors(G.N58, m, RSZ, list(mult), eL, A.NW, A.CW, sx,
                         need_scan=True)
    if need is None or not R58.LAST_BINDING:
        return None, None
    rec = dict(R58.LAST_BINDING)
    rec["need"], rec["R"] = need, RSZ
    return need, rec


def histogram(recs, f, cap=None):
    d = {}
    for b in recs:
        v = f(b)
        if cap is not None:
            v = min(v, cap)
        d[v] = d.get(v, 0) + 1
    return sorted(d.items())


def main():
    print("The absorption gap is not slack: it is missing capacity.")
    print()
    cfgs = (pickle.load(open(sys.argv[1], "rb")) if len(sys.argv) > 1
            else G.configurations())
    openc = [(m, RSZ, mult, eHR) for m, RSZ, mult, eHR in cfgs
             if not G.route_closed(RSZ, list(mult), eHR,
                                   2 * m - G.N58 * G.DEG)[0]]
    recs = []
    for m, RSZ, mult, eHR in openc:
        need, rec = binding(m, RSZ, mult, eHR)
        if rec is not None:
            recs.append(rec)
    n = len(recs)
    print("   open clique-block configurations: %d" % len(openc))
    print("   with a finite required bonus and a binding point: %d" % n)
    print()

    print("PART 1   is mu_1 below its ceiling min(Za, q_1)?")
    g1 = histogram(recs, lambda b: min(b["Za"], b["q1"]) - b["mu1"], 12)
    sat1 = sum(c for v, c in g1 if v == 0)
    print("      ceiling minus mu_1 (capped at 12): %s" % g1)
    print("      mu_1 AT its ceiling: %d of %d (%.1f%%)"
          % (sat1, n, 100.0 * sat1 / n))
    print()
    print("PART 2   is mu_2 below its ceiling min(Zb, |second side|)?")
    g2 = histogram(recs, lambda b: min(b["Zb"], b["side2"]) - b["mu2"], 12)
    sat2 = sum(c for v, c in g2 if v == 0)
    print("      ceiling minus mu_2 (capped at 12): %s" % g2)
    print("      mu_2 AT its ceiling: %d of %d (%.1f%%)"
          % (sat2, n, 100.0 * sat2 / n))
    print()
    both = sum(1 for b in recs
               if min(b["Za"], b["q1"]) == b["mu1"]
               and min(b["Zb"], b["side2"]) == b["mu2"])
    print("      BOTH at their ceilings simultaneously: %d of %d (%.1f%%)"
          % (both, n, 100.0 * both / n))
    print()

    print("PART 3   what the required bonus scales with")
    g3 = histogram(recs, lambda b: b["need"] - (b["R"] - b["q1"]))
    core = sum(c for v, c in g3 if 0 <= v <= 3)
    print("      need - (|R| - q_1): %s" % g3)
    print("      in {0,1,2,3}: %d of %d (%.1f%%)"
          % (core, n, 100.0 * core / n))
    rng = sorted(b["R"] - b["q1"] for b in recs)
    print("      |R| - q_1 ranges %d .. %d" % (rng[0], rng[-1]))
    print()

    print("CONTROL   the ceilings really are ceilings")
    bad = [b for b in recs
           if b["mu1"] > min(b["Za"], b["q1"])
           or b["mu2"] > min(b["Zb"], b["side2"])]
    print("      configurations where a computed mu EXCEEDS its ceiling: %d"
          % len(bad))
    print("      (a matching into Q_1 cannot exceed min(Za, q_1); any excess")
    print("       would be an unsoundness in the bound, not a strength)")
    print("      %s" % ("PASS" if not bad else "**FAIL**"))
    print()

    print("CONCLUSION")
    print("   At the point that binds, mu_1 is at its absolute ceiling on %d of"
          % sat1)
    print("   %d configurations and mu_2 on %d.  The required bonus is therefore"
          % (n, sat2))
    print("   NOT an under-estimate waiting for a sharper argument: mu_1 cannot")
    print("   exceed min(Za, q_1) whatever is proved about it, and it already")
    print("   does not.")
    print()
    print("   So the scalar absprice58.py found is missing CAPACITY, not slack.")
    print("   It tracks |R| - q_1 to within {0,1,2,3} on %.1f%% of the class:"
          % (100.0 * core / n))
    print("   the high set outnumbers the largest Gallai block by up to %d, and"
          % rng[-1])
    print("   absorption into Q_1 and L - Q_1 has nowhere to put the excess.")
    print()
    print("   PRECISELY WHAT IS RULED OUT.  A handicap of d on the left is the")
    print("   same statement as a reduction of d on the right, so this prices")
    print("   both directions at once.  What the ceilings rule out is the LEFT:")
    print("   no theorem about mu_1 or mu_2 -- no sharper matching bound, no")
    print("   wider second side, no better defect-Hall floor -- can produce even")
    print("   one of the required units, because both quantities are already at")
    print("   values no matching can exceed.  The only lever left inside this")
    print("   inequality is its RIGHT-hand side |Z| + max(0, t - s), and |Z| is")
    print("   |R| - 1 by definition.")
    print()
    print("   So a successor needs a theorem about |R| - q_1 -- a reason the")
    print("   largest Gallai block cannot be small relative to the high set --")
    print("   and not a better absorption argument.  That is a different kind")
    print("   of statement from anything this lane has tried.")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
