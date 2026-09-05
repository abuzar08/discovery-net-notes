"""Compare the base (orbit) clause set of each regenerated published CNF with
reviewer-1's independent encoder.  For hybrid files the manifest gives the
number of leading base clauses; for base files it is the whole file.
usage: python3 compare_base.py regen_dir tags.txt"""
import sys, json, os
from indep_encode import permutation, orbits_of_pairs, base_clauses

regen, tagfile = sys.argv[1], sys.argv[2]
bad = 0
for line in open(tagfile):
    tag, kind = line.split()
    f, p, k = (int(x) for x in tag.replace('f', '').replace('p', ' ').replace('k', ' ').replace('_', '').split())
    path = os.path.join(regen, tag + '.cnf')
    cls = []
    nv_hdr = None
    for l in open(path):
        if l[0] == 'c':
            continue
        if l[0] == 'p':
            nv_hdr = int(l.split()[2]); continue
        cls.append(frozenset(int(x) for x in l.split()[:-1]))
    if kind == 'hybrid':
        man = json.load(open(path + '.manifest.json'))
        nbase = man['base_clauses']; nv_orbit = man['orbit_vars']
    else:
        nbase = len(cls); nv_orbit = nv_hdr
    sig = permutation(42, f, p, k)
    var, nv = orbits_of_pairs(42, sig)
    mine = base_clauses(42, var)
    theirs = cls[:nbase]
    ok = (nv == nv_orbit) and len(set(theirs)) == len(theirs) == len(mine) and set(theirs) == mine
    # every base clause must be an orbit-5-set clause; and the redundant tail must not mention only orbit vars in a way that duplicates base
    print(f"{tag}: orbit vars {nv} (file {nv_orbit}), base clauses {len(mine)} (file {nbase}), {'MATCH' if ok else 'MISMATCH'}")
    bad += not ok
print("all base clause sets match" if not bad else f"{bad} MISMATCHES")
sys.exit(bad != 0)
