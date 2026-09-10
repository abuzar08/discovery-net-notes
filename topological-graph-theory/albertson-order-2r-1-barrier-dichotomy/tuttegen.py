#!/usr/bin/env python3
"""
Every Tutte set at once: a general obstruction count for the (k, 30-2k) routes.

WHAT THIS REPLACES.  tutte324.py checked two hand-picked FAMILIES of Tutte set
and left the question open because "some OTHER Tutte set" might obstruct.
adv58.py then answered it on a handful of explicit graphs by computing nu.
Neither quantifies over all Tutte sets and all admissible H at once.

This does.  It parameterises an ARBITRARY Tutte set by six integers and derives
six counting inequalities that every Tutte set of every admissible H must
satisfy.  If no value of the six satisfies all six, the configuration has no
obstructing Tutte set at all, the route succeeds on EVERY admissible H, and
theta(H) <= 28 against theta(H) = 29 -- so the configuration is impossible.

==============================================================================
THE FAMILY.  Removing k vertex-disjoint triangles of H leaves n' = 58 - 3k
vertices needing a matching of 30 - 2k, i.e. Tutte-Berge deficiency at most
k - 2.  The deficiency has the parity of n', hence of k, so an obstruction needs
a Tutte set of deficiency D = k: A LARGER k ASKS THE ADVERSARY FOR MORE, at the
cost of deleting more of L.

THE PARAMETRISATION.  With H' = H - T_1 - ... - T_k,

  A   = L' minus S, the surviving low vertices;  a = |A|,  a_i = |A ^ Q_i|
  s_L = |L'| - a,   s_R = |S ^ R|
  U   = union of the components of H' - S containing NO vertex of A; every such
        component lies inside R.   u = |U|,  t = their number
  W   = R - S_R - U, the R-vertices in components that DO meet A;  p = the
        number of components of H[W]
  iso = the number of vertices of A whose R-neighbours all lie in S_R

and c_A for the number of components meeting A.

THE BLOCK-FOREST BOUNDS ON c_A (blockcut.py).  Three low vertices that pairwise
share a block share a COMMON block, because the block-cut tree is acyclic and
two blocks meet in at most one vertex.  Hence

        A inside one block        A is independent in H,  c_A <= iso + p
        A not inside one block    H[A] has at most 2 components,  c_A <= 2
        blocks partition L        H[L] is complete multipartite,  c_A = 1

and, sharper: if A is not inside one block and H[A] has exactly TWO components,
ONE OF THEM IS A SINGLETON.  Were both of size at least 2, any x,x' in one and
y,y' in the other would close a cycle in the block-cut tree unless all four
shared a block, and extending that over both parts puts all of A inside one
block.  So c_A = 2 costs the adversary something concrete: the singleton is a
separate component of H' - S only if it has no W-neighbour at all (making it one
of the iso vertices, which needs rho <= s_R) or the W-vertices split, p >= 2.

==============================================================================
THE SIX INEQUALITIES.  Each follows from the class constraints alone -- no
placement is fixed -- so each holds for every admissible H.  Throughout
turan(x) = floor(x^2/3) and rho_i = q_i + |R| - 29.

 (1) COUNT.    c_A^odd + t^odd >= s_L + s_R + D.
     o(H' - S) <= c_A + t, and o counts ODD components only: the U-components
     have total size u so the number of odd ones has the parity of u, and the
     components meeting A have total size a + |W| likewise.

 (2) DEGREE.   sum_i a_i rho_i + e(H[R]) - turan(u - t + 1) <= 28(|R| - u).
     Sum d_H(z) over z in R - U; no vertex of U has an A-neighbour.

 (3) TURAN.    e(H[R]) <= C(|R|,2) - C(|R| - s_R, 2)
                          + turan( (|R| - s_R) - (t + p) + 1 ).

 (4) SPREAD.   sum_i a_i rho_i <= a(|R| - u).

 (5) S_R-DEGREE.
       max(0, sum_i a_i rho_i - (a - iso)|W|)
          + e(H[R]) - turan(|W| - p + 1) - turan(u - t + 1)   <=   28 s_R.

 (6) U-DEGREE.  28u + |R| - X + 24*[w not in U]
                     <=  u(s_L + 3k + s_R) + 2 turan(u - t + 1).
     Every z in R has x_z >= 1 and sum_{z in R} x_z = X = 2m - 1624 <= 56, so
     the vertices of U carry nearly the full degree 29 each; but a vertex of U
     has NO neighbour in A, so its L-neighbours lie in S_L or among the 3k
     deleted triangle vertices, and its H[R]-neighbours lie in its own component
     or in S_R.  A LARGE U CANNOT EXIST: its vertices are too high-degree to be
     cut off.  This was found by pricing the sharpenings (slack58.py) rather
     than by guessing, and it is worth more than the two component-count
     refinements put together.

Since x_w >= 25 gives d_H(w) <= 4, a degree cap over a set containing w is 24
smaller; the adversary's placement of w among S_R, W and U is scanned, and (2),
(5) and (6) all use it.

Monotonicity keeping the scan finite and exact: raising t or p only shrinks the
turan terms, so it tightens (2), (3), (5) and (6) while only loosening (1); the
adversary takes t + p at the minimum (1) allows, and the scan runs over every
split of that minimum and every u.

==============================================================================
SOUNDNESS.  All six are NECESSARY conditions, so an infeasible scan is a proof
and a feasible scan proves nothing.  Getting the direction wrong here would be
the twelfth defect, so the inequalities are tested rather than trusted: part 0
takes the explicit admissible H of adv58.py, computes its Gallai-Edmonds set --
a genuine Tutte set attaining the true deficiency -- reads all six parameters
off it and checks every inequality against the real set; part 0b re-runs the
scan at D = 1, where an obstruction provably exists because n' = 49 is odd, so a
scan reporting INFEASIBLE there would prove an inequality false.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import auditc as AC
import alpha58 as A58
import turan58 as T
import residue58 as R58
import blockr58 as BR
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N58 = 2 * r
ALPHA = 3
CW = 4


HANDICAP = [0, 0, 0, 0, 0]      # sensitivity probe; see slack58.py


def turan(x):
    """Maximum edges of a K_4-free graph on x vertices."""
    return x * x // 3 if x > 0 else 0


def cap_w(RSZ):
    return (RSZ - 1) * (RSZ - 1) // 3 + CW


def min_rho_sum(a, cells, min_blocks):
    """Least sum_i a_i rho_i placing a vertices in cells (rho, capacity),
    using at least min_blocks distinct cells.  None if impossible."""
    cs = sorted(cells)
    if a > sum(c for _, c in cs):
        return None
    left, tot, used = a, 0, 0
    for rho, cap in cs:
        if left <= 0:
            break
        k = min(left, cap)
        if k:
            used += 1
            tot += k * rho
            left -= k
    if left > 0:
        return None
    if used < min_blocks:
        fill = [(rho, cap) for rho, cap in cs if cap > 0]
        if len(fill) < 2:
            return None
        tot += fill[1][0] - fill[0][0]      # move one vertex to the next cell
    return tot


def max_rho_sum(n, cells):
    """Largest sum_i n_i rho_i placing n vertices in cells (rho, capacity)."""
    tot = 0
    for rho, cap in sorted(cells, reverse=True):
        if n <= 0:
            break
        take = min(n, cap)
        tot += take * rho
        n -= take
    return tot


def _ok(RSZ, eHR, rsum, a, iso, sL, sR, u, t, p, cA, D, X=52, k=3):
    """The six inequalities at one point of the parameter space.

    The singleton w has x_w >= 25, so d_H(w) <= 4 while every other z in R has
    only x_z >= 1 and d_H(z) <= 28.  A degree cap over a set containing w is
    therefore 24 smaller.  The adversary chooses where w sits, so the point is
    feasible if ANY of the three placements works."""
    W = RSZ - sR - u
    if W < 0 or p > W or (W > 0 and p < 1) or (W == 0 and p != 0):
        return False
    if t > u or (u > 0 and t < 1) or (u == 0 and t != 0):
        return False
    # o counts ODD components only.  The U-components have total size u, so
    # the number of odd ones has the parity of u and is at most t; likewise the
    # components meeting A have total size a + |W|, so the number of odd ones
    # among them has that parity and is at most c_A.  Either bound may cost one.
    todd = t if (u - t) % 2 == 0 else t - 1
    cAodd = cA if (a + W - cA) % 2 == 0 else cA - 1
    if cAodd + todd - HANDICAP[0] < sL + sR + D:                    # (1)
        return False
    if rsum > a * (RSZ - u) - HANDICAP[3]:                          # (4)
        return False
    ein = turan(u - t + 1)
    ew = turan(W - p + 1)
    full = RSZ * (RSZ - 1) // 2
    rest = RSZ - sR
    if eHR > (full - rest * (rest - 1) // 2
              + turan(rest - (t + p) + 1) - HANDICAP[2]):
        return False                                                 # (3)
    lhs2 = rsum + eHR - ein
    lhs5 = max(0, rsum - (a - iso) * W) + eHR - ew - ein
    # (6) U-DEGREE.  Every z in R has x_z >= 1 and sum_{z in R} x_z = X <= 56,
    # so the vertices of U carry nearly the full degree 29 each:
    #     sum_{z in U} d_H(z) = 29u - sum_U x_z >= 28u + |R| - X ,
    # and 24 more when w lies outside U, since x_w >= 25.  But a vertex of U has
    # NO neighbour in A, so its L-neighbours lie in S_L or among the 3k deleted
    # triangle vertices, and its H[R]-neighbours lie in its own component or in
    # S_R.  Hence
    #     sum_{z in U} d_H(z) <= u(s_L + 3k + s_R) + 2 turan(u - t + 1) .
    # A large U therefore cannot exist: its vertices are too high-degree to be
    # cut off.  This is the constraint the sensitivity table said was missing.
    #
    # The competing L-side bound sum_{z in U} d_L(z) = e(L - A, U) <=
    # sum_{v in L - A} rho_{b(v)}, which does not grow with u, was implemented
    # and MEASURED: it never binds -- taking the minimum of the two changes the
    # closure count by nothing at all, at three times the runtime.  Recorded so
    # a successor does not re-derive it.
    hi6 = u * (sL + 3 * k + sR) + 2 * ein
    h2, h5 = HANDICAP[1], HANDICAP[4]
    for where, cap2, cap5 in (("S", 28 * (RSZ - u) - 24 - h2, 28 * sR - 24 - h5),
                              ("W", 28 * (RSZ - u) - 24 - h2, 28 * sR - h5),
                              ("U", 28 * (RSZ - u) - h2, 28 * sR - h5)):
        if where == "S" and sR < 1:
            continue
        if where == "W" and W < 1:
            continue
        if where == "U" and u < 1:
            continue
        if 28 * u + RSZ - X + (0 if where == "U" else 24) > hi6:
            continue                                                 # (6)
        if lhs2 <= cap2 and lhs5 <= cap5:                     # (2) and (5)
            return True
    return False


def route_closed(RSZ, mult, eHR, X=56):
    """(closed, k or reason).

    Tries the family (t_3,t_2) = (k, 30-2k) for every k the blocks allow, and
    returns the first k whose scan is infeasible.  Removing k disjoint triangles
    leaves n' = 58 - 3k vertices needing a matching of 30 - 2k, i.e. deficiency
    at most k - 2; the deficiency has the parity of n', which is the parity of
    k, so an obstruction needs D = k.  A LARGER k therefore asks the adversary
    for more, at the cost of deleting more of L."""
    NL = N58 - RSZ
    qs = sorted(mult, reverse=True)
    if len(qs) < 3:
        return False, "fewer than three blocks"
    # k disjoint triangles: take k vertices from each of the three largest
    # blocks, avoiding the at most two vertices a block shares with the other
    # two (blocks of a Gallai forest meet in at most one vertex).  Vertices of
    # different blocks that are not those cut vertices share no block, so they
    # are H-adjacent.
    kmax = kmax_guaranteed(mult, NL)
    ks = list(range(3, kmax + 1))
    if not ks:
        return False, "three disjoint triangles not guaranteed"
    for k in ks:
        if not obstructed(RSZ, mult, eHR, k, NL, X=X):
            return True, k
    return False, "a parameter point survives"


def obstructed(RSZ, mult, eHR, k=3, NL=None, Dover=None, X=56):  # noqa: C901
    """True if some parameter point satisfies all six inequalities.

    False is a proof that no Tutte set of any admissible H obstructs the
    (k, 30-2k) route, hence that theta(H) <= 28 and the configuration is
    impossible."""
    if NL is None:
        NL = N58 - RSZ
    extra = sum(mult) - NL
    part = (extra == 0)                 # the blocks partition L
    D = k if Dover is None else Dover
    LP = NL - 3 * k                                  # |L'|, the true value
    if LP < 0:
        return True, "L too small"
    # Lower bound on |N_H(v) ^ R| for a vertex charged to block i.  A vertex in
    # several blocks has a LARGER D_v, so assigning each vertex to its cheapest
    # block and filling blocks to capacity q_i bounds sum_i a_i rho_i from
    # below whether or not the blocks partition L.
    avail = [q if part else max(0, q - extra) for q in mult]
    cells = sorted((max(0, mult[i] + RSZ - 29), mult[i], avail[i])
                   for i in range(len(mult)))
    # The k triangles are OURS to choose.  Taking their 3k vertices from the
    # cheapest blocks -- at most k from any one, which is exactly when k
    # disjoint triangles with that distribution exist -- leaves the surviving
    # low vertices as expensive as possible, which is what (2) and (5) want.
    need, red = 3 * k, []
    for rho, q, av in cells:
        take = min(need, k, av)
        red.append((rho, q - take))
        need -= take
    if need > 0:
        return True                      # k disjoint triangles unavailable
    cells = red

    # a = 0: every vertex of R - S_R lies in U, so W is empty
    for sR in range(0, RSZ + 1):
        u = RSZ - sR
        for t in range(1 if u else 0, u + 1):
            if _ok(RSZ, eHR, 0, 0, 0, LP, sR, u, t, 0, 0, D, X, k):
                return True
    # case A: A is NOT inside a single block.  In a Gallai forest three
    # vertices that pairwise share a block share a COMMON block, since the
    # block-cut tree has no cycle; so if A is not inside one block, the
    # complement H[A] has at most two components and c_A <= 2.
    # If A is not inside one block, H[A] has at most two components, and when
    # it has exactly two ONE OF THEM IS A SINGLETON: were both of size >= 2,
    # any x,x' in one and y,y' in the other would close a cycle in the block-cut
    # tree unless all four shared a block, and extending that over both parts
    # puts all of A inside one block.  So c_A = 2 costs the adversary something
    # concrete -- the singleton {v} is a separate component of H' - S only if v
    # has no W-neighbour at all (then v is one of the iso vertices, which needs
    # rho_v <= s_R) or the W-vertices split, forcing p >= 2.
    minrho = min((rho for rho, cap in cells if cap > 0), default=0)
    for a in range(2, LP + 1):
        rsum = min_rho_sum(a, cells, 2 if part else 1)
        if rsum is None:
            continue
        sL = LP - a
        for sR in range(0, RSZ + 1):
            branches = [(1, 0, 1)]
            if not part:
                if minrho <= sR:
                    branches.append((2, 1, 1))       # singleton isolated
                branches.append((2, 0, 2))           # W splits, p >= 2
            for cA, iso, pmin in branches:
                t = max(0, sL + sR + D - cA)
                for u in range(t if t else 0, RSZ - sR + 1):
                    W = RSZ - sR - u
                    p = min(pmin, W) if W else 0
                    if W and p < pmin:
                        continue
                    tt = max(t, 1 if u else 0)
                    if _ok(RSZ, eHR, rsum, a, iso, sL, sR, u, tt, p, cA,
                           D, X, k):
                        return True
    # case B: A inside a single block, c_A <= iso + p
    for rh, cap in cells:
        for a in range(1, min(cap, LP) + 1):
            rsum = a * rh
            sL = LP - a
            for sR in range(0, RSZ + 1):
                isomax = a if rh <= sR else 0
                for iso in range(0, isomax + 1):
                    tp = sL + sR + D - iso
                    if tp < 0:
                        tp = 0
                    if tp > RSZ - sR:
                        continue
                    for t in range(0, tp + 1):
                        p = tp - t
                        for u in range(t if t else 0, RSZ - sR - p + 1):
                            if _ok(RSZ, eHR, rsum, a, iso, sL, sR, u, t, p,
                                   iso + p, D, X, k):
                                return True
    return False


def configurations():
    """The surviving order-58 clique-block configurations, as in state29.py."""
    out = []
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            cap = min(T.turan_k4free(RSZ), cap_w(RSZ))
            for mult, eL in AC.multisets_audited(NL, max(base, 0),
                                                 base + RSZ * (RSZ - 1) // 2,
                                                 d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                eGR = eL - base
                eHR = RSZ * (RSZ - 1) // 2 - eGR
                if eGR < 0 or eHR < 0 or eHR > cap:
                    continue
                if A58.alpha_lb(mult, NL) > ALPHA:
                    continue
                if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                    continue
                if BR.blockR(mult, NL, RSZ, eHR) >= Z:
                    continue
                out.append((m, RSZ, tuple(mult), eHR))
    return out


def part0():
    """Soundness: the six inequalities hold on a genuine Tutte set."""
    print("PART 0   the inequalities tested on a real Tutte set")
    import adv58
    from matching import max_matching, size, check_matching, odd_components
    built = adv58.build(0)
    if built is None:
        print("   the reference placement failed; soundness test SKIPPED")
        return False
    lab, adj, Ridx, wv = built
    _, ok = adv58.admissible(lab, adj, Ridx, wv)
    if not ok:
        print("   reference placement not admissible; SKIPPED")
        return False
    B = [[x for x in range(adv58.NL) if lab[x] == i] for i in range(3)]
    T9 = set()
    for k in range(3):
        for i in range(3):
            T9.add(B[i][k])
    keep = [v for v in range(adv58.N) if v not in T9]
    idx = {v: i for i, v in enumerate(keep)}
    a2 = [set() for _ in keep]
    for v in keep:
        for x in adj[v]:
            if x in idx:
                a2[idx[v]].add(idx[x])
    nk = len(keep)
    mt = max_matching(nk, a2)
    assert check_matching(nk, a2, mt)
    nu = size(mt)
    exposed = [v for v in range(nk) if mt[v] == -1]
    even, stack = set(exposed), list(exposed)
    while stack:
        v = stack.pop()
        for x in a2[v]:
            if mt[x] != -1 and mt[x] not in even:
                even.add(mt[x])
                stack.append(mt[x])
    Aset = {x for v in even for x in a2[v] if x not in even}
    oc = odd_components(nk, a2, sorted(Aset))
    defi = oc - len(Aset)
    print("   nu = %d on %d vertices; Gallai-Edmonds set |S| = %d, o = %d,"
          % (nu, nk, len(Aset), oc))
    print("   deficiency = %d  (equals n - 2 nu = %d): %s"
          % (defi, nk - 2 * nu, "PASS" if defi == nk - 2 * nu else "FAIL"))
    Sset = {keep[i] for i in Aset}
    Aliv = [v for v in range(adv58.NL) if v not in T9 and v not in Sset]
    sR = len([z for z in Ridx if z in Sset])
    sL = len([v for v in range(adv58.NL) if v not in T9 and v in Sset])
    rem = [v for v in keep if v not in Sset]
    remset = set(rem)
    seen, comps = set(), []
    for v in rem:
        if v in seen:
            continue
        st, comp = [v], []
        seen.add(v)
        while st:
            x = st.pop()
            comp.append(x)
            for y in adj[x]:
                if y in remset and y not in seen:
                    seen.add(y)
                    st.append(y)
        comps.append(comp)
    Uc = [c for c in comps if all(v >= adv58.NL for v in c)]
    u, t = sum(len(c) for c in Uc), len(Uc)
    cA = len(comps) - t
    Uset = {v for c in Uc for v in c}
    Wset = [z for z in Ridx if z not in Sset and z not in Uset]
    wsub = set(Wset)
    seenw, p = set(), 0
    for v in Wset:
        if v in seenw:
            continue
        p += 1
        st = [v]
        seenw.add(v)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y in wsub and y not in seenw:
                    seenw.add(y)
                    st.append(y)
    rsum = sum(len([z for z in adj[v] if z >= adv58.NL]) for v in Aliv)
    iso = sum(1 for v in Aliv
              if all(z in Sset for z in adj[v] if z >= adv58.NL))
    RSZ, eHR, a = adv58.RS, adv58.EHR, len(Aliv)
    print("   read off the real S: a = %d, iso = %d, s_L = %d, s_R = %d,"
          % (a, iso, sL, sR))
    print("   u = %d, t = %d, |W| = %d, p = %d, c_A = %d, sum a_i rho_i = %d"
          % (u, t, len(Wset), p, cA, rsum))
    good = _ok(RSZ, eHR, rsum, a, iso, sL, sR, u, t, p, cA, defi)
    print("   all six inequalities hold on a genuine Tutte set: %s"
          % ("PASS" if good else "FAIL -- an inequality is false"))
    print()
    return good and defi == nk - 2 * nu


def main():
    print("Every Tutte set at once: the (k, 30-2k) routes on all admissible H")
    print("order 58, r = %d;  removing k disjoint triangles leaves 58 - 3k" % r)
    print("vertices needing a matching of 30 - 2k, so an obstruction needs a")
    print("Tutte set of deficiency D = k")
    print()
    sound = part0()
    print("PART 0b  negative control: D = 1 must always be reachable")
    cs = [(24, [17, 12, 5], 178), (26, [20, 8, 4], 120), (22, [18, 13, 7], 149)]
    bad = [c for c in cs
           if not obstructed(c[0], c[1], c[2], 3, None, Dover=1)]
    print("   for k = 3 the graph H' has 49 vertices, so its deficiency is odd")
    print("   and at least 1; a scan at D = 1 that reported INFEASIBLE would")
    print("   therefore prove an inequality false.  Configurations tested: %d,"
          % len(cs))
    print("   wrongly reported infeasible: %d -> %s"
          % (len(bad), "PASS" if not bad else "FAIL"))
    print()
    negok = not bad

    print("PART 1   the scan over all surviving configurations")
    cfgs = configurations()
    closed, open_ = [], []
    for m, RSZ, mult, eHR in cfgs:
        cl, wit = route_closed(RSZ, list(mult), eHR, 2 * m - N58 * DEG)
        (closed if cl else open_).append((m, RSZ, mult, eHR, wit))
    print("   configurations scanned: %d" % len(cfgs))
    print("   NO Tutte set can obstruct -- the route succeeds on EVERY")
    print("   admissible H, so the configuration is IMPOSSIBLE: %d"
          % len(closed))
    print("   the counts still permit an obstruction: %d" % len(open_))
    print()
    for name, lst in (("closed", closed), ("still open", open_)):
        if not lst:
            continue
        byR = {}
        for m, RSZ, mult, eHR, wit in lst:
            byR[RSZ] = byR.get(RSZ, 0) + 1
        print("   %s by |R|: %s" % (name, sorted(byR.items())))
    print()
    reasons = {}
    for m, RSZ, mult, eHR, wit in open_:
        reasons[wit] = reasons.get(wit, 0) + 1
    print("   why the open ones are open: %s" % sorted(reasons.items()))
    used = {}
    for m, RSZ, mult, eHR, wit in closed:
        used[wit] = used.get(wit, 0) + 1
    print("   the k that closed them: %s" % sorted(used.items()))
    print()
    print("CONCLUSION")
    print("   The six inequalities are necessary conditions on an ARBITRARY")
    print("   Tutte set, so an infeasible scan closes the configuration for")
    print("   every admissible H, not for a sample.  %d of %d configurations"
          % (len(closed), len(cfgs)))
    print("   fall; %d do not, and for those the counts do not decide --"
          % len(open_))
    print("   which is not the same as an obstruction existing.")
    print()
    print("   Soundness controls: real Tutte set %s; D = 1 negative control %s"
          % ("PASS" if sound else "FAIL", "PASS" if negok else "FAIL"))
    print()
    print("   r = 29 is NOT proved.")


def kmax_guaranteed(mult, NL):
    """The largest k for which EVERY Gallai block forest with these block
    orders contains k vertex-disjoint triangles of H.

    A triangle of H needs three vertices pairwise sharing no block, and three
    PRIVATE vertices of three distinct blocks always qualify.  Let c_i be the
    number of non-private vertices of block i.  Writing b_v for the number of
    blocks containing v and extra = sum_i q_i - |L| = sum_v (b_v - 1),

        sum_i c_i = sum_{b_v >= 2} b_v = extra + #{cut vertices} <= 2 extra ,

    since a cut vertex contributes at least one to extra; and separately
    c_i <= #{cut vertices} <= extra for each single block.  k disjoint triangles
    exist as soon as r_i <= min(k, q_i - c_i) can be chosen with sum r_i = 3k,
    which is possible exactly when sum_i min(k, q_i - c_i) >= 3k.  The worst
    forest is the one minimising that sum, so this maximises the reduction a
    budget of 2 extra can buy: pushing block i below k costs (q_i - k)+ first
    and then one per unit, down to zero.

    Conservative on purpose -- the c_i are coupled in ways this ignores, so a
    real forest may carry more triangles than the bound certifies.  It is a
    GUARANTEE, not a census: "not guaranteed" is not "does not exist"."""
    extra = sum(mult) - NL
    budget = 2 * extra
    best = 0
    for k in range(3, 16):
        base = sum(min(k, q) for q in mult)
        # room_i is the most min(k,q_i) can fall, given c_i <= extra as well
        costs = sorted((max(0, q - k),
                        min(k, q) - min(k, max(0, q - min(extra, q))))
                       for q in mult)
        left, cut = budget, 0
        for entry, room in costs:
            if room <= 0 or left <= entry:
                continue
            take = min(room, left - entry)
            cut += take
            left -= entry + take
        if base - cut >= 3 * k:
            best = k
    return best


if __name__ == "__main__":
    main()
