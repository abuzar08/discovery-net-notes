r"""reviewer-1: the \((4,5,24)\) control for the homogeneous-shape derivation.

The derivation: if the size-4 orbit \(O\) is independent, then no vertex may miss
all of \(O\) (it would complete an independent 5-set), every fixed vertex is
joined to all of \(O\), so each vertex of \(O\) has degree at least \(f\) and at
most \(R(3,5) - 1 = 13\) in a \((4,5)\)-graph; the vertices outside \(F \cup O\)
that meet \(O\) number at most \(4(13-f)\), and the rest would give an
independent 5-set, so \(n - f - 4 - 4(13-f) \le 0\), i.e. \(3f \le 56 - n\).
At \(n = 24\) that is \(f \le 10\).

The check: over catalogue graphs, for every independent 4-set \(S\), count the
vertices adjacent to all of \(S\) and verify the count never exceeds 10.
"""
import itertools
import sys

sys.path.insert(0, '../r45')
from indep_r45 import graph6

CAT = '../r45/dl/r45_24.g6'
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 2000


def main():
    n_graphs = 0
    worst = 0
    viol = 0
    sets = 0
    for line in open(CAT):
        if n_graphs >= LIMIT:
            break
        if not line.strip():
            continue
        n, adj = graph6(line)
        n_graphs += 1
        for S in itertools.combinations(range(n), 4):
            a, b, c, d = S
            if (adj[a] >> b) & 1 or (adj[a] >> c) & 1 or (adj[a] >> d) & 1 \
               or (adj[b] >> c) & 1 or (adj[b] >> d) & 1 or (adj[c] >> d) & 1:
                continue
            sets += 1
            common = adj[a] & adj[b] & adj[c] & adj[d]
            k = bin(common).count('1')
            worst = max(worst, k)
            if k > 10:
                viol += 1
    print(f'(4,5,24) control on {n_graphs} catalogue graphs, {sets} independent '
          f'4-sets examined')
    print(f'   largest number of vertices joined to all of an independent '
          f'4-set: {worst}')
    print(f'   the derivation predicts at most 10 -> violations: {viol}')
    print(f'   arithmetic: 3f <= 56 - n gives f <= {(56-24)//3} at n = 24 and '
          f'f <= {(100-42)//3} at n = 42 for (5,5)')


if __name__ == '__main__':
    main()
