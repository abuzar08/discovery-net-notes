r"""reviewer-1: independent audit of the leaf manifest of h3297 — prefix-freeness,
the exact Kraft sum, the per-depth counts, the tree bookkeeping and the
certificate size. My own trie, my own exact rational arithmetic.
"""
import gzip
import json
from collections import Counter
from fractions import Fraction

P = ('../../notes/graph-ramsey-theory/r46-automorphism-obstructions/'
     'cube-manifests/r46-1_0-5_7-leaves.jsonl.gz')


def main():
    recs = [json.loads(l) for l in gzip.open(P, 'rt')]
    tags = [r['tag'] for r in recs]
    print(f'leaves in the manifest: {len(recs)}')
    print(f'   distinct tags: {len(set(tags))}, alphabet '
          f'{sorted(set("".join(tags)))}')
    depths = Counter(len(t) for t in tags)
    print(f'   per-depth counts: {dict(sorted(depths.items()))}')

    # prefix-freeness, by my own trie
    root = {}
    clashes = []
    for t in sorted(tags, key=len):
        node = root
        for i, ch in enumerate(t):
            if node.get('END'):
                clashes.append(t)
                break
            node = node.setdefault(ch, {})
        else:
            if node:
                clashes.append(t)
            node['END'] = True
    print(f'   prefix-free: {"yes" if not clashes else clashes[:5]}')

    K = sum(Fraction(1, 2 ** len(t)) for t in tags)
    D = 2 ** max(depths)
    print(f'   Kraft sum = {K} = {K.numerator * (D // K.denominator)}/{D} '
          f'= {float(K):.9f}')
    print(f'   open fraction = {1 - K} = '
          f'{(1 - K).numerator * (D // (1 - K).denominator)}/{D} '
          f'= {float(1 - K):.9f}')
    print(f'   published: refuted 4188429/4194304 = 0.998599291..., '
          f'open 5875/4194304 = 0.001400709...')

    # tree bookkeeping: children of every internal node
    parents = Counter()
    for t in tags:
        if len(t) > 1:
            parents[t[:-1]] += 1
    fanout = Counter(parents.values())
    print(f'   internal-node fan-out distribution: {dict(sorted(fanout.items()))}')
    for d in sorted(depths):
        below = sum(1 for t in tags if len(t) > d)
        print(f'   depth {d}: {depths[d]} leaves, {below} tags deeper; '
              f'{depths[d]} + {below // (2 ** (min([x for x in sorted(depths) if x > d], default=d) - d)) if below else 0} '
              f'consistency figure')

    total = sum(r['bytes'] for r in recs)
    print(f'   certificate bytes summed: {total} = {total / 2**30:.2f} GiB '
          f'= {total / 1e9:.2f} GB (published "about 28 GB")')
    print(f'   distinct sha256 values: {len({r["sha256"] for r in recs})}')


if __name__ == '__main__':
    main()
