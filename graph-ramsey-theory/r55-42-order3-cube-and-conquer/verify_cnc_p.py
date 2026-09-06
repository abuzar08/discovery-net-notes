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
If some cubes were too hard and were refined by a complete case split on further
variables (refine_p.py), pass the refined .icnf together with `--refine map.json`:
the checker then verifies that the children of every refined cube are exactly the
2^m assignments of the m split variables (so the split is a complete case
distinction), runs checks 2 and 3 on the parent cubes, and replays one certificate
per child.
Long runs whose proofs are too large to keep replay each certificate as it appears
(sweep_verify.py) and delete it. Pass those sweep logs with `--verified a.jsonl,b.jsonl`:
a cube whose certificate is no longer on disk is then accepted if some log records a
VERIFIED replay for exactly its literals, and such cubes are reported separately from
the ones replayed in this run.
usage: python3 verify_cnc_p.py f p k L cubes.icnf formula.cnf manifest.json certdir [--jobs N] [--refine map.json] [--verified logs] [--skip-lrat] [--skip-complete]
Exit status 0 iff everything checked passed."""
import sys, os, json, itertools, hashlib, lzma
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for d in (os.path.join(HERE, '..', 'r55-42-prime-order-automorphisms'), os.path.join(HERE, '..'), os.path.join(HERE, '..', '..', '..', 'notes', 'graph-ramsey-theory', 'r55-42-prime-order-automorphisms')):
    if os.path.exists(os.path.join(d, 'verify.py')): sys.path.insert(0, d); break
from verify import read_dimacs, check_lrat as check_lrat_strict, sha256

def check_lrat(cls, path):
    """LRAT check that also accepts hints which are already satisfied.

    verify.check_lrat (cited pass-1 artifact) requires every hint clause to be
    unit or falsified, which is what drat-trim emits. CaDiCaL's own LRAT
    (--lrat=true) sometimes lists a hint whose clause is already satisfied at
    that point: the literal it would propagate was propagated earlier by another
    clause. Skipping such a hint is sound -- it adds no propagation, and the
    lemma is still accepted only if the hints that do propagate lead to a
    conflict -- so this variant skips them and is otherwise identical.
    """
    import lzma as _lzma
    db = {i + 1: c for i, c in enumerate(cls)}
    opener = _lzma.open if path.endswith('.xz') else open
    empty = False
    with opener(path, 'rt') as fh:
        for line in fh:
            parts = line.split()
            if not parts: continue
            cid = int(parts[0])
            if parts[1] == 'd':
                for t in parts[2:]:
                    t = int(t)
                    if t == 0: break
                    db.pop(t, None)
                continue
            z = parts.index('0')
            lemma = [int(x) for x in parts[1:z]]
            hints = [int(x) for x in parts[z + 1:]]
            assert hints[-1] == 0
            assign = {-l for l in lemma}
            conflict = False
            for h in hints[:-1]:
                if h < 0:
                    raise ValueError(f'RAT hint in lemma {cid}; only RUP supported')
                c = db[h]
                if any(l in assign for l in c):
                    continue                      # already satisfied: no propagation
                unassigned = [l for l in c if -l not in assign]
                if not unassigned:
                    conflict = True; break
                if len(unassigned) == 1:
                    assign.add(unassigned[0])
                else:
                    raise ValueError(f'hint {h} neither unit nor falsified in lemma {cid}')
            if not conflict:
                raise ValueError(f'no conflict for lemma {cid}')
            db[cid] = lemma
            if not lemma: empty = True
    return empty
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
    prev = {}
    if '--verified' in argv:
        i = argv.index('--verified')
        for path in argv[i + 1].split(','):
            for line in open(path):
                r = json.loads(line)
                if r.get('status') == 'VERIFIED' and r.get('cube_lits') is not None:
                    prev[tuple(r['cube_lits'])] = r.get('sha256')
        del argv[i:i + 2]
        print(f'{len(prev)} cubes recorded VERIFIED by earlier replay sweeps')
    refine = None
    if '--refine' in argv:
        i = argv.index('--refine'); refine = json.load(open(argv[i + 1])); del argv[i:i + 2]
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
    if refine is None:
        parents = cubes
    else:
        sv = refine['split_vars']; recs = refine['cubes']
        assert len(recs) == len(cubes), 'refinement map does not match the cube file'
        par = {}
        for c, rec in zip(cubes, recs):
            i, add = rec['parent'], rec['added']
            assert add == c[len(c) - len(add):] if add else True, 'child does not end in its added literals'
            base = c[:len(c) - len(add)] if add else c
            par.setdefault(i, {'cube': base, 'added': set()})
            assert par[i]['cube'] == base, f'inconsistent parent cube {i}'
            if add:
                assert sorted(map(abs, add)) == sorted(sv), f'child of cube {i} splits on the wrong variables'
                par[i]['added'].add(tuple(add))
        assert sorted(par) == list(range(len(par))), 'parent indices are not 0..n-1'
        full = {tuple(s * v for s, v in zip(signs, sv)) for signs in itertools.product((1, -1), repeat=len(sv))}
        nref = 0
        for i in sorted(par):
            a = par[i]['added']
            if a:
                assert a == full, f'cube {i}: children are not the complete 2^{len(sv)} split'
                nref += 1
            assert not (set(map(abs, par[i]['cube'])) & set(sv)), f'cube {i} already fixed a split variable'
        parents = [par[i]['cube'] for i in sorted(par)]
        print(f'refinement: {len(parents)} cubes, {nref} of them split completely on {len(sv)} variables {sv} into {len(cubes)} subcubes')
    dec = [decode(c, var, f, p, L) for c in parents]
    assert len(set(dec)) == len(parents), 'duplicate cubes'
    G = group(p, L)
    bad = 0; orbit_sum = 0
    with Pool(jobs, initializer=_init_kw, initargs=({'p': p, 'group': G},)) as pool:
        for i, canonical, stab, gd in pool.imap_unordered(canon_stab, [(i,) + d for i, d in enumerate(dec)], chunksize=8):
            if not canonical: print(f'cube {i}: not canonical'); bad += 1
            if not gd: print(f'cube {i}: not (5,5)-good'); bad += 1
            assert len(G) % stab == 0; orbit_sum += len(G) // stab
        print(f'cubes: {len(parents)} distinct canonical (5,5)-good Z_{p}-graphs on {L} cycles ({bad} failures); group order {len(G)}; sum of orbit sizes {orbit_sum}')
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
    todo = []
    for i, c in enumerate(cubes):
        if not os.path.exists(os.path.join(certdir, f'c{i}.lrat.xz')) and tuple(c) in prev:
            counts['VERIFIED earlier'] = counts.get('VERIFIED earlier', 0) + 1
        else:
            todo.append((i, c))
    with Pool(jobs, initializer=_init_kw, initargs=({'cls': cls, 'certdir': certdir, 'manifest': manifest},)) as pool:
        for i, res in pool.imap_unordered(check_cube, todo, chunksize=4):
            counts[res] = counts.get(res, 0) + 1
            if res not in ('VERIFIED', 'missing', 'not in manifest'): print(f'cube {i}: {res}')
    print('certificates:', ', '.join(f'{v} {k}' for k, v in sorted(counts.items())))
    soft = ('VERIFIED', 'VERIFIED earlier', 'missing', 'not in manifest')
    ok = bad == 0 and all(k in soft for k in counts) and counts.get('VERIFIED', 0) + counts.get('VERIFIED earlier', 0) == len(cubes)
    print('RESULT:', 'all checks passed' if ok else ('FAILURES' if bad or any(k not in soft for k in counts) else 'incomplete (missing certificates)'))
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
