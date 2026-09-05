"""reviewer-1: compare an independently regenerated cube-and-conquer directory with the
manifest in certs.json (per-cube SHA-256 and size), check the cube CNFs are exactly the
base formula (own union-find construction) plus one unit clause per cube literal, that the
64 cubes are all sign patterns on variables 1..6, and replay every cube LRAT with drat-trim's
lrat-check.   usage: python compare_cubes.py certs.json CUBEDIR LRATCHECK"""
import hashlib, itertools, json, os, subprocess, sys
from indep_orbit_encode import build, read_cnf
J = json.load(open(sys.argv[1])); d = sys.argv[2]; LC = sys.argv[3]
man = [c for c in J['cube_certificates'] if c['tag'] == os.path.basename(d.rstrip('/'))][0]
n, f, p, k = man['n'], man['f'], man['p'], man['k']; D = len(man['split_vars'])
nv, base = build(n, 4, 6, f, p, k)
want = {tuple((i + 1) if b else -(i + 1) for i, b in enumerate(sg)) for sg in itertools.product((True, False), repeat=D)}
print(f"type 1^{f} {p}^{k} n={n}: own base vars={nv} clauses={len(base)}; manifest cubes={man['n_cubes']}")
hash_ok = size_ok = cnf_ok = ver_ok = 0; seen = set(); total = 0
for cube in sorted(want):
    tag = "c" + "".join("1" if x > 0 else "0" for x in cube)
    cnf, lrat = os.path.join(d, tag + ".cnf"), os.path.join(d, tag + ".lrat")
    if not (os.path.exists(cnf) and os.path.exists(lrat)):
        print("  MISSING", tag); continue
    seen.add(cube)
    gv, gc = read_cnf(cnf)
    exp = set(base) | {frozenset([x]) for x in cube}
    ok = gv == nv and set(gc) == exp and len(gc) == len(exp); cnf_ok += ok
    h = hashlib.sha256(open(lrat, 'rb').read()).hexdigest(); sz = os.path.getsize(lrat); total += sz
    m = man['cubes'][tag]; hash_ok += (h == m['sha256']); size_ok += (sz == m['bytes'])
    out = subprocess.run([LC, cnf, lrat], capture_output=True, text=True).stdout
    v = 'c VERIFIED' in out; ver_ok += v
    print(f"  {tag}: cnf=base+cube {ok}  sha256 {'match' if h == m['sha256'] else 'DIFFERS'}  bytes {sz} ({'=' if sz == m['bytes'] else '!='} manifest)  lrat-check {'VERIFIED' if v else 'FAILED'}")
print(f"cubes present: {len(seen)}/{2**D}, all sign patterns exactly once: {seen == want}")
print(f"cnf ok {cnf_ok}/{len(seen)}, sha256 matches {hash_ok}/{len(seen)}, sizes match {size_ok}/{len(seen)}, lrat-check VERIFIED {ver_ok}/{len(seen)}, total LRAT {total/1048576:.1f} MB (manifest {man['total_lrat_bytes']/1048576:.1f} MB)")
