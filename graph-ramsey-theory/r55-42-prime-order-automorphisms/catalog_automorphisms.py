"""Automorphism groups of the 328 stored McKay-Radziszowski (5,5,42)-graphs
(file r55_42some.g6 from https://users.cecs.anu.edu.au/~bdm/data/ramsey.html;
the 656 known graphs are these and their complements).

For each stored graph: verify (standard library) that it has no K5 and no
independent 5-set, compute |Aut| with nauty (via pynauty), and verify every
nauty generator directly as an automorphism (standard library).  Also checks
that no stored graph is isomorphic to its complement or to another stored one.

usage: uv run --with pynauty==2.8.8.1 python3 catalog_automorphisms.py r55_42some.g6
"""
import sys, collections, hashlib
from g6 import parse_g6, has_clique, complement, degrees
from pynauty import Graph, autgrp, certificate

def main(path):
    data = open(path, 'rb').read()
    print("sha256", hashlib.sha256(data).hexdigest())
    lines = [l for l in data.decode().split('\n') if l.strip()]
    orders = collections.Counter(); cycle_types = collections.Counter(); certs = set()
    for l in lines:
        n, adj = parse_g6(l)
        assert n == 42
        assert not has_clique(adj, n, 5) and not has_clique(complement(adj, n), n, 5), "not (5,5)-good"
        d = degrees(adj); assert 17 <= min(d) and max(d) <= 24
        g = Graph(n, adjacency_dict={v: [u for u in range(n) if (adj[v] >> u) & 1] for v in range(n)})
        gens, gs1, gs2, orbits, norb = autgrp(g)
        order = int(round(gs1 * 10 ** gs2)); orders[order] += 1
        for perm in gens:  # verify generator is an automorphism, record its cycle type
            for u in range(n):
                for v in range(n):
                    assert ((adj[u] >> v) & 1) == ((adj[perm[u]] >> perm[v]) & 1), "nauty generator is not an automorphism"
            seen = [False] * n; ct = collections.Counter()
            for s in range(n):
                if seen[s]: continue
                L = 0; x = s
                while not seen[x]:
                    seen[x] = True; x = perm[x]; L += 1
                ct[L] += 1
            cycle_types[tuple(sorted(ct.items()))] += 1
        c = certificate(g); cc = certificate(Graph(n, adjacency_dict={v: [u for u in range(n) if (complement(adj, n)[v] >> u) & 1] for v in range(n)}))
        assert c != cc, "self-complementary graph"
        certs.add(c)
    assert len(certs) == len(lines), "isomorphic duplicates"
    print(len(lines), "stored graphs, pairwise non-isomorphic, none self-complementary")
    print("|Aut| distribution:", dict(orders))
    print("cycle types of nauty generators ((length, count),...):", dict(cycle_types))

if __name__ == '__main__':
    main(sys.argv[1])
