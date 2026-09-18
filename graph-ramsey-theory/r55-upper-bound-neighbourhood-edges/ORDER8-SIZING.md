# The order-8 row, sized: 728,432 actions against order 4's 1,377

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-18.
Checkers: `order8_exact.py` (Burnside), `order8.py` (direct enumeration).
Output: `order8_exact.txt`.
**Offered by citation; none of researcher-1's instances were run.**

researcher-1's census note opens order 8 and closes it as a route:

> *"order 8 is no better, which kills the obvious escape. Excluding every group
> of order 8 would bound the Sylow 2-subgroup by 4 and so bound \(a\) — which
> nothing does today … An action of \(Z_2^3\) on 42 points (five regular orbits
> and one of size 2) has 126 pair orbits, more than the 97 to 99 of the
> \(Z_3 \times Z_3\) actions … 15 of 15 timed out at 120 s."*

That is **one action**, measured. This note supplies the row: the per-orbit
fixed-point caps, and the exact number of faithful actions surviving them for
each of the five groups of order 8.

## 1. The caps

Evaluated by the orbit lemma on the actual induced action, not on orbit size
alone — which matters, because two groups give different bounds on an orbit of
the same size:

| orbit | induced group | cap on \(|\operatorname{Fix}(H)|\) |
|---|---|---|
| size 2 | — | 37 |
| size 4 | cyclic or Klein | **22** (the global count at \(n = 42\)) |
| size 8 | cyclic \(C_8\) | **17** |
| size 8 | \(Z_2^3\) or \(Z_4 \times Z_2\) regular | **13** |

The \(22\) is `FIXED-POINT-MAXIMUM.md`'s theorem, not the raw lemma value of
\(26\).

> **I did not apply my own theorem on the first attempt.** The first version of
> `order8.py` used \(26\) at size-4 orbits and reported
> \(\max|\operatorname{Fix}| = 26\) for \(Z_4 \times Z_2\); with \(22\) in place
> it is \(22\). **This is exactly the failure I diagnosed in researcher-1's
> lane at pass 53** — a lane's strongest result not pointed at a newly opened
> row, because it is filed under the row it was proved for. Two passes after
> writing the rule down I broke it.

## 2. The row

A faithful action is a multiset of point stabilisers: a function \(c\) on the
subgroup lattice with \(\sum_H c(H)\,[G:H] = 42\), trivial kernel, and
\(c(G) \le \min\) cap over the used subgroups of index \(> 1\). Counted **up to
\(\operatorname{Aut}(G)\)**, which permutes the lattice — the ordered-versus-
unordered distinction reviewer-1 flagged for the Klein case.

| group | \(|\operatorname{Aut}|\) | subgroups | actions surviving the caps |
|---|---|---|---|
| \(Z_8\) | 4 | 4 | \(\mathbf{155}\) |
| \(Z_4 \times Z_2\) | 8 | 8 | \(\mathbf{22\,366}\) |
| \(Z_2^3\) | 168 | 16 | \(\mathbf{630\,495}\) |
| \(D_4\) | 8 | 10 | \(\mathbf{74\,430}\) |
| \(Q_8\) | 24 | 6 | \(\mathbf{986}\) |
| **total** | | | \(\mathbf{728\,432}\) |

**Against the order-4 row's \(78 + 1299 = 1377\), order 8 is larger by a factor
of about \(530\).** researcher-1 concluded from one probe that order 8 is no
easier than order 4; the count says it is *much* worse, and says by how much.
\(Q_8\) is the one small corner — \(986\) actions, because it has only six
subgroups and every one of them contains the centre.

## 3. How it was counted, and how it was checked

`order8.py` enumerated actions one at a time and **did not finish \(Z_2^3\)**:
sixteen subgroups, and canonicalising each accepted action against the \(168\)
elements of \(GL_3(2)\) dominates. Three changes make it exact and immediate:

1. **Burnside instead of canonical forms.** The number of \(\operatorname{Aut}(G)\)-orbits
   is the average number of actions fixed by each automorphism, and an action
   fixed by \(a\) is one constant on the \(a\)-orbits of the lattice — so each
   automorphism costs one dynamic program rather than a canonical form per
   accepted action.
2. **Inclusion–exclusion for faithfulness.** The kernel is non-trivial exactly
   when it contains a minimal subgroup; summing over subsets of the atoms with
   alternating sign and collecting by the subgroup generated leaves at most
   sixteen terms.
3. **Stratify by the cap.** \(c(G)\) is the fixed-point count and the cap
   constrains only it, so "min cap \(\ge f\)" is a restriction on which
   subgroups may be used; the caps take few values, so few strata.

**Checked, not asserted.** Two independent checks:

- On point counts where both methods run — \(n = 10, 14, 18\) — Burnside and
  direct enumeration agree for **all five groups at all three sizes**, fifteen
  comparisons.
- At the real \(n = 42\), Burnside reproduces `order8.py`'s direct counts for
  the two groups that one finished: \(155\) and \(22\,366\), exactly.

The faithfulness test now uses the **core** of each stabiliser rather than the
subgroup itself, so \(D_4\) and \(Q_8\) are exact here; last pass's note
recorded them as an upper bound, and that caveat is discharged.

## 4. What this does and does not establish

**Establishes** the caps; the five counts and their total; and that the
order-8 row is roughly \(530\times\) the order-4 row.

**Does not establish** that any of these actions is realisable — every one is a
candidate to be refuted, exactly as in the order-4 row, and none has been run.
Nor does it bound \(a\): that would need *excluding* all of them, which is the
thing researcher-1 correctly says nothing does today.

**One sub-case resists the caps.** For \(Z_2^3\) a faithful action with every
orbit of size \(\le 2\) exists — three index-2 subgroups can intersect
trivially — and there the only bound is the involution lemma's \(36\). For
\(Z_8\) and \(Z_4 \times Z_2\) no such action exists, because all their
index-2 subgroups share a common involution. That is where a sharper argument
would have to bite.

**Cited, not proved.** \(R(3,5) = 14\), \(R(4,5) = 25\); researcher-1's census
note for the \(126\)-orbit measurement quoted above.
