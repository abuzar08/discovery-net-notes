"""Independent checker for the cube-and-conquer refutation of a cycle type 1^f p^k
(a (5,5,42)-graph with an automorphism having f fixed points and k cycles of
prime length p), with level-L canonical Z_p-prefix cubes, hybrid formula,
fixed-vertex lex-leader clauses (L) and residual free-cycle clauses (S).

Certificate = (cubes.icnf, formula.cnf, manifest.json, certificates c<i>.lrat.xz).
Checks (standard library only, code written separately from the generators):
  1. formula.cnf is exactly: hybrid formula of the type (verify_hybrid.regenerate)
     + lex-leader clauses (verify_symF.lex_clauses) + residual clauses S
     regenerated here from their definition (for each free cycle j >= L the word
     W_0j = (x(c0, c_j+r))_r is the least of its p rotations; consecutive free
     cycles have val(W_0j) <= val(W_0l)), as multisets of clauses;
  2. every cube fixes exactly the orbit variables of the first L cycles
     (internal distances 1..(p-1)/2 and the p cross variables per pair) and,
     decoded as a Z_p-graph on L cycles, is (5,5)-good and equal to its own
     canonical form under the full group complement x Z_p^* x S_L x Z_p^(L-1)
     (brute force); cubes are pairwise distinct;
  3. completeness (exact, orbit-stabiliser): the number of labelled (5,5)-good
     Z_p-graphs on L cycles (brute force over all 2^L * 2^(p*C(L,2)) labelled
     graphs) equals sum over cubes of |group| / |stabiliser(cube)|;
  4. every certificate c<i>.lrat.xz decompresses to the LRAT text whose SHA-256 is
     recorded in the manifest and
     is a valid LRAT refutation of formula.cnf + the unit clauses of cube i
     (clause ids: file order, then the cube literals in cube order).
usage: python3 verify_cnc_p.py f p k L cubes.icnf formula.cnf manifest.json certdir [--jobs N] [--skip-lrat] [--skip-complete]
Exit status 0 iff everything checked passed."""
import sys, os, json, itertools, hashlib, lzma
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for d in (os.path.join(HERE, '..', 'r55-42-fixed-vertex-lex-leader'),):
    if os.path.exists(os.path.join(d, 'verify_symF.py')): sys.path.insert(0, d)
for d in (os.path.join(HERE, '..', 'r55-42-prime-order-automorphisms'), os.path.join(HERE, '..'), os.path.join(HERE, '..', '..', '..', 'notes', 'graph-ramsey-theory', 'r55-42-prime-order-automorphisms')):
    if os.path.exists(os.path.join(d, 'verify.py')): sys.path.insert(0, d); break
from verify import read_dimacs, check_lrat, sha256
from verify_hybrid import regenerate, orbit_var
from verify_symF import lex_clauses

N = 42

def rot(W, t, p): return sum(1 << ((r + t) % p) for r in range(p) if W >> r & 1)
def mul(W, u, p): return sum(1 << ((r * u) % p) for r in range(p) if W >> r & 1)
def val(W, p): return int(''.join('1' if W >> r & 1 else '0' for r in range(p)), 2)

def residual_clauses(var, f, p, k, L):
    FULL = (1 << p) - 1
    minimal = [W for W in range(FULL + 1) if all(val(W, p) <= val(rot(W, t, p), p) for t in range(p))]
    c = lambda j, i: f + p * j + i
    wv = {j: [var[(c(0, 0), c(j, r))] for r in range(p)] for j in range(L, k)}
    forbid = lambda vs, W: [-v if W >> r & 1 else v for r, v in enumerate(vs)]
    out = []
    for j in range(L, k):
        out += [forbid(wv[j], W) for W in range(FULL + 1) if W not in minimal]
    for j, l in zip(range(L, k), range(L + 1, k)):
        out += [forbid(wv[j], A) + forbid(wv[l], B) for A in minimal for B in minimal if val(A, p) > val(B, p)]
    return out

