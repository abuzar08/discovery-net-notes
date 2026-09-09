r"""reviewer-1: a larger replication of the '150 s closed zero' claim of h3297,
with per-cube solve times."""
import random
import sys
from concurrent.futures import ThreadPoolExecutor

import indep_residue as R

tags = [l.strip() for l in open(R.RES) if l.strip() and len(l.strip()) == 18]
rng = random.Random(11)
first = set(rng.sample(tags, 12))
rest = [t for t in tags if t not in first]
rng2 = random.Random(99)
sample = rng2.sample(rest, 30)
print(f'a further {len(sample)} of the {len(tags)} published depth-18 '
      f'survivors, cap 150 s:')
with ThreadPoolExecutor(max_workers=6) as ex:
    res = list(ex.map(lambda t: R.run(t, 150), sample))
closed = [(t, d) for t, rc, d in res if rc == 20]
print(f'   closed: {len(closed)} of {len(sample)}')
times = sorted(d for _, d in closed)
if times:
    print(f'   solve times of the closures: min {times[0]:.1f} s, median '
          f'{times[len(times)//2]:.1f} s, max {times[-1]:.1f} s')
    print(f'   closures needing more than 30 s: '
          f'{sum(1 for d in times if d > 30)}')
