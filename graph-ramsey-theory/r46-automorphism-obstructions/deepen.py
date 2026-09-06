"""Adaptive second-level cube split: deepen only the cubes that did not close.

`cubes.py` splits on variables 1..D and refutes each of the 2^D cubes.  On
hard instances a fraction of those cubes survives the per-cube timeout.  This
file takes such a directory, finds the survivors, and splits each of them
further on variables D+1..D+E, refuting the 2^E children separately.

SOUNDNESS needs no new lemma, exactly as for `cubes.py`.  The 2^D cubes
partition the space of total assignments (every assignment satisfies exactly
one sign pattern on variables 1..D), and the 2^E children of a cube partition
that cube the same way.  So

    {solved D-cubes}  union  {all 2^E children of each unsolved D-cube}

is again a partition of the whole space, and refuting every leaf refutes the
formula.  Leaves live at two different depths; that is fine, because what the
argument needs is a partition, not a uniform depth.

Iterating this is still a partition: replacing any leaf by all 2^E of its
children keeps one.  `verify.py tree` checks the property directly and at any
depth -- the leaf tags must be prefix-free with Kraft sum exactly 1 -- and
replays every leaf, so the depths never have to be declared to it.

    python3 deepen.py N S T F P K D OLDDIR E NEWDIR [JOBS] [TIMEOUT] [flags]

Flags: --limit=N (first N parents only), --parents=FILE (split exactly the
tags listed in FILE, whose lengths need not be D; used for third and later
levels).
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


def unsolved(olddir, D):
    """D-cube tags with no non-empty LRAT in olddir."""
    done = set()
    if os.path.isdir(olddir):
        for f in os.listdir(olddir):
            if f.endswith(".done"):
                done.add(f[1:-5])
            elif f.endswith(".lrat") and os.path.getsize(os.path.join(olddir, f)) > 0:
                done.add(f[1:-5])
    return [t for t in ("".join(x) for x in itertools.product("01", repeat=D))
            if t not in done]


def run_leaf(args):
    newdir, nvar, base, tag, lits, timeout = args
    cnf = os.path.join(newdir, "c" + tag + ".cnf")
    drat = os.path.join(newdir, "c" + tag + ".drat")
    lrat = os.path.join(newdir, "c" + tag + ".lrat")
    if os.path.exists(os.path.join(newdir, "c" + tag + ".done")):
        for f in (cnf, drat, lrat):
            if os.path.exists(f):
                os.remove(f)
        return tag, "cached", 0
    if os.path.exists(lrat) and os.path.getsize(lrat) > 0:
        for f in (cnf, drat):
            if os.path.exists(f):
                os.remove(f)
        return tag, "cached", os.path.getsize(lrat)
    encode.write_dimacs(cnf, nvar, base + [[x] for x in lits])
    try:
        r = subprocess.run([CADICAL, "-q", "--binary=false", cnf, drat],
                           capture_output=True, timeout=timeout)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    if rc != 20:
        for f in (cnf, drat):
            if os.path.exists(f):
                os.remove(f)
        return tag, f"rc={rc}", 0
    v = subprocess.run([DRATTRIM, cnf, drat, "-L", lrat],
                       capture_output=True, text=True)
    ok = "s VERIFIED" in v.stdout
    if not ok:                      # transient under load; see cubes.py
        v = subprocess.run([DRATTRIM, cnf, drat, "-L", lrat],
                           capture_output=True, text=True)
        ok = "s VERIFIED" in v.stdout
    for f in (cnf, drat):
        if os.path.exists(f):
            os.remove(f)
    if not ok:
        if os.path.exists(lrat):
            os.remove(lrat)
        return tag, "drat-trim FAILED", 0
    return tag, "VERIFIED", os.path.getsize(lrat)


def main():
    n, s, t, f, p, k, D = (int(x) for x in sys.argv[1:8])
    olddir = sys.argv[8]
    E = int(sys.argv[9])
    newdir = sys.argv[10]
    jobs = int(sys.argv[11]) if len(sys.argv) > 11 else 4
    timeout = int(sys.argv[12]) if len(sys.argv) > 12 else 400
    flags = sys.argv[13:]
    limit = 0
    parents_file = None
    for a in list(flags):
        if a.startswith("--limit="):
            limit = int(a.split("=")[1])
            flags.remove(a)
        elif a.startswith("--parents="):
            parents_file = a.split("=", 1)[1]
            flags.remove(a)

    nvar, base = encode.build(n, s, t, f, p, k,
                              symf="--symf" in flags,
                              symc="--symc" in flags,
                              syms="--syms" in flags,
                              symkg="--symkg" in flags)
    if parents_file:
        # Third and later levels: split an explicit list of surviving tags,
        # whose length need not be D.  The partition argument is unchanged --
        # replacing any leaf by all 2^E of its children keeps a partition --
        # and `verify.py tree` re-derives it from the filenames alone.
        todo = [x.strip() for x in open(parents_file) if x.strip()]
    else:
        todo = unsolved(olddir, D)
    if limit:
        todo = todo[:limit]
    os.makedirs(newdir, exist_ok=True)

    work = []
    for parent in todo:
        plits = [(i + 1) if c == "1" else -(i + 1) for i, c in enumerate(parent)]
        base_d = len(parent)
        for child in itertools.product("01", repeat=E):
            clits = [(base_d + i + 1) if c == "1" else -(base_d + i + 1)
                     for i, c in enumerate(child)]
            work.append((newdir, nvar, base, parent + "".join(child),
                         plits + clits, timeout))

    print(f"parents {len(todo)}  leaves {len(work)}  "
          f"vars {nvar}  jobs {jobs}  timeout {timeout}s", flush=True)
    ok = bad = 0
    tot = 0
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for i, (tag, st, sz) in enumerate(ex.map(run_leaf, work), 1):
            if st in ("VERIFIED", "cached"):
                ok += 1
                tot += sz
            else:
                bad += 1
                print(f"  MISS {tag} {st}", flush=True)
            if i % 16 == 0:
                print(f"  {i}/{len(work)} ok={ok} miss={bad} "
                      f"{tot/2**20:.0f} MB", flush=True)
    print(f"DONE leaves={len(work)} ok={ok} miss={bad} "
          f"total={tot/2**20:.0f} MB "
          f"mean={(tot/ok/2**20 if ok else 0):.2f} MB", flush=True)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