# ---- Z_p-graphs on L cycles ----
def decode(cube, var, f, p, L):
    H = (p - 1) // 2
    c = lambda j, i: f + p * j + i
    inv = {}
    for e in sorted(var): inv.setdefault(var[e], e)
    assign = {}
    for l in cube:
        e = inv[abs(l)]; assert e not in assign, 'duplicate variable in cube'
        assign[e] = l > 0
    want = {(c(j, 0), c(j, d)) for j in range(L) for d in range(1, H + 1)} | {(c(j, 0), c(l, r)) for j in range(L) for l in range(j + 1, L) for r in range(p)}
    assert set(assign) == want, 'cube does not fix exactly the first L cycles'
    codes = tuple(sum(1 << (d - 1) for d in range(1, H + 1) if assign[(c(j, 0), c(j, d))]) for j in range(L))
    words = tuple(sum(1 << r for r in range(p) if assign[(c(j, 0), c(l, r))]) for l in range(1, L) for j in range(l))
    return codes, words

def adjacency(codes, words, p):
    L = len(codes); H = (p - 1) // 2; adj = [0] * (p * L); idx = 0
    for j, s in enumerate(codes):
        for i in range(p):
            for d in range(1, H + 1):
                if s >> (d - 1) & 1:
                    adj[p * j + i] |= 1 << (p * j + (i + d) % p) | 1 << (p * j + (i - d) % p)
    for l in range(1, L):
        for j in range(l):
            W = words[idx]; idx += 1
            for i in range(p):
                for r in range(p):
                    if W >> r & 1:
                        a, b = p * j + i, p * l + (i + r) % p
                        adj[a] |= 1 << b; adj[b] |= 1 << a
    return adj

def clique(adj, cand, size):
    if size == 0: return True
    while cand:
        v = cand.bit_length() - 1; cand &= ~(1 << v)
        if clique(adj, cand & adj[v], size - 1): return True
    return False

def good(adj):
    n = len(adj); allv = (1 << n) - 1
    cadj = [allv & ~adj[v] & ~(1 << v) for v in range(n)]
    return not clique(adj, allv, 5) and not clique(cadj, allv, 5)

def group(p, L):
    return [(c, u, perm, (0,) + ts) for c in (0, 1) for u in range(1, p)
            for perm in itertools.permutations(range(L)) for ts in itertools.product(range(p), repeat=L - 1)]

def transform(codes, words, g, p):
    c, u, perm, ts = g; L = len(codes); H = (p - 1) // 2; CF = (1 << H) - 1; FULL = (1 << p) - 1
    def cmul(s):
        A = {(d * u) % p for d in range(1, H + 1) if s >> (d - 1) & 1}
        return sum(1 << (d - 1) for d in range(1, H + 1) if d in A or p - d in A)
    cd = [cmul(s) for s in codes]; wd = {}
    idx = 0
    for l in range(1, L):
        for j in range(l):
            wd[(j, l)] = mul(words[idx], u, p); idx += 1
    if c:
        cd = [CF ^ s for s in cd]; wd = {jl: FULL ^ W for jl, W in wd.items()}
    ncodes = tuple(cd[perm[a]] for a in range(L)); nw = []
    for b in range(1, L):
        for a in range(b):
            ja, jb = perm[a], perm[b]
            W = wd[(ja, jb)] if ja < jb else mul(wd[(jb, ja)], p - 1, p)
            nw.append(rot(W, ts[b] - ts[a], p))
    return ncodes, tuple(nw)

_G = {}
def _init_kw(d): _G.update(d)

def canon_stab(args):
    """(brute-force canonical form, stabiliser order, goodness) of a cube."""
    i, codes, words = args
    p = _G['p']; best = None; stab = 0; key = (codes, words)
    for g in _G['group']:
        k = transform(codes, words, g, p)
        if k == key: stab += 1
        if best is None or k < best: best = k
    return i, best == key, stab, good(adjacency(codes, words, p))

def count_good(args):
    """number of labelled good graphs with the given code tuple (all word tuples)."""
    codes = args; p = _G['p']; L = len(codes); m = L * (L - 1) // 2; FULL = (1 << p) - 1
    return sum(1 for words in itertools.product(range(FULL + 1), repeat=m) if good(adjacency(codes, words, p)))

def raw_sha256(path):
    """SHA-256 of the (decompressed) LRAT text, as recorded by the driver before xz."""
    h = hashlib.sha256()
    with (lzma.open(path, 'rb') if path.endswith('.xz') else open(path, 'rb')) as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def check_cube(args):
    i, cube = args
    path = os.path.join(_G['certdir'], f'c{i}.lrat.xz')
    if not os.path.exists(path): return i, 'missing'
    rec = _G['manifest'].get(str(i))
    if rec is None: return i, 'not in manifest'
    if rec['cube'] != cube: return i, 'manifest cube mismatch'
    if raw_sha256(path) != rec['sha256']: return i, 'sha256 mismatch'
    try:
        ok = check_lrat(_G['cls'] + [[l] for l in cube], path)
    except Exception as e:
        return i, f'LRAT error: {e}'
    return i, 'VERIFIED' if ok else 'no empty clause'

