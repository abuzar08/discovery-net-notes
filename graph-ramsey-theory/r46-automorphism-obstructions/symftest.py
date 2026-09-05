"""Brute-force soundness test for the fixed-vertex lex-leader (symF).

The construction and its soundness argument are researcher-1's (Discovery Net
h2689); this file does not re-derive them.  It checks that MY encoding of the
constraint has the property the argument requires: every S_f-orbit of
sigma-invariant graphs contains at least one member satisfying it, so adding
the clauses cannot remove the last witness of any isomorphism class.

    python3 symftest.py N F P K
"""
import itertools, sys
import encode


def setup(n, f, p, k):
    idx = encode.pair_index(n)
    sig = encode.permutation(n, f, p, k)
    orb, nvar = encode.pair_orbits(n, sig, idx)
    return idx, orb, nvar


def predicate(n, f, p, k, idx, orb, bits):
    """R_u <=_lex R_{u+1} for every u, evaluated directly."""
    def val(a, b):
        return bits[orb[idx[(a, b)] if a < b else idx[(b, a)]]]
    for u in range(f - 1):
        others = [w for w in range(f) if w != u and w != u + 1]
        ra = [val(u, f + j * p) for j in range(k)] + [val(u, w) for w in others]
        rb = [val(u + 1, f + j * p) for j in range(k)] + \
             [val(u + 1, w) for w in others]
        for a, b in zip(ra, rb):
            if a != b:
                if a > b:
                    return False
                break
    return True


def relabel(n, f, idx, orb, nvar, bits, perm):
    """Apply a permutation of F (identity on cycles) to an assignment."""
    def img(x):
        return perm[x] if x < f else x
    out = [0] * nvar
    for (a, b), i in idx.items():
        ia, ib = img(a), img(b)
        out[orb[idx[(min(ia, ib), max(ia, ib))]]] = bits[orb[i]]
    return out


def main():
    n, f, p, k = (int(x) for x in sys.argv[1:5])
    idx, orb, nvar = setup(n, f, p, k)
    print(f"n={n} 1^{f} {p}^{k}: {nvar} orbit variables, "
          f"{2**nvar} assignments, |S_{f}| = {len(list(itertools.permutations(range(f))))}")
    perms = list(itertools.permutations(range(f)))
    seen, bad, classes = set(), 0, 0
    for m in range(1 << nvar):
        bits = [(m >> i) & 1 for i in range(nvar)]
        key = tuple(bits)
        if key in seen:
            continue
        orbit = set()
        for pm in perms:
            orbit.add(tuple(relabel(n, f, idx, orb, nvar, bits, pm)))
        seen |= orbit
        classes += 1
        if not any(predicate(n, f, p, k, idx, orb, list(o)) for o in orbit):
            bad += 1
            if bad <= 3:
                print("  UNSOUND: orbit with no representative:", key)
    print(f"  {classes} S_{f}-orbits, {bad} with no satisfying representative")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
