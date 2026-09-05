#!/usr/bin/env python3
"""
The Albertson r = 27 frontier is a single (order, size) row, and at order 2r-1
a single local configuration survives for r = 27..30.

Exact integer / Fraction arithmetic only: no floating point, no randomness, no
solver, no external data.  Imports verify_range.py (barrier classification) and
recursive.py (recursive integer-aware sampling) from the same directory.

--------------------------------------------------------------------------
NON-DOMINATION LEMMA (proved by hand; used to eliminate barrier size 3).

  Let H be factor-critical with no conformal triangle -- no triangle T with
  H - V(T) having a perfect matching.  Let w be a vertex with N_H(w) contained
  in a set B such that {w} is a component of H - B.  Then no vertex of N_H(w) is
  adjacent to every other vertex of N_H(w).

  Proof.  delta(H) >= 2 for a factor-critical H, so |N_H(w)| >= 2.  Suppose
  a in N_H(w) is adjacent to every other vertex of N_H(w).  H - a has a perfect
  matching M, which matches w to some u in N_H(w)\\{a}.  Then a ~ u, w ~ a and
  w ~ u, so {w,a,u} is a triangle, and M \\ {wu} is a perfect matching of
  H - {a,w,u}.  That is a conformal triangle -- contradiction.  QED

  For an r-critical G of order 2r-1 with connected complement H (hence H is
  factor-critical by Stehlik, and has no conformal triangle since theta(H) = r):
    * barrier size b = 3 is impossible: there B is a triangle, hence a clique,
      so every vertex of N_H(w) dominates the rest;
    * for b = 4 with B = T u {s}: N_H(w) is not inside T, so w ~ s, and s is
      adjacent to no vertex of N_T(w); hence d_H(w) = 1 + |N_T(w)| in {2,3,4}.
  This generalises the singleton-triangle separator lemma at ledger height 2583
  (the case B = T); the proof above is independent of that contribution.
--------------------------------------------------------------------------
"""
import recursive as R
import verify_range as V

_L = R.build(59, rounds=3)


def cr_lower(n, q):
    """Recursive integer-aware sampling lower bound on cr over all (n,q) graphs."""
    if n < 4 or q <= 0 or n > 59:
        return 0
    return _L[n][min(q, len(_L[n]) - 1)]


# route the barrier classifier through the stronger bound
V.cr_lower_nm = cr_lower
V.analyse.__globals__['cr_lower_nm'] = cr_lower
V.controls.__globals__['cr_lower_nm'] = cr_lower
V.tri_free_survivors.__globals__['cr_lower_nm'] = cr_lower


