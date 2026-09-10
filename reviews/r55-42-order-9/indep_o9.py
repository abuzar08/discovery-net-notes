r"""reviewer-1: my own orbit encoding for automorphisms of a \((5,5,42)\)-graph,
written to check the order-9 exclusions of the r55-42-order-9-automorphisms lane.

For a permutation \(\sigma\) of the 42 vertices, a \(\sigma\)-invariant graph is
exactly an assignment of Booleans to the \(\sigma\)-orbits of vertex pairs. The
graph is a \((5,5,42)\)-graph iff no 5-set is complete and no 5-set is empty, so
for every 5-subset there are two clauses, one all-negative and one all-positive,
over the orbit variables of its ten pairs. UNSAT means no \((5,5,42)\)-graph
admits an automorphism of that cycle type.
"""
import itertools
import subprocess
import sys
import time

N = 42
CAD = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/scratch/'
       'r55auto/tools/cadical/build/cadical')
DT = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/scratch/'
      'r55auto/tools/drat-trim/drat-trim')


def perm_from_type(cycles):
    """cycles: list of cycle lengths summing to N"""
    p = list(range(N))
    at = 0
    for L in cycles:
        block = list(range(at, at + L))
        for i, v in enumerate(block):
            p[v] = block[(i + 1) % L]
        at += L
    assert at == N
    return p


def pair_orbits(p):
    idx = {}
    for u in range(N):
        for v in range(u + 1, N):
            idx[(u, v)] = None
    orb = {}
    nxt = 0
    for u in range(N):
        for v in range(u + 1, N):
            key = (u, v)
            if orb.get(key) is not None:
                continue
            a, b = u, v
            cyc = []
            while True:
                e = (min(a, b), max(a, b))
                if orb.get(e) is not None:
                    break
                cyc.append(e)
                orb[e] = nxt
                a, b = p[a], p[b]
            nxt += 1
    return orb, nxt


def build(cycles, path):
    p = perm_from_type(cycles)
    orb, north = pair_orbits(p)
    cls = set()
    for S in itertools.combinations(range(N), 5):
        vs = sorted({orb[(a, b)] for a, b in itertools.combinations(S, 2)})
        cls.add(tuple(-(x + 1) for x in vs))
        cls.add(tuple((x + 1) for x in vs))
    with open(path, 'w') as fh:
        fh.write(f'p cnf {north} {len(cls)}\n')
        for c in sorted(cls):
            fh.write(' '.join(str(x) for x in c) + ' 0\n')
    return north, len(cls)


def run(name, cycles, proof=False):
    cnf = f'{name}.cnf'
    t0 = time.time()
    nv, nc = build(cycles, cnf)
    t1 = time.time()
    args = [CAD, '-q', '--binary=false', cnf] + ([f'{name}.drat'] if proof else [])
    r = subprocess.run(args, capture_output=True, timeout=7200)
    t2 = time.time()
    verdict = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, f'rc={r.returncode}')
    print(f'{name}: {nv} orbit variables, {nc} deduplicated clauses '
          f'(encode {t1-t0:.0f} s) -> {verdict} in {t2-t1:.1f} s', flush=True)
    if proof and r.returncode == 20:
        v = subprocess.run([DT, cnf, f'{name}.drat'], capture_output=True,
                           text=True, timeout=7200)
        ok = 's VERIFIED' in v.stdout
        print(f'   drat-trim: {"s VERIFIED" if ok else v.stdout.strip()[:200]}',
              flush=True)
    return verdict


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    types = {
        '1^6 9^4': [1] * 6 + [9] * 4,
        '1^3 3^1 9^4': [1] * 3 + [3] + [9] * 4,
        '3^2 9^4': [3, 3] + [9] * 4,
        '1^9 3^11': [1] * 9 + [3] * 11,
    }
    for name, cyc in types.items():
        if which != 'all' and which != name:
            continue
        run(name.replace(' ', '_').replace('^', ''), cyc,
            proof=True)
