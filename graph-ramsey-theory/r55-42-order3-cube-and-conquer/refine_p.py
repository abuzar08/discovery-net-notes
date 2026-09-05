"""Refine hard cubes by a complete case split on the orbit variables of the next cycle.

A cube that the solver does not refute within the time limit is replaced by the
2^m assignments of m further variables (a complete binary split: sound and
symmetry-free, no group argument needed). The variables are those of cycle L
(the first free cycle): its internal distance variables x(c_L0, c_Ld), d = 1..(p-1)/2,
and the cross variables x(c_00, c_Lr), r = 0..p-1 -- m = (p-1)/2 + p of them,
so 2^m children per refined cube (p = 3: 16, p = 5: 128).

usage: python3 refine_p.py in.icnf results.jsonl out.icnf map.json f p k L [--nvars m]
--nvars m keeps only the first m variables of that list (code bits, then cross
words), giving 2^m children per refined cube; the default is all of them.
Cubes whose last record in results.jsonl is UNSAT-VERIFIED are copied unchanged and
those with any other status (TIMEOUT, trim failure) are split; a cube with no record
at all is an unfinished run and is an error unless --include-missing is given. map.json records, for every cube
of out.icnf, its parent index in in.icnf and the literals added.
"""
import sys, os, json, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from encode import sigma_of, pair_orbits

def split_vars(var, f, p, L):
    H = (p - 1) // 2
    c = lambda j, i: f + p * j + i
    return [var[(c(L, 0), c(L, d))] for d in range(1, H + 1)] + [var[(min(c(0, 0), c(L, r)), max(c(0, 0), c(L, r)))] for r in range(p)]

def main():
    argv = sys.argv[1:]; nvars = None
    missing_ok = '--include-missing' in argv; argv = [a for a in argv if a != '--include-missing']
    if '--nvars' in argv:
        i = argv.index('--nvars'); nvars = int(argv[i + 1]); del argv[i:i + 2]
    inp, resj, outp, mapp = argv[:4]
    f, p, k, L = map(int, argv[4:8])
    n = 42; assert f + p * k == n and L < k
    sig = sigma_of(n, f, p, k); var, _ = pair_orbits(n, sig)
    sv = split_vars(var, f, p, L)
    if nvars is not None: sv = sv[:nvars]
    cubes = [list(map(int, l.split()[1:-1])) for l in open(inp) if l.startswith('a ')]
    done = {}
    for l in open(resj):
        r = json.loads(l); done[r['cube']] = r['status']
    missing = [i for i in range(len(cubes)) if i not in done]
    if missing and not missing_ok:
        sys.exit(f'{len(missing)} cubes have no record in {resj} (run unfinished): {missing[:5]}... '
                 'rerun the driver, or pass --include-missing to split them too')
    hard = [i for i in range(len(cubes)) if done.get(i, 'MISSING') != 'UNSAT-VERIFIED']
    for i in hard:
        assert not (set(map(abs, cubes[i])) & set(sv)), f'cube {i} already fixes a split variable'
    out = []; mapping = []
    for i, cube in enumerate(cubes):
        if i in set(hard):
            for signs in itertools.product((1, -1), repeat=len(sv)):
                add = [s * v for s, v in zip(signs, sv)]
                out.append(cube + add); mapping.append({'parent': i, 'added': add})
        else:
            out.append(cube); mapping.append({'parent': i, 'added': []})
    with open(outp, 'w') as fh:
        for c in out: fh.write('a ' + ' '.join(map(str, c)) + ' 0\n')
    json.dump({'in': os.path.basename(inp), 'split_vars': sv, 'refined_parents': hard, 'cubes': mapping}, open(mapp, 'w'))
    print(f'{len(cubes)} cubes in, {len(hard)} refined on {len(sv)} variables {sv} -> {len(out)} cubes out')

if __name__ == '__main__':
    main()
