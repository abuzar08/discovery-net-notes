"""Status map for Mohar's Conjecture 5 on cr(M_{n,t}) = K_n minus a t-matching.

Lower bounds come from the vertex-deletion recursion.  Deleting a covered vertex
of M_{n,t} leaves M_{n-1,t-1} (its partner becomes uncovered); deleting an
uncovered vertex leaves M_{n-1,t}.  Each crossing involves four distinct vertices
and so survives n-4 of the n deletions, giving

    cr(M_{n,t}) >= ceil( [ 2t*cr(M_{n-1,t-1}) + (n-2t)*cr(M_{n-1,t}) ] / (n-4) ).

Seeds are values that are known or were computed exactly in this workspace.
Nothing here assumes the conjecture.
"""
from math import comb, ceil

def Z(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4

def mohar(n, t):
    """The conjecture's value, defined for even n = 2k."""
    if n % 2:
        return None
    k = n // 2
    return Z(n) - t * (k - 1) * (k - 2) // 2

# --- seeds: known, or computed exactly here ---------------------------------
KNOWN = {}
for n in range(5, 13):
    KNOWN[(n, 0)] = Z(n)                                   # Harary-Hill, n <= 12
    KNOWN[(n, 1)] = Z(n) - comb((n - 1) // 2, 2)           # Chia-Lee, true n <= 12
KNOWN[(6, 2)] = 1        # computed here
KNOWN[(6, 3)] = 0        # octahedron, planar
KNOWN[(7, 2)] = 4        # computed here, exhaustive planarisation
KNOWN[(7, 3)] = 3        # computed here; = Ho's K_{2,2,2,n} at n=1
KNOWN[(8, 4)] = 6        # Ho (2008)
for n in range(5, 13):
    KNOWN.setdefault((n, 0), Z(n))

def lower(n, t, memo={}):
    if (n, t) in KNOWN:
        return KNOWN[(n, t)], 'known'
    if t == 0 or n < 5 or t > n // 2:
        return 0, '-'
    if (n, t) in memo:
        return memo[(n, t)]
    a, _ = lower(n - 1, t - 1)
    b, _ = lower(n - 1, t)
    val = ceil((2 * t * a + (n - 2 * t) * b) / (n - 4))
    memo[(n, t)] = (val, 'counting')
    return memo[(n, t)]

if __name__ == '__main__':
    print("Mohar Conjecture 5 status map (even n; odd rows shown as they feed it)")
    print(f"{'n':>3} {'t':>3} {'conjecture':>11} {'lower bound':>12} {'source':>9} {'status':>22}")
    for n in range(6, 13):
        for t in range(0, n // 2 + 1):
            lo, src = lower(n, t)
            pred = mohar(n, t)
            if (n, t) in KNOWN:
                st = 'KNOWN' + (' = conjecture' if pred is not None and KNOWN[(n,t)] == pred else '')
                if pred is not None and KNOWN[(n, t)] != pred:
                    st = '*** CONTRADICTS conjecture'
            elif pred is None:
                st = '(odd n: not covered)'
            elif lo > pred:
                st = '*** REFUTES conjecture'
            elif lo == pred:
                st = 'SETTLED by counting'
            else:
                st = f'open, gap {pred - lo}'
            p = '' if pred is None else f'{pred}'
            print(f"{n:>3} {t:>3} {p:>11} {lo:>12} {src:>9} {st:>22}")
        print()
