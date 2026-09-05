"""Standard-library-only checker for census_certificate.json.

For every certified member H it verifies, from first principles:

  * H is simple with minimum degree at least 3;
  * H is non-planar, and every 1-crossing planarization of H is non-planar,
    so cr(H) >= 2                       [Kuratowski subdivisions]
  * some 2-crossing planarization of H is planar, so cr(H) = 2
                                        [rotation system + Euler]
  * for every edge e, some <=1-crossing planarization of H - e is planar,
    so cr(H - e) <= 1                   [rotation systems + Euler]

Hence each member is 2-crossing-critical with crossing number exactly 2.
No planarity algorithm is trusted; the primitives are reused from
verify_certificate.py, which is likewise standard-library only.

    python3 verify_census.py census_certificate.json [n6.txt n7.txt ...]

Passing the census output files additionally checks that the certified set is
exactly the set of `CRIT2` lines those files report.
"""
import itertools
import json
import sys

from verify_certificate import (check_kuratowski, check_planar_embedding,
                                indep, planarize)


def deser(cfg):
    out = []
    for c in cfg:
        out.append(tuple([c[0]] + [tuple(x) for x in c[1:]]))
    return out


def check_good_config(E, cfg):
    """A configuration is a good 2-crossing drawing: two crossings of
    independent edge pairs, no edge used twice within a crossing, and either
    four distinct edges or one edge crossed twice."""
    if len(cfg) == 2 and all(c[0] == 'x' for c in cfg):
        a, b = cfg[0][1], cfg[0][2]
        c, d = cfg[1][1], cfg[1][2]
        if len({a, b, c, d}) != 4:
            return False
        if not (indep(a, b) and indep(c, d)):
            return False
        return all(x in E for x in (a, b, c, d))
    if len(cfg) == 1 and cfg[0][0] == 'xx':
        _, e, f, g = cfg[0]
        if len({e, f, g}) != 3:
            return False
        if not (indep(e, f) and indep(e, g)):
            return False
        return all(x in E for x in (e, f, g))
    return False


def check_member(rec):
    n = rec["n"]
    E = [tuple(sorted(e)) for e in rec["edges"]]
    if len(set(E)) != len(E):
        return False, "repeated edge"
    deg = {}
    for u, v in E:
        if u == v or not (0 <= u < n and 0 <= v < n):
            return False, "bad edge"
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    if len(deg) != n or min(deg.values()) < 3:
        return False, "minimum degree below 3"

    ok, why = check_kuratowski(n, E, rec["nonplanar"])
    if not ok:
        return False, f"non-planarity of H: {why}"

    pairs = [(e, f) for e, f in itertools.combinations(E, 2) if indep(e, f)]
    if len(pairs) != len(rec["one_crossing"]):
        return False, "wrong number of 1-crossing witnesses"
    for (f, g), w in zip(pairs, rec["one_crossing"]):
        nn, ee = planarize(E, [('x', f, g)], n)
        ok, why = check_kuratowski(nn, ee, w)
        if not ok:
            return False, f"1-crossing {f},{g}: {why}"

    cfg = deser(rec["cr_le_2"]["config"])
    if not check_good_config(E, cfg):
        return False, "cr<=2 configuration is not a good 2-crossing drawing"
    nn, ee = planarize(E, cfg, n)
    ok, why = check_planar_embedding(nn, ee, rec["cr_le_2"]["rotation"])
    if not ok:
        return False, f"cr<=2 witness: {why}"

    if len(rec["delete"]) != len(E):
        return False, "wrong number of edge-deletion witnesses"
    seen = set()
    for w in rec["delete"]:
        e = tuple(sorted(w["e"]))
        if e not in E:
            return False, f"deleted edge {e} not in H"
        seen.add(e)
        rest = [f for f in E if f != e]
        if w["crossing"] is None:
            nn, ee = n, rest
        else:
            f, g = (tuple(sorted(x)) for x in w["crossing"])
            if f not in rest or g not in rest or not indep(f, g):
                return False, f"bad crossing pair for H-{e}"
            nn, ee = planarize(rest, [('x', f, g)], n)
        ok, why = check_planar_embedding(nn, ee, w["rotation"])
        if not ok:
            return False, f"H-{e}: {why}"
    if seen != set(E):
        return False, "not every edge deleted"
    return True, "2-crossing-critical, cr = 2"


def load_census(path):
    out = set()
    for line in open(path):
        p = line.split()
        if len(p) < 4 or p[0] != "CRIT2":
            continue
        E = tuple(sorted(tuple(sorted(map(int, x.split('-'))))
                         for x in p[3].strip(',').split(',')))
        out.add((int(p[1]), E))
    return out


def main(certpath, censuspaths):
    cert = json.load(open(certpath))
    members = cert["members"]
    bynum = {}
    got = set()
    for i, rec in enumerate(members):
        ok, why = check_member(rec)
        if not ok:
            print(f"FAIL member {i} (n={rec['n']}): {why}")
            return 1
        bynum[rec["n"]] = bynum.get(rec["n"], 0) + 1
        got.add((rec["n"], tuple(sorted(tuple(sorted(e)) for e in rec["edges"]))))
    print(f"verified {len(members)} members, each 2-crossing-critical with cr = 2")
    for n in sorted(bynum):
        print(f"    n = {n:2d} : {bynum[n]}")

    if censuspaths:
        want = set()
        for p in censuspaths:
            want |= load_census(p)
        if want != got:
            print(f"MISMATCH with census files: "
                  f"{len(want - got)} uncertified, {len(got - want)} extra")
            return 1
        print(f"certified set equals the {len(want)} `CRIT2` lines of "
              f"{len(censuspaths)} census files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2:]))
