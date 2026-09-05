"""Re-check every stored certificate: regenerate the formula, compare its
SHA-256 with certs.json, replay the LRAT proof with the independent checker.
usage: python3 check_all.py [workdir]      (standard library only)"""
import json, os, sys, subprocess, hashlib, time
here = os.path.dirname(os.path.abspath(__file__))
work = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'regen')
os.makedirs(work, exist_ok=True)
certs = json.load(open(os.path.join(here, 'certs.json')))
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
bad = 0; n = 0
for tag, c in sorted(certs.items(), key=lambda t: t[1]['lrat_xz_bytes']):
    cert = os.path.join(here, 'certificates', tag + '.lrat.xz')
    if not os.path.exists(cert):
        print(f"{tag}: certificate not stored (sha256 {c['sha256']}) - skipped"); continue
    n += 1
    gen = 'encode.py' if c['kind'] == 'base' else 'hybrid.py'
    chk = 'verify.py' if c['kind'] == 'base' else 'verify_hybrid.py'
    cnf = os.path.join(work, tag + '.cnf')
    t = time.time()
    subprocess.run([sys.executable, os.path.join(here, gen), '42', str(c['f']), str(c['p']), str(c['k']), cnf], check=True, capture_output=True)
    ok_cnf = sha(cnf) == c['cnf_sha256']
    ok_cert = sha(cert) == c['sha256']
    r = subprocess.run([sys.executable, os.path.join(here, chk), '42', str(c['f']), str(c['p']), str(c['k']), cnf, cert], capture_output=True, text=True)
    ok = r.returncode == 0 and 'VERIFIED' in r.stdout
    print(f"{tag}: cnf-sha {'ok' if ok_cnf else 'MISMATCH'}, cert-sha {'ok' if ok_cert else 'MISMATCH'}, {chk} {'VERIFIED' if ok else 'FAILED'} ({time.time() - t:.1f} s)", flush=True)
    bad += not (ok and ok_cnf and ok_cert)
print(f"{n - bad}/{n} stored certificates verified" + ("" if bad == 0 else f"; {bad} FAILURES"))
sys.exit(1 if bad else 0)
