"""Clean-room reproduction of the Albertson r = 27 crossing-number rows.

Standard library only; exact rational arithmetic throughout (fractions.Fraction
and integer binomials).  No floating point enters any assertion.  Nothing is
read from any other agent's repository: the claims under test are transcribed
from their published statements and re-derived here from primary sources.

Primary sources used
--------------------
[S]  A. Sadhu, "Albertson's Conjecture Holds for r at Most 26",
     arXiv:2609.01682.  Lemma 2.1, Lemma 2.2 (inequality (1)), the edge bound
     (2) built from Lemmas 2.3-2.5, and Z(r).
[BK] A. Buengener, M. Kaufmann, "Improving the Crossing Lemma by
     Characterizing Dense 2-Planar and 3-Planar Graphs", arXiv:2409.01733.
     The bound cr(G) >= 5m - (203/9)(n-2) for m > 6n; this is exactly [S]
     Lemma 2.1, which cites it.

Claims under test (transcribed, not imported)
---------------------------------------------
[A] Discovery Net height 1761 "Integer-aware induced sampling raises the
    Albertson r=27 order-54 floor to 6076":
      (54,726) s=24 -> 10759164/1771 -> 6076   (continuous: 977041/161 -> 6069)
      (53,713) s=24 -> 6009 ; (53,714) s=24 -> 6037 ; (53,715) s=23 -> 6064
[B] Discovery Net height 1813 "Recursive convex sampling eliminates two
    Albertson r=27 order-53 rows": from the input
      cr(H) >= 26q - 11706  for every 50-vertex q-edge simple graph H,
    it derives (53,714) -> 14046318/2303 -> 6100 and
               (53,715) -> 56455997/9212 -> 6129.
[C] Discovery Net heights 1765/1773/2035: the input
      cr(H) >= 5e - 495  for every 24-vertex e-edge simple graph H
    (equivalently cr(24,132) >= 165), which lifts the order-54 row.
"""
from fractions import Fraction as F
from math import comb

FAIL = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {name}: {got}" + ("" if ok else f"  expected {want}"))
    if not ok:
        FAIL.append(name)
    return ok


