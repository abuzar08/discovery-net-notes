"""reviewer-1: independent replay of the 1576 cube certificates of h2873.

For each cube of the .icnf: build (formula + cube units) exactly as the target's
driver does, re-solve with CaDiCaL, run drat-trim -L, compare the LRAT size and
SHA-256 with the target's manifest, then verify the LRAT with lrat-check (a
checker the target does not use) and delete every large file.  Appends one JSON
record per cube to replay.jsonl; re-runnable (finished cubes are skipped).

usage: python3 replay.py CNF ICNF MANIFEST OUTDIR WORKERS [ONLY_JSON]
  ONLY_JSON: optional path to a JSON list of cube indices to run.
"""
import sys, os, json, time, hashlib, subprocess, concurrent.futures as cf

CNF, ICNF, MAN, OUT, W = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
ONLY = json.load(open(sys.argv[6])) if len(sys.argv) > 6 else None
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'r46', 'tools')
CAD = os.path.join(TOOLS, 'cadical', 'build', 'cadical')
DT = os.path.join(TOOLS, 'drat-trim', 'drat-trim')
LC = os.path.join(TOOLS, 'drat-trim', 'lrat-check')

hdr = open(CNF).readline().split()
nv, nc = int(hdr[2]), int(hdr[3])
body = open(CNF).read().split('\n', 1)[1]
cubes = [l.split()[1:-1] for l in open(ICNF) if l.startswith('a')]
man = json.load(open(MAN))
os.makedirs(OUT, exist_ok=True)
logp = os.path.join(OUT, 'replay.jsonl')
done = set()
if os.path.exists(logp):
    for l in open(logp):
        try:
            r = json.loads(l)
        except ValueError:
            continue
        if r.get('ok'):
            done.add(r['cube'])
log = open(logp, 'a')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def manrec(i):
    """the manifest's record for cube i, whatever its layout"""
    if isinstance(man, dict):
        for key in ('cubes', 'certificates', 'entries'):
            if key in man:
                return man[key][i] if isinstance(man[key], list) else man[key][str(i)]
        return man[str(i)]
    return man[i]


def run(i):
    if i in done:
        return None
    cnf = os.path.join(OUT, f'r{i}.cnf')
    drat = os.path.join(OUT, f'r{i}.drat')
    lrat = os.path.join(OUT, f'r{i}.lrat')
    with open(cnf, 'w') as fh:
        fh.write(f'p cnf {nv} {nc + len(cubes[i])}\n')
        fh.write(body)
        for lit in cubes[i]:
            fh.write(f'{lit} 0\n')
    rec = {'cube': i}
    t0 = time.time()
    r = subprocess.run([CAD, '-q', '--no-binary', cnf, drat], capture_output=True, text=True)
    rec['solve_s'] = round(time.time() - t0, 1)
    rec['cadical_exit'] = r.returncode
    rec['unsat'] = r.returncode == 20 and 's UNSATISFIABLE' in r.stdout
    if rec['unsat']:
        t0 = time.time()
        d = subprocess.run([DT, cnf, drat, '-L', lrat], capture_output=True, text=True)
        rec['trim_s'] = round(time.time() - t0, 1)
        rec['trim_verified'] = 's VERIFIED' in d.stdout
        if rec['trim_verified']:
            m = manrec(i)
            rec['lrat_bytes'] = os.path.getsize(lrat)
            rec['lrat_sha256'] = sha(lrat)
            rec['bytes_match'] = rec['lrat_bytes'] == m.get('lrat_bytes', m.get('bytes'))
            rec['sha_match'] = rec['lrat_sha256'] == m.get('lrat_sha256', m.get('sha256'))
            c = subprocess.run([LC, cnf, lrat], capture_output=True, text=True)
            rec['lrat_check'] = 'c VERIFIED' in c.stdout
    for p in (drat, lrat, cnf):
        if os.path.exists(p):
            os.remove(p)
    rec['ok'] = bool(rec.get('unsat') and rec.get('trim_verified') and rec.get('bytes_match')
                     and rec.get('sha_match') and rec.get('lrat_check'))
    log.write(json.dumps(rec) + '\n')
    log.flush()
    return rec


todo = ONLY if ONLY is not None else list(range(len(cubes)))
bad = 0
with cf.ThreadPoolExecutor(W) as ex:
    for r in ex.map(run, todo):
        if r and not r['ok']:
            bad += 1
            print('FAIL', json.dumps(r), flush=True)
print(f'ALL DONE cubes={len(todo)} failures={bad}', flush=True)
