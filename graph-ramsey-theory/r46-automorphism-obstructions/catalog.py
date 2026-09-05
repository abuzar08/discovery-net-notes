"""Check Exoo's catalog of (4,6,35)-graphs and report their symmetry.

The 37 graphs in `r46_35some.g6` are the largest known Ramsey(4,6)-graphs
(Exoo 2012); their existence is what gives R(4,6) >= 36.

This script (a) decodes graph6 with its own decoder, (b) re-checks that each
graph really is a (4,6,35)-graph using verify.py's checker, and (c) reports
the automorphism group order via nauty, which is an OBSERVATION about the
known catalog and is not part of any certificate.

    python3 catalog.py r46_35some.g6            # (a) + (b), stdlib only
    uv run --with pynauty python3 catalog.py r46_35some.g6 --aut   # + (c)
"""

import sys

import verify


def g6_decode(line):
    """graph6 -> (n, adjacency matrix).  Own implementation.

    A graph6 string is: the order, then ceil(C(n,2)/6) data bytes.  Each byte
    b encodes six bits as b-63, most significant first.  The bit sequence is
    the upper triangle read column by column: for j = 1..n-1, for i = 0..j-1.
    Orders 0..62 are a single byte n+63; 63..258047 use the prefix 126.
    """
    s = line.strip()
    if not s:
        return None
    if ord(s[0]) == 126:
        if ord(s[1]) == 126:
            raise SystemExit("graph6 orders above 258047 not supported")
        n = ((ord(s[1]) - 63) << 12) | ((ord(s[2]) - 63) << 6) | (ord(s[3]) - 63)
        data = s[4:]
    else:
        n = ord(s[0]) - 63
        data = s[1:]
    bits = []
    for ch in data:
        v = ord(ch) - 63
        if not 0 <= v < 64:
            raise SystemExit(f"bad graph6 byte {ord(ch)}")
        for shift in range(5, -1, -1):
            bits.append((v >> shift) & 1)
    adj = [[False] * n for _ in range(n)]
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i][j] = adj[j][i] = True
            idx += 1
    return n, adj


def main():
    path = sys.argv[1]
    want_aut = "--aut" in sys.argv[2:]
    graphs = []
    for line in open(path):
        g = g6_decode(line)
        if g:
            graphs.append(g)
    print(f"{len(graphs)} graphs decoded from {path}")

    degs = set()
    bad = 0
    for i, (n, adj) in enumerate(graphs):
        err = verify.check_graph(n, adj, 4, 6)
        if err:
            print(f"  graph {i}: NOT a (4,6,{n})-graph: {err}")
            bad += 1
        for v in range(n):
            degs.add(sum(adj[v]))
    print(f"all on {graphs[0][0]} vertices; "
          f"{len(graphs) - bad}/{len(graphs)} are (4,6,35)-graphs; "
          f"degrees observed: {sorted(degs)}")

    if want_aut:
        import pynauty
        orders = {}
        for i, (n, adj) in enumerate(graphs):
            d = {v: [w for w in range(n) if adj[v][w]] for v in range(n)}
            g = pynauty.Graph(n, adjacency_dict=d)
            _, grpsize1, grpsize2, _, _ = pynauty.autgrp(g)
            order = int(round(grpsize1 * 10 ** grpsize2))
            orders[order] = orders.get(order, 0) + 1
        print("automorphism group orders (nauty): "
              + ", ".join(f"|Aut|={o}: {c} graphs"
                          for o, c in sorted(orders.items())))


if __name__ == "__main__":
    main()