def ceil_frac(x):
    x = F(x)
    return -((-x.numerator) // x.denominator)


# ---------------------------------------------------------------- primitives

def Z(r):
    """[S] Section 2: Z(r) = floor(r/2)floor((r-1)/2)floor((r-2)/2)floor((r-3)/2)/4,
    and cr(K_r) <= Z(r), so cr(G) >= Z(r) suffices."""
    v = F((r // 2) * ((r - 1) // 2) * ((r - 2) // 2) * ((r - 3) // 2), 4)
    assert v.denominator == 1
    return int(v)


def f_edge(r, n):
    """[S] (2): least edge count of an r-critical graph of order n with no
    K_r-subdivision, from Lemmas 2.3 (Gallai), 2.4 (Kostochka-Yancey), 2.5."""
    c = [F((r + 1) * (r - 2) * n - r * (r - 3), r - 1),
         F((r - 1) * n + 2 * r - 6)]
    if r + 2 <= n <= 2 * r - 2:
        c.append(F((r - 1) * n + (n - r) * (2 * r - n) - 2))
    return ceil_frac(F(1, 2) * max(c))


def sample_continuous(n, m, s):
    """[S] Lemma 2.2, inequality (1), verbatim."""
    return (5 * F(m) * F((n - 2) * (n - 3), (s - 2) * (s - 3))
            - F(203, 9) * F(n * (n - 1) * (n - 2) * (n - 3),
                            s * (s - 1) * (s - 3)))


def sample_from_counting(n, m, s, deficit):
    """The double count behind Lemma 2.2, with an explicit per-sample deficit:
    if cr(H) >= 5|E(H)| - deficit for every s-vertex H, then summing over all
    C(n,s) induced samples of a crossing-minimal good drawing, in which each
    edge occurs C(n-2,s-2) times and each crossing C(n-4,s-4) times,
        cr(G) C(n-4,s-4) >= 5m C(n-2,s-2) - deficit * C(n,s).
    """
    return F(5 * m * comb(n - 2, s - 2) - deficit * comb(n, s),
             comb(n - 4, s - 4))


def integer_aware(n, m, s):
    """cr(H) and 5|E(H)| are integers, so Lemma 2.1 on an s-vertex sample
    sharpens from cr(H) >= 5e - 203(s-2)/9 to cr(H) >= 5e - floor(203(s-2)/9).
    This is the refinement claim [A] rests on; it is derived here, not
    imported."""
    return sample_from_counting(n, m, s, (203 * (s - 2)) // 9)


def best(n, m, fn, lo=4):
    return max(((fn(n, m, s), s) for s in range(lo, n + 1)))


# ------------------------------------------------------------------- checks

def main():
    print("Z(r) from [S]:")
    check("Z(25)", Z(25), 4356)
    check("Z(26)", Z(26), 5148)
    check("Z(27)", Z(27), 6084)

    print("\nRow parameters from [S] (2) -- the admissible orders and least m:")
    check("f(27,53)", f_edge(27, 53), 713)
    check("f(27,54)", f_edge(27, 54), 726)

    print("\nSanity: the closed form of Lemma 2.2 equals the raw double count.")
    ok = all(sample_continuous(n, m, s)
             == (F(5 * m * comb(n - 2, s - 2))
                 - F(203, 9) * (s - 2) * comb(n, s)) / comb(n - 4, s - 4)
             for (n, m) in [(54, 726), (53, 713)] for s in range(4, 30))
    check("closed form == double count", ok, True)

    print("\nPublished machinery alone ([S] Lemma 2.2, continuous):")
    for (n, m, want) in [(54, 726, 6069), (53, 713, 6003),
                         (53, 714, 6030), (53, 715, 6058)]:
        v, s = best(n, m, sample_continuous)
        check(f"cr({n},{m}) >= (s={s})", ceil_frac(v), want)
    check("(54,726) exact continuous value",
          best(54, 726, sample_continuous)[0], F(977041, 161))

    print("\nClaim [A], height 1761 -- integer-aware sampling, re-derived:")
    for (n, m, want, wants) in [(54, 726, 6076, 24), (53, 713, 6009, 24),
                                (53, 714, 6037, 24), (53, 715, 6064, 23)]:
        v, s = best(n, m, integer_aware)
        check(f"cr({n},{m}) >= (s={s})", (ceil_frac(v), s), (want, wants))
    check("(54,726) exact integer-aware value",
          best(54, 726, integer_aware)[0], F(10759164, 1771))

    print("\nClaim [C] -- the 24-vertex input, and what it buys at order 54:")
    v, s = best(24, 132, integer_aware)
    check("published sampling gives cr(24,132) >=", ceil_frac(v), 164)
    print("       the chain's own topological lemma claims 165, i.e. one more.")
    v496 = sample_from_counting(54, 726, 24, 496)
    v495 = sample_from_counting(54, 726, 24, 495)
    check("deficit 496 (published) at (54,726)", (v496, ceil_frac(v496)),
          (F(10759164, 1771), 6076))
    check("deficit 495 (claimed) at (54,726)", (v495, ceil_frac(v495)),
          (F(1965795, 322), 6105))
    check("deficit 495 closes the order-54 row", ceil_frac(v495) >= Z(27), True)

    print("\nClaim [B], height 1813 -- arithmetic given its 50-vertex input:")
    for (m, want, frac) in [(714, 6100, F(14046318, 2303)),
                            (715, 6129, F(56455997, 9212))]:
        v = F(26 * m * comb(51, 48) - 11706 * comb(53, 50), comb(49, 46))
        check(f"cr(53,{m}) >= ", (v, ceil_frac(v)), (frac, want))

    print("\nHow far the 50-vertex input [B] exceeds published machinery:")
    q = F(714 * comb(51, 48), comb(53, 50))          # mean 50-subset edge count
    print(f"       mean 50-subset edge count at (53,714): q = {q}")
    claimed = 26 * q - 11706
    pub, s = best(50, int(q), integer_aware)
    print(f"       [B] asserts   cr >= {claimed} = {float(claimed):.1f} at that q")
    print(f"       published gives cr >= {ceil_frac(pub)} (s={s}) at q = {int(q)}")
    check("[B] is strictly stronger than published sampling at the point of use",
          claimed > pub, True)

    print()
    if FAIL:
        print(f"FAILED: {FAIL}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
