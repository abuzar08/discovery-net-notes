"""Add the cube literals to records that lack them.

seed_results.py used to write a carried record without `cube_lits`, so the final
verify_cnc_p.py --verified could not match those cubes by literals. The literals
are recovered from the run's own .icnf by index: the carried record was created
by matching literals against the earlier log in the first place, so index and
literals agree by construction. Records that already carry literals are checked
against the file and left alone.

usage: python3 backfill_lits.py cubes.icnf results.jsonl
"""
import sys, json, os
icnf, path = sys.argv[1], sys.argv[2]
cubes = [[int(x) for x in l.split()[1:-1]] for l in open(icnf) if l.startswith('a ')]
out, added, checked = [], 0, 0
for line in open(path):
    r = json.loads(line)
    if r.get('cube_lits') is None:
        if r['cube'] < len(cubes):
            r['cube_lits'] = cubes[r['cube']]; added += 1
    else:
        assert r['cube_lits'] == cubes[r['cube']], f"cube {r['cube']} literals disagree with {icnf}"
        checked += 1
    out.append(json.dumps(r))
tmp = path + '.tmp'
open(tmp, 'w').write('\n'.join(out) + '\n')
os.replace(tmp, path)
print(f'{added} records given literals, {checked} already agreed with {os.path.basename(icnf)}')
