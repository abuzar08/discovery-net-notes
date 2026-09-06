"""Carry verified cubes over to a refined cube file.

When hard cubes are refined (refine_p.py) the surviving cubes keep exactly their
literals, so a cube of the new .icnf whose literals were already refuted and whose
certificate was already replayed (sweep log) does not have to be solved again.
This writes matching UNSAT-VERIFIED records into the new run's results.jsonl (the
driver skips them) with the old certificate's hash, so that the final
verify_cnc_p.py --verified <sweep logs> accepts them by literal match.

usage: python3 seed_results.py new.icnf old_verified.jsonl [more.jsonl ...] > new_dir/results.jsonl
"""
import sys, json
cubes = [tuple(map(int, l.split()[1:-1])) for l in open(sys.argv[1]) if l.startswith('a ')]
prev = {}
for path in sys.argv[2:]:
    for line in open(path):
        r = json.loads(line)
        if r.get('status') in ('VERIFIED', 'UNSAT-VERIFIED') and r.get('cube_lits'):
            prev[tuple(r['cube_lits'])] = r
n = 0
for i, c in enumerate(cubes):
    r = prev.get(c)
    if r:
        n += 1
        print(json.dumps({'cube': i, 'solve_s': 0.0, 'exit': 20, 'status': 'UNSAT-VERIFIED',
                          'lrat_bytes': r.get('bytes', r.get('lrat_bytes')), 'lrat_sha256': r.get('sha256', r.get('lrat_sha256')),
                          'cube_lits': list(c),
                          'carried_from': {'cube': r['cube'], 'log': sys.argv[2]}}))
print(f'{n} of {len(cubes)} cubes carried over as already verified', file=sys.stderr)
