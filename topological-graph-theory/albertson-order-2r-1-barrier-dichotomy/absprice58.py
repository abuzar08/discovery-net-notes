#!/usr/bin/env python3
"""
What would the absorption inequality actually BUY?  Priced by a scan.

WHY THIS FILE EXISTS.  After defect 20 the absorption inequality

        mu_1 + mu_2  >=  |Z| + max(0, t - s)

is the last target standing in this lane, and the number attached to it is
"one unconditional unit closes 3196 of the 6054".  That number is a HISTOGRAM,
not a scan: shortfall58.py reports, per configuration, the least

        (|Z| + max(0,t-s)) - (mu_1 + mu_2)

over the surviving (k_1,k_2) sub-cases, and counts how many configurations have
that least value equal to 1.

Defect 20 was exactly this shape -- a number that looked like a price and was
not one -- so before another pass is spent on this inequality the price is
measured the way slack58.py measures the Tutte ones: give the inequality d more
units UNCONDITIONALLY, re-run the decision, and count what falls.

TWO REASONS THE HISTOGRAM CAN OVERSTATE, both structural:

  (a) it is a MINIMUM over surviving sub-cases.  A configuration is closed only
      when EVERY surviving (k_1,k_2) dies.  Killing the cheapest one leaves the
      rest, so "deficit 1" means "one unit kills the easiest sub-case", not
      "one unit closes the configuration".

  (b) the absorption inequality is one of THREE conjuncts.  A sub-case survives
      if any of Za >= t, mu_1 >= t, or the absorption inequality fails.  A
      sub-case escaping through the first two is untouchable by ANY absorption
      bonus, however large.

WHAT IS MEASURED.  residue58.survivors gains a need_scan mode that walks the
same code path and returns the LEAST unconditional bonus closing the
configuration -- 0 if already closed, None if no bonus ever closes it.  One code
path, so the price cannot drift from the thing priced.  The scan is then exact
at every d at once, and the control below re-derives four rows of it the slow
way, by setting residue58.ABS_HANDICAP and re-running the real decision.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import pickle
import sys

import profile58 as PF
import residue58 as R58
import tuttegen as G

DELTAS = (1, 2, 3, 5, 8, 10, 11, 12, 13, 15, 20, 25, 100)
NW, CW = 1, 4


def parts(m, RSZ, eHR):
    X = 2 * m - G.N58 * G.DEG
    sx = X - (G.RCHI + 2 - 6)
    base = m - G.DEG * RSZ - X
    eL = base + RSZ * (RSZ - 1) // 2 - eHR
    return X, sx, eL


def price(m, RSZ, mult, eHR):
    """(least closing bonus or None, histogram deficit or None)."""
    X, sx, eL = parts(m, RSZ, eHR)
    bad = R58.survivors(G.N58, m, RSZ, list(mult), eL, NW, CW, sx)
    if bad is None:
        return "inadmissible", None
    need = R58.survivors(G.N58, m, RSZ, list(mult), eL, NW, CW, sx,
                         need_scan=True)
    hist = PF.absorption_deficit(G.N58, m, RSZ, list(mult), eL, sx, bad)
    return need, hist


def control(openc, rows):
    """Re-derive four rows of the scan the slow way, through the real decision.

    Sets residue58.ABS_HANDICAP and re-runs survivors itself, counting the
    configurations whose survivor list becomes empty.  If the fast scan and the
    real decision ever disagree the price is not a price."""
    print("CONTROL   the same four rows, re-derived through the real decision")
    ok = True
    for d in (1, 2, 5, 25):
        R58.ABS_HANDICAP = d
        got = 0
        for m, RSZ, mult, eHR in openc:
            X, sx, eL = parts(m, RSZ, eHR)
            bad = R58.survivors(G.N58, m, RSZ, list(mult), eL, NW, CW, sx)
            if bad is not None and not bad:
                got += 1
        R58.ABS_HANDICAP = 0
        want = rows[d]
        print("   d = %-4d scan says %-6d re-run says %-6d  %s"
              % (d, want, got, "PASS" if got == want else "**MISMATCH**"))
        ok = ok and got == want
    return ok


def main():
    print("What would the absorption inequality buy?  Priced by a scan.")
    print()
    cfgs = (pickle.load(open(sys.argv[1], "rb")) if len(sys.argv) > 1
            else G.configurations())
    openc = [(m, RSZ, mult, eHR) for m, RSZ, mult, eHR in cfgs
             if not G.route_closed(RSZ, list(mult), eHR,
                                   2 * m - G.N58 * G.DEG)[0]]
    print("   open clique-block configurations: %d" % len(openc))
    print()

    needs, hists, bad_input = [], [], 0
    for m, RSZ, mult, eHR in openc:
        need, hist = price(m, RSZ, mult, eHR)
        if need == "inadmissible":
            bad_input += 1
            continue
        needs.append(need)
        hists.append(hist)
    finite = [n for n in needs if n is not None]
    print("   configurations NO absorption bonus ever closes: %d of %d"
          % (len(needs) - len(finite), len(needs)))
    if bad_input:
        print("   inadmissible under the residue (excluded): %d" % bad_input)
    print()

    rows = {}
    print("   %-8s %-12s %-12s %s" % ("d", "scan", "histogram", "histogram"))
    print("   %-8s %-12s %-12s %s" % ("", "closes", "predicts", "overstates by"))
    for d in DELTAS:
        got = sum(1 for n in finite if n <= d)
        pred = sum(1 for h in hists if h is not None and h <= d)
        rows[d] = got
        print("   %-8d %-12d %-12d %d" % (d, got, pred, pred - got))
    print()
    print("   least bonus that closes anything: %s"
          % (min(finite) if finite else "none at any d"))
    hist_d = {}
    for n in finite:
        k = min(n, 20)
        hist_d[k] = hist_d.get(k, 0) + 1
    print("   distribution of the least closing bonus (capped at 20): %s"
          % sorted(hist_d.items()))
    srt = sorted(finite)
    print("   median least closing bonus: %d;  largest: %d"
          % (srt[len(srt) // 2], srt[-1]))
    print()
    ok = control(openc, rows)
    print()
    print("CONCLUSION")
    one = rows[1]
    hist1 = sum(1 for h in hists if h is not None and h <= 1)
    if one == 0:
        print("   One unconditional unit on the absorption inequality closes")
        print("   NOTHING.  The histogram figure of %d is not a price: it is" % hist1)
        print("   the count of configurations whose CHEAPEST surviving sub-case")
        print("   is one unit short, and closing a configuration needs EVERY")
        print("   surviving sub-case to die.")
    else:
        print("   One unconditional unit closes %d, against the %d the histogram"
              % (one, hist1))
        print("   predicts -- an overstatement of %d." % (hist1 - one))
    inf = len(needs) - len(finite)
    print("   But the REACH is the other half of the story, and it is the")
    print("   opposite of the count inequality's.  Exactly %d configuration%s"
          % (inf, "" if inf == 1 else "s") + " of the %d" % len(needs))
    print("   escape%s through Za >= t or mu_1 >= t, which no absorption bonus"
          % ("s" if inf == 1 else ""))
    print("   of any size touches; a large enough bonus closes ALL THE REST --")
    print("   %d of %d, including configurations outside the clique-cover"
          % (len(finite), len(needs)))
    print("   route entirely.  The count inequality, by contrast, is stuck at")
    print("   3561 of 4486 at every handicap tried (slack58.py).")
    print("   So the absorption inequality does not lack REACH, it lacks")
    print("   MAGNITUDE: the median configuration needs %d units, not one."
          % srt[len(srt) // 2])
    print("   Control: %s." % ("PASS" if ok else "**MISMATCH**"))
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
