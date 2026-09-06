r"""reviewer-1: my own \(1^0 7^5\) formula, with my own symS clauses, solved.

h3295's measured payoff is that \(1^0 7^5\) goes from no verdict in 3600 s to
UNSAT in 600 s once symS is added.  This builds that instance from
\((n,s,t,f,p,k) = (35,4,6,0,7,5)\) with my own orbit numbering and my own
encoding of symS — for each cross row \(y^{(j)}\), \(j = 1..k-1\), the 7-bit
words that are NOT lex-greatest among their seven rotations are blocked
directly, one clause each, so there are no auxiliary variables and no lex-chain
transcription — then runs CaDiCaL and checks the proof with drat-trim.

usage: python3 indep_run75.py OUTDIR
"""
import itertools
import os
import subprocess
import sys
import time

from indep_syms import orbits, cross_row

TOOLS = os.path.expanduser('~/.discovery-research-team/workspaces/reviewer-1/'
                           'scratch/r46/tools')
CAD = os.path.join(TOOLS, 'cadical', 'build', 'cadical')
DT = os.path.join(TOOLS, 'drat-trim', 'drat-trim')

F, P, K, S, T = 0, 7, 5, 4, 6
N = F + P * K


def base_clauses(oid, norb):
    seen, out = set(), []
    for A in itertools.combinations(range(N), S):
        cl = tuple(sorted({-(oid[(u, v)] + 1)
                           for u, v in itertools.combinations(A, 2)}))
        if cl not in seen:
            seen.add(cl)
            out.append(cl)
    for B in itertools.combinations(range(N), T):
        cl = tuple(sorted({oid[(u, v)] + 1
                           for u, v in itertools.combinations(B, 2)}))
        if cl not in seen:
            seen.add(cl)
            out.append(cl)
    return out


def rot_greatest(word):
    return all(list(word[r:] + word[:r]) <= list(word) for r in range(1, P))


def syms_clauses(oid):
    """block every 7-bit cross-row word that is not lex-greatest among its
    rotations; no auxiliary variables"""
    out = []
    for j in range(1, K):
        row = [oid[(F, F + j * P + d)] + 1 for d in range(P)]
        for word in itertools.product((0, 1), repeat=P):
            if rot_greatest(word):
                continue
            out.append(tuple(sorted(-row[i] if word[i] else row[i]
                                    for i in range(P))))
    return out


def symc_clauses(oid):
    """my own symC: internal codes sorted, c_j <=_lex c_{j+1}; the (p-1)/2 bit
    pairs that violate the order are blocked directly, no auxiliaries"""
    half = (P - 1) // 2
    out = []
    for j in range(K - 1):
        a, b = F + j * P, F + (j + 1) * P
        ra = [oid[(a, a + d)] + 1 for d in range(1, half + 1)]
        rb = [oid[(b, b + d)] + 1 for d in range(1, half + 1)]
        for wa in itertools.product((0, 1), repeat=half):
            for wb in itertools.product((0, 1), repeat=half):
                if list(wa) <= list(wb):
                    continue
                lits = [(-ra[i] if wa[i] else ra[i]) for i in range(half)]
                lits += [(-rb[i] if wb[i] else rb[i]) for i in range(half)]
                out.append(tuple(sorted(set(lits))))
    return out


def main():
    out = sys.argv[1]
    with_symc = len(sys.argv) > 2 and sys.argv[2] == '--symc' 
    os.makedirs(out, exist_ok=True)
    oid, norb = orbits(F, P, K)
    t0 = time.time()
    base = base_clauses(oid, norb)
    syms = syms_clauses(oid) + (symc_clauses(oid) if with_symc else [])
    print(f'{norb} orbit variables, {len(base)} base clauses, '
          f'{len(syms)} breaking clauses (symC {with_symc}), built in '
          f'{time.time() - t0:.0f} s', flush=True)
    cnf = os.path.join(out, 'indep_1_0_7_5_syms.cnf')
    with open(cnf, 'w') as fh:
        fh.write(f'p cnf {norb} {len(base) + len(syms)}\n')
        for c in base + syms:
            fh.write(' '.join(map(str, c)) + ' 0\n')
    proof = os.path.join(out, 'proof.drat')
    t0 = time.time()
    r = subprocess.run([CAD, '-q', cnf, proof], capture_output=True, text=True)
    solve = time.time() - t0
    verdict = ('UNSAT' if 's UNSATISFIABLE' in r.stdout else
               'SAT' if 's SATISFIABLE' in r.stdout else 'UNKNOWN')
    print(f'CaDiCaL: {verdict} in {solve:.0f} s; proof '
          f'{os.path.getsize(proof) / 1e6:.0f} MB', flush=True)
    if verdict != 'UNSAT':
        return
    t0 = time.time()
    r = subprocess.run([DT, cnf, proof, '-f'], capture_output=True, text=True)
    ok = 's VERIFIED' in r.stdout
    print(f'drat-trim: {"s VERIFIED" if ok else r.stdout[-300:]} in '
          f'{time.time() - t0:.0f} s', flush=True)
    os.unlink(proof)


if __name__ == '__main__':
    main()
