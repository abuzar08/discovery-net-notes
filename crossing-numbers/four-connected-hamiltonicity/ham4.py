"""4-connected, non-Hamiltonian, small crossing number: the search pipeline.

DS21 open question: if G is 4-connected with cr(G) <= 3, is G Hamiltonian?
Known: true for cr(G) <= 2 (Ozeki and Zamfirescu, SIAM J. Discrete Math. 32
(2018) 2783-2794); false for cr(G) <= 6.  The gap cr = 3, 4, 5 is open, and a
single 4-connected non-Hamiltonian graph with cr = 3 would settle it, with the
graph itself as a certificate anyone can check.

Pipeline, cheapest test first and the expensive one last:
  geng -d4         min degree >= 4 (necessary for 4-connectivity)
  -> 4-connected   no vertex cut of size <= 3
  -> NOT Hamiltonian
  -> cr = 3        exact, only on the survivors

Chvatal-Erdos gives the pruning that makes this feasible: connectivity >=
independence number implies Hamiltonian, so a 4-connected non-Hamiltonian graph
must have independence number >= 5.
"""
import sys
from itertools import combinations

def g6_bits(line):
    """graph6 -> (n, adjacency bitmask list)."""
    d = line.strip()
    if not d: return None
    b = [ord(c) - 63 for c in d]
    n = b[0]
    if n >= 63: raise ValueError("n >= 63 unsupported")
    bits = []
    for v in b[1:]:
        bits.extend((v >> k) & 1 for k in range(5, -1, -1))
    adj = [0]*n
    i = 0
    for j in range(1, n):
        for k in range(j):
            if i < len(bits) and bits[i]:
                adj[j] |= 1 << k
                adj[k] |= 1 << j
            i += 1
    return n, adj

def connected(adj, alive):
    v0 = (alive & -alive).bit_length() - 1
    seen, stack = 1 << v0, [v0]
    while stack:
        u = stack.pop()
        nb = adj[u] & alive & ~seen
        while nb:
            w = (nb & -nb).bit_length() - 1
            seen |= 1 << w; stack.append(w); nb &= nb - 1
    return seen == alive

def four_connected(n, adj):
    """No cut of size <= 3 (min degree >= 4 assumed from geng)."""
    full = (1 << n) - 1
    if n < 5: return False
    for k in (1, 2, 3):
        for cut in combinations(range(n), k):
            alive = full
            for c in cut: alive &= ~(1 << c)
            if not connected(adj, alive):
                return False
    return True

def hamiltonian(n, adj):
    """Backtracking Hamiltonian-cycle test; exact."""
    full = (1 << n) - 1
    start = 0
    def rec(v, visited, count):
        if count == n:
            return bool(adj[v] >> start & 1)
        nb = adj[v] & ~visited
        while nb:
            w = (nb & -nb).bit_length() - 1
            nb &= nb - 1
            # prune: every unvisited vertex needs 2 available neighbours
            rest = ~(visited | (1 << w)) & full
            ok = True
            r = rest
            while r:
                u = (r & -r).bit_length() - 1; r &= r - 1
                if bin(adj[u] & (rest | (1 << w) | (1 << start))).count('1') < 2:
                    ok = False; break
            if ok and rec(w, visited | (1 << w), count + 1):
                return True
        return False
    return rec(start, 1 << start, 1)

if __name__ == "__main__":
    seen = c4 = nonham = 0
    out = []
    for line in sys.stdin:
        r = g6_bits(line)
        if r is None: continue
        n, adj = r
        seen += 1
        if not four_connected(n, adj): continue
        c4 += 1
        if hamiltonian(n, adj): continue
        nonham += 1
        out.append(line.strip())
        print("NONHAM", line.strip(), flush=True)
    print(f"read {seen}, 4-connected {c4}, 4-connected non-Hamiltonian {nonham}")
