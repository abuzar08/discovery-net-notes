"""Measure proof size for the two logically equivalent min-degree encodings.

Does not touch the published encoder or any published certificate: it builds
its own DIMACS, runs CaDiCaL, and reports the DRAT size, so the comparison is
"same instance, same solver, two encodings of the same constraint".

    python3 exp_encoding.py N K Q PARTS.txt {subsets|seq}
"""

import subprocess
import sys
import os

import encode

CADICAL = "../tools/cadical/build/cadical"


def build(n, k, q, parts, mode):
    idx, _ = encode.pair_index(n)
    E = n * (n - 1) // 2
    clauses = encode.clique_clauses(n, q, idx)
    for p in parts:
        clauses.append(encode.block_clause(p, idx))

    naux_md = 0
    if mode == "subsets":
        clauses += encode.mindeg_clauses(n, k - 1, idx)
    else:
        md, naux_md = encode.mindeg_seq_clauses(n, k - 1, idx, E)
        clauses += md

    # symmetry breaking allocates its auxiliaries starting at E; shift them
    # past the min-degree auxiliaries.
    sb, naux_sb = encode.symbreak_clauses(n, idx)
    if naux_md:
        def shift(lit):
            a = abs(lit)
            if a > E:
                a += naux_md
            return a if lit > 0 else -a
        sb = [[shift(x) for x in cl] for cl in sb]
    clauses += sb
    return E + naux_md + naux_sb, clauses


def main():
    n, k, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    parts = encode.read_partitions(sys.argv[4])
    mode = sys.argv[5]
    nvar, clauses = build(n, k, q, parts, mode)
    cnf = f"exp_{mode}_n{n}_k{k}_q{q}.cnf"
    drat = cnf.replace(".cnf", ".drat")
    encode.write_dimacs(cnf, nvar, clauses)
    r = subprocess.run([CADICAL, "-q", "--binary=false", cnf, drat],
                       capture_output=True, text=True)
    ds = os.path.getsize(drat) if os.path.exists(drat) else 0
    print(f"{mode:8s} n={n} k={k} q={q}: vars={nvar} clauses={len(clauses)} "
          f"cnf={os.path.getsize(cnf)}B cadical={r.returncode} "
          f"drat={ds}B ({ds/1048576:.1f} MB)")
    os.remove(drat)
    os.remove(cnf)


if __name__ == "__main__":
    main()
