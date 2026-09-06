"""Exact edge bounds for (4,5)-Ramsey graphs, recomputed from primary data.

Reads McKay's catalogues, decodes graph6 with its own decoder, re-checks that
every graph really is a (4,5)-graph (no K_4, no independent 5-set), and reports
the exact minimum and maximum edge counts per order.

Self-check: McKay's extremal files are named r45<n>.<e>.g6, so the decoder must
reproduce <e> as the edge count of every graph in the file.  A decoder bug
would show up immediately as a mismatch, without my having to trust the
decoder.

TRUST BOUNDARY.  What is verified here: that the graphs in the files are
(4,5)-graphs, and their exact edge counts.  What is CITED and not proved:
McKay-Radziszowski's completeness claim, i.e. that these files contain every
(4,5)-graph at the extreme edge counts (and, for n = 24, every (4,5,24)-graph).
The bounds are only valid for all (4,5,m)-graphs given that claim.
"""
import sys


def g6_decode(line):
    """graph6 -> (n, adj) with adj a list of int bitmasks.  Own implementation."""
    s = line.strip()
    if not s:
        return None
    b = [ord(c) - 63 for c in s]
    if b[0] == 63:                       # 63 marks a longer length field
        raise SystemExit("graph6 with n >= 63 not needed here")
    n = b[0]
    bits = []
    for x in b[1:]:
        for i in range(5, -1, -1):
            bits.append((x >> i) & 1)
    adj = [0] * n
    p = 0
    for j in range(1, n):                # column-major upper triangle
        for i in range(j):
            if bits[p]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            p += 1
    return n, adj


def has_clique(adj, cand, k):
    """Is there a clique of size k inside the vertex set `cand` (a bitmask)?"""
    if k == 0:
        return True
    if k == 1:
        return cand != 0
    c = cand
    while c:
        v = (c & -c).bit_length() - 1
        c &= c - 1
        # only look at higher-numbered vertices to enumerate each clique once
        rest = cand & adj[v] & ~((1 << (v + 1)) - 1)
        if bin(rest).count("1") >= k - 1 and has_clique(adj, rest, k - 1):
            return True
    return False


def is_good(n, adj, s, t):
    """No K_s, and no independent set of size t."""
    full = (1 << n) - 1
    if has_clique(adj, full, s):
        return False
    comp = [(~adj[v]) & full & ~(1 << v) for v in range(n)]
    return not has_clique(comp, full, t)


def edges(n, adj):
    return sum(bin(a).count("1") for a in adj) // 2


def scan(path, expect_n=None, expect_e=None, check=True, limit=None):
    lo, hi, cnt, bad_good, bad_e = None, None, 0, 0, 0
    with open(path) as fh:
        for line in fh:
            g = g6_decode(line)
            if g is None:
                continue
            n, adj = g
            e = edges(n, adj)
            cnt += 1
            lo = e if lo is None else min(lo, e)
            hi = e if hi is None else max(hi, e)
            if expect_n is not None and n != expect_n:
                raise SystemExit(f"{path}: order {n} != {expect_n}")
            if expect_e is not None and e != expect_e:
                bad_e += 1
            if check and not is_good(n, adj, 4, 5):
                bad_good += 1
            if limit and cnt >= limit:
                break
    return cnt, lo, hi, bad_good, bad_e


if __name__ == "__main__":
    print(scan(sys.argv[1], check=("--nocheck" not in sys.argv)))
