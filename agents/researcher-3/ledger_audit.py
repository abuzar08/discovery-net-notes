"""Check every artifact reference this seat's worklog records against the node.

principal-1, pass 43 restart brief: *"researcher-1 and researcher-3 should
query the graph before resubmitting"* — reporting that only **2** of my
contributions were committed after the stall height 3443, and *"most of your
published work is in git and not in the ledger"*.

That would be a costly thing to act on without checking, because resubmitting
work that is already committed creates duplicate contributions — the exact
failure my `pending/README.md` conditionals were written to avoid. So: check,
rather than resubmit.

The method is the one researcher-2 used at its own restart — take every
reference the worklog records and ask the node about each, rather than trusting
either a remembered submission or an aggregate count.

    python3 ledger_audit.py
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLI = "/Users/abuzark/.discovery-research-team/bin/discovery-net"
LEDGER = ("/Users/abuzark/Dev/discovery_net/run/discovery-net/node-local/"
          "ledger-data/artifact-ledger.sqlite")

# Nodes I cite but did not author: problem statements and area nodes.
NOT_MINE = {
    "Mathematics", "Graph Ramsey Theory",
    "The Classical Ramsey Number R(4,6)",
    "Determine the Classical Ramsey Number R(5,5)",
    "Chromatic Vertex Folkman Numbers n(k,q) = F_v(2,...,2;q)",
}


def refs_in(paths):
    out = set()
    for p in paths:
        if not os.path.exists(p):
            continue
        with open(p) as fh:
            out |= set(re.findall(r"bafkre[a-z0-9]{50,}", fh.read()))
    return sorted(out)


def lookup(ref):
    r = subprocess.run([CLI, "query", "--ledger-path", LEDGER, "artifact",
                        ref], capture_output=True, text=True, timeout=60)
    try:
        arts = json.loads(r.stdout)["artifacts"]
    except Exception:
        return None
    if not arts:
        return None
    return arts[0]["artifact"].get("title", "")


def main():
    paths = [os.path.join(HERE, "WORKLOG.md")]
    pend = os.path.join(HERE, "pending")
    if os.path.isdir(pend):
        paths += [os.path.join(pend, f) for f in sorted(os.listdir(pend))
                  if f.endswith(".md")]
    refs = refs_in(paths)
    print(f"{len(refs)} artifact references recorded in this seat's worklog "
          f"and queue\n")

    committed, missing, cited = [], [], []
    for ref in refs:
        title = lookup(ref)
        if title is None:
            missing.append((ref, ""))
            print(f"  MISSING    {ref[:16]}…")
            continue
        (cited if title in NOT_MINE else committed).append((ref, title))
        tag = "cited node" if title in NOT_MINE else "COMMITTED "
        print(f"  {tag} {ref[:16]}…  {title[:58]}")

    print()
    print(f"  authored by this seat and committed: {len(committed)}")
    print(f"  nodes cited but not authored here:   {len(cited)}")
    print(f"  recorded but NOT on the ledger:      {len(missing)}")
    if missing:
        print("\n  These need resubmitting from git:")
        for ref, _ in missing:
            print(f"    {ref}")
        return 1
    print("\n  Nothing recorded here is missing from the ledger, so there is")
    print("  nothing to resubmit and resubmitting would create duplicates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
