# bounds-registry: consumer
"""Cube-and-conquer for the handful of instances a flat solve cannot reach.

The f = 23, n = 36 sweep decided 3141 of 3146 catalogue pairs.  Five resisted a
100 s cap.  They are not a different mathematical problem -- their neighbours
in the same split solve in a tenth of a second -- they are simply instances
where the solver's heuristics do badly, and the standard remedy is to split
them.

This is the technique I certified for researcher-1 at passes 50-51, applied to
my own lane for the first time: choose k variables, enumerate all 2^k
assignments of them, and solve each restricted formula.  The pair is UNSAT
exactly when every cube is.  Exhaustiveness is not argued -- the 2^k cubes over
k fixed variables are all of them by construction, and `verify.py cover` can
check that independently if it is ever in doubt.

    python3 cube_hard.py [--k K] [--cap SECONDS] [--only I]
"""
import os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixmax as FM, orbit4_exact as X

F, N = 23, 36
HARD = [(11, 0, 2), (11, 9, 2), (10, 1, 0), (10, 63, 0), (10, 82, 0)]
W = os.path.join(FM.SCRATCH, "fixmax", "cube_hard")


def adaptive(a, ia, ib, cap, maxdepth, verbose=True):
    """Split only the cubes that resist.

    A uniform split is the wrong shape here: at depth 10 some cubes refute in a
    tenth of a second and others still time out, so a depth that clears the
    worst cube wastes most of its work on the easy ones.  Refine adaptively --
    solve, and on a timeout split that cube on one more variable and recurse.
    This is researcher-1's mixed-depth recipe, applied in my own lane.

    Exhaustiveness is structural: at every step a cube is replaced by its two
    children on one further variable, so the leaves partition the space.
    """
    b = F - a
    pre = FM.precompute(N, "C4", a, b)
    A = X.load35(a)[ia]
    B = X.complement(b, X.load35(b)[ib])
    r = FM.specialise(pre, FM.bits_of(A, a), FM.bits_of(B, b))
    if r is None:
        return "trivial", 0, 0, 0.0
    nv, cls = r
    freq = {}
    for c in cls:
        for lit in c:
            freq[abs(lit)] = freq.get(abs(lit), 0) + 1
    order = [v for v, _ in sorted(freq.items(), key=lambda t: -t[1])]
    os.makedirs(W, exist_ok=True)
    base = os.path.join(W, "adapt.cnf")
    # CaDiCaL requires the header clause count to be exact, so the body is
    # pre-formatted once into a single string and only the header and the unit
    # lines change per cube.  The cost of a cube was never the disk write, it
    # was re-formatting 139000 clauses in Python.
    body = "".join(" ".join(map(str, c)) + " 0\n" for c in cls)

    # RESUME, one level down.  The pair sweep is journalled because a session
    # ends mid-run; the cube tree needs the same treatment for the same reason,
    # and at ~4 s per leaf a tree that needs hundreds of leaves cannot finish
    # in one window.  Two kinds of entry:
    #   L <lits>   this cube was refuted, so its whole subtree is done
    #   C <lits>   this cube hit the cap, so skip the solve and split it
    # Replay is then almost free and each window extends the tree.
    jpath = os.path.join(W, f"tree_{a}_{ia}_{ib}.txt")
    refuted, capped = set(), set()
    if os.path.exists(jpath):
        with open(jpath) as fh:
            for line in fh:
                t = line.split()
                if len(t) >= 1 and t[0] in ("L", "C"):
                    key = tuple(int(x) for x in t[1:])
                    (refuted if t[0] == "L" else capped).add(key)
    jfh = open(jpath, "a")
    if verbose and (refuted or capped):
        print(f"        resuming: {len(refuted)} refuted leaves, "
              f"{len(capped)} nodes known to need splitting", flush=True)

    t0 = time.time()
    leaves = [len(refuted)]
    deepest = [max((len(k) for k in refuted), default=0)]

    def run(units):
        with open(base, "w") as fh:
            fh.write(f"p cnf {nv} {len(cls) + len(units)}\n")
            fh.write(body)
            fh.write("".join(f"{u} 0\n" for u in units))
        return subprocess.run(["timeout", str(cap), FM.CAD, "-q", base],
                              capture_output=True, text=True).returncode

    def rec(units, depth):
        key = tuple(units)
        # a refuted ancestor settles this whole subtree
        for i in range(len(key) + 1):
            if key[:i] in refuted:
                return "UNSAT"
        if key in capped:
            rc = 0                       # known to need splitting; do not solve
        else:
            rc = run(units)
        if rc == 10:
            return "SAT"
        if rc == 20:
            refuted.add(key)
            jfh.write("L " + " ".join(map(str, key)) + "\n")
            jfh.flush()
            leaves[0] += 1
            deepest[0] = max(deepest[0], depth)
            if verbose and leaves[0] % 25 == 0:
                print(f"        {leaves[0]} leaves refuted, deepest "
                      f"{deepest[0]}, {time.time()-t0:.0f}s", flush=True)
            return "UNSAT"
        if depth >= maxdepth:
            return "UNRESOLVED"
        if key not in capped:
            capped.add(key)
            jfh.write("C " + " ".join(map(str, key)) + "\n")
            jfh.flush()
        v = order[depth]
        for lit in (-v, v):
            out = rec(units + [lit], depth + 1)
            if out != "UNSAT":
                return out
        return "UNSAT"

    verdict = rec([], 0)
    jfh.close()
    return verdict, leaves[0], deepest[0], time.time() - t0


