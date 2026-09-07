r"""reviewer-1: independent check of h3293 (researcher-2), the last order-57 row.

My own code for everything this contribution actually claims:

  1. the counting identities, from the degree condition alone;
  2. the Koenig lower bound on a matching, implemented from the definition and
     validated exhaustively against true matching numbers on small bipartite
     graphs;
  3. my own enumeration of block multisets and my own shortfall table, using
     only lower bounds on both sides (the sound form);
  4. the direction of every inequality, so that the negative conclusion can be
     seen to be robust to the bounds being loose;
  5. a search for the "26 against 145" aggregate-versus-per-block comparison.

The admissibility filters on block multisets (the e(L) band via `eGR_min`, the
covering condition, the (a, j, sigma) ranges) come from the lane's earlier
order-57 lemmas and are inherited here, not re-derived; that is stated in the
review.
"""
import itertools
import sys

N, DEG, M, RCHI = 57, 28, 828, 29
EH = N * (N - 1) // 2 - M            # edges of the complement H


# ------------------------------------------------------------- identities
def identities(RSZ, eL):
    """every relation h3293 states, recomputed from d_G(v) = 28 for v in L"""
    NL = N - RSZ
    eGLR = DEG * NL - 2 * eL                      # sum of degrees in L
    eGR = M - eL - eGLR
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    eHL = NL * (NL - 1) // 2 - eL
    eHLR = NL * RSZ - eGLR
    return dict(eGLR=eGLR, eGR=eGR, eHR=eHR, eHL=eHL, eHLR=eHLR,
                eHLR_id=NL * (RSZ - DEG) + 2 * eL,
                eHLR_cross=EH - eHL - eHR)


# ------------------------------------------------------------------ Koenig
def cover_capacity(k, side, nz):
    """most edges a vertex cover of size k can carry in a bipartite graph with
    parts of sizes nz and side: cz vertices taken on the Z side carry at most
    cz*side edges, and each of the nz - cz remaining Z-vertices sends at most
    min(k - cz, side) edges into the covered side-vertices"""
    return max(cz * side + (nz - cz) * min(k - cz, side)
               for cz in range(0, min(k, nz) + 1))


def mu_lower(edge_total, side, nz):
    """least k whose covers could carry edge_total edges; by Koenig this is a
    lower bound on the maximum matching"""
    for k in range(0, nz + 1):
        if cover_capacity(k, side, nz) >= edge_total:
            return k
    return nz + 1


def validate_koenig(maxnz=4, maxside=4):
    """exhaustive: for every bipartite graph on parts of size nz and side, the
    bound must not exceed the true matching number"""
    bad = 0
    total = 0
    for nz in range(1, maxnz + 1):
        for side in range(1, maxside + 1):
            cells = [(i, j) for i in range(nz) for j in range(side)]
            for mask in range(1 << len(cells)):
                es = [cells[i] for i in range(len(cells)) if mask >> i & 1]
                total += 1
                # true matching number by brute force
                best = 0
                for r in range(min(nz, side), 0, -1):
                    found = False
                    for sub in itertools.combinations(es, r):
                        if (len({a for a, _ in sub}) == r
                                and len({b for _, b in sub}) == r):
                            found = True
                            break
                    if found:
                        best = r
                        break
                if mu_lower(len(es), side, nz) > best:
                    bad += 1
    return total, bad


# -------------------------------------------------------- block multisets
def block_multisets(RSZ, eLo, eHi):
    """my own enumeration: multisets of block orders q >= 2 with
    sum (q - 1) = |L| - c for some number c >= 1 of components, e(L) = sum
    C(q,2) inside the band, and the two filters the lane documents (no isolated
    low vertex; small blocks must cover the low vertices not in big blocks)"""
    NL = N - RSZ
    d0 = DEG - RSZ
    out = set()
    def rec(rem, cap, edges, blocks):
        if edges > eHi:
            return
        if rem == 0:
            if eLo <= edges <= eHi and blocks:
                big = [q for q in blocks if q - 1 >= d0]
                sb = sum(big)
                if sb <= NL and sum(q * (q - 1) for q in blocks
                                    if q - 1 < d0) >= d0 * (NL - sb):
                    out.add((tuple(sorted(blocks, reverse=True)), edges))
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem - u, u, edges + (u + 1) * u // 2, blocks + [u + 1])
    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return sorted(out)


