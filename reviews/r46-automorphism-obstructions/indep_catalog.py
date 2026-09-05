"""reviewer-1: own graph6 decoder; (4,6,35) check; degrees; |Aut| via networkx VF2 (not nauty)."""
import itertools, sys, collections
import networkx as nx

def g6(line):
    b = [c - 63 for c in line.strip().encode()]
    n = b[0]; bits = []
    for x in b[1:]:
        bits += [(x >> (5 - i)) & 1 for i in range(6)]
    E = []; t = 0
    for v in range(1, n):
        for u in range(v):
            if bits[t]: E.append((u, v))
            t += 1
    return n, E

def has_clique(n, A, q):
    def rec(c, s):
        if s == q: return True
        while c:
            v = (c & -c).bit_length() - 1; c &= c - 1
            if rec(c & A[v], s + 1): return True
        return False
    return rec((1 << n) - 1, 0)

def main():
  auts = collections.Counter(); degs = set(); ok = 0
  for i, line in enumerate(open(sys.argv[1])):
      n, E = g6(line)
      A = [0] * n
      for u, v in E: A[u] |= 1 << v; A[v] |= 1 << u
      comp = [((1 << n) - 1) ^ A[v] ^ (1 << v) for v in range(n)]
      k4 = has_clique(n, A, 4); i6 = has_clique(n, comp, 6)
      d = sorted(bin(a).count('1') for a in A); degs |= set(d)
      G = nx.Graph(E)
      na = sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G, G).isomorphisms_iter())
      auts[na] += 1
      good = (n == 35 and not k4 and not i6); ok += good
      print(f"graph {i:2d}: n={n} m={len(E)} K4={k4} I6={i6} deg[{d[0]},{d[-1]}] |Aut|={na}")
  print(f"genuine (4,6,35)-graphs: {ok}/{i+1}; degrees seen {sorted(degs)}; |Aut| distribution {dict(auts)}")

if __name__ == '__main__':
    main()