def solve_pair(a, ia, ib, k, cap, verbose=True):
    b = F - a
    pre = FM.precompute(N, "C4", a, b)
    A = X.load35(a)[ia]
    B = X.complement(b, X.load35(b)[ib])
    r = FM.specialise(pre, FM.bits_of(A, a), FM.bits_of(B, b))
    if r is None:
        return "trivial", 0, 0.0
    nv, cls = r
    os.makedirs(W, exist_ok=True)
    base = os.path.join(W, "base.cnf")
    # split on the k most frequently occurring variables
    freq = {}
    for c in cls:
        for lit in c:
            freq[abs(lit)] = freq.get(abs(lit), 0) + 1
    pick = [v for v, _ in sorted(freq.items(), key=lambda t: -t[1])[:k]]
    # Write the base ONCE and append only the k unit clauses per cube.  The
    # formula has ~139000 clauses; rewriting it 1024 times would cost far more
    # than the solving does.
    with open(base, "w") as fh:
        fh.write(f"p cnf {nv} {len(cls) + k}\n")
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")
    prefix = os.path.getsize(base)
    t0, done = time.time(), 0
    for mask in range(1 << k):
        units = [(v if (mask >> i) & 1 else -v) for i, v in enumerate(pick)]
        with open(base, "r+") as fh:
            fh.truncate(prefix)
            fh.seek(prefix)
            fh.write("".join(f"{u} 0\n" for u in units))
        rc = subprocess.run(["timeout", str(cap), FM.CAD, "-q", base],
                            capture_output=True, text=True).returncode
        if rc == 10:
            return "SAT", done, time.time() - t0
        if rc != 20:
            return f"CUBE-CAP at {mask}", done, time.time() - t0
        done += 1
    return "UNSAT", done, time.time() - t0


def main():
    args = sys.argv[1:]
    def opt(nm, d):
        return int(args[args.index(nm) + 1]) if nm in args else d
    k, cap = opt("--k", 6), opt("--cap", 20)
    only = opt("--only", -1)
    if "--adaptive" in args:
        md = opt("--maxdepth", 24)
        print(f"ADAPTIVE CUBE-AND-CONQUER, cap {cap} s, max depth {md}\n")
        print("   pair            verdict        leaves  deepest  seconds")
        for i, (a, ia, ib) in enumerate(HARD):
            if only >= 0 and i != only:
                continue
            v, lv, dp, el = adaptive(a, ia, ib, cap, md)
            print(f"   |A|={a} ({ia},{ib})   {v:13s} {lv:6d}  {dp:7d}  "
                  f"{el:7.1f}s", flush=True)
        return 0
    print(f"CUBE-AND-CONQUER on the {len(HARD)} instances a flat solve could "
          f"not reach\n   f = {F}, n = {N}, k = {k} split variables "
          f"({1<<k} cubes), {cap} s per cube\n")
    print("   pair            cubes refuted   verdict      seconds")
    for i, (a, ia, ib) in enumerate(HARD):
        if only >= 0 and i != only:
            continue
        v, done, el = solve_pair(a, ia, ib, k, cap)
        print(f"   |A|={a} ({ia},{ib})   {done:5d}/{1<<k}       {v:12s} "
              f"{el:7.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
