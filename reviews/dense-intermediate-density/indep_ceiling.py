r"""reviewer-1: independent check of the ceiling claim of h3285 (researcher-4).

The claim: an explicit 2-page drawing of \(K_{32}\) with \(Z(32) = 12600\)
crossings, minus 113 edges and re-optimised, leaves a 383-edge drawing with 4644
crossings, so any bound reading only \((n, q)\) is at most 4644 at \((32, 383)\).

I build my own 2-page drawings from scratch: vertices in convex position in a
fixed cyclic order, every edge assigned to one of two pages, and two edges on the
same page cross exactly when their endpoints interleave around the circle. Local
search over page assignments; then my own greedy deletion of 113 edges with
re-optimisation.
"""
import random

N = 32


def Zh(n):
    return (n//2)*((n-1)//2)*((n-2)//2)*((n-3)//2)//4


def interleave(e, f):
    a, b = e
    c, d = f
    if len({a, b, c, d}) < 4:
        return False
    return (a < c < b < d) or (c < a < d < b)


def build(edges):
    """crossing pairs of the convex order, as an adjacency structure"""
    idx = {e: i for i, e in enumerate(edges)}
    cross = [[] for _ in edges]
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            if interleave(edges[i], edges[j]):
                cross[i].append(j)
                cross[j].append(i)
    return cross


def count(page, cross):
    t = 0
    for i, cs in enumerate(cross):
        for j in cs:
            if j > i and page[i] == page[j]:
                t += 1
    return t


def optimise(cross, page, rng, rounds=400):
    """local search: flip the page of one edge while it helps"""
    cur = count(page, cross)
    order = list(range(len(page)))
    for _ in range(rounds):
        rng.shuffle(order)
        moved = False
        for i in order:
            same = sum(1 for j in cross[i] if page[j] == page[i])
            other = len(cross[i]) - same
            if other < same:
                page[i] ^= 1
                cur += other - same
                moved = True
        if not moved:
            break
    return cur


def main():
    rng = random.Random(20260909)
    edges = [(i, j) for i in range(N) for j in range(i + 1, N)]
    cross = build(edges)
    print(f'K_{N}: {len(edges)} edges, Z({N}) = {Zh(N)}')

    best, bestpage = None, None
    for trial in range(12):
        page = [rng.randrange(2) for _ in edges]
        c = optimise(cross, page, rng)
        if best is None or c < best:
            best, bestpage = c, page[:]
    print(f'   my best 2-page drawing of K_{N}: {best} crossings '
          f'({"equals" if best == Zh(N) else "against"} Z({N}) = {Zh(N)})')

    # delete 113 edges, greedily taking the edge in the most same-page crossings
    page = bestpage[:]
    alive = [True] * len(edges)
    for _ in range(113):
        loads = []
        for i in range(len(edges)):
            if not alive[i]:
                continue
            loads.append((sum(1 for j in cross[i] if alive[j] and
                              page[j] == page[i]), i))
        loads.sort(reverse=True)
        alive[loads[0][1]] = False
    sub = [i for i in range(len(edges)) if alive[i]]
    remap = {e: k for k, e in enumerate(sub)}
    subedges = [edges[i] for i in sub]
    subcross = build(subedges)
    p = [page[i] for i in sub]
    c0 = count(p, subcross)
    c1 = optimise(subcross, p, rng)
    bestsub = c1
    for trial in range(8):
        q = [rng.randrange(2) for _ in subedges]
        bestsub = min(bestsub, optimise(subcross, q, rng))
    print(f'   after deleting 113 edges ({len(subedges)} left): {c0} crossings, '
          f'{c1} after re-optimising, {bestsub} best over restarts')
    print(f'   published ceiling 4644: my drawing gives '
          f'{"<= it" if bestsub <= 4644 else "> it"} ({bestsub})')
    print(f'   incumbent 3022 as a fraction of my ceiling: '
          f'{3022 / bestsub:.3f}; of 4644: {3022 / 4644:.3f}')


if __name__ == '__main__':
    main()
