"""Solve cubes with CaDiCaL writing LRAT directly, replay every proof with the
independent checker, then delete the proof.

CaDiCaL 3.0.1 emits LRAT itself (--lrat=true --no-binary), so drat-trim is not
needed: the proof that matters is the one replayed by verify_cnc_p.check_lrat
against the formula regenerated from its definition. Removing the drat-trim and
xz stages removes what measurement showed to be the dominant cost (for one
1^2 5^8 child: 73 s solve, then drat-trim still running after 80 minutes; with
native LRAT the same child takes 84 s to solve and 23 s to replay).

Each cube produces one record in <outdir>/results.jsonl:
  {cube, solve_s, replay_s, status, lrat_bytes, lrat_sha256, cube_lits}
with status UNSAT-VERIFIED (refuted and replayed to the empty clause), TIMEOUT,
SAT, or REPLAY-FAILED. Certificates are deleted after a successful replay unless
--keep is given; their SHA-256 stays in the record, so a later
verify_cnc_p.py --verified <results.jsonl> accepts the cube by literal match.
Resuming skips cubes already UNSAT-VERIFIED and cubes that timed out at a limit
at least as long as the current one (--retry-timeouts overrides).

usage: [CADICAL=path] python3 run_lrat_p.py base.cnf cubes.icnf outdir workers timeout_s [--keep] [--retry-timeouts]
"""
import sys, os, json, time, hashlib, subprocess
import concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_cnc_p import read_dimacs, check_lrat

argv = [a for a in sys.argv[1:] if not a.startswith('--')]
KEEP = '--keep' in sys.argv; RETRY = '--retry-timeouts' in sys.argv
BASE, ICNF, OUTD, W, TO = argv[0], argv[1], argv[2], int(argv[3]), int(argv[4])
CAD = os.environ.get('CADICAL', '../../tools/cadical/build/cadical')

_hdr = open(BASE).readline().split()
NV, NC = int(_hdr[2]), int(_hdr[3])
CUBES = [l.split()[1:-1] for l in open(ICNF) if l.startswith('a')]
os.makedirs(OUTD, exist_ok=True)

_CLS = None
def formula():
    global _CLS
    if _CLS is None:
        _CLS = read_dimacs(BASE)[1]
    return _CLS

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def run(i):
    cube = CUBES[i]
    cnf = os.path.join(OUTD, f'c{i}.cnf'); lrat = os.path.join(OUTD, f'c{i}.lrat')
    rec = {'cube': i}
    try:
        with open(cnf, 'w') as fh:
            fh.write(f'p cnf {NV} {NC + len(cube)}\n')
            fh.write(open(BASE).read().split('\n', 1)[1])
            for lit in cube: fh.write(f'{lit} 0\n')
        t0 = time.time()
        r = subprocess.run(['timeout', str(TO), CAD, '-q', '--lrat=true', '--no-binary', cnf, lrat],
                           capture_output=True, text=True)
        rec['solve_s'] = round(time.time() - t0, 1); rec['exit'] = r.returncode
        if r.returncode == 20:
            rec['lrat_bytes'] = os.path.getsize(lrat); rec['lrat_sha256'] = sha256_of(lrat)
            t1 = time.time()
            ok = check_lrat(formula() + [[int(l)] for l in cube], lrat)
            rec['replay_s'] = round(time.time() - t1, 1)
            rec['status'] = 'UNSAT-VERIFIED' if ok else 'REPLAY-FAILED'
            if ok and not KEEP: os.remove(lrat)
        elif r.returncode == 10:
            rec['status'] = 'SAT'
        else:
            rec['status'] = 'TIMEOUT'
            if os.path.exists(lrat): os.remove(lrat)
        rec['cube_lits'] = [int(l) for l in cube]
    except Exception as e:                      # never let one cube kill the run
        rec['status'] = f'ERROR: {type(e).__name__}: {e}'
    finally:
        if os.path.exists(cnf) and rec.get('status') != 'SAT': os.remove(cnf)
    return rec

def main():
    done = set()
    path = os.path.join(OUTD, 'results.jsonl')
    if os.path.exists(path):
        for l in open(path):
            r = json.loads(l)
            if r['status'] == 'UNSAT-VERIFIED': done.add(r['cube'])
            elif r['status'] == 'TIMEOUT' and not RETRY and r.get('solve_s', 0) >= TO: done.add(r['cube'])
            elif r['cube'] in done: done.discard(r['cube'])
    todo = [i for i in range(len(CUBES)) if i not in done]
    print(f'{len(CUBES)} cubes, {len(done)} skipped, {len(todo)} to run', flush=True)
    log = open(path, 'a')
    with cf.ProcessPoolExecutor(W) as ex:
        for rec in ex.map(run, todo, chunksize=1):
            log.write(json.dumps(rec) + '\n'); log.flush()
            if rec['status'] != 'UNSAT-VERIFIED': print(rec, flush=True)
    print('ALL DONE', flush=True)

if __name__ == '__main__':
    main()
