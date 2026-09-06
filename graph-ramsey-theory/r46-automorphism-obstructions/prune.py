"""Replay leaf proofs, record their hashes, and release the disk.

A complete adaptive-split certificate for a hard instance runs to tens of
gigabytes, which is more than the working directory is allowed to hold and far
more than can be committed.  This file makes the checking incremental instead
of deferring it:

  for each leaf LRAT present
      replay it, with verify.py's own checker, against the formula
      regenerated here from (n,s,t,f,p,k) plus that leaf's unit clauses
      record (tag, sha256, bytes) in a manifest
      delete the LRAT and leave a zero-byte <tag>.done marker

WHAT THIS DOES AND DOES NOT ESTABLISH.  Every leaf is replayed to the empty
clause by the same code path `verify.py tree` uses, so no proof is trusted on
a solver's word.  What is given up is that the replays happen incrementally
rather than in one final atomic pass: after pruning, `verify.py tree` can
still check that the surviving tag set is a partition (that check reads only
file names), but it cannot re-replay a pruned leaf without regenerating it.
The manifest records the exact regeneration command for each leaf, so the run
is reproducible; it is not a substitute for the proof.  Anyone wanting a
single end-to-end check should re-run without pruning on a machine with the
disk for it.

    python3 prune.py N S T F P K DIR MANIFEST.jsonl [flags]

--min-age=SECONDS (default 120) skips files written recently, so this is safe
to run concurrently with deepen.py.
"""

import hashlib
import json
import os
import sys
import time

import verify


def main():
    n, s, t, f, p, k = (int(x) for x in sys.argv[1:7])
    d = sys.argv[7]
    manifest = sys.argv[8]
    flags = sys.argv[9:]

    nvar, base = verify.regenerate(n, s, t, f, p, k,
                                   profile="--profile" in flags,
                                   symf="--symf" in flags,
                                   symc="--symc" in flags,
                                   syms="--syms" in flags)
    seen = set()
    if os.path.exists(manifest):
        with open(manifest) as fh:
            for line in fh:
                if line.strip():
                    seen.add(json.loads(line)["tag"])

    # Only touch files that have been untouched for min_age seconds, so this
    # can run alongside a live deepen.py without ever reading an LRAT that
    # drat-trim is still writing.
    min_age = 120
    for a in flags:
        if a.startswith("--min-age="):
            min_age = int(a.split("=")[1])
    now = time.time()
    todo = sorted(fn for fn in os.listdir(d)
                  if fn.startswith("c") and fn.endswith(".lrat")
                  and os.path.getsize(os.path.join(d, fn)) > 0
                  and now - os.path.getmtime(os.path.join(d, fn)) >= min_age)
    done = 0
    freed = 0
    with open(manifest, "a") as out:
        for fn in todo:
            tag = fn[1:-5]
            if tag in seen:
                continue
            q = os.path.join(d, fn)
            lits = [(i + 1) if c == "1" else -(i + 1)
                    for i, c in enumerate(tag)]
            verify.replay(base + [(x,) for x in lits], q)   # to the empty clause
            h = hashlib.sha256()
            with open(q, "rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b""):
                    h.update(chunk)
            sz = os.path.getsize(q)
            out.write(json.dumps({"tag": tag, "sha256": h.hexdigest(),
                                  "bytes": sz}) + "\n")
            out.flush()
            os.remove(q)
            open(os.path.join(d, "c" + tag + ".done"), "w").close()
            done += 1
            freed += sz
            if done % 200 == 0:
                print(f"  replayed and released {done}, "
                      f"{freed / 2**30:.2f} GB freed", flush=True)
    print(f"DONE replayed {done} leaves, freed {freed / 2**30:.2f} GB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
