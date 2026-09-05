"""reviewer-1: is the redundant hybrid block invariant under the symmetries used
by the cube split of h2873?

The README says "the hybrid clauses are invariant under every step".  As a CNF
clause set that is false (the totalizer's auxiliary variables are tied to the
particular vertex or cycle a constraint is about).  What the soundness argument
needs is that the CONSTRAINTS are invariant, so that the image of a solution
still satisfies them.  This script checks exactly that, on hybrid.py's own
constraint manifest: for every generator of the split group, mapping the orbit
variables (and, for complementation, replacing "lo <= #true <= hi" by
"len-hi <= #true <= len-lo" and flipping the condition literal) permutes the
constraint list onto itself.

usage: python3 hybrid_inv.py f p k level
"""
import sys, os
from collections import Counter
from indep_encode import permutation, orbits_of_pairs
from split_sound import cycle_perm, mult_perm, normalises

N = 42


def norm(c, nvars=None):
    lits = tuple(sorted(c['lits']))
    return (lits, c['lo'], c['hi'], c['cond'])


def main():
    f, p, k, level = map(int, sys.argv[1:5])
    sig = permutation(N, f, p, k)
    var, nvo = orbits_of_pairs(N, sig)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r55-42-prime-order-automorphisms'))
    from hybrid import hybrid
    *_, manifest = hybrid(N, f, p, k)
    want = Counter(norm(c) for c in manifest)
    print(f'{len(manifest)} redundant constraints in hybrid.py\'s manifest '
          f'({sum(len(c["lits"]) for c in manifest)} literal slots)')

    gens = []
    tr = list(range(level)); tr[0], tr[1] = 1, 0
    gens.append(('swap cycles 0,1', cycle_perm(f, p, k, tr + list(range(level, k)), [0] * k), 0))
    lc = [(a + 1) % level for a in range(level)]
    gens.append(('cycle 0->1->2->3->0', cycle_perm(f, p, k, lc + list(range(level, k)), [0] * k), 0))
    for a in range(level):
        rot = [0] * k; rot[a] = 1
        gens.append((f'rotate cycle {a}', cycle_perm(f, p, k, list(range(k)), rot), 0))
    for a in range(level, k):
        rot = [0] * k; rot[a] = 1
        gens.append((f'rotate free cycle {a}', cycle_perm(f, p, k, list(range(k)), rot), 0))
    sw = list(range(k)); sw[level], sw[level + 1] = level + 1, level
    gens.append((f'swap free cycles {level},{level+1}', cycle_perm(f, p, k, sw, [0] * k), 0))
    pi = list(range(N)); pi[0], pi[1] = 1, 0
    gens.append(('swap fixed vertices 0,1', pi, 0))
    gens.append(('i -> 2i (all cycles)', mult_perm(f, p, k, 2), 0))
    gens.append(('complement', list(range(N)), 1))

    allok = True
    for name, perm, comp in gens:
        assert normalises(perm, sig, N), name
        vmap = {}
        for (u, w), v in var.items():
            a, b = perm[u], perm[w]
            vmap[v] = var[(a, b) if a < b else (b, a)]
        got = Counter()
        for c in manifest:
            lits = [vmap[l] for l in c['lits']]
            lo, hi, cond = c['lo'], c['hi'], c['cond']
            if cond is not None:
                cond = vmap[cond] if cond > 0 else -vmap[-cond]
            if comp:
                lo, hi = len(lits) - hi, len(lits) - lo
                if cond is not None:
                    cond = -cond
            got[(tuple(sorted(lits)), lo, hi, cond)] += 1
        ok = got == want
        allok &= ok
        print(f'  {name}: constraint list invariant: {ok}')
    print('HYBRID CONSTRAINT INVARIANCE ' + ('OK' if allok else 'FAILED'))


if __name__ == '__main__':
    main()
