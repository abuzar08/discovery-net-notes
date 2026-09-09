r"""reviewer-1: independent recomputation of the per-seed coverage of the
d <= 4 expansion run (h3285, researcher-4).

For every seed with d <= 3 I enumerate ALL 31^d expansions with my own
construction (terminals joined to neighbours, terminal-to-terminal for edges
between two patched vertices, then degree-2 suppression), count what the
criticality checker could represent — at most 28 vertices and 62 edges, with
extra parallel copies subdivided before testing, as the lane does — and compare
with the published coverage.
"""
import collections, itertools, json, random
import networkx as nx
from indep_3038 import census, p4c, expand, LANE

art = json.load(open(LANE + 'figure_15_1_configurations.json'))['configurations']
seeds = [G for G in census() if G.number_of_nodes() <= 10 and p4c(G)]
bydeg = collections.defaultdict(list)
for G in seeds:
    bydeg[sum(1 for _, d in G.degree() if d == 3)].append(G)


def sizes(H):
    extra = sum(c - 1 for c in collections.Counter(
        (min(u, v), max(u, v)) for u, v in H.edges()).values())
    return H.number_of_nodes() + extra, H.number_of_edges() + extra


def decidable_fraction(G, exhaustive=True, sample=4000):
    deg3 = [v for v, d in G.degree() if d == 3]
    d = len(deg3)
    tot = 31 ** d
    dec = 0
    if exhaustive:
        it = itertools.product(range(31), repeat=d)
    else:
        it = ([random.randrange(31) for _ in range(d)] for _ in range(sample))
    seen = 0
    for choice in it:
        seen += 1
        H = expand(G, dict(zip(deg3, choice)), art)
        n, m = sizes(H)
        if n <= 28 and m <= 62:
            dec += 1
    return d, tot, dec, seen


random.seed(20260909)
print('PER-SEED COVERAGE, my own construction')
for d in (0, 2, 3):
    for G in bydeg.get(d, []):
        dd, tot, dec, seen = decidable_fraction(G)
        print(f'   seed on {G.number_of_nodes()} vertices, d = {dd}: '
              f'{dec} of {tot} decidable = {100*dec/tot:.2f}%', flush=True)
print()
print('d = 4 SEEDS, sampled (4000 per seed)')
for G in bydeg.get(4, []):
    dd, tot, dec, seen = decidable_fraction(G, exhaustive=False)
    print(f'   seed on {G.number_of_nodes()} vertices: {100*dec/seen:.2f}% of '
          f'{seen} sampled (published: 17.73% at 8 vertices, 13.17% at 9, '
          f'9.57% at 10)', flush=True)
print()
print('ARITHMETIC OF THE PUBLISHED COVERAGE')
for (lbl, dec, tot) in [('d=2', 960, 961), ('d=3', 19614, 29791),
                        ('d=4, 8 vertices', 163783, 923521),
                        ('d=4, 9 vertices', 121643, 923521),
                        ('d=4, 10 vertices', 88427, 923521)]:
    print(f'   {lbl}: {dec}/{tot} = {100*dec/tot:.2f}%')
tot_dec = 4*1 + 960 + 2*19614 + 5*163783 + 2*121643 + 3*88427
print(f'   total decided = {tot_dec} (published 1367674), '
      f'total expansions = {4*1 + 961 + 2*29791 + 10*923521} '
      f'(published 9295757), skipped = '
      f'{4*1 + 961 + 2*29791 + 10*923521 - tot_dec} (published 7928083)')