# ------------------------------------------------------------- the table
def shortfall(RSZ, verbose=True):
    NL, NZ = N - RSZ, RSZ - 2
    X = 2 * M - N * DEG
    base = M - (DEG * RSZ + X)
    sys.path.insert(0, '../../notes/topological-graph-theory/'
                       'albertson-order-2r-1-barrier-dichotomy')
    import r29
    eLo, eHi = base + r29.eGR_min(RSZ), base + RSZ * (RSZ - 1) // 2
    amin = max(1, NZ - X + 2 * DEG - 2)
    rows = []
    for mult, eL in block_multisets(RSZ, eLo, eHi):
        I = identities(RSZ, eL)
        assert I['eHLR'] == I['eHLR_id'] == I['eHLR_cross'], (mult, eL, I)
        maxq = max(mult)
        q2 = mult[1] if len(mult) > 1 else 1
        nu = min(I['eHR'], RSZ // 2)              # upper bound on nu(H[R])
        tneed = maxq + RSZ - 28 - nu
        if tneed <= 0:
            rows.append((mult, eL, maxq, tneed, None, None, 'closes: t <= 0'))
            continue
        # lower bounds on both sides, disjoint: Q_1 and Q_2 - Q_1
        e1 = maxq * (maxq + RSZ - RCHI)
        e2 = max(0, (q2 - 1) * (q2 + RSZ - RCHI))
        side2 = max(q2 - 1, 1)
        best = None
        for a in range(amin, 4):
            for j in range(1, 4):
                for sig in (0, 1):
                    jA = max(0, j + a - 3)
                    c = 2 * (1 - sig) + a - jA
                    if c < 0:
                        continue
                    for c1 in range(0, c + 1):
                        m1 = mu_lower(e1 - c1, maxq, NZ)
                        m2 = mu_lower(e2 - (c - c1), side2, NZ)
                        if best is None or m1 + m2 < best[0]:
                            best = (m1 + m2, a, j, sig, c1, c - c1, m1, m2)
        need = NZ + tneed
        rows.append((mult, eL, maxq, tneed, best[0], need, need - best[0]))
    if verbose:
        print(f'|R| = {RSZ}: |L| = {NL}, |Z| = {NZ}, e(L) band [{eLo}, {eHi}], '
              f'a >= {amin}, {len(rows)} admissible multisets')
        for r in sorted(rows, key=lambda r: (r[6] if isinstance(r[6], int)
                                             else -1)):
            if r[4] is None:
                print(f'   {str(r[0]):18s} e(L)={r[1]} chi={r[2]} {r[6]}')
            else:
                print(f'   {str(r[0]):18s} e(L)={r[1]} chi={r[2]} t>={r[3]} '
                      f'mu_1+mu_2 >= {r[4]}, needed {r[5]}, short by {r[6]}')
    return rows


def aggregate_hunt():
    """look for the '26 against 145' pair the body quotes"""
    print('search for the aggregate-versus-per-block comparison (26 vs 145)')
    for RSZ in (9, 10, 11):
        NL, NZ = N - RSZ, RSZ - 2
        X = 2 * M - N * DEG
        base = M - (DEG * RSZ + X)
        import r29
        eLo, eHi = base + r29.eGR_min(RSZ), base + RSZ * (RSZ - 1) // 2
        for mult, eL in block_multisets(RSZ, eLo, eHi):
            I = identities(RSZ, eL)
            maxq = max(mult)
            agg = I['eHLR'] - NZ * (NL - maxq)
            per = maxq * (maxq + RSZ - RCHI)
            if agg in (26, 145) or per in (26, 145):
                print(f'   |R|={RSZ} {mult}: aggregate {agg}, per-block {per}')
        print(f'   |R|={RSZ}: aggregate values '
              f'{sorted({identities(RSZ, e)["eHLR"] - NZ * (NL - max(m)) for m, e in block_multisets(RSZ, eLo, eHi)})}, '
              f'per-block values '
              f'{sorted({max(m) * (max(m) + RSZ - RCHI) for m, e in block_multisets(RSZ, eLo, eHi)})}')


if __name__ == '__main__':
    tot, bad = validate_koenig()
    print(f'Koenig bound validated on {tot} bipartite graphs, violations {bad}')
    print()
    for RSZ in (10, 11):
        shortfall(RSZ)
        print()
    aggregate_hunt()
