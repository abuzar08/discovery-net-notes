"""Transfer test: the same question, applied to R(4,6) instead of R(5,5).

principal-1, pass 33: *"apply the same question to the papers that bound R(4,6)
and the other lanes' problems, not only R(5,5): the method is not specific to
your seat, and if it transfers you should say so rather than keep it."*

THE QUESTION.  What did the step need, and has a later catalogue, table or
theorem since made that input available?

McKay and Radziszowski (JCTB 69, 1997) prove R(4,6) <= 41 by showing LP(4,6,41)
infeasible.  Section 5 is explicit that its inputs were limited by what was not
yet known:

  "the values e'_2, e''_2, t' and t'' depend on the (4,5,23)-graphs and
   (4,5,24)-graphs, of which our knowledge is incomplete"

and it states, in the same section, a sufficient condition for the next bound:

  "the result R(4,6) <= 40 would follow if it was known that (4,5,22)-,
   (4,5,23)- and (4,5,24)-graphs had at least 93, 105 and 113 edges,
   respectively.  These bounds are quite likely to hold, but we have not
   proved them."

Those are lower bounds on e over EVERY (4,5,i)-graph -- their e'_2(i) inputs.
The complete (4,5,24) catalogue (Angeltveit-McKay 2016) and McKay's extreme-
edge-count files settle all three.  This file does that, and also compares
their Table IV triangle bounds at n = 24 against the exact values computed
here from the complete catalogue.

    python3 mr46transfer.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# The conjecture of Section 5: every (4,5,i)-graph has at least this many edges.
HOPED = {22: 93, 23: 105, 24: 113}

# What LP(4,5,i) gave them in 1995, from the same section.
THEIRS = {23: (98, 130), 24: (109, 132)}

# Table IV, n = 24 column: e -> (t_min, t_max) as printed.
TABLE_IV_24 = {
    109: (112, 112), 110: (111, 117), 111: (110, 121), 112: (110, 125),
    113: (109, 128), 114: (108, 131), 115: (108, 135), 116: (107, 138),
    117: (107, 142), 118: (109, 145), 119: (112, 148), 120: (114, 151),
    121: (117, 154), 122: (119, 156), 123: (122, 159), 124: (125, 162),
    125: (127, 165), 126: (130, 168), 127: (133, 169), 128: (135, 170),
    129: (138, 172), 130: (142, 173), 131: (146, 174), 132: (176, 176),
}


def main():
    with open(os.path.join(HERE, "e45.json")) as fh:
        d = json.load(fh)
    emin = {int(k): v for k, v in d["emin"].items()}
    emax = {int(k): v for k, v in d["emax"].items()}

    print("(1) the sufficient condition McKay and Radziszowski state for "
          "R(4,6) <= 40")
    print("    'every (4,5,i)-graph has at least H(i) edges', which they call "
          "'quite likely to hold'\n")
    print("     i    hoped H(i)    true e_min(4,5,i)    verdict")
    refuted = []
    for i in sorted(HOPED):
        h, t = HOPED[i], emin[i]
        ok = t >= h
        if not ok:
            refuted.append(i)
        print(f"    {i:2d}    {h:9d}    {t:16d}    "
              f"{'holds' if ok else 'FALSE, by ' + str(h - t)}")
    print()
    if refuted:
        print(f"    REFUTED at i = {refuted}.  There are (4,5,{refuted[0]})-"
              f"graphs with only {emin[refuted[0]]} edges,")
        print("    so the condition is false and this route to R(4,6) <= 40 "
              "is closed.")
        print("    (The bound R(4,6) <= 41 is unaffected -- it does not use "
              "the condition -- and")
        print("     R(4,6) <= 40 was later obtained by other means, "
              "Angeltveit and McKay.)")
    else:
        print("    All three hold; the stated route to R(4,6) <= 40 is open.")

    print("\n(2) their LP-derived e-bounds against the now-exact values")
    print("     i    their [e'_2, e''_2]    exact [e_min, e_max]    sharpened by")
    for i in sorted(THEIRS):
        a, b = THEIRS[i]
        print(f"    {i:2d}    [{a:3d}, {b:3d}]            "
              f"[{emin[i]:3d}, {emax[i]:3d}]            "
              f"lower +{emin[i] - a}, upper -{b - emax[i]}")

    print("\n(3) their Table IV triangle bounds at n = 24 against the exact "
          "values")
    tpath = os.path.join(HERE, "t45_24.json")
    with open(tpath) as fh:
        exact = {int(k): v for k, v in json.load(fh).items()}
    print("      e    Table IV [t',t'']    exact [t_min,t_max]    status")
    vacuous, sharper = [], 0
    for e in sorted(TABLE_IV_24):
        a, b = TABLE_IV_24[e]
        if e not in exact:
            vacuous.append(e)
            print(f"    {e:3d}    [{a:3d}, {b:3d}]           "
                  f"      --  EMPTY  --     no such graph exists")
            continue
        tmin, tmax = exact[e][0], exact[e][1]
        if tmin < a or tmax > b:
            raise SystemExit(f"e={e}: exact [{tmin},{tmax}] escapes their "
                             f"[{a},{b}] -- one of the two is wrong")
        sharper += 1
        print(f"    {e:3d}    [{a:3d}, {b:3d}]            [{tmin:3d}, {tmax:3d}]"
              f"            +{tmin - a} / -{b - tmax}")
    print(f"\n    every exact range lies inside theirs -- {sharper} rows "
          f"sharpened, none contradicted,")
    print(f"    and {len(vacuous)} rows are vacuous: e = {vacuous} is below "
          f"e_min(4,5,24) = {emin[24]},")
    print("    so no graph has those edge counts at all.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
