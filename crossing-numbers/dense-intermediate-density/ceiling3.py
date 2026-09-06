"""Ceiling, seeded from the greedy deletion of an optimal K_32 drawing."""
import random
import sys

from ceiling import build, optimise, greedy_delete


def reopt_pages(keptset, inter, page):
    improved = True
    while improved:
        improved = False
        for i in keptset:
            same = sum(1 for j in inter[i] if j in keptset and page[j] == page[i])
            other = sum(1 for j in inter[i] if j in keptset) - same
            if other < same:
                page[i] ^= 1
                improved = True
    return page


def count(keptset, inter, page):
    return sum(1 for i in keptset for j in inter[i]
               if j > i and j in keptset and page[j] == page[i])


if __name__ == '__main__':
    n, K = 32, 113
    E, idx, inter = build(n)
    c0, page = optimise(E, inter)
    tot, rem, alive = greedy_delete(E, inter, page, K)
    keptset = {i for i in range(len(E)) if alive[i]}
    dele = set(range(len(E))) - keptset
    page = reopt_pages(keptset, inter, page)
    best = count(keptset, inter, page)
    print(f"seed: K_32 drawing {c0:,}; after greedy deletion + page re-opt: "
          f"{best:,}", flush=True)
    rnd = random.Random(11)
    stall = 0
    for it in range(4000):
        load = {i: sum(1 for j in inter[i] if j in keptset and page[j] == page[i])
                for i in keptset}
        gain = {d: sum(1 for j in inter[d] if j in keptset and page[j] == page[d])
                for d in dele}
        h = max(load, key=lambda i: load[i])
        cands = sorted(gain, key=lambda i: gain[i])[:8]
        l = rnd.choice(cands)
        if load[h] <= gain[l]:
            stall += 1
            if stall > 60:
                break
            continue
        keptset.discard(h); dele.add(h)
        keptset.add(l); dele.discard(l)
        page = reopt_pages(keptset, inter, page)
        c = count(keptset, inter, page)
        if c < best:
            best = c
            stall = 0
        else:
            stall += 1
        if it % 400 == 0:
            print(f"   it {it}: current {c:,}  best {best:,}", flush=True)
    print(f"\nbest 32-vertex 383-edge drawing: {best:,} crossings")
    print(f"=> L(32,383) <= {best:,} for ANY bound depending only on (n,q)")
    print(f"   current sampling bound 3022; target 3557; ceiling {best:,}")
