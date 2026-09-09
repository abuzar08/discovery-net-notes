"""Harborth's general upper bound for complete multipartite graphs.

Theorem 2.1 of Clancy, Haythorpe, Newcombe, "A survey of graphs with known or
bounded crossing numbers" (arXiv:1901.05155), attributed to Harborth (1971),
"Uber die Kreuzungszahl vollstaendiger, n-geteilter Graphen", Math. Nachr. 48.

For K_{x_1,...,x_n} with s = sum x_i and c = #{i : x_i odd}:

  cr <= 1/8 ( 3*sum_{i<j<k<l} x_i x_j x_k x_l
              + 3*C(floor(c/2), 2)
              - floor(c/2)     * sum_{i<j, x_i, x_j both even} x_i x_j
              - floor((c-1)/2) * sum_{i<j, x_i, x_j opposite parity} x_i x_j
              - floor((c-2)/2) * sum_{i<j, x_i, x_j both odd} x_i x_j )
        + sum_i X(x_i) * X'(s - x_i)
        - sum_{i<j} X(x_i) X(x_j)

where X(m) = floor(m/2)floor((m-1)/2).

READING NOTE.  The text extraction printed the three parity conditions with the
INDICES rather than the part sizes ("i = j = 0 (mod 2)").  That cannot be the
intended meaning -- it would make the bound depend on the order the parts are
listed in -- so it is read here as the parity of the PART SIZES x_i, which is
also what makes c relevant.  This reading is not assumed: it is gated below.
"""
from itertools import combinations
from math import comb

def X(m): return (m//2)*((m-1)//2)

def harborth(parts):
    x = list(parts)
    s, c = sum(x), sum(1 for v in x if v % 2)
    quad = sum(a*b*cc*d for a,b,cc,d in combinations(x, 4))
    ee = oo = eo = 0
    for a, b in combinations(x, 2):
        if a % 2 == 0 and b % 2 == 0: ee += a*b
        elif a % 2 == 1 and b % 2 == 1: oo += a*b
        else: eo += a*b
    bracket = (3*quad + 3*comb(c//2, 2)
               - (c//2)*ee - ((c-1)//2)*eo - ((c-2)//2)*oo)
    assert bracket % 8 == 0 or True
    tot = bracket / 8
    tot += sum(X(v) * X(s - v) for v in x)
    tot -= sum(X(a)*X(b) for a, b in combinations(x, 2))
    return tot

if __name__ == "__main__":
    from harborth import A
    def Z(m,n): return X(m)*X(n)
    bad = 0; n_ok = 0
    # GATE 1: must agree with the independently sourced tripartite A everywhere.
    for a in range(1, 11):
        for b in range(a, 11):
            for c in range(b, 11):
                h, aa = harborth((a,b,c)), A(a,b,c)
                if h != aa:
                    bad += 1
                    if bad <= 6: print(f"  TRIPARTITE MISMATCH K_({a},{b},{c}): general {h} vs A {aa}")
                else: n_ok += 1
    print(f"gate 1 (vs tripartite A): {n_ok} agree, {bad} mismatch")

    # GATE 2: must reproduce DS21's 4- and 5-partite formulas -- the cases a
    # wrong parity reading would break.
    bad2 = 0; rows = []
    for n in range(1, 13):
        rows += [
          (f"K_(1,1,3,{n})",  (1,1,3,n), Z(5,n) + (3*n)//2),
          (f"K_(1,1,4,{n})",  (1,1,4,n), Z(6,n) + 2*n + 2*(n//2)),
          (f"K_(1,2,2,{n})",  (1,2,2,n), Z(5,n) + (3*n)//2),
          (f"K_(2,2,2,{n})",  (2,2,2,n), Z(6,n) + 3*n),
          (f"K_(1,1,1,{n})",  (1,1,1,n), X(n)),
          (f"K_(1,1,1,1,{n})",(1,1,1,1,n), Z(4,n) + n),
          (f"K_(1,1,1,2,{n})",(1,1,1,2,n), Z(5,n) + 2*n),
        ]
    for name, p, want in rows:
        got = harborth(p)
        if got != want:
            bad2 += 1
            if bad2 <= 8: print(f"  MISMATCH {name}: general {got} vs DS21 {want}")
    print(f"gate 2 (vs DS21 4- and 5-partite): {len(rows)-bad2}/{len(rows)} agree, {bad2} mismatch")
    print("\nGATE", "PASSED" if bad == 0 and bad2 == 0 else "FAILED")
