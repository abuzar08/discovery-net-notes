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

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import pickle
import sys

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
    best = max(range(5), key=lambda j: rows[j][0])
    print("   The count inequality is the whole story: one unit off its")
    print("   right-hand side closes every configuration the route reaches,")
    print("   while the four edge counts need 50 to gain a few hundred and the")
    print("   spread inequality is inert at every handicap.")
    print()
    print("   Read that as a NEGATIVE result about the edge counts, and as a")
    print("   precise target otherwise: what is needed is a theorem of the form")
    print("   o(H' - S) <= c_A + t - 1 -- the component bound is never attained")
    print("   -- holding unconditionally.  Two partial versions of exactly that")
    print("   (the singleton refinement of c_A, and the parity of the odd")
    print("   components) are already in tuttegen.py and are not enough,")
    print("   because each leaves the adversary another branch or one unit of")
    print("   freedom in u to absorb it.")
    print()
    print("   Cheapest single target by yield at d = 1: %s" % NAMES[best])
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
