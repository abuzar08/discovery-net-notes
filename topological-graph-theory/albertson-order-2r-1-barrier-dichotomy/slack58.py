#!/usr/bin/env python3
"""
How strong would a sharpening have to be?  Priced, before anything is sharpened.

WHY.  tuttegen.py leaves configurations where a parameter point survives every
inequality.  The obvious next move is to sharpen one of them.  This lane has
guessed WHICH one wrong repeatedly -- the Hall sharpening of s changed nothing
at all, the widened second side closed none, the matroid intersection closed one
of 1843 -- so the target is priced first.

==============================================================================
WHAT IS MEASURED, AND A FRAMING THAT WAS WRONG.

The first version of this file measured, for each surviving parameter point, the
slack RHS_j - LHS_j of each inequality, and reported

        M_j  =  max over surviving points of that slack,

on the reasoning that improving inequality j by more than M_j removes every
surviving point.  That produced M_1 = 0 on every undecided configuration and the
conclusion "one unit off the count inequality closes all of them".

**That framing is misleading and is withdrawn.**  The count inequality is tight
at every surviving point *by construction*: the scan gives the adversary t at
the minimum inequality (1) allows, so (1) is always met with equality.  A slack
of zero there measures the scan's own search order, not the mathematics.  Two
genuine strengthenings of the component count -- the singleton refinement of
c_A, and the parity of the odd components -- were implemented on the strength of
that reading, and between them they moved the closure count by 12 and 0.

What is measured here instead is the honest question:

        subtract d from the RIGHT-HAND SIDE of inequality j, unconditionally,
        re-run the whole closure scan, and count what falls.

That prices a real theorem -- "inequality j holds with d to spare" -- rather than
a property of the enumeration.  It is slower, because the scan is re-run once
per (j, d), and it is the number worth quoting.

==============================================================================
AND A SECOND WRONG CONCLUSION, FROM THE SAME FILE (defect 20).

A price is only meaningful against the size of what it would buy, and that
denominator -- "configurations the route reaches at all" -- was computed here by
the SUPERSEDED knapsack bound kmax_guaranteed, applied to the RAW multiset,
while route_closed decides reach by the exact packing number on the TRUE block
multiset.  Weaker bound, understating reach; unlisted blocks (defect 19),
overstating it.  The two errors did not cancel: they produced 3712, which
coincided EXACTLY with the count inequality's d = 1 row, and the coincidence was
published as "one unconditional unit on the count inequality closes every
configuration the route reaches".

It does not.  With reach computed by the same guarantee route_closed uses, the
route reaches 4486 and one unit on the count inequality closes 3561 of them --
925 short.  NO inequality here is decisive at one unit.  The claim is withdrawn.

Exact integer arithmetic; no floating-point value enters any comparison.
"""

import pickle
import sys

import packing58 as PK
import tuttegen as G

NAMES = ("(1) count", "(2) degree", "(3) Turan", "(4) spread",
         "(5) S_R-degree")
DELTAS = (1, 5, 25, 50)


def closed(cfgs):
    return sum(1 for m, RSZ, mult, eHR in cfgs
               if G.route_closed(RSZ, list(mult), eHR,
                                 2 * m - G.N58 * G.DEG)[0])


def main():
    print("How strong would a sharpening have to be?  Priced by re-running the")
    print("closure scan with each inequality handicapped.")
    print()
    cfgs = (pickle.load(open(sys.argv[1], "rb")) if len(sys.argv) > 1
            else G.configurations())
    G.HANDICAP = [0] * 5
    base = closed(cfgs)
    print("   configurations scanned: %d" % len(cfgs))
    print("   closed with no handicap: %d" % base)
    print()
    print("   Configurations closed when inequality j holds with d to spare:")
    print()
    print("   %-16s %s" % ("inequality",
                           "  ".join("d=%-5d" % d for d in DELTAS)))
    rows = []
    for j, name in enumerate(NAMES):
        row = []
        for d in DELTAS:
            G.HANDICAP = [0] * 5
            G.HANDICAP[j] = d
            row.append(closed(cfgs))
        G.HANDICAP = [0] * 5
        rows.append(row)
        print("   %-16s %s" % (name, "  ".join("%-7d" % v for v in row)))
    print()
    # The reach of the route is decided by the SAME guarantee route_closed
    # uses -- the exact packing number on the TRUE block multiset.  This line
    # previously called the superseded knapsack bound kmax_guaranteed on the
    # raw multiset: weaker in one direction, and inflated by the unlisted
    # blocks of defect 19 in the other.  Two errors, not cancelling.
    total = base + sum(1 for m, RSZ, mult, eHR in cfgs
                       if not G.route_closed(RSZ, list(mult), eHR,
                                             2 * m - G.N58 * G.DEG)[0]
                       and PK.kmax_exact(
                           G.true_blocks(mult, RSZ, eHR,
                                         2 * m - G.N58 * G.DEG),
                           G.N58 - RSZ) >= 3)
    print("   configurations the route reaches at all: %d" % total)
    print()
    # Everything below is DERIVED from the table.  An earlier revision stated
    # the conclusions in prose, and they went stale the moment the inequalities
    # changed underneath them -- the same trap as defect 14.
    full = [NAMES[j] for j in range(5) if rows[j][0] >= total]
    inert = [NAMES[j] for j in range(5) if rows[j][-1] == base]
    order = sorted(range(5), key=lambda j: -rows[j][0])
    if full:
        print("   One unit is already decisive for: %s -- a single"
              % ", ".join(full))
        print("   unconditional unit there closes every configuration the")
        print("   route reaches.")
    else:
        # Print the ABSENCE as a measured statement, not as silence.  This
        # block used to fire, on a reach figure computed by the superseded
        # kmax_guaranteed on the raw multiset; it coincided exactly with the
        # count row, and the coincidence was published as a theorem
        # (defect 20).  With the reach computed by the same guarantee
        # route_closed uses, no inequality is decisive at one unit.
        best = max(range(5), key=lambda j: rows[j][0])
        print("   NO inequality is decisive at one unit.  The best is %s,"
              % NAMES[best])
        print("   closing %d of the %d the route reaches -- %d short."
              % (rows[best][0], total, total - rows[best][0]))
        print("   Even at d = 50 the best is %s, %d of %d."
              % (NAMES[max(range(5), key=lambda j: rows[j][-1])],
                 max(rows[j][-1] for j in range(5)), total))
    if inert:
        print("   Inert at every handicap tried: %s." % ", ".join(inert))
    print("   Ranked by yield at d = 1: %s"
          % ", ".join("%s %d" % (NAMES[j], rows[j][0]) for j in order))
    print()
    print("   Read the small numbers as a NEGATIVE result: an inequality whose")
    print("   d = 50 column is near the baseline will not be worth sharpening,")
    print("   however natural the sharpening looks.  Read the large ones as")
    print("   targets, and note that they move as the other inequalities move")
    print("   -- the spread inequality was inert on the six-inequality scan of")
    print("   the previous pass and is not inert here, so this table is only")
    print("   ever a statement about the current set.")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
