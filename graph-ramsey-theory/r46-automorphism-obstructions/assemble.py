"""Assemble the publication directory for the (4,6,n) automorphism work.

A certificate here is self-contained: the formula is determined by
(n, s, t, f, p, k) alone, so only the LRAT proof has to be stored.  Proofs
whose xz-compressed size exceeds MAX_STORE are recorded by SHA-256 together
with the command that regenerates them.
"""

import hashlib
import json
import lzma
import os
import re
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
DST = ("/Users/abuzark/.discovery-research-team/workspaces/researcher-3/notes/"
       "graph-ramsey-theory/r46-automorphism-obstructions")
MAX_STORE = 6 * 1024 * 1024
NS = (36, 37, 38, 39)
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def enc_info():
    """orbit vars / clause counts, parsed from the .enc notes one.sh wrote."""
    info = {}
    for fn in os.listdir(SRC):
        if not fn.endswith(".enc"):
            continue
        txt = open(os.path.join(SRC, fn)).read()
        m = re.search(r"orbit vars=(\d+) clauses=(\d+)", txt)
        if m:
            info[fn[:-4]] = (int(m.group(1)), int(m.group(2)))
    return info


def main():
    os.makedirs(f"{DST}/certificates", exist_ok=True)
    info = enc_info()
    certs = []
    for fn in sorted(os.listdir(SRC)):
        m = re.match(r"n(\d+)_f(\d+)_p(\d+)_k(\d+)\.lrat$", fn)
        if not m:
            continue
        n, f, p, k = (int(m.group(i)) for i in (1, 2, 3, 4))
        tag = fn[:-5]
        path = os.path.join(SRC, fn)
        size = os.path.getsize(path)
        comp = lzma.compress(open(path, "rb").read(), preset=6) \
            if size <= 8 * MAX_STORE else None
        v, c = info.get(tag, (None, None))
        e = {"tag": tag, "n": n, "f": f, "p": p, "k": k,
             "orbit_vars": v, "clauses": c,
             "lrat_bytes": size, "lrat_sha256": sha256(path),
             "lrat_xz_bytes": len(comp) if comp else -1,
             "stored": bool(comp) and len(comp) <= MAX_STORE}
        if e["stored"]:
            with open(f"{DST}/certificates/{tag}.lrat.xz", "wb") as fh:
                fh.write(comp)
        certs.append(e)

    # cube-and-conquer certificates: a directory of 2^D per-cube LRATs.
    # Too large to store wholesale, so the artifact is the manifest of
    # per-cube SHA-256 hashes plus the exact regeneration command; the split
    # itself needs no lemma (every assignment satisfies exactly one cube).
    cubes = []
    for dn in sorted(os.listdir(SRC)):
        m = re.match(r"cubes_n(\d+)_(\d+)_(\d+)$", dn)
        if not m or not os.path.isdir(os.path.join(SRC, dn)):
            continue
        n, p, k = (int(m.group(i)) for i in (1, 2, 3))
        f = n - p * k
        d = os.path.join(SRC, dn)
        lr = sorted(x for x in os.listdir(d) if x.endswith(".lrat"))
        D = len(lr[0]) - len("c.lrat") if lr else 0
        if len(lr) != 2 ** D:
            print(f"  {dn}: {len(lr)} cubes, expected {2**D} -- skipping")
            continue
        per = {x[:-5]: {"sha256": sha256(os.path.join(d, x)),
                        "bytes": os.path.getsize(os.path.join(d, x))}
               for x in lr}
        cubes.append({"tag": dn, "n": n, "f": f, "p": p, "k": k,
                      "split_vars": list(range(1, D + 1)), "n_cubes": len(lr),
                      "total_lrat_bytes": sum(v["bytes"] for v in per.values()),
                      "cubes": per,
                      "regenerate": f"python3 cubes.py {n} 4 6 {f} {p} {k} "
                                    f"{D} {dn}",
                      "check": f"python3 verify.py cubes {n} 4 6 {f} {p} {k} "
                               f"{dn} {D}"})
        certs.append({"tag": dn, "n": n, "f": f, "p": p, "k": k,
                      "orbit_vars": None, "clauses": None,
                      "lrat_bytes": sum(v["bytes"] for v in per.values()),
                      "lrat_sha256": "cube-and-conquer, see cube_certificates",
                      "lrat_xz_bytes": -1, "stored": False,
                      "cube_and_conquer": True})

    # Carry forward entries whose LRAT is no longer present locally (large
    # proofs are deleted from scratch once checked and hashed, per the scratch
    # policy).  Without this the manifest silently loses them on the next
    # assemble -- the same defect that had to be fixed in the Folkman
    # assembler.
    prev_path = f"{DST}/certs.json"
    carried = 0
    if os.path.exists(prev_path):
        have = {c["tag"] for c in certs}
        for c in json.load(open(prev_path)).get("certificates", []):
            if c["tag"] not in have:
                c = dict(c)
                c["lrat_present_locally"] = False
                certs.append(c)
                carried += 1
    print(f"carried_forward={carried}")

    done = {(c["n"], c["f"], c["p"], c["k"]) for c in certs}

    # classify every prime cycle type in range
    hand, open_types, small = [], [], []
    for n in NS:
        for p in PRIMES:
            for k in range(1, n // p + 1):
                f = n - p * k
                if (n, f, p, k) in done:
                    continue
                if p >= 18 and f >= 1:
                    hand.append((n, f, p, k, "Theorem 4"))
                elif p >= 6 and f > 22:
                    hand.append((n, f, p, k, "Corollary 3 (f<=22)"))
                elif p <= 3:
                    small.append((n, f, p, k))
                else:
                    open_types.append((n, f, p, k))

    lines = ["### Certified: no (4,6,n)-graph has an automorphism of this "
             "cycle type", "",
             "| n | cycle type | orbit vars | clauses | LRAT | stored | "
             "sha256 (prefix) |", "|---|---|---|---|---|---|---|"]
    for c in sorted(certs, key=lambda c: (c["n"], -c["p"], c["k"])):
        t = f"1^{c['f']} {c['p']}^{c['k']}" if c["f"] else f"{c['p']}^{c['k']}"
        lines.append(
            f"| {c['n']} | `{t}` | {c['orbit_vars']} | {c['clauses']} | "
            f"{c['lrat_bytes']/1024:.0f} KB | "
            f"{'yes' if c['stored'] else 'no (hash only)'} | "
            f"`{c['lrat_sha256'][:16]}` |")

    lines += ["", "### Excluded by the analytic lemma (no certificate needed)",
              "", "| n | cycle type | reason |", "|---|---|---|"]
    for n, f, p, k, why in sorted(hand):
        t = f"1^{f} {p}^{k}" if f else f"{p}^{k}"
        lines.append(f"| {n} | `{t}` | {why} |")

    lines += ["", "### Open at p >= 5 (neither excluded nor certified here)",
              "", "| n | cycle type | orbit vars (approx) | why |",
              "|---|---|---|---|"]
    for n, f, p, k in sorted(open_types):
        t = f"1^{f} {p}^{k}" if f else f"{p}^{k}"
        why = ("Corollary 3 needs p >= 6, so f is unbounded here"
               if p == 5 and f > 22 else "solver did not finish in 1500 s")
        lines.append(f"| {n} | `{t}` | ~{f*(f-1)//2 + f*k + k*(p-1)//2} | "
                     f"{why} |")
    lines += ["", f"### Not attempted: p = 2 and p = 3 ({len(small)} types)",
              "",
              "For `p in {2,3}` neither Theorem 4 nor Corollary 3 applies "
              "(Corollary 3 needs `p >= 6`, and an orbit of size 2 or 3 may "
              "be a clique, so Lemma 2(3) can fail). These types also have "
              "the largest formulas: `f` is at least `n - 3k`, so the fixed "
              "part alone contributes `C(f,2)` singleton orbits, several "
              "hundred variables in most cases. None was attempted.", ""]

    with open(f"{DST}/RESULTS.md", "w") as fh:
        fh.write("\n".join(lines) + "\n")

    json.dump({"window": "36 <= R(4,6) <= 40",
               "tools": {"cadical": "3.0.1 (git c607304)",
                         "drat_trim": "git 2e3b2dc",
                         "python": sys.version.split()[0]},
               "certificates": certs,
               "cube_certificates": cubes,
               "excluded_by_lemma": [
                   {"n": n, "f": f, "p": p, "k": k, "reason": w}
                   for n, f, p, k, w in sorted(hand)],
               "open_p_ge_5": [{"n": n, "f": f, "p": p, "k": k}
                               for n, f, p, k in sorted(open_types)],
               "not_attempted_p_2_3": [{"n": n, "f": f, "p": p, "k": k}
                                       for n, f, p, k in sorted(small)]},
              open(f"{DST}/certs.json", "w"), indent=2, sort_keys=True)

    print(f"cube-certificates={len(cubes)}")
    print(f"certificates={len(certs)} stored={sum(c['stored'] for c in certs)} "
          f"hand-excluded={len(hand)} open(p>=5)={len(open_types)} "
          f"not-attempted(p<=3)={len(small)}")
    print("publication dir:",
          subprocess.run(["du", "-sh", DST], capture_output=True,
                         text=True).stdout.strip())


if __name__ == "__main__":
    main()
