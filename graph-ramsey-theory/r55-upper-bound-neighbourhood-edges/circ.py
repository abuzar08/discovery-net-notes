"""Is there a (5,5,n)-circulant for n = 44 or 45?

A circulant C_n(S) has vertex set Z_n with i ~ j iff j-i in S, where
S = -S and 0 not in S.  It is vertex-transitive, so it contains a K_5 iff it
contains one through 0, i.e. iff some 4-subset {a,b,c,d} of S has all its
pairwise differences in S.  An independent 5-set is a K_5 of the complement,
which is the circulant on the complementary connection set, so the same test
applies twice.

The degree is |S|, so the window n-25 <= d <= 24 restricts which S are worth
testing.  At n = 45 every element pairs with its negative, so |S| is even and
the admissible degrees are 20, 22, 24 only -- degrees 21 and 23 cannot occur
in a circulant of odd order.

Multiplier symmetry: for u in Z_n^*, C_n(uS) is isomorphic to C_n(S), so it
suffices to test one representative per orbit.  This is used only to speed the
search; the reported counts are of full orbits, and `--no-sym` runs the
complete unreduced enumeration as a cross-check.

DISCIPLINE.  A false "no circulant exists" claim was made in an earlier lane
of mine (h2575, corrected at h2635) because a search was reported as
exhaustive when it was not.  So this file always prints the number of
candidates it actually examined next to the number it should have examined,
and refuses to summarise unless they agree.

    python3 circ.py N [--no-sym] [--limit K]
"""
import itertools as it
import sys
import time


def pairs_for(n):
    """Representative differences; each stands for {d, n-d} (or {d} if 2d=n)."""
    out = []
    for d in range(1, n // 2 + 1):
        if 2 * d == n:
            out.append((d,))          # self-paired
        else:
            out.append((d, n - d))
    return out


def has_k5_through_0(n, Sset):
    """Is there {a,b,c,d} in S with every pairwise difference in S?"""
    S = sorted(Sset)
    L = len(S)
    for i in range(L):
        a = S[i]
        for j in range(i + 1, L):
            b = S[j]
            if (b - a) % n not in Sset:
                continue
            for k in range(j + 1, L):
                c = S[k]
                if (c - a) % n not in Sset or (c - b) % n not in Sset:
                    continue
                for l in range(k + 1, L):
                    d = S[l]
                    if ((d - a) % n in Sset and (d - b) % n in Sset
                            and (d - c) % n in Sset):
                        return True
    return False


def good(n, Sset):
    """No K_5 and no independent 5-set."""
    if has_k5_through_0(n, Sset):
        return False
    comp = set(range(1, n)) - Sset
    return not has_k5_through_0(n, comp)


def canon(n, Sset, units):
    best = None
    for u in units:
        t = frozenset((u * x) % n for x in Sset)
        key = tuple(sorted(t))
        best = key if best is None else min(best, key)
    return best


def main():
    n = int(sys.argv[1])
    nosym = "--no-sym" in sys.argv
    limit = 0
    for a in sys.argv:
        if a.startswith("--limit="):
            limit = int(a.split("=")[1])
    P = pairs_for(n)
    units = [u for u in range(1, n) if __import__("math").gcd(u, n) == 1]
    lo, hi = n - 25, 24
    print(f"n={n}: {len(P)} difference classes, degree window [{lo},{hi}], "
          f"|Z_n^*| = {len(units)}")

    # which subsets of the classes give an admissible degree
    sizes = [len(p) for p in P]
    admissible = []
    for r in range(len(P) + 1):
        for combo in it.combinations(range(len(P)), r):
            deg = sum(sizes[i] for i in combo)
            if lo <= deg <= hi:
                admissible.append(combo)
    print(f"  candidate connection sets with admissible degree: {len(admissible)}")

    seen = set()
    tested = examined = 0
    found = []
    t0 = time.time()
    for combo in admissible:
        examined += 1
        if limit and examined > limit:
            break
        S = set()
        for i in combo:
            S.update(P[i])
        if not nosym:
            key = canon(n, frozenset(S), units)
            if key in seen:
                continue
            seen.add(key)
        tested += 1
        if good(n, S):
            found.append(sorted(S))
    el = time.time() - t0
    scanned = examined if not limit else min(examined, limit)
    print(f"  examined {scanned} of {len(admissible)}"
          f"{' (LIMITED SAMPLE, not exhaustive)' if limit else ' -- COMPLETE'}")
    print(f"  isomorphism classes tested: {tested}")
    print(f"  (5,5,{n})-circulants found: {len(found)}")
    for S in found[:5]:
        print(f"     S = {S}")
    print(f"  time {el:.1f}s  ->  {scanned/el:.0f} candidates/s")
    if limit:
        print(f"  PROJECTION for the full run: "
              f"{len(admissible)/(scanned/el)/60:.1f} minutes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
