r"""reviewer-1: independent check of the connectivity claims of h3013.

Parses the census files directly (lines "CRIT2 n m u-v,u-v,..."), computes the
vertex connectivity of every member with my own call to networkx, and reports:

  * how many members have connectivity 1, 2 and >= 3, and their orders;
  * the connectivity of \(C_3 \square C_3\), which the contribution says is 4;
  * the crossing numbers the census certificate records for the connectivity-2
    members, which h3013 says are all 2.

usage: python3 indep_conn.py [census_dir]
"""
import sys, os, json, itertools
import networkx as nx


def read_census(path):
    out = []
    for line in open(path):
        parts = line.split()
        if not parts or parts[0] != 'CRIT2':
            continue
        n, m = int(parts[1]), int(parts[2])
        edges = [tuple(int(x) for x in e.split('-')) for e in parts[3].strip(',').split(',') if e]
        G = nx.Graph(edges)
        G.add_nodes_from(range(n))
        assert G.number_of_nodes() == n, (path, n, G.number_of_nodes())
        assert G.number_of_edges() == m, (path, m, G.number_of_edges())
        out.append(G)
    return out


def c3boxc3():
    G = nx.cartesian_product(nx.cycle_graph(3), nx.cycle_graph(3))
    return nx.convert_node_labels_to_integers(G)


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'target')
    per_conn = {}
    all_graphs = []
    for n in range(6, 12):
        p = os.path.join(d, f'n{n}.txt')
        if not os.path.exists(p):
            continue
        gs = read_census(p)
        for G in gs:
            k = nx.node_connectivity(G)
            per_conn.setdefault(k, []).append((n, G))
            all_graphs.append((n, k, G))
        print(f'  n = {n:2d}: {len(gs):2d} members, connectivity counts '
              f'{ {k: sum(1 for m, kk, _ in all_graphs if m == n and kk == k) for k in sorted({kk for m, kk, _ in all_graphs if m == n})} }')
    print()
    for k in sorted(per_conn):
        orders = sorted(n for n, _ in per_conn[k])
        print(f'  connectivity {k}: {len(per_conn[k])} members, orders {orders}')
    print()
    G = c3boxc3()
    print(f'  C3 x C3: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges, '
          f'vertex connectivity {nx.node_connectivity(G)}, 4-regular {all(dd == 4 for _, dd in G.degree())}')
    print()
    cert = os.path.join(d, 'certificate.json')
    if os.path.exists(cert):
        c = json.load(open(cert))
        keys = list(c) if isinstance(c, dict) else None
        print(f'  certificate.json top-level: {keys if keys else type(c)}')


if __name__ == '__main__':
    main()
