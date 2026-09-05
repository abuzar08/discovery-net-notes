"""Cube-and-conquer for one automorphism type, with per-cube LRAT.

Splits on variables 1..D (with the orbit numbering of encode.py these are the
lowest-indexed pair orbits, i.e. the internal orbits of the first cycle) and
refutes each of the 2^D cubes separately.  Soundness is trivial and needs no
extra lemma: every total assignment satisfies exactly one sign pattern on
those D variables, so if all 2^D cubes are unsatisfiable the base formula is.
verify.py's `cubes` subcommand re-checks that the stored cubes are exactly
all 2^D patterns, once each, and replays every one.

    python3 cubes.py N S T F P K D OUTDIR [JOBS] [TIMEOUT]
"""

import itertools
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import encode

CADICAL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "tools", "cadical", "build", "cadical")
DRATTRIM = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "tools", "drat-trim", "drat-trim")


def run_cube(args):
    outdir, nvar, base, cube, timeout = args
    tag = "c" + "".join("1" if x > 0 else "0" for x in cube)
    cnf = os.path.join(outdir, tag + ".cnf")
    drat = os.path.join(outdir, tag + ".drat")
    lrat = os.path.join(outdir, tag + ".lrat")
    if os.path.exists(lrat) and os.path.getsize(lrat) > 0:
        return tag, "cached", os.path.getsize(lrat)
    encode.write_dimacs(cnf, nvar, base + [[x] for x in cube])
    r = subprocess.run([CADICAL, "-q", "--binary=false", cnf, drat],
                       capture_output=True, timeout=timeout)
    if r.returncode != 20:
        for f in (drat,):
            if os.path.exists(f):
                os.remove(f)
        return tag, f"rc={r.returncode}", 0
    v = subprocess.run([DRATTRIM, cnf, drat, "-L", lrat],
                       capture_output=True, text=True)
    ok = "s VERIFIED" in v.stdout
    os.remove(drat)
    return tag, "VERIFIED" if ok else "drat-trim FAILED", \
        os.path.getsize(lrat) if os.path.exists(lrat) else 0


def main():
    n, s, t, f, p, k, D = (int(x) for x in sys.argv[1:8])
    outdir = sys.argv[8]
    jobs = int(sys.argv[9]) if len(sys.argv) > 9 else 3
    timeout = int(sys.argv[10]) if len(sys.argv) > 10 else 3600
    os.makedirs(outdir, exist_ok=True)
    nvar, base = encode.build(n, s, t, f, p, k)
    base = [list(c) for c in base]
    print(f"n={n} type 1^{f} {p}^{k}: vars={nvar} clauses={len(base)}; "
          f"splitting on 1..{D} -> {2**D} cubes", flush=True)
    cubes = [tuple((i + 1) if b else -(i + 1) for i, b in enumerate(sg))
             for sg in itertools.product((True, False), repeat=D)]
    tasks = [(outdir, nvar, base, c, timeout) for c in cubes]
    bad, total = [], 0
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for i, (tag, status, sz) in enumerate(ex.map(run_cube, tasks), 1):
            total += sz
            if status not in ("VERIFIED", "cached"):
                bad.append((tag, status))
            if i % 8 == 0 or status not in ("VERIFIED", "cached"):
                print(f"  {i}/{len(cubes)} {tag} {status} "
                      f"({sz/1024:.0f} KB)", flush=True)
    print(f"done: {len(cubes) - len(bad)}/{len(cubes)} cubes refuted and "
          f"drat-trim VERIFIED, total LRAT {total/1048576:.1f} MB")
    for tag, st in bad:
        print("  UNRESOLVED", tag, st)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
