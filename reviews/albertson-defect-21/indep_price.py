"""Independent re-derivation of the defect-21 price table.

The contribution prices the absorption inequality with a new `need_scan` mode
inside `residue58.survivors`, and controls it at four values of d by setting
`residue58.ABS_HANDICAP` and re-running the real decision.  This script does
that slow re-derivation at EVERY d instead of four: for each open
configuration it finds the least handicap that empties the survivor list, by
bisection on the real decision, and reports the whole distribution.

`need_scan` is never used here.  Monotonicity, which bisection needs, holds by
inspection: ABS_HANDICAP enters only the conjunct
`mu1 + mu2 + ABS_HANDICAP >= need`, and none of mu1, mu2, need, Za, t depends
on it, so raising d can only turn escaping splits into killed ones.  It is also
checked directly below on a sample.
"""
import random
import sys

import residue58 as R58
import tuttegen as G

NW, CW = 1, 4
PROBE = 1000          # a configuration not closed at this d is called unreachable


def parts(m, RSZ, eHR):
    X = 2 * m - G.N58 * G.DEG
    sx = X - (G.RCHI + 2 - 6)
    base = m - G.DEG * RSZ - X
    eL = base + RSZ * (RSZ - 1) // 2 - eHR
    return X, sx, eL


def closed_at(cfg, d):
    m, RSZ, mult, eHR = cfg
    X, sx, eL = parts(m, RSZ, eHR)
    R58.ABS_HANDICAP = d
    try:
        bad = R58.survivors(G.N58, m, RSZ, list(mult), eL, NW, CW, sx)
    finally:
        R58.ABS_HANDICAP = 0
    return None if bad is None else not bad


def least_bonus(cfg):
    """Least d with the configuration closed, None if not closed at PROBE."""
    if closed_at(cfg, 0):
        return 0
    if not closed_at(cfg, PROBE):
        return None
    lo, hi = 1, PROBE                      # not closed at lo-1, closed at hi
    while lo < hi:
        mid = (lo + hi) // 2
        if closed_at(cfg, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def main():
    cfgs = G.configurations()
    openc = [c for c in cfgs
             if not G.route_closed(c[1], list(c[2]), c[3],
                                   2 * c[0] - G.N58 * G.DEG)[0]]
    adm = [c for c in openc if closed_at(c, 0) is not None]
    print("open clique-block configurations: %d" % len(openc))
    print("admissible under the residue:     %d" % len(adm))

    print()
    print("monotonicity of closure in d, direct check on a sample")
    random.seed(29)
    bad_mono = 0
    for cfg in random.sample(adm, 300):
        seq = [closed_at(cfg, d) for d in range(0, 31)]
        if any(seq[i] and not seq[i + 1] for i in range(30)):
            bad_mono += 1
    print("   configurations sampled: 300;  non-monotone: %d" % bad_mono)

    print()
    least = {}
    for cfg in adm:
        least[cfg] = least_bonus(cfg)
    finite = sorted(v for v in least.values() if v is not None)
    print("never closed at any bonus (d = %d probe): %d"
          % (PROBE, len(adm) - len(finite)))
    for cfg, v in least.items():
        if v is None:
            print("   the unreachable configuration: m=%d |R|=%d mult=%s eHR=%d"
                  % (cfg[0], cfg[1], list(cfg[2]), cfg[3]))
    print()
    print("   %-6s %s" % ("d", "closed by bisection on the real decision"))
    for d in (1, 2, 3, 5, 8, 10, 11, 12, 13, 15, 20, 21, 25, 100):
        print("   %-6d %d" % (d, sum(1 for v in finite if v <= d)))
    print()
    print("   least: %d  median: %d  largest: %d"
          % (finite[0], finite[len(finite) // 2], finite[-1]))
    hist = {}
    for v in finite:
        hist[v] = hist.get(v, 0) + 1
    print("   full distribution: %s" % sorted(hist.items()))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
