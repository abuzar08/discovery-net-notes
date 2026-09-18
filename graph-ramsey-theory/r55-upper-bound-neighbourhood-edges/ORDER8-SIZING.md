# The order-8 row: per-orbit caps complete, two of five groups enumerated

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-18.
Checker: `order8.py`. Output: `order8.txt`.
**Offered by citation; none of researcher-1's instances were run.**

researcher-1's census note opens order 8 and closes it as a route:

> *"order 8 is no better, which kills the obvious escape. Excluding every group
> of order 8 would bound the Sylow 2-subgroup by 4 and so bound \(a\) — which
> nothing does today … An action of \(Z_2^3\) on 42 points (five regular orbits
> and one of size 2) has 126 pair orbits, more than the 97 to 99 of the
> \(Z_3 \times Z_3\) actions … 15 of 15 timed out at 120 s."*

That is **one action**, measured. This note supplies the part this seat owes:
the per-orbit fixed-point caps for every orbit an order-8 group can have, and
the case list as far as it was affordable.

## 1. The caps, complete

Evaluated by the orbit lemma on the actual induced action, not on orbit size
alone — which matters, because two groups can give different bounds on an orbit
of the same size:

| orbit | induced group | cap on \(|\operatorname{Fix}(H)|\) |
|---|---|---|
| size 2 | — | 37 |
| size 4 | cyclic or Klein | 26, and **22** after the global count at \(n = 42\) |
| size 8 | cyclic \(C_8\) | **17** |
| size 8 | \(Z_2^3\) regular | **13** |
| size 8 | \(Z_4 \times Z_2\) regular | **13** |

So an order-8 group with a regular orbit fixes at most \(17\) points, and at
most \(13\) unless it is cyclic. The \(22\) at size \(4\) is
`FIXED-POINT-MAXIMUM.md`'s theorem, not the raw lemma.

> **I did not apply my own theorem on the first attempt.** The first version of
> `order8.py` used the raw orbit-lemma value \(26\) at size-4 orbits and so
> reported \(\max |\operatorname{Fix}| = 26\) for \(Z_4 \times Z_2\). With the
> \(22\) in place it is \(22\), and the count falls from \(22\,531\) to
> \(22\,366\). **This is exactly the failure I diagnosed in researcher-1's lane
> at pass 53** — a lane's own strongest result not being pointed at a newly
> opened row, because it is filed under the row it was proved for. Two passes
> after writing that down I did it myself.

## 2. The enumeration, as far as it got

An action is a multiset of point stabilisers with indices summing to \(42\),
faithful, counted up to \(\operatorname{Aut}(G)\) — the same ordered-versus-
unordered distinction reviewer-1 flagged for the Klein case.

| group | subgroups | ordered | up to \(\operatorname{Aut}(G)\) | \(\max |\operatorname{Fix}|\) |
|---|---|---|---|---|
| \(Z_8\) | 4 | \(155\) | \(\mathbf{155}\) | \(16\) |
| \(Z_4 \times Z_2\) | 8 | \(67\,914\) | \(\mathbf{22\,366}\) | \(22\) |
| \(Z_2^3\) | 16 | — | **not completed** | — |
| \(D_4\) | — | — | **not reached** | — |
| \(Q_8\) | — | — | **not reached** | — |

\(Z_8\)'s ordered and unordered counts agree because every subgroup of a cyclic
group is characteristic, so \(\operatorname{Aut}(Z_8)\) cannot move one
stabiliser multiset to another.

**\(Z_2^3\) did not finish and the per-group time cap failed to stop it.** With
\(16\) subgroups the composition count is far larger than for the other two,
and canonicalising each accepted action against the \(168\) elements of
\(\operatorname{Aut}(Z_2^3) = GL_3(2)\) is the dominant cost. The cap is
written as a wall-clock test inside the recursion and evidently does not fire
where I expected; that is a defect in this file, not a property of the problem,
and it is recorded rather than hidden. The fix is to enumerate by *set* of
distinct stabilisers first — at most \(2^{16}\) sets, each faithfulness-checked
and canonicalised once — and count the compositions for each by dynamic
programming, instead of canonicalising per action.

## 3. What is usable now

- The caps of §1 are complete and are the load-bearing part: they say what any
  order-8 group can fix, whatever its action.
- **A group of order 8 acting on a \((5,5,42)\)-graph fixes at most 22
  points**, because a faithful action cannot have all orbits of size \(\le 2\)
  for \(Z_8\) or \(Z_4 \times Z_2\) (their index-2 subgroups all contain a
  common involution), and any orbit of size \(4\) or \(8\) caps at \(22\) or
  less. For \(Z_2^3\) an all-orbits-\(\le 2\) faithful action does exist, and
  there the cap is only the involution bound \(36\) — so that sub-case is the
  one a sharper argument would have to attack.
- \(Z_8\) is a small row: \(155\) actions, none fixing more than \(16\) points.

## 4. What this does and does not establish

**Establishes** the caps table; the \(Z_8\) and \(Z_4 \times Z_2\) counts up to
\(\operatorname{Aut}(G)\); and that no \(Z_8\) or \(Z_4\times Z_2\) action fixes
more than \(16\) or \(22\) points respectively.

**Does not establish** anything about \(Z_2^3\), \(D_4\) or \(Q_8\) beyond the
caps, and does not claim the order-8 row is sized. The faithfulness test for
\(D_4\) and \(Q_8\) in this file intersects the chosen stabilisers rather than
their cores, which is exact only when every subgroup is normal — true for the
three abelian groups, not for the other two, where it would give an upper
bound.

**Cited, not proved.** \(R(3,5) = 14\), \(R(4,5) = 25\); researcher-1's census
note for the \(126\)-orbit measurement quoted above.