def main():
    argv = sys.argv[1:]; jobs = 4
    if '--jobs' in argv:
        i = argv.index('--jobs'); jobs = int(argv[i + 1]); del argv[i:i + 2]
    flags = {a for a in argv if a.startswith('--')}; args = [a for a in argv if not a.startswith('--')]
    f, p, k, L = map(int, args[:4]); icnf, cnfpath, manpath, certdir = args[4:8]
    assert f + p * k == N
    H = (p - 1) // 2
    # 1. formula
    var, nvo = orbit_var(N, f, p, k)
    nvo2, nvh, base, extra = regenerate(N, f, p, k)
    lex, nvl = lex_clauses(N, f, p, k, var, nvh)
    S = residual_clauses(var, f, p, k, L)
    nvfile, cls = read_dimacs(cnfpath)
    canon_c = lambda c: tuple(sorted(c, key=lambda x: (abs(x), x)))
    got = sorted(canon_c(c) for c in cls)
    want = sorted(canon_c(c) for c in list(base) + list(extra) + lex + S)
    assert nvfile == nvl, (nvfile, nvl)
    assert got == want, 'formula mismatch'
    print(f'formula 1^{f} {p}^{k}: {len(base)} orbit + {len(extra)} redundant + {len(lex)} lex-leader + {len(S)} residual clauses, {nvfile} variables ({nvo} orbit variables); matches {os.path.basename(cnfpath)} (sha256 {sha256(cnfpath)})')
    # 2./3. cubes
    cubes = [list(map(int, l.split()[1:-1])) for l in open(icnf) if l.startswith('a ')]
    dec = [decode(c, var, f, p, L) for c in cubes]
    assert len(set(dec)) == len(cubes), 'duplicate cubes'
    G = group(p, L)
    bad = 0; orbit_sum = 0
    with Pool(jobs, initializer=_init_kw, initargs=({'p': p, 'group': G},)) as pool:
        for i, canonical, stab, gd in pool.imap_unordered(canon_stab, [(i,) + d for i, d in enumerate(dec)], chunksize=8):
            if not canonical: print(f'cube {i}: not canonical'); bad += 1
            if not gd: print(f'cube {i}: not (5,5)-good'); bad += 1
            assert len(G) % stab == 0; orbit_sum += len(G) // stab
        print(f'cubes: {len(cubes)} distinct canonical (5,5)-good Z_{p}-graphs on {L} cycles ({bad} failures); group order {len(G)}; sum of orbit sizes {orbit_sum}')
        if '--skip-complete' not in flags:
            code_tuples = list(itertools.product(range(1 << H), repeat=L))
            total = sum(pool.imap_unordered(count_good, code_tuples))
            print(f'completeness: {total} labelled (5,5)-good Z_{p}-graphs on {L} cycles', '== sum of orbit sizes' if total == orbit_sum else f'!= {orbit_sum} FAILURE')
            if total != orbit_sum: bad += 1
    # 4. certificates
    if '--skip-lrat' in flags:
        print('RESULT:', 'all checks passed (no certificates checked)' if bad == 0 else 'FAILURES'); sys.exit(0 if bad == 0 else 1)
    manifest = json.load(open(manpath))
    counts = {}
    with Pool(jobs, initializer=_init_kw, initargs=({'cls': cls, 'certdir': certdir, 'manifest': manifest},)) as pool:
        for i, res in pool.imap_unordered(check_cube, list(enumerate(cubes)), chunksize=4):
            counts[res] = counts.get(res, 0) + 1
            if res not in ('VERIFIED', 'missing', 'not in manifest'): print(f'cube {i}: {res}')
    print('certificates:', ', '.join(f'{v} {k}' for k, v in sorted(counts.items())))
    soft = ('VERIFIED', 'missing', 'not in manifest')
    ok = bad == 0 and all(k in soft for k in counts) and counts.get('VERIFIED', 0) == len(cubes)
    print('RESULT:', 'all checks passed' if ok else ('FAILURES' if bad or any(k not in soft for k in counts) else 'incomplete (missing certificates)'))
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