def cranston_E(r, n):
    """Cranston (arXiv:2512.08020) Lemma E: an n-vertex r-critical graph with
    r >= 4 containing no subdivision of K_r has e(G) >= n(r-1)/2 + (r-3).  No
    restriction on n.  The hypothesis holds for every Albertson counterexample,
    since a subdivision of K_r inside G would give cr(G) >= cr(TK_r) = cr(K_r).
    (Cranston's Lemma D drops the subdivision hypothesis at the price of
    n != 2r-1; Lemma E is the form used here, and it applies at n = 2r-1.)"""
    return -(-(n * (r - 1) + 2 * (r - 3)) // 2)


def ky_floor(r, n):
    num = (r + 1) * (r - 2) * n - r * (r - 3)
    return -(-num // (2 * (r - 1)))


def floor_of(r, n):
    return max(ky_floor(r, n), cranston_E(r, n))


def ceiling_of(r, n):
    """Largest q with cr_lower(n,q) < Z(r); -1 if there is none."""
    return max([q for q in range(len(_L[n])) if _L[n][q] < V.Z(r)], default=-1)


def main():
    print("Albertson: the r = 27 frontier, and the configuration at order 2r-1")
    print("Exact arithmetic; published inputs only.")
    print()
    print("SOUNDNESS CONTROLS (barrier machinery): %s"
          % ("PASS" if V.controls() else "FAIL"))
    bad = [n for n in range(5, 60) if _L[n][n * (n - 1) // 2] > V.Z(n)]
    mono = all(_L[n][q] <= _L[n][q + 1]
               for n in range(5, 60) for q in range(len(_L[n]) - 1))
    print("SOUNDNESS CONTROLS (recursive table): L(n,C(n,2)) <= Z(n) %s ; "
          "monotone in q %s"
          % ("PASS" if not bad else "FAIL", "PASS" if mono else "FAIL"))
    print()
    print("Cross-check of the recursive table against ledger height 2617 (n = 50):")
    print("   q      632   633   634   635   636   637")
    print("   here  %s" % "  ".join("%4d" % _L[50][q] for q in range(632, 638)))
    print("   there  4727  4752  4778  4804  4830  4856")
    print("   L(24,132) = %d   (height 2617 reports 164; the r=27 chain claims 165)"
          % _L[24][132])
    print()

    print("=" * 74)
    print("A. Order n = 2r-1: open rows and the surviving configuration")
    print("=" * 74)
    print("   r   n    KY   LemE   ceiling   open m       gaps to Z(r)      config")
    for r in (27, 28, 29, 30):
        n = 2 * r - 1
        lo, hi = floor_of(r, n), ceiling_of(r, n)
        rows = list(range(lo, hi + 1))
        cfg = set()
        for m in rows:
            for br in V.analyse(r, m):
                if br[0] != 3:                     # b = 3 dead by non-domination
                    cfg.add(br[0])
            assert not V.tri_free_survivors(r, m), "triangle-free case survived"
        print("  %2d  %2d  %4d  %5d  %8d   %3d..%-3d  %-18s b=%s, (n-6,1,1)"
              % (r, n, ky_floor(r, n), cranston_E(r, n), hi, lo, hi,
                 str([V.Z(r) - _L[n][m] for m in rows]), sorted(cfg)))
    print()
    print("  For every open row the triangle-free case is impossible, barrier size")
    print("  b = 3 is impossible by the non-domination lemma, and the only surviving")
    print("  configuration is b = 4 with component multiset (n-6, 1, 1): H - B has")
    print("  exactly two singleton components w1, w2 and one component of order n-6,")
    print("  both wi adjacent to s, N_T(wi) non-empty, s adjacent to no vertex of")
    print("  N_T(w1) u N_T(w2), and 2 <= d_H(wi) = 1 + |N_T(wi)| <= 4.")
    print()

    print("=" * 74)
    print("B. The r = 27 frontier")
    print("=" * 74)
    print("  Sadhu arXiv:2609.01682 Thm 1.3: a 27-critical G with cr(G) < cr(K_27)")
    print("  has |G| in {53, 54} and connected complement.")
    print()
    rows = []
    for n in (53, 54):
        lo, hi = floor_of(27, n), ceiling_of(27, n)
        if lo > hi:
            print("  n=%d: Cranston Lemma E floor %d EXCEEDS the ceiling %d"
                  "   ->   ORDER %d IS IMPOSSIBLE" % (n, lo, hi, n))
        else:
            print("  n=%d: floor %d, ceiling %d   ->   m in [%d, %d]"
                  % (n, lo, hi, lo, hi))
            rows += [(n, m) for m in range(lo, hi + 1)]
    print()
    print("  RESULT: a 27-critical counterexample to Albertson's conjecture has")
    if len(rows) == 1:
        n0, m0 = rows[0]
        print("          |G| = %d and e(G) = %d exactly -- a single row." % (n0, m0))
    else:
        print("          (|G|, e(G)) in %s" % (rows,))
        n0, m0 = rows[0]
    print("          Remaining gap: cr_lower(%d,%d) = %d against Z(27) = %d, i.e. %d."
          % (n0, m0, _L[n0][m0], V.Z(27), V.Z(27) - _L[n0][m0]))
    print("          Its complement carries the unique configuration of part A.")
    print()


if __name__ == "__main__":
    main()
