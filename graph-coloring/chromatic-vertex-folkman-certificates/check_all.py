"""Re-check every stored artifact in this directory, from scratch.

For each stored certificate: decompress the LRAT, regenerate the DIMACS
formula from (n, k, q) and the partition list with `encode.py`, and replay
the proof with `verify.py` (standard library only, independent regeneration).
For each witness: check K_q-freeness and chi >= k with `verify.py upper`.
Also runs the symmetry-breaking soundness tests.

    python3 check_all.py            # everything
    python3 check_all.py --quick    # skip symtest (its n=6 pass is the slow part)

Exit status is non-zero if anything fails.  No SAT solver is needed: this
script never runs CaDiCaL or drat-trim, it only replays stored proofs.
"""

import hashlib
import json
import lzma
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    quick = "--quick" in sys.argv
    manifest = json.load(open(os.path.join(HERE, "certs.json")))
    fails, checked, skipped = [], 0, 0

    if not quick:
        print("== symmetry-breaking soundness ==", flush=True)
        r = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"),
                            "symtest", "6"], capture_output=True, text=True)
        if r.returncode != 0:
            fails.append("symtest: " + r.stdout + r.stderr)
        print(r.stdout.strip())

    print("== upper bounds (witness graphs) ==", flush=True)
    for w in manifest["witnesses"]:
        p = os.path.join(HERE, "witnesses", w.get(
            "file", f"witness_n{w['n']}_k{w['k']}_q{w['q']}.txt"))
        if sha256(p) != w["sha256"]:
            fails.append(f"{p}: sha256 mismatch")
            continue
        r = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"),
                            "upper", str(w["k"]), str(w["q"]), p],
                           capture_output=True, text=True)
        ok = r.returncode == 0 and "VERIFIED" in r.stdout
        checked += ok
        if not ok:
            fails.append(f"witness {w}: {r.stdout}{r.stderr}")
        print(("  OK   " if ok else "  FAIL ") + r.stdout.strip()[:110])

    print("== lower bounds (LRAT refutations) ==", flush=True)
    with tempfile.TemporaryDirectory() as td:
        for c in sorted(manifest["certificates"],
                        key=lambda c: (c["k"], c["q"], c["n"])):
            tag = c["tag"]
            parts = os.path.join(HERE, "certificates", f"{tag}.parts.txt")
            if sha256(parts) != c["parts_sha256"]:
                fails.append(f"{tag}: partition list sha256 mismatch")
                continue
            xz = os.path.join(HERE, "certificates", f"{tag}.lrat.xz")
            if not c["stored"] or not os.path.exists(xz):
                skipped += 1
                print(f"  SKIP {tag} (proof not stored; "
                      f"sha256 {c['lrat_sha256'][:16]}, regenerate to check)")
                continue
            lrat = os.path.join(td, f"{tag}.lrat")
            with open(lrat, "wb") as f:
                f.write(lzma.decompress(open(xz, "rb").read()))
            if sha256(lrat) != c["lrat_sha256"]:
                fails.append(f"{tag}: LRAT sha256 mismatch after decompression")
                continue
            cnf = os.path.join(td, f"{tag}.cnf")
            args = ["--symbreak", "--mindeg", str(c["mindeg"])]
            r = subprocess.run(
                [sys.executable, os.path.join(HERE, "encode.py"),
                 str(c["n"]), str(c["k"]), str(c["q"]), parts, cnf] + args,
                capture_output=True, text=True)
            if r.returncode != 0:
                fails.append(f"{tag}: encode failed {r.stderr}")
                continue
            r = subprocess.run(
                [sys.executable, os.path.join(HERE, "verify.py"), "lower",
                 str(c["n"]), str(c["k"]), str(c["q"]), parts, cnf, lrat]
                + args, capture_output=True, text=True)
            ok = r.returncode == 0 and "VERIFIED" in r.stdout
            checked += ok
            if not ok:
                fails.append(f"{tag}: {r.stdout}{r.stderr}")
            print(f"  {'OK  ' if ok else 'FAIL'} {tag}  "
                  f"partitions={c['partitions']}")
            os.remove(lrat)
            os.remove(cnf)

    print(f"\n{checked} artifacts verified, {skipped} skipped "
          f"(proof too large to store), {len(fails)} failed")
    for f in fails:
        print("FAIL:", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
