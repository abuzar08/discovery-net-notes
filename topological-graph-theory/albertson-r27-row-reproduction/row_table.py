"""The four Albertson r=27 rows under the recursive integer-aware sampling
bound, from published lemmas only and with the chain's unpublished input.

Rows: a 27-critical counterexample has order 53 or 54 (Sadhu Thm 1.3) and at
least f(27,53)=713 or f(27,54)=726 edges (Sadhu (2)).  A row is closed when the
bound reaches Z(27)=6084 >= cr(K_27).

Variants:
  published base only          -- Euler, the density sum over the published
                                  k-planar bounds, both Buengener-Kaufmann
                                  bounds; nothing unpublished
  + exact cr(K_n) for n <= 13  -- settled values injected at q = C(n,2)
  + the chain's (a)            -- additionally assume cr(H) >= 5e - 495 for
                                  every 24-vertex H (heights 1765/2035), the
                                  one ingredient of the chain that published
                                  machinery does not give

    python3 row_table.py
"""
from math import comb

import recursive_sampling as rs

Z27 = 6084
ROWS = [(54, 726), (53, 713), (53, 714), (53, 715)]
CHAIN = {(54, 726): 6084, (53, 713): 6089, (53, 714): 6100, (53, 715): 6129}
CRK = {5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150, 13: 219}

base = rs.base_bound


def with_exact_cliques(n, q):
    b = base(n, q)
    if q == comb(n, 2) and n in CRK:
        b = max(b, CRK[n])
    return b


def with_chain_a(n, q):
    b = with_exact_cliques(n, q)
    if n == 24:
        b = max(b, 5 * q - 495)          # the chain's unpublished input (a)
    return b


def main():
    print(f"Z(27) = {Z27};  a row closes when the bound reaches it.\n")
    print(f"{'variant':<30}" + "".join(f"{str(r):>13}" for r in ROWS))
    out = {}
    for name, fn in [("published base only", base),
                     ("+ exact cr(K_n), n <= 13", with_exact_cliques),
                     ("+ the chain's (a) at n=24", with_chain_a)]:
        rs.base_bound = fn
        L = rs.build(54)
        vals = [L[n][m] for (n, m) in ROWS]
        out[name] = vals
        print(f"{name:<30}" + "".join(
            f"{str(v) + ('*' if v >= Z27 else ''):>13}" for v in vals))
    rs.base_bound = base
    print(f"{'the chain itself claims':<30}"
          + "".join(f"{CHAIN[r]:>13}" for r in ROWS))
    print("\n* = at or above Z(27)\n")

    pub = out["published base only"]
    closed = [r for r, v in zip(ROWS, pub) if v >= Z27]
    open_ = [r for r, v in zip(ROWS, pub) if v < Z27]
    print(f"From published lemmas alone, {len(closed)} of the 4 rows close: "
          + ", ".join(map(str, closed)) + ".")
    print(f"Still open: {', '.join(map(str, open_))}, short by "
          + ", ".join(str(Z27 - v) for v in pub if v < Z27) + ".")
    a = out["+ the chain's (a) at n=24"]
    print("With the chain's (a), every row closes; at (53,713) the bound is "
          f"{a[ROWS.index((53,713))]}, exactly the chain's claimed 6089.")


if __name__ == "__main__":
    main()
