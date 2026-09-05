"""Re-check every stored certificate in this directory, from scratch.

For each stored proof: decompress the LRAT, regenerate the whole DIMACS
formula from (n, 4, 6, f, p, k) with `encode.py`, and replay the proof with
`verify.py` (standard library only, independently regenerated orbits).

No SAT solver is needed: CaDiCaL and drat-trim are never invoked here.

    python3 check_all.py             # everything stored
    python3 check_all.py --fast      # only the small certificates

Exit status is non-zero if anything fails.
"""

import hashlib
import json
import lzma
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FAST_LIMIT = 2 * 1024 * 1024


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    fast = "--fast" in sys.argv
    man = json.load(open(os.path.join(HERE, "certs.json")))
    fails, ok, skipped = [], 0, 0

    print("== checker self-test ==", flush=True)
    r = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"),
                        "selftest"], capture_output=True, text=True)
    if r.returncode != 0:
        fails.append("selftest: " + r.stdout + r.stderr)
    print("  " + r.stdout.strip())

    print("== certificates ==", flush=True)
    with tempfile.TemporaryDirectory() as td:
        for c in sorted(man["certificates"],
                        key=lambda c: (c["n"], -c["p"], c["k"])):
            tag = c["tag"]
            xz = os.path.join(HERE, "certificates", f"{tag}.lrat.xz")
            if not c["stored"] or not os.path.exists(xz):
                skipped += 1
                print(f"  SKIP {tag} (proof not stored; "
                      f"sha256 {c['lrat_sha256'][:16]})")
                continue
            if fast and c["lrat_bytes"] > FAST_LIMIT:
                skipped += 1
                continue
            lrat = os.path.join(td, f"{tag}.lrat")
            with open(lrat, "wb") as fh:
                fh.write(lzma.decompress(open(xz, "rb").read()))
            if sha256(lrat) != c["lrat_sha256"]:
                fails.append(f"{tag}: LRAT sha256 mismatch")
                continue
            cnf = os.path.join(td, f"{tag}.cnf")
            args = [str(c["n"]), "4", "6", str(c["f"]), str(c["p"]),
                    str(c["k"])]
            flag = ["--symf"] if c.get("symf") else []
            r = subprocess.run(
                [sys.executable, os.path.join(HERE, "encode.py")]
                + args + [cnf] + flag, capture_output=True, text=True)
            if r.returncode != 0:
                fails.append(f"{tag}: encode failed {r.stderr}")
                continue
            r = subprocess.run(
                [sys.executable, os.path.join(HERE, "verify.py"), "lower"]
                + args + [cnf, lrat] + flag, capture_output=True, text=True)
            good = r.returncode == 0 and "VERIFIED" in r.stdout
            ok += good
            if not good:
                fails.append(f"{tag}: {r.stdout}{r.stderr}")
            t = (f"1^{c['f']} {c['p']}^{c['k']}" if c["f"]
                 else f"{c['p']}^{c['k']}")
            print(f"  {'OK  ' if good else 'FAIL'} n={c['n']} type {t}")
            os.remove(lrat)
            os.remove(cnf)

    print(f"\n{ok} certificates verified, {skipped} skipped, "
          f"{len(fails)} failed")
    for f in fails:
        print("FAIL:", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
