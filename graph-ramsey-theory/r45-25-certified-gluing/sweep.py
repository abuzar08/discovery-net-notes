"""Refute every gluing (H, M) at a given degree, with a checked proof each.

For degree d in a (4,5,25)-graph: m = 24-d, H ranges over the complete
(3,5,d)-catalogue and M over the complete (4,4,m)-catalogue.  Each instance is
a pure bipartite completion (d*m variables).  A verdict is only recorded when
drat-trim verifies the refutation; proofs are hashed and released immediately,
so disk stays flat.

    python3 sweep.py D [JOBS] [TIMEOUT]
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import cert45
import r45bounds as R

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(HERE, "..", "tools", "cadical", "build", "cadical")
DRAT = os.path.join(HERE, "..", "tools", "drat-trim", "drat-trim")


def one(args):
    d, m, hi, Hadj, mi, Madj, timeout, tag = args
    nvar, cls = cert45.build_fixed_M(Hadj, d, Madj, m)
    if any(len(c) == 0 for c in cls):
        return tag, "EMPTY", 0, ""          # refuted at generation
    cnf = os.path.join(HERE, f"w{tag}.cnf")
    drat = os.path.join(HERE, f"w{tag}.drat")
    cert45.write(cnf, nvar, cls)
    try:
        r = subprocess.run([CAD, "-q", "--binary=false", cnf, drat],
                           capture_output=True, timeout=timeout)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    if rc != 20:
        for f in (cnf, drat):
            if os.path.exists(f):
                os.remove(f)
        return tag, f"rc={rc}", 0, ""
    v = subprocess.run([DRAT, cnf, drat], capture_output=True, text=True)
    ok = "s VERIFIED" in v.stdout
    h = ""
    if ok:
        hh = hashlib.sha256()
        with open(drat, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                hh.update(chunk)
        h = hh.hexdigest()
    sz = os.path.getsize(drat)
    for f in (cnf, drat):
        if os.path.exists(f):
            os.remove(f)
    return tag, ("VERIFIED" if ok else "DRAT-FAILED"), sz, h


def main():
    d = int(sys.argv[1])
    jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    m = 24 - d
    Hs = [R.g6_decode(l) for l in open(os.path.join(HERE, f"r35_{d}.g6")).read().split()]
    Ms = [R.g6_decode(l) for l in open(os.path.join(HERE, f"r44_{m}.g6")).read().split()]
    Hs = [x for x in Hs if x]
    Ms = [x for x in Ms if x]
    for o, a in Hs:
        assert o == d and R.is_good(d, a, 3, 5), "H not a genuine (3,5)-graph"
    for o, a in Ms:
        assert o == m and R.is_good(m, a, 4, 4), "M not a genuine (4,4)-graph"
    print(f"d={d} m={m}: {len(Hs)} H x {len(Ms)} M = {len(Hs)*len(Ms)} instances, "
          f"{d*m} variables each", flush=True)
    work = [(d, m, hi, H, mi, M, timeout, f"_{d}_{hi}_{mi}")
            for hi, (_, H) in enumerate(Hs) for mi, (_, M) in enumerate(Ms)]
    t0 = time.time()
    counts = {}
    manifest = open(os.path.join(HERE, f"proofs_d{d}.jsonl"), "w")
    bad = []
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for i, (tag, st, sz, h) in enumerate(ex.map(one, work), 1):
            counts[st] = counts.get(st, 0) + 1
            if st in ("VERIFIED", "EMPTY"):
                manifest.write(json.dumps({"tag": tag, "status": st,
                                           "bytes": sz, "sha256": h}) + "\n")
            else:
                bad.append((tag, st))
            if i % 500 == 0:
                print(f"  {i}/{len(work)} {counts} {time.time()-t0:.0f}s", flush=True)
    manifest.close()
    print(f"DONE d={d}: {counts} in {time.time()-t0:.0f}s", flush=True)
    if bad:
        print(f"  NOT REFUTED ({len(bad)}): {bad[:10]}", flush=True)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
