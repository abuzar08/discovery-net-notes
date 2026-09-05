"""Incremental independent replay of the certificates that are on disk, then delete them.

Same check as step 4 of verify_cnc_p.py (regenerated formula + cube units, LRAT
replayed to the empty clause, SHA-256 of the decompressed LRAT against the
manifest), but run on whatever certificates are currently present so that a long
cube-and-conquer run does not have to keep tens of GB of proofs. Every result is
appended to <certdir>/verified.jsonl; verified certificates are deleted unless
--keep is given. The formula and cube checks (steps 1-3) stay in verify_cnc_p.py
and are run once at the end over the whole cube set.

usage: python3 sweep_verify.py f p k L cubes.icnf formula.cnf manifest.json certdir [--jobs N] [--keep] [--refine map.json]
"""
import sys, os, json
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_cnc_p as V

def main():
    argv = sys.argv[1:]; jobs = 4; keep = '--keep' in argv
    if '--jobs' in argv:
        i = argv.index('--jobs'); jobs = int(argv[i + 1]); del argv[i:i + 2]
    if '--refine' in argv:
        i = argv.index('--refine'); del argv[i:i + 2]  # child cubes are read from the .icnf itself
    args = [a for a in argv if not a.startswith('--')]
    f, p, k, L = map(int, args[:4]); icnf, cnfpath, manpath, certdir = args[4:8]
    nvfile, cls = V.read_dimacs(cnfpath)
    manifest = json.load(open(manpath))
    cubes = [list(map(int, l.split()[1:-1])) for l in open(icnf) if l.startswith('a ')]
    seen = set()
    vpath = os.path.join(certdir, 'verified.jsonl')
    if os.path.exists(vpath):
        for l in open(vpath):
            r = json.loads(l)
            if r['status'] == 'VERIFIED': seen.add(r['cube'])
    todo = [(i, c) for i, c in enumerate(cubes)
            if i not in seen and os.path.exists(os.path.join(certdir, f'c{i}.lrat.xz'))]
    print(f'{len(cubes)} cubes, {len(seen)} already replayed, {len(todo)} certificates on disk to replay', flush=True)
    out = open(vpath, 'a'); counts = {}
    with Pool(jobs, initializer=V._init_kw, initargs=({'cls': cls, 'certdir': certdir, 'manifest': manifest},)) as pool:
        for i, res in pool.imap_unordered(V.check_cube, todo, chunksize=1):
            counts[res] = counts.get(res, 0) + 1
            rec = manifest.get(str(i), {})
            out.write(json.dumps({'cube': i, 'status': res, 'sha256': rec.get('sha256'), 'bytes': rec.get('bytes'), 'cube_lits': cubes[i]}) + '\n'); out.flush()
            if res != 'VERIFIED': print(f'cube {i}: {res}', flush=True)
            elif not keep: os.remove(os.path.join(certdir, f'c{i}.lrat.xz'))
    print('replayed:', ', '.join(f'{v} {k}' for k, v in sorted(counts.items())))
    sys.exit(0 if set(counts) <= {'VERIFIED'} else 1)

if __name__ == '__main__':
    main()
