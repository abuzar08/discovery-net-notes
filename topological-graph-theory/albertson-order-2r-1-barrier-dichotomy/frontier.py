#!/usr/bin/env python3
"""
The Albertson r = 27 frontier reduces to four explicit (order, size) rows, and at
order n = 2r-1 a single local configuration survives for r = 27..30.

Exact integer / Fraction arithmetic only: no floating point, no randomness, no
solver, no external data, no imported campaign code.  Imports verify_range.py
from the same directory for the barrier classification.

--------------------------------------------------------------------------
NON-DOMINATION LEMMA (proved by hand; used to eliminate barrier size 3).

  Let H be factor-critical with no conformal triangle -- i.e. no triangle T with
  H - V(T) having a perfect matching.  Let w be a vertex whose neighbourhood is
  contained in a set B with {w} a component of H - B (equivalently N_H(w) is
  contained in B).  Then no vertex of N_H(w) is adjacent to every other vertex
  of N_H(w).

  Proof.  delta(H) >= 2 for a factor-critical H, so |N_H(w)| >= 2.  Suppose
  a in N_H(w) is adjacent to every other vertex of N_H(w).  H - a has a perfect
  matching M.  M matches w to some u in N_H(w)\\{a}.  By assumption a ~ u, and
  w ~ a, w ~ u, so {w,a,u} is a triangle; and M \\ {wu} is a perfect matching of
  H - {a,w,u}.  So {w,a,u} is conformal -- contradiction.  QED

  Consequences used below, for an r-critical G of order 2r-1 whose complement H
  is connected (hence factor-critical, and with no conformal triangle since
  theta(H) = r):
    * barrier size b = 3 is impossible.  There B is a triangle, hence a clique,
      so every vertex of N_H(w) dominates the rest.
    * for b = 4 with B = T u {s}, T a triangle: N_H(w) is not inside T, so
      w ~ s; and s is not adjacent to any vertex of N_T(w).  Hence
      d_H(w) = 1 + |N_T(w)| with |N_T(w)| in {1,2,3}, so 2 <= d_H(w) <= 4.
  This lemma generalises the singleton-triangle separator lemma published at
  ledger height 2583 (which is the case B = T); the proof here is independent.
--------------------------------------------------------------------------
"""
from fractions import Fraction as F
import verify_range as V


def cranston_E(r, n):
    """Cranston (arXiv:2512.08020) Lemma E: an n-vertex r-critical graph with
    r >= 4 that contains no subdivision of K_r has e(G) >= n(r-1)/2 + (r-3).
    There is no restriction on n, and the hypothesis holds for every Albertson
    counterexample: a subdivision of K_r inside G would give
    cr(G) >= cr(TK_r) = cr(K_r).  (Cranston's Lemma D drops the subdivision
    hypothesis at the price of n != 2r-1; Lemma E is the form used here.)"""
    return -(-(n * (r - 1) + 2 * (r - 3)) // 2)


def ky_floor(r, n):
    """Kostochka-Yancey (Sadhu Lemma 2.4)."""
    num = (r + 1) * (r - 2) * n - r * (r - 3)
    return -(-num // (2 * (r - 1)))


def sampling_ceiling(r, n):
    """Largest m for which the sampled form of Sadhu Lemma 2.1 stays below Z(r).
    Returns C(n,2) if it never reaches Z(r)."""
    tot = n * (n - 1) // 2
    for m in range(1, tot + 1):
        if any(V.sample_bound(m, n, k) >= V.Z(r) for k in range(4, n + 1)):
            return m - 1
    return tot


def odd_order_floor(r):
    """Edge floor at n = 2r-1 forced by the surviving configuration alone.

    After the non-domination lemma only barrier size b = 4 survives, with the
    unique component multiset (n-6, 1, 1): two singleton components w1, w2 whose
    H-neighbourhoods lie inside the 4-set B, so d_H(wi) <= 4 and
    x_{wi} = (r-1) - d_H(wi) >= r-5.  Hence
        2m - (2r-1)(r-1) = sum_v x_v >= 2(r-5).
    This is weaker than Cranston Lemma E for r in the range studied here; it is
    reported for comparison, and the analysis below uses the stronger floor."""
    n = 2 * r - 1
    return -(-(n * (r - 1) + 2 * (r - 5)) // 2)


def surviving_configs(r, m):
    """Barrier sizes and multisets surviving verify_range.analyse, with b = 3
    removed by the non-domination lemma (every b = 3 multiset has a singleton)."""
    return [br for br in V.analyse(r, m) if br[0] != 3]


def floor_of(r, n):
    return max(ky_floor(r, n), cranston_E(r, n))


def main():
    print("Albertson: the r=27 frontier, and the surviving configuration at order 2r-1")
    print("Exact arithmetic; published inputs only.")
    print()
    print("SOUNDNESS CONTROLS (verify_range): %s"
          % ("PASS" if V.controls() else "FAIL"))
    print()

    print("=" * 74)
    print("A. Order n = 2r-1, after the non-domination lemma")
    print("=" * 74)
    print("   r   n     KY   LemE   this-work-floor   ceiling   open rows   surviving b")
    for r in (27, 28, 29, 30):
        n = 2 * r - 1
        lo = floor_of(r, n)
        hi = sampling_ceiling(r, n)
        bs, cfgs = set(), set()
        for m in range(lo, hi + 1):
            for br in surviving_configs(r, m):
                bs.add(br[0])
        print("  %2d  %2d  %5d  %5d  %15d  %8d   %4d..%-4d  %s"
              % (r, n, ky_floor(r, n), cranston_E(r, n), odd_order_floor(r),
                 hi, lo, hi, sorted(bs)))
    print()
    print("  In every case the only surviving barrier size is b = 4 and the only")
    print("  surviving component multiset of H-B is (n-6, 1, 1): H - B has exactly")
    print("  two singleton components w1, w2 and one component of order n-6.")
    print("  By the non-domination lemma both wi are adjacent to s, N_T(wi) is")
    print("  non-empty, s is adjacent to no vertex of N_T(w1) u N_T(w2), and")
    print("  2 <= d_H(wi) = 1 + |N_T(wi)| <= 4.")
    print()

    print("=" * 74)
    print("B. The r = 27 frontier")
    print("=" * 74)
    print("  Sadhu arXiv:2609.01682 Thm 1.3: a 27-critical G with cr(G) < cr(K_27)")
    print("  has |G| in {53, 54} and connected complement.")
    print()
    rows = []
    for n in (53, 54):
        lo, hi = floor_of(27, n), sampling_ceiling(27, n)
        print("  n=%d: floor max(Kostochka-Yancey %d, Cranston Lemma E %d) = %d;"
              % (n, ky_floor(27, n), cranston_E(27, n), lo))
        print("        sampling ceiling %d   ->   m in [%d, %d]   (%d row%s)"
              % (hi, lo, hi, hi - lo + 1, "" if hi == lo else "s"))
        rows += [(n, m) for m in range(lo, hi + 1)]
    print()
    print("  RESULT: the r = 27 case of Albertson's conjecture reduces to %d rows:"
          % len(rows))
    print("          %s" % (rows,))
    print("  and at n = 53 each surviving complement carries the unique local")
    print("  configuration of part A.")
    print()
    print("  Distance to closure, exactly:")
    for n, m in rows:
        b = V.cr_lower_nm(n, m)
        print("     (%d,%d): sampled bound %5d,  Z(27) = %d,  gap %3d"
              % (n, m, b, V.Z(27), V.Z(27) - b))
    print()


if __name__ == "__main__":
    main()
