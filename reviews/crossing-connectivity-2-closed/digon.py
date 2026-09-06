r"""reviewer-1: is the crossing number preserved when a digon is replaced by a
digonal path?

h3285 closes branch (3) of BORS Theorem 1.3 with the sentence "a digonal path is
a path with every edge doubled (Definition 14.4), so the replacement subdivides
both edges of a digon in parallel; the crossing number is a topological
invariant, hence cr(G) = cr(C~)".  That justification is not sound as stated: a
digonal path of length t >= 2 is a chain of t digons, which is NOT homeomorphic
to a single digon (the internal vertices have degree four, and the chain has
t - 1 two-vertex cuts a digon does not have), so topological invariance of the
crossing number does not apply.

The equality itself is true; the proof is a redrawing argument, given in my
review.  This script corroborates it computationally.  Multigraphs are handled
by subdividing every parallel edge once, which IS a subdivision and so does
preserve the crossing number.

For each base graph and each edge uv of it, the edge is replaced by a digon and
then by digonal paths of length 2 and 3, and the crossing-number class
(<= 1, = 2, >= 3) of all three is compared with my own exact planarisation code.
"""
import itertools

import networkx as nx

from indep_fig143 import cr_le_1, cr_le_2


def cr_class(G):
    if cr_le_1(G):
        return '<=1'
    return '=2' if cr_le_2(G) else '>=3'


def digonal(G, u, v, t):
    """Replace the edge uv by a digonal path with t segments, as a simple graph:
    every parallel edge is subdivided once (a subdivision, so cr is unchanged)."""
    H = nx.Graph(G)
    H.remove_edge(u, v)
    nxt = max(H.nodes) + 1
    spine = [u] + [nxt + i for i in range(t - 1)] + [v]
    nxt += t - 1
    for a, b in zip(spine, spine[1:]):
        for _ in range(2):          # two parallel edges, each subdivided once
            H.add_edge(a, nxt)
            H.add_edge(nxt, b)
            nxt += 1
    return H


def bases():
    yield 'K5', nx.complete_graph(5)
    yield 'K33', nx.complete_bipartite_graph(3, 3)
    yield 'K6', nx.complete_graph(6)
    yield 'Petersen', nx.petersen_graph()
    yield 'C3xC3', nx.cartesian_product(nx.cycle_graph(3), nx.cycle_graph(3))
    yield 'K7-e', nx.restricted_view(nx.complete_graph(7), [], [(0, 1)]).copy()


if __name__ == '__main__':
    for name, G in bases():
        G = nx.convert_node_labels_to_integers(G)
        print(f'{name}: n={G.number_of_nodes()} m={G.number_of_edges()} '
              f'cr class {cr_class(G)}', flush=True)
        for u, v in itertools.islice(G.edges(), 3):
            cs = [cr_class(digonal(G, u, v, t)) for t in (1, 2, 3)]
            ok = 'SAME' if len(set(cs)) == 1 else '*** DIFFERENT ***'
            print(f'   edge {u}-{v}: digon {cs[0]}, digonal path of 2 {cs[1]}, '
                  f'of 3 {cs[2]}   {ok}', flush=True)
