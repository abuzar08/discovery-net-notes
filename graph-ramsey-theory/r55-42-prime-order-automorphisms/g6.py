"""Minimal graph6 reader/writer and bitset K5/I5 checker (standard library only)."""
import sys
from itertools import combinations

def parse_g6(line):
    s = line.strip()
    if s.startswith('>>graph6<<'):
        s = s[10:]
    b = [ord(c) - 63 for c in s]
    if b[0] < 63:
        n = b[0]; i = 1
    else:
        n = (b[1] << 12) | (b[2] << 6) | b[3]; i = 4
    bits = []
    for v in b[i:]:
        for k in range(5, -1, -1):
            bits.append((v >> k) & 1)
    adj = [0] * n
    idx = 0
    for j in range(1, n):
        for i2 in range(j):
            if bits[idx]:
                adj[i2] |= 1 << j
                adj[j] |= 1 << i2
            idx += 1
    return n, adj

def to_g6(n, adj):
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if (adj[i] >> j) & 1 else 0)
    while len(bits) % 6:
        bits.append(0)
    out = chr(n + 63)
    for k in range(0, len(bits), 6):
        v = 0
        for bit in bits[k:k+6]:
            v = (v << 1) | bit
        out += chr(v + 63)
    return out

def has_clique(adj, n, k):
    """Return True if graph has a clique of size k (bitset recursion)."""
    def rec(cand, depth):
        if depth == k:
            return True
        while cand:
            v = (cand & -cand).bit_length() - 1
            cand &= cand - 1
            if bin(cand & adj[v]).count('1') >= k - depth - 1:
                if rec(cand & adj[v], depth + 1):
                    return True
        return False
    return rec((1 << n) - 1, 0)

def complement(adj, n):
    full = (1 << n) - 1
    return [(~adj[v]) & full & ~(1 << v) for v in range(n)]

def degrees(adj):
    return [bin(a).count('1') for a in adj]
