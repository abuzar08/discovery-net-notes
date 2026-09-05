"""Conquer phase: solve hybrid CNF + cube units for every cube of an icnf file.
usage: [CADICAL=... DRATTRIM=...] python3 run_cnc.py cubes.icnf formula.cnf outdir workers timelimit_s [--lrat] [cube indices...]
Solves formula.cnf + unit clauses of each cube with CaDiCaL (DRAT), verifies with drat-trim (-L: trimmed LRAT),
xz-compresses the LRAT and deletes the DRAT. Appends to outdir/results.jsonl (idx, cube, status, time, drat_bytes,
drat_trim verdict, lrat_xz_bytes, sha256); rerunning skips cubes already recorded."""
import sys, os, subprocess, time, json, hashlib, random
from concurrent.futures import ThreadPoolExecutor
CADICAL = os.environ.get('CADICAL', 'cadical')      # CaDiCaL binary (3.0.1 used)
DRATTRIM = os.environ.get('DRATTRIM', 'drat-trim')  # drat-trim binary
icnf, hyb, out, workers, tl = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
want_lrat = '--lrat' in sys.argv
only = [int(a) for a in sys.argv[6:] if a.isdigit()]
os.makedirs(out, exist_ok=True)
cubes = [list(map(int, l.split()[1:-1])) for l in open(icnf) if l.startswith('a ')]
hdr = None; body = []
with open(hyb) as fh:
    for l in fh:
        if l.startswith('c'): continue
        if l.startswith('p'): hdr = l.split(); continue
        body.append(l)
nv, ncl = int(hdr[2]), int(hdr[3])
bodytxt = ''.join(body)
done = set()
resf = os.path.join(out, 'results.jsonl')
if os.path.exists(resf):
    for l in open(resf):
        try: done.add(json.loads(l)['idx'])
        except: pass
lock = __import__('threading').Lock()
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def one(i):
    cube = cubes[i]
    cnf = os.path.join(out, f'c{i}.cnf'); drat = os.path.join(out, f'c{i}.drat')
    with open(cnf, 'w') as fh:
        fh.write(f'p cnf {nv} {ncl + len(cube)}\n'); fh.write(bodytxt)
        for l in cube: fh.write(f'{l} 0\n')
    t = time.time()
    try:
        r = subprocess.run([CADICAL, '-q', '-t', str(int(tl)), '--binary=false', cnf, drat], capture_output=True, text=True)
        status = 'UNSAT' if 's UNSATISFIABLE' in r.stdout else 'SAT' if 's SATISFIABLE' in r.stdout else 'TIMEOUT'
    except Exception as e:
        status = 'ERROR ' + str(e)
    dt = time.time() - t
    rec = {'idx': i, 'cube': cube, 'status': status, 'time': round(dt, 2), 'drat_bytes': os.path.getsize(drat) if os.path.exists(drat) else None}
    if status == 'SAT':
        rec['model'] = r.stdout
    if status == 'UNSAT' and want_lrat:
        lrat = os.path.join(out, f'c{i}.lrat')
        r2 = subprocess.run([DRATTRIM, cnf, drat, '-L', lrat], capture_output=True, text=True)
        rec['drat_trim'] = 'VERIFIED' if 's VERIFIED' in r2.stdout else 'FAILED'
        subprocess.run(['xz', '-9', '-T', '2', '-f', lrat], check=True)
        rec['lrat_xz_bytes'] = os.path.getsize(lrat + '.xz'); rec['sha256'] = sha(lrat + '.xz')
    if os.path.exists(drat) and status != 'TIMEOUT': os.remove(drat)
    if os.path.exists(drat) and status == 'TIMEOUT': os.remove(drat)
    os.remove(cnf)
    with lock:
        with open(resf, 'a') as fh: fh.write(json.dumps(rec) + '\n')
        print(f"cube {i} {status} {dt:.1f}s drat {rec['drat_bytes']}" + (f" lrat.xz {rec.get('lrat_xz_bytes')}" if want_lrat else ''), flush=True)
    return rec
todo = [i for i in (only if only else range(len(cubes))) if i not in done]
with ThreadPoolExecutor(workers) as ex:
    list(ex.map(one, todo))
