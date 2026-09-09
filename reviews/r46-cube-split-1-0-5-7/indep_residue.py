r"""reviewer-1: replicate the transferable claim of h3297 — that the residue is
short of case distinctions, not of time. A sample of the published depth-18
survivors is run at 30 s and at 150 s; then some are split one level deeper and
the children are run at 30 s.
"""
import os
import random
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, '../../notes/graph-ramsey-theory/r46-automorphism-obstructions')
import encode

CAD = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/scratch/'
       'r55auto/tools/cadical/build/cadical')
RES = ('../../notes/graph-ramsey-theory/r46-automorphism-obstructions/'
       'residual-1_0-5_7.txt')

NVAR, BASE = encode.build(35, 4, 6, 0, 5, 7, symc=True, syms=True)


def run(tag, cap):
    lits = [(i + 1) if c == '1' else -(i + 1) for i, c in enumerate(tag)]
    cnf = f'r{tag}_{cap}.cnf'
    encode.write_dimacs(cnf, NVAR, BASE + [[x] for x in lits])
    t0 = time.time()
    try:
        r = subprocess.run([CAD, '-q', cnf], capture_output=True, timeout=cap)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    os.remove(cnf)
    return tag, rc, time.time() - t0


def main():
    tags = [l.strip() for l in open(RES) if l.strip() and len(l.strip()) == 18]
    rng = random.Random(11)
    sample = rng.sample(tags, 12)
    print(f'{len(tags)} published depth-18 survivors; my sample of '
          f'{len(sample)}')
    for cap in (30, 150):
        with ThreadPoolExecutor(max_workers=6) as ex:
            res = list(ex.map(lambda t: run(t, cap), sample))
        closed = [t for t, rc, _ in res if rc == 20]
        print(f'   cap {cap:3d} s: {len(closed)} of {len(sample)} closed'
              + (f' {closed}' if closed else ' — none'), flush=True)

    deeper = sample[:3]
    print('   splitting three of them four levels deeper (16 children each), '
          'cap 30 s:')
    for t in deeper:
        kids = [t + f'{i:04b}' for i in range(16)]
        with ThreadPoolExecutor(max_workers=6) as ex:
            res = list(ex.map(lambda x: run(x, 30), kids))
        closed = sum(1 for _, rc, _ in res if rc == 20)
        worst = max(d for _, _, d in res)
        print(f'      {t}: {closed} of 16 children closed, slowest '
              f'{worst:.1f} s', flush=True)


if __name__ == '__main__':
    main()
