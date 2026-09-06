"""Run cubes of base.cnf (+ residual sym) with per-cube timeout; DRAT -> drat-trim LRAT (xz), delete DRAT.
usage: python3 run_cnc_p.py base.cnf cubes.icnf outdir workers timeout_s [--retry-timeouts]
Resuming skips cubes already UNSAT-VERIFIED, and also cubes whose last record is a
TIMEOUT at a limit at least as long as the current one (they need refinement, not a
rerun) unless --retry-timeouts is given."""
import sys, subprocess, os, json, time, hashlib, concurrent.futures as cf
argv = [a for a in sys.argv[1:] if not a.startswith('--')]; RETRY = '--retry-timeouts' in sys.argv
base, icnf, outd, W, TO = argv[0], argv[1], argv[2], int(argv[3]), int(argv[4])
CAD = '../../tools/cadical/build/cadical'; DT = '../../tools/drat-trim/drat-trim'
hdr = open(base).readline().split(); nv, nc = int(hdr[2]), int(hdr[3])
body = open(base).read().split('\n', 1)[1]
cubes = [l.split()[1:-1] for l in open(icnf) if l.startswith('a')]
os.makedirs(outd, exist_ok=True)
log = open(os.path.join(outd, 'results.jsonl'), 'a')
done = set()
try:
    for l in open(os.path.join(outd, 'results.jsonl')):
        r = json.loads(l)
        if r['status'] == 'UNSAT-VERIFIED': done.add(r['cube'])
        elif r['status'] == 'TIMEOUT' and not RETRY and r.get('solve_s', 0) >= TO: done.add(r['cube'])
        elif r['cube'] in done: done.discard(r['cube'])
except FileNotFoundError: pass
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def run(i):
    if i in done: return None
    cnf = os.path.join(outd, f'c{i}.cnf'); drat = os.path.join(outd, f'c{i}.drat'); lrat = os.path.join(outd, f'c{i}.lrat')
    with open(cnf, 'w') as fh:
        fh.write(f'p cnf {nv} {nc + len(cubes[i])}\n'); fh.write(body)
        for lit in cubes[i]: fh.write(f'{lit} 0\n')
    t0 = time.time()
    r = subprocess.run(['timeout', str(TO), CAD, '-q', '--no-binary', cnf, drat], capture_output=True, text=True)
    t1 = time.time() - t0
    res = {'cube': i, 'solve_s': round(t1, 1), 'exit': r.returncode}
    if r.returncode == 20:
        d = subprocess.run(['timeout', str(4 * TO), DT, cnf, drat, '-L', lrat], capture_output=True, text=True)
        ok = 's VERIFIED' in d.stdout
        res['status'] = 'UNSAT-VERIFIED' if ok else 'UNSAT-TRIM-FAIL'
        if ok:
            res['lrat_bytes'] = os.path.getsize(lrat); res['lrat_sha256'] = sha(lrat)
            subprocess.run(['xz', '-f', '-T2', lrat])
        os.remove(drat)
    elif r.returncode == 10:
        res['status'] = 'SAT'
    else:
        res['status'] = 'TIMEOUT'
        if os.path.exists(drat): os.remove(drat)
    if res['status'] != 'SAT': os.remove(cnf)
    log.write(json.dumps(res) + '\n'); log.flush()
    return res
with cf.ThreadPoolExecutor(W) as ex:
    for r in ex.map(run, range(len(cubes))):
        if r: print(r, flush=True)
print('ALL DONE', flush=True)
