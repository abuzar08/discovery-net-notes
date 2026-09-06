r"""reviewer-1: independent replay of the 19741 cube certificates of h2621.

For each cube of `level3.icnf`: build (formula + cube units) as the target's own
driver does, re-solve with CaDiCaL, run drat-trim to emit an LRAT, verify that
LRAT with `lrat-check` (a checker the target's own pipeline does not use),
compress with the same `xz -9 -T 2` settings and compare the SHA-256 with the
manifest — the manifest hashes the compressed file, so a mismatch there is not by
itself a defect, and the verdict that matters is the pair (drat-trim VERIFIED,
lrat-check c VERIFIED). Every large file is deleted immediately.

usage: python3 replay7.py CNF ICNF MANIFEST OUTDIR WORKERS [FIRST LAST]
"""
import sys, os, json, time, hashlib, subprocess, concurrent.futures as cf

CNF, ICNF, MAN, OUT, W = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
FIRST = int(sys.argv[6]) if len(sys.argv) > 6 else 0
LAST = int(sys.argv[7]) if len(sys.argv) > 7 else None
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
    rec['solve_s'] = round(time.time() - t0, 2)
    rec['unsat'] = r.returncode == 20 and 's UNSATISFIABLE' in r.stdout
    if rec['unsat']:
        d = subprocess.run([DT, cnf, drat, '-L', lrat], capture_output=True, text=True)
        rec['trim_verified'] = 's VERIFIED' in d.stdout
        if rec['trim_verified']:
            c = subprocess.run([LC, cnf, lrat], capture_output=True, text=True)
            rec['lrat_check'] = 'c VERIFIED' in c.stdout
            subprocess.run(['xz', '-9', '-T', '2', '-f', lrat], check=False)
            xzp = lrat + '.xz'
            if os.path.exists(xzp):
                rec['xz_sha'] = sha(xzp)
                rec['xz_match'] = rec['xz_sha'] == man[str(i)]['sha256']
                os.remove(xzp)
    for p in (drat, lrat, cnf):
        if os.path.exists(p):
            os.remove(p)
    rec['ok'] = bool(rec.get('unsat') and rec.get('trim_verified') and rec.get('lrat_check'))
    log.write(json.dumps(rec) + '\n')
    log.flush()
    return rec


todo = list(range(FIRST, LAST if LAST is not None else len(cubes)))
bad = 0
with cf.ThreadPoolExecutor(W) as ex:
    for r in ex.map(run, todo):
        if r and not r['ok']:
            bad += 1
            print('FAIL', json.dumps(r), flush=True)
print(f'ALL DONE cubes={len(todo)} failures={bad}', flush=True)
