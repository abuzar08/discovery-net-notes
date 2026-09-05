"""Upper bound for n(7,4) = F_v(2^6;K_4) via a Mycielskian.

Step 1: find a Ramsey (4,4,16)-graph, i.e. a K_4-free graph on 16 vertices
        with alpha <= 3.  This is a plain SAT problem (two forbidden-subgraph
        families, no quantifier alternation).
Step 2: check chi = 6 for it -- that is F_v(2^5;K_4) = 16 realised.
Step 3: the Mycielskian mu(G) has 2n+1 vertices, chi(mu(G)) = chi(G)+1, and
        omega(mu(G)) = omega(G) when omega(G) >= 2, so it stays K_4-free.
        That gives a K_4-free graph with chi >= 7 on 33 vertices.
Step 4: hand it to shrink.py.

Every graph produced here is written out and re-checked by verify.py, which
trusts nothing in this file.

    uv run --with python-sat python3 mycielski.py
"""

import itertools

from pysat.solvers import Cadical153

import encode


def find_ramsey(n, q, a):
    """A K_q-free graph on n vertices with alpha <= a, or None."""
    idx, pairs = encode.pair_index(n)
    cls = encode.clique_clauses(n, q, idx) + encode.indep_clauses(n, a, idx)
    s = Cadical153(bootstrap_with=cls)
    if not s.solve():
        return None
    pos = set(x for x in s.get_model() if x > 0)
    adj = [0] * n
    for i, (u, v) in enumerate(pairs):
        if (i + 1) in pos:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return adj


def chi_at_least(n, adj, k):
    c = k - 1
    colour = [-1] * n

    def rec(v, used):
        if v == n:
            return True
        for col in range(min(used + 1, c)):
            ok = True
            m = adj[v] & ((1 << v) - 1)
            while m:
                b = m & -m
                w = b.bit_length() - 1
                m ^= b
                if colour[w] == col:
                    ok = False
                    break
            if ok:
                colour[v] = col
                if rec(v + 1, max(used, col + 1)):
                    return True
                colour[v] = -1
        return False

    return not rec(0, 0)


def mycielskian(n, adj):
    """mu(G): v_0..v_{n-1}, u_0..u_{n-1}, w.

    u_i ~ N_G(v_i) and u_i ~ w.  The u_i form an independent set.
    """
    m = 2 * n + 1
    out = [0] * m
    W = 2 * n
    for v in range(n):
        for w in range(n):
            if adj[v] >> w & 1:
                out[v] |= 1 << w            # v_v ~ v_w
                out[n + v] |= 1 << w        # u_v ~ v_w
                out[w] |= 1 << (n + v)      # symmetric
        out[n + v] |= 1 << W
        out[W] |= 1 << (n + v)
    return m, out


def write(path, n, adj):
    edges = [(u, v) for u in range(n) for v in range(u + 1, n)
             if adj[u] >> v & 1]
    with open(path, "w") as f:
        f.write(f"{n}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")
    return len(edges)


def has_clique(n, adj, q):
    for S in itertools.combinations(range(n), q):
        if all(adj[u] >> v & 1 for u, v in itertools.combinations(S, 2)):
            return True
    return False


def main():
    n = 16
    adj = find_ramsey(n, 4, 3)
    if adj is None:
        print("no (4,4,16)-graph found -- unexpected")
        return
    e = write("ramsey_4_4_16.txt", n, adj)
    print(f"(4,4,16)-graph: {e} edges; K_4-free={not has_clique(n, adj, 4)}; "
          f"chi>=6 {chi_at_least(n, adj, 6)}; chi>=7 {chi_at_least(n, adj, 7)}")

    m, mu = mycielskian(n, adj)
    e2 = write("myc_n33_k7_q4.txt", m, mu)
    print(f"Mycielskian: {m} vertices, {e2} edges; "
          f"K_4-free={not has_clique(m, mu, 4)}; "
          f"chi>=7 {chi_at_least(m, mu, 7)}; chi>=8 {chi_at_least(m, mu, 8)}")


if __name__ == "__main__":
    main()
