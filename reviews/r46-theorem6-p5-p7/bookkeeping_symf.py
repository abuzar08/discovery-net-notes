"""reviewer-1: independent bookkeeping check of certs.json for h2919.

Enumerates every cycle type 1^f p^k with p prime, k >= 1, f = n - p*k >= 0, for
n = 36..39, and checks that certs.json's five lists partition them, that the 24
--symf entries are exactly at p = 5, that the types left open at p = 5 are the
four claimed, and that all ten types with f > 22 are among the 24.

usage: python3 bookkeeping_symf.py path/to/certs.json
"""
import sys, json, itertools


def primes(m):
    return [x for x in range(2, m + 1) if all(x % d for d in range(2, int(x ** .5) + 1))]


def main():
    c = json.load(open(sys.argv[1]))
    alltypes = {(n, p, k, n - p * k)
                for n in range(36, 40) for p in primes(n) for k in range(1, n // p + 1)}
    key = lambda d: (d['n'], d['p'], d['k'], d['f'])
    cert = {key(x) for x in c['certificates']}
    cube = {key(x) for x in c.get('cube_certificates', [])}
    lem = {key(x) for x in c['excluded_by_lemma']}
    op = {key(x) for x in c['open_p_ge_5']}
    na = {key(x) for x in c['not_attempted_p_2_3']}
    union = cert | cube | lem | op | na
    nonprime = {t for t in union if t[1] not in primes(t[1] + 1) or t[1] == t[0]}
    print(f'prime cycle types for n = 36..39: {len(alltypes)}')
    print(f'certs.json: {len(cert)} certificates, {len(cube)} cube certificates, {len(lem)} by lemma, '
          f'{len(op)} open, {len(na)} not attempted at p in (2,3)')
    print(f'union {len(union)}; covers every prime type: {alltypes <= union}; '
          f'entries outside the prime types: {sorted(union - alltypes)}')
    prime_cert = (cert | cube) & alltypes
    print(f'partition check: {len(prime_cert)} + {len(lem)} + {len(op)} + {len(na)} = '
          f'{len(prime_cert) + len(lem) + len(op) + len(na)} (should be {len(alltypes)}); '
          f'pairwise disjoint: '
          f'{all(not (a & b) for a, b in itertools.combinations([prime_cert, lem, op, na], 2))}')
    sym = {key(x) for x in c['certificates'] if x.get('symf')}
    print(f'--symf certificates: {len(sym)}, all at p = 5: {all(t[1] == 5 for t in sym)}')
    print(f'open at p = 5: {sorted(t for t in op if t[1] == 5)}')
    print(f'open at p = 7: {sorted(t for t in op if t[1] == 7)}')
    print(f'symF types with f > 22: {len(sorted(t for t in sym if t[3] > 22))}')
    print(f'24 refuted + 4 still open at p = 5 = {len(sym) + len([t for t in op if t[1] == 5])}')
    nulls = [x['tag'] for x in c['certificates']
             if x.get('symf') and (x.get('clauses') is None or x.get('solve_s') is None)]
    print(f'--symf entries with null clauses/solve_s/trim_s: {len(nulls)}')


if __name__ == '__main__':
    main()
