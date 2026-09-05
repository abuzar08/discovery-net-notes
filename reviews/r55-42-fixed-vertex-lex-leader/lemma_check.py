"""reviewer-1: exhaustive checks of the soundness lemma for constraint (L)
(fixed-vertex lex-leader with profile columns) of r55-42-fixed-vertex-lex-leader.

An *object* is (profiles, A): profiles[u] in {0,1}^k for u in F = 0..f-1 and A
a symmetric 0/1 f x f matrix with zero diagonal (G[F]).  S_f acts by
relabelling F.  For u = 0..f-2 the two rows compared use the SAME columns
(profile columns, then w in 0..f-1 with w not in {u, u+1}):
  R_u = profiles[u] + (A[u][w]), R_{u+1} = profiles[u+1] + (A[u+1][w]);
(L) is R_u <=lex R_{u+1}.  (A first draft of this script excluded {u+1, u+2}
for the second row and reported spurious counterexamples; the README's "for
the same w in the same order" is essential and is what symF.py /
verify_symF.py implement.)  Key(object) = (profile sequence, A row by row).

check A (proof step, every object): if rows u, u+1 violate (L) then the
object with u and u+1 swapped has strictly smaller Key.  This is the descent
step of the README's proof; it implies the lemma (finite descent).
check B (statement, every S_f-orbit): some member satisfies (L); done by
enumerating all f! relabellings of every object (small cases only).
usage: python3 lemma_check.py A f k | python3 lemma_check.py B f k
"""
import sys
from itertools import product, combinations, permutations


def objects(f, k):
    pairs = list(combinations(range(f), 2))
    for pbits in product((0, 1), repeat=f * k):
        profiles = tuple(tuple(pbits[u * k:(u + 1) * k]) for u in range(f))
        for ebits in product((0, 1), repeat=len(pairs)):
            A = [[0] * f for _ in range(f)]
            for (u, v), b in zip(pairs, ebits):
                A[u][v] = A[v][u] = b
            yield profiles, A


def pair_rows(profiles, A, f, u):
    """(R_u, R_{u+1}) over the SAME columns: profile columns, then w not in {u, u+1}."""
    cols = [w for w in range(f) if w not in (u, u + 1)]
    return (profiles[u] + tuple(A[u][w] for w in cols),
            profiles[u + 1] + tuple(A[u + 1][w] for w in cols))


def satisfies_L(profiles, A, f):
    return all(pair_rows(profiles, A, f, u)[0] <= pair_rows(profiles, A, f, u)[1] for u in range(f - 1))


def key(profiles, A):
    return (profiles, tuple(tuple(r) for r in A))


def relabel(profiles, A, f, pi):
    """object obtained by giving old vertex v the new label pi[v]."""
    inv = [0] * f
    for v in range(f):
        inv[pi[v]] = v
    P2 = tuple(profiles[inv[u]] for u in range(f))
    A2 = [[A[inv[u]][inv[w]] for w in range(f)] for u in range(f)]
    return P2, A2


def check_A(f, k):
    n = 0
    viol = 0
    for profiles, A in objects(f, k):
        n += 1
        K = key(profiles, A)
        for u in range(f - 1):
            a, b = pair_rows(profiles, A, f, u)
            if a > b:
                viol += 1
                pi = list(range(f))
                pi[u], pi[u + 1] = u + 1, u
                P2, A2 = relabel(profiles, A, f, pi)
                if not key(P2, A2) < K:
                    print('COUNTEREXAMPLE to descent step', profiles, A, 'u =', u)
                    return False
    print(f'check A f={f} k={k}: {n} objects, {viol} (object,u) violations, every violation fixed by a strictly descending swap: OK')
    return True


def check_B(f, k):
    n = 0
    bad = 0
    perms = list(permutations(range(f)))
    for profiles, A in objects(f, k):
        n += 1
        if satisfies_L(profiles, A, f):
            continue
        if not any(satisfies_L(*relabel(profiles, A, f, pi), f) for pi in perms):
            bad += 1
            print('ORBIT WITHOUT (L)-MEMBER', profiles, A)
            return False
    print(f'check B f={f} k={k}: {n} objects, every S_{f}-orbit contains an (L)-satisfying member: OK')
    return True


if __name__ == '__main__':
    which, f, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    ok = check_A(f, k) if which == 'A' else check_B(f, k)
    sys.exit(0 if ok else 1)
