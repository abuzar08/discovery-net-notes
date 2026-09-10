"""The stale-input index applied to McKay-Radziszowski, R(4,5) = 25 (JGT 19, 1995).

This is the foundation of the whole R(5,5) chain: it is what fixes the degree
window n - 25 <= d(v) <= 24 in every R(5,5) upper-bound argument, mine and
researcher-1's included.  So it is the right place for the index to point after
the chain above it was swept (see ../method-notes/STALE-INPUT-INDEX.md).

WHAT THE PAPER SAYS ABOUT ITS OWN INPUTS, section 6:

  "In Table 3, the values are exact for n <= 11 and are estimates based on our
   random sampling for 12 <= n <= 22. ... The value for n = 23 is a barely more
   than a guess.  We expect that the correct value for n = 24 is at most a few
   hundred beyond the number given."

  "Also in Table 3 we record our current best bounds on e(4,5,n) and E(4,5,n)
   ... The exact values were found by direct computation.  The upper bounds on
   e(4,5,n) and the lower bounds on E(4,5,n) were proved by constructing
   examples.  Otherwise, the bounds are derived from linear programming."

So each range [a,b] on e has b CONSTRUCTED and a from LP; each range [c,d] on E
has c CONSTRUCTED and d from LP.  All of it is now settled by data that arrived
later, and this file checks every entry.

    python3 mr45table3.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Table 3 as printed, for the orders where it gives a range or a lower bound.
# n -> (e range, E range)
TABLE3 = {
    18: ((48, 50), (85, 88)),
    19: ((56, 57), (92, 97)),
    20: ((66, 68), (100, 105)),
    21: ((75, 77), (107, 114)),
    22: ((86, 88), (114, 122)),
    23: ((98, 102), (121, 130)),
    24: ((109, 116), (132, 132)),
}
COUNT24_1995 = 350904          # "|R(4,5,24)| >= 350904"
COUNT24_TRUE = 352366          # Angeltveit-McKay 2016
TOTAL_1995 = 2.91e19           # their "all" row
TOTAL_2026 = 2.93e19           # Angeltveit-McKay, R(5,5) <= 46, appendix


def main():
    with open(os.path.join(HERE, "e45.json")) as fh:
        d = json.load(fh)
    emin = {int(k): v for k, v in d["emin"].items()}
    emax = {int(k): v for k, v in d["emax"].items()}

    print("(1) the count at n = 24, and the expectation attached to it\n")
    gap = COUNT24_TRUE - COUNT24_1995
    print(f"    1995: |R(4,5,24)| >= {COUNT24_1995}, and 'we expect that the "
          f"correct value")
    print("          for n = 24 is at most A FEW HUNDRED beyond the number "
          "given'")
    print(f"    true: {COUNT24_TRUE} (Angeltveit-McKay 2016)")
    print(f"    shortfall: {gap}")
    if gap > 999:
        print(f"    -> the expectation is WRONG.  {gap} is not 'a few hundred' "
              f"on any reading;")
        print(f"       it is roughly {gap // 300}x that.  An informal "
              f"expectation, not a conjecture,")
        print("       so this is a smaller object than the R(4,6) refutation "
              "-- but it was")
        print("       quantitative enough to be checkable, and it does not "
              "hold.")
    else:
        print("    -> within 'a few hundred'; the expectation holds.")

    print(f"\n    Their sampling held up elsewhere: total estimate "
          f"{TOTAL_1995:.2e} against {TOTAL_2026:.2e}")
    print("    in the 2026 appendix -- the method was sound, the n = 24 "
          "extrapolation was not.")

    print("\n(2) every range in Table 3, against the exact values\n")
    print("      n   e: 1995 [LP, constructed]  exact   verdict"
          "        E: 1995 [constructed, LP]  exact   verdict")
    bad = []
    subopt = []
    for n in sorted(TABLE3):
        (ea, eb), (Ec, Ed) = TABLE3[n]
        te, tE = emin[n], emax[n]
        ok_e = ea <= te <= eb
        ok_E = Ec <= tE <= Ed
        if not ok_e or not ok_E:
            bad.append(n)
        # the constructed end is eb for e (an upper bound on the minimum)
        # and Ec for E (a lower bound on the maximum)
        se = eb - te          # >0 means their example was not extremal
        sE = tE - Ec
        if se or sE:
            subopt.append((n, se, sE))
        print(f"    {n:3d}   [{ea:4d}, {eb:4d}]{'':12s}{te:5d}   "
              f"{'in' if ok_e else 'OUT':7s}"
              f"     [{Ec:4d}, {Ed:4d}]{'':10s}{tE:5d}   "
              f"{'in' if ok_E else 'OUT'}")
    if bad:
        raise SystemExit(f"Table 3 ranges do not contain the true value at "
                         f"n = {bad} -- one of the two is wrong")
    print("\n    Every 1995 range contains the true value: a clean "
          "consistency check on their LP,")
    print("    and all fourteen ranges now collapse to a point.")

    print("\n(3) where their constructed examples were not extremal\n")
    if not subopt:
        print("    nowhere -- every construction was optimal.")
    else:
        for n, se, sE in subopt:
            parts = []
            if se:
                parts.append(f"e: constructed {TABLE3[n][0][1]}, true {emin[n]}"
                             f" (short by {se})")
            if sE:
                parts.append(f"E: constructed {TABLE3[n][1][0]}, true "
                             f"{emax[n]} (short by {sE})")
            print(f"    n = {n}: " + "; ".join(parts))
        ns = sorted({n for n, _, _ in subopt})
        print(f"\n    Only n = {ns}.  At every other order in the table their "
              f"examples were extremal,")
        print("    on both the minimum and the maximum.  That is a strong "
              "record for hand-built")
        print("    constructions, and it isolates the one order where a better "
              "example existed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
