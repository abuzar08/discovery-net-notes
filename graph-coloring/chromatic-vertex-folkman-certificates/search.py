"""CEGAR search for CF(n,k,q): a K_q-free graph on n vertices with chi >= k.

Untrusted search.  Its only durable outputs are
  * on UNSAT: a list of partitions R such that Q(n,q) + {B(P):P in R} is
    already unsatisfiable -- feed that list to encode.py and refute it with
    an external solver to obtain the certificate for n(k,q) > n;
  * on SAT: an explicit graph, which is then checked independently.

Run with:  uv run --with python-sat python3 search.py N K Q [--symbreak]
"""

import sys
import time

from pysat.solvers import Cadical153

import encode


# ---------------------------------------------------------------- colouring

def chromatic_le(adj, n, c):
    """Return a proper c-colouring (list of colours) of adj, or None.

    adj is a list of int bitmasks.  Exact DSATUR-style backtracking with the
    standard "new colours in increasing order" symmetry break.
    """
    colour = [-1] * n
    # forbidden[v] = bitmask of colours already used by neighbours of v
    forbidden = [0] * n
    order_cache = []

    def pick():
        best, best_key = -1, None
        for v in range(n):
            if colour[v] >= 0:
                continue
            sat = bin(forbidden[v]).count("1")
            deg = bin(adj[v]).count("1")
            key = (-sat, -deg)
            if best_key is None or key < best_key:
                best, best_key = v, key
        return best

    def rec(assigned, used):
        if assigned == n:
            return True
        v = pick()
        order_cache.append(v)
        limit = min(used + 1, c)
        for col in range(limit):
            if forbidden[v] >> col & 1:
                continue
            colour[v] = col
            touched = []
            m = adj[v]
            while m:
                b = m & -m
                w = b.bit_length() - 1
                m ^= b
                if colour[w] < 0 and not (forbidden[w] >> col & 1):
                    forbidden[w] |= 1 << col
                    touched.append(w)
            # prune: some uncoloured vertex has all c colours forbidden
            dead = False
            for w in range(n):
                if colour[w] < 0 and forbidden[w] & ((1 << c) - 1) == (1 << c) - 1:
                    dead = True
                    break
            if not dead and rec(assigned + 1, max(used, col + 1)):
                return True
            for w in touched:
                forbidden[w] &= ~(1 << col)
            colour[v] = -1
        order_cache.pop()
        return False

    if rec(0, 0):
        return colour[:]
    return None


def rebalance(adj, n, colour, c):
    """Greedily move vertices to smaller colour classes.

    A partition with fewer monochromatic pairs yields a SHORTER, hence
    logically stronger, blocking clause B(P).  Correctness of the search does
    not depend on this; only clause strength does.
    """
    colour = colour[:]
    improved = True
    while improved:
        improved = False
        sizes = [0] * c
        for v in colour:
            sizes[v] += 1
        for v in range(n):
            cur = colour[v]
            for col in range(c):
                if col == cur or sizes[col] + 1 >= sizes[cur]:
                    continue
                # legal only if no neighbour of v has colour `col`
                ok = True
                m = adj[v]
                while m:
                    b = m & -m
                    w = b.bit_length() - 1
                    m ^= b
                    if colour[w] == col:
                        ok = False
                        break
                if ok:
                    sizes[cur] -= 1
                    sizes[col] += 1
                    colour[v] = col
                    improved = True
                    break
    return colour


def colouring_to_partition(colour, c):
    blocks = [[] for _ in range(c)]
    for v, col in enumerate(colour):
        blocks[col].append(v)
    return [b for b in blocks if b]


def mono_pairs(part):
    return sum(len(b) * (len(b) - 1) // 2 for b in part)


# ------------------------------------------------------------------- search

def run(n, k, q, symbreak=False, mindeg=None, maxindep=None, report=2.0):
    c = k - 1
    idx, pairs = encode.pair_index(n)
    nvar = len(pairs)
    base = encode.clique_clauses(n, q, idx)
    extra = []
    if mindeg is not None:
        extra += encode.mindeg_clauses(n, mindeg, idx)
    if maxindep is not None:
        extra += encode.indep_clauses(n, maxindep, idx)
    if symbreak:
        sb, naux = encode.symbreak_clauses(n, idx)
        extra += sb
        nvar += naux

    solver = Cadical153(bootstrap_with=base + extra)
    partitions = []
    seen = set()
    t0 = time.time()
    last = t0
    it = 0
    while True:
        it += 1
        if not solver.solve():
            return ("UNSAT", partitions, it, time.time() - t0)
        model = solver.get_model()
        pos = set(lit for lit in model if lit > 0)
        adj = [0] * n
        for i, (u, v) in enumerate(pairs):
            if (i + 1) in pos:
                adj[u] |= 1 << v
                adj[v] |= 1 << u

        colour = chromatic_le(adj, n, c)
        if colour is None:
            return ("SAT", adj, it, time.time() - t0)

        colour = rebalance(adj, n, colour, c)
        part = colouring_to_partition(colour, c)
        key = tuple(sorted(tuple(sorted(b)) for b in part))
        if key not in seen:
            seen.add(key)
            partitions.append(part)
        solver.add_clause(encode.block_clause(part, idx))

        now = time.time()
        if now - last > report:
            last = now
            print(f"  it={it} partitions={len(partitions)} "
                  f"last|clause|={mono_pairs(part)} t={now - t0:.1f}s",
                  flush=True)


def main():
    n, k, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rest = sys.argv[4:]
    sb = "--symbreak" in rest
    md = int(rest[rest.index("--mindeg") + 1]) if "--mindeg" in rest else None
    mi = int(rest[rest.index("--maxindep") + 1]) if "--maxindep" in rest else None
    print(f"CF(n={n}, k={k}, q={q})  symbreak={sb} mindeg={md} maxindep={mi}",
          flush=True)
    status, data, it, el = run(n, k, q, symbreak=sb, mindeg=md, maxindep=mi)
    if status == "UNSAT":
        print(f"UNSAT: no K_{q}-free graph on {n} vertices with chi >= {k}")
        print(f"  iterations={it}  partitions={len(data)}  time={el:.1f}s")
        out = f"parts_n{n}_k{k}_q{q}.txt"
        encode.write_partitions(out, data)
        print(f"  partitions written to {out}")
    else:
        adj = data
        print(f"SAT: witness found  iterations={it}  time={el:.1f}s")
        edges = [(u, v) for u in range(n) for v in range(u + 1, n)
                 if adj[u] >> v & 1]
        print(f"  edges({len(edges)}): {edges}")
        with open(f"witness_n{n}_k{k}_q{q}.txt", "w") as f:
            f.write(f"{n}\n")
            for u, v in edges:
                f.write(f"{u} {v}\n")


if __name__ == "__main__":
    main()
