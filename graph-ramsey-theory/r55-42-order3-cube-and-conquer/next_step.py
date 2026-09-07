"""Report the state of one type's cube-and-conquer run and the exact next command.

The loop for a type 1^f p^k is always the same: sweep the cube set at a short
limit, re-attempt the survivors at a longer one, split what still survives, and
when nothing is left run the chained check. This prints where a run stands and
which command comes next, so that the decision is made from the recorded numbers
rather than from memory.

usage: python3 next_step.py f p k L base.cnf cubes.icnf outdir [map1,map2,...]
"""
import sys, json, os, collections

f, p, k, L = map(int, sys.argv[1:5])
base, icnf, outd = sys.argv[5:8]
maps = sys.argv[8] if len(sys.argv) > 8 else ''

cubes = sum(1 for l in open(icnf) if l.startswith('a '))
rec = {}
path = os.path.join(outd, 'results.jsonl')
if os.path.exists(path):
    for line in open(path):
        r = json.loads(line); rec[r['cube']] = r
counts = collections.Counter(r['status'].split(':')[0] for r in rec.values())
verified = counts.get('UNSAT-VERIFIED', 0)
hard = [i for i, r in rec.items() if r['status'] != 'UNSAT-VERIFIED']
missing = cubes - len(rec)
limits = sorted({r.get('solve_s', 0) for i, r in rec.items() if r['status'] == 'TIMEOUT'})
print(f'type 1^{f} {p}^{k}, level {L}: {cubes} cubes, {verified} verified, '
      f'{len(hard)} unresolved, {missing} not yet attempted')
print(' statuses:', dict(counts))
if limits: print(' limits at which cubes timed out:', limits[-3:])

nxt = None
if missing:
    nxt = f'python3 run_lrat_p.py {base} {icnf} {outd} 4 20        # finish the sweep'
elif hard:
    tried = max(limits) if limits else 0
    if tried < 300:
        nxt = (f'python3 run_lrat_p.py {base} {icnf} {outd} 3 300 --retry-timeouts'
               f'   # escalate the {len(hard)} survivors')
    else:
        nxt = (f'python3 refine_p.py {icnf} {outd}/results.jsonl <new.icnf> <new_map.json> {f} {p} {k} {L}\n'
               f'  then seed_results.py and run_lrat_p.py on the refined file'
               f'   # split the {len(hard)} survivors')
else:
    nxt = (f'python3 manifest_p.py {icnf} {outd}/results.jsonl {outd}/manifest.json && \\\n'
           f'  python3 verify_cnc_p.py {f} {p} {k} {L} {icnf} {base} {outd}/manifest.json {outd}'
           + (f' --refine {maps}' if maps else '')
           + f' --complete-from level{L-1}_p{p}.json --verified {outd}/results.jsonl --jobs 4')
print('next:', nxt)
