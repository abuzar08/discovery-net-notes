"""Refine unresolved cubes by a complete case split on given variables.

refine_p.py picks the split variables from the cycle structure of a type
1^f p^k. The group and arbitrary-cycle-type formulas here are split on the
variables occurring in the most clauses instead, so the variables are passed in
explicitly. Everything else is the same, and in particular the map is written in
the format verify_cnc_p.collapse expects, so the refinement is checked by the
same reviewed code that checks the order-3 and order-5 refinements.

A cube whose last record is UNSAT-VERIFIED is copied unchanged; any other status
is split into the 2^m assignments of the m given variables -- a complete case
distinction, sound with no group argument. A cube with no record at all means an
unfinished run and is an error unless --include-missing is given.

usage: python3 refine_generic.py in.icnf results.jsonl out.icnf map.json v1,v2,...
"""
import sys, json, itertools

argv = [a for a in sys.argv[1:] if not a.startswith('--')]
MISSING_OK = '--include-missing' in sys.argv
inp, results, outp, mapp, vs = argv[0], argv[1], argv[2], argv[3], argv[4]
SPLIT = [int(x) for x in vs.split(',')]

cubes = [[int(t) for t in l.split()[1:-1]] for l in open(inp) if l.startswith('a ')]
last = {}
for line in open(results):
    r = json.loads(line)
    last[r['cube']] = r['status']

missing = [i for i in range(len(cubes)) if i not in last]
if missing and not MISSING_OK:
    sys.exit(f'{len(missing)} cubes have no record (unfinished run); first is {missing[0]}')

for i, c in enumerate(cubes):
    if set(map(abs, c)) & set(SPLIT):
        sys.exit(f'cube {i} already fixes one of the split variables')

out, recs, nref = [], [], 0
for i, c in enumerate(cubes):
    if last.get(i) == 'UNSAT-VERIFIED':
        out.append(c)
        recs.append({'parent': i, 'added': []})
        continue
    nref += 1
    for signs in itertools.product((1, -1), repeat=len(SPLIT)):
        add = [s * v for s, v in zip(signs, SPLIT)]
        out.append(c + add)
        recs.append({'parent': i, 'added': add})

with open(outp, 'w') as fh:
    for c in out:
        fh.write('a ' + ' '.join(map(str, c)) + ' 0\n')
json.dump({'split_vars': SPLIT, 'cubes': recs}, open(mapp, 'w'))
print(f'{len(cubes)} cubes, {nref} refined on {len(SPLIT)} variables {SPLIT} '
      f'-> {len(out)} cubes in {outp}')
