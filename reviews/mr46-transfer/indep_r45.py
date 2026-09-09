r"""reviewer-1: independent verification of the refutation in MR46-TRANSFER.md.

McKay and Radziszowski hoped that every \((4,5,22)\)-, \((4,5,23)\)- and
\((4,5,24)\)-graph has at least 93, 105 and 113 edges. The refutation needs only
*witnesses*: one \((4,5,22)\)-graph with fewer than 93 edges and one
\((4,5,23)\)-graph with fewer than 105. Completeness of any catalogue is not
needed for that direction, so this check is unconditional.

My own graph6 decoder and my own certification: no \(K_4\) (clique number at most
3) and no independent 5-set (independence number at most 4), both by exhaustive
subset search over bitsets.
"""
import itertools
import sys


def graph6(line):
    """my own decoder: order byte, then six bits per byte, column-major upper
    triangle"""
    b = [ord(c) - 63 for c in line.strip()]
    n = b[0]
    if n == 63:
        raise ValueError('extended order not handled')
    bits = []
    for x in b[1:]:
        for k in range(5, -1, -1):
            bits.append((x >> k) & 1)
    adj = [0] * n
    p = 0
    for j in range(1, n):
        for i in range(j):
            if bits[p]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            p += 1
    return n, adj


def edges(n, adj):
    return sum(bin(a).count('1') for a in adj) // 2


def has_clique(n, adj, k):
    """exhaustive: is there a clique of order k?"""
    def rec(cand, chosen):
        if len(chosen) == k:
            return True
        if len(chosen) + bin(cand).count('1') < k:
            return False
        c = cand
        while c:
            v = (c & -c).bit_length() - 1
            c &= c - 1
            cand &= ~(1 << v)
            if rec(cand & adj[v], chosen + [v]):
                return True
        return False
    return rec((1 << n) - 1, [])


def has_independent(n, adj, k):
    comp = [(~a) & ((1 << n) - 1) & ~(1 << i) for i, a in enumerate(adj)]
    return has_clique(n, comp, k)


def check(path, expect_n, expect_e):
    out = []
    for line in open(path):
        if not line.strip():
            continue
        n, adj = graph6(line)
        e = edges(n, adj)
        k4 = has_clique(n, adj, 4)
        i5 = has_independent(n, adj, 5)
        out.append((n, e, k4, i5))
    ok = all(n == expect_n and e == expect_e and not k4 and not i5
             for n, e, k4, i5 in out)
    print(f'{path}: {len(out)} graphs; orders {sorted({o[0] for o in out})}, '
          f'edge counts {sorted({o[1] for o in out})}, '
          f'any K_4 {any(o[2] for o in out)}, any independent 5-set '
          f'{any(o[3] for o in out)} -> '
          f'{"all are genuine (4,5,%d)-graphs with %d edges" % (expect_n, expect_e) if ok else "MISMATCH"}')
    return ok


if __name__ == '__main__':
    D = 'dl/r45extreme/'
    print('WITNESSES AGAINST THE CONJECTURED BOUNDS (McKay-Radziszowski 1997 §5)')
    a = check(D + 'r4522.88.g6', 22, 88)
    b = check(D + 'r4523.101.g6', 23, 101)
    print(f'   hoped: every (4,5,22)-graph has at least 93 edges -> '
          f'{"REFUTED by an 88-edge witness" if a else "not refuted here"}')
    print(f'   hoped: every (4,5,23)-graph has at least 105 edges -> '
          f'{"REFUTED by a 101-edge witness" if b else "not refuted here"}')
    print()
    print('THE MAXIMA, for the sharpening table')
    check(D + 'r4522.114.g6', 22, 114)
    check(D + 'r4523.122.g6', 23, 122)
