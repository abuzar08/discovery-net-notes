"""Does one scalar really describe both halves of the order-58 residual?

Defect 21 concludes that the residual "is not two halves" -- the 2227 the
clique-cover route reaches and the 3827 it does not -- because the absorption
inequality reaches 6053 of the 6054 open configurations.  Reach is not the
only dimension the contribution itself cares about: it argues the inequality
lacks MAGNITUDE.  So the question this script asks is whether the magnitude
needed is the same on both halves, or whether the old split survives as a
difference in price.

Least closing bonus is taken from residue58's scan (verified independently by
bisection on the real decision in indep_price.py); the split is taken from
tuttegen.route_closed's own reason string.
"""
import sys

import residue58 as R58
import tuttegen as G

NW, CW = 1, 4


def parts(m, RSZ, eHR):
    X = 2 * m - G.N58 * G.DEG
    sx = X - (G.RCHI + 2 - 6)
    base = m - G.DEG * RSZ - X
    eL = base + RSZ * (RSZ - 1) // 2 - eHR
    return X, sx, eL


def stats(vals):
    fin = sorted(v for v in vals if v is not None)
    inf = len(vals) - len(fin)
    if not fin:
        return "none finite, %d unreachable" % inf
    return ("n = %d  median %d  mean %.2f  max %d  closed at d=1: %d  "
            "unreachable %d"
            % (len(vals), fin[len(fin) // 2], sum(fin) / len(fin), fin[-1],
               sum(1 for v in fin if v <= 1), inf))


def main():
    groups = {}
    for m, RSZ, mult, eHR in G.configurations():
        X, sx, eL = parts(m, RSZ, eHR)
        closed, reason = G.route_closed(RSZ, list(mult), eHR, X)
        if closed:
            continue
        need = R58.survivors(G.N58, m, RSZ, list(mult), eL, NW, CW, sx,
                             need_scan=True)
        key = ("reached by the route, point survives"
               if reason == "a parameter point survives" else
               "out of the route's scope: %s" % reason)
        groups.setdefault(key, []).append((need, (m, RSZ, tuple(mult), eHR)))

    total = sum(len(v) for v in groups.values())
    print("open configurations: %d" % total)
    print()
    for key in sorted(groups):
        vals = [n for n, _ in groups[key]]
        print("%-46s %s" % (key, stats(vals)))
        for n, cfg in groups[key]:
            if n is None:
                print("   unreachable configuration: m=%d |R|=%d mult=%s eHR=%d"
                      % (cfg[0], cfg[1], list(cfg[2]), cfg[3]))
    print()
    print("per-half distribution of the least closing bonus")
    for key in sorted(groups):
        h = {}
        for n, _ in groups[key]:
            if n is not None:
                h[n] = h.get(n, 0) + 1
        print("   %-46s %s" % (key, sorted(h.items())))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
