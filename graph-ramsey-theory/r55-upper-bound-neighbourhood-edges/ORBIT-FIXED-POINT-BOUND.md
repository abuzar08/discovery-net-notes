# How many points can a group fix? The general orbit form of researcher-1's lemma

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
Checkers: `orbitbound.py`, `orbit4_exact.py`. Witness: `orbit4_witness.g6`.
About researcher-1's `r55-42-automorphism-census` (`c81e3ad`).
**Offered by citation; none of researcher-1's instances were run.**

principal-1, pass 39: *"The order-4 row is where the completeness work now
lives."* The thing that makes that row finite is a fixed-point bound, so that
is what I checked — and it generalises.

## 1. What researcher-1 proved, and the one line that generalises it

researcher-1's lemma: **an involution of a \((5,5,42)\)-graph fixes at most
\(36\) points.** For a \(2\)-cycle \(\{u, \sigma u\}\), a fixed vertex is
joined to both or to neither, so the fixed set splits as \(F = A \sqcup B\);
\(A\) is triangle-free, \(B\) has no independent \(4\)-set, \(13 + 24 = 37\),
and \(f\) is even, so \(f \le 36\). Re-derived at pass 51 and correct.

The proof uses a \(2\)-cycle, but **nothing in it is about \(2\)-cycles.** Let
\(G \le \operatorname{Aut}(F)\) and let \(O\) be *any* \(G\)-orbit. If \(w\) is
fixed by all of \(G\) and \(x, y \in O\), pick \(g \in G\) with \(gx = y\);
then

$$
w \sim x \iff gw \sim gx \iff w \sim y ,
$$

so \(w\) is joined to all of \(O\) or to none of it — for every orbit at once,
whatever its size.

## 2. The lemma

Write \(\omega = \omega(F[O])\) and \(\alpha = \alpha(F[O])\) for the clique and
independence numbers of the orbit's own induced subgraph.

> **Lemma.** Let \(F\) be an \((s,t)\)-graph, \(G \le \operatorname{Aut}(F)\),
> and \(O\) any \(G\)-orbit. Then
> $$
> |\operatorname{Fix}(G)| \;\le\; \bigl(R(s-\omega,\,t) - 1\bigr) + \bigl(R(s,\,t-\alpha) - 1\bigr).
> $$

*Proof.* \(\operatorname{Fix}(G) = A \sqcup B\) with \(A\) joined to all of
\(O\) and \(B\) to none. A \(K_s\) inside \(A \cup O\) may use at most
\(\omega\) vertices of \(O\), and every vertex of \(A\) is joined to all of
\(O\), so \(A\) contains no \(K_{s-\omega}\); \(A\) contains no \(I_t\) either,
so \(|A| \le R(s-\omega,t) - 1\). Dually an \(I_t\) inside \(B \cup O\) may use
at most \(\alpha\) vertices of \(O\), so \(B\) contains no \(I_{t-\alpha}\) and
no \(K_s\), giving \(|B| \le R(s,t-\alpha)-1\). A clique meeting both \(A\) and
\(B\) and \(O\) is impossible, since \(B\) misses \(O\); likewise an
independent set. \(\square\)

At \(|O| = 2\) in a \((5,5)\)-graph this is \(13 + 24 = 37\) — researcher-1's
lemma. **At every larger orbit it is strictly better**, because a bigger orbit
forces a bigger \(\omega\) or a bigger \(\alpha\).

## 3. The table

Evaluated by machine on \((5,5)\)-graphs, enumerating the invariant graphs on
the orbit rather than arguing about them, and discarding those that already
contain a \(K_5\) or an \(I_5\):

| \(\vert O\vert\) | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bound on \(\vert\operatorname{Fix}(G)\vert\) | **37** | 28 | **26** | 26 | 17 | 17 | 17 | 13 | 13 | 13 | 13 |

The \(\vert O\vert = 2\) column is researcher-1's, before parity takes it to
\(36\). The \(Z_2 \times Z_2\) regular orbit gives the same \(26\) as the
cyclic \(4\)-orbit: eight invariant shapes, all admissible, none better.

Two corollaries, read off the table rather than asserted:

> **Corollary A.** A subgroup of \(\operatorname{Aut}(F)\) fixing more than
> \(28\) vertices of a \((5,5,42)\)-graph has every orbit of size \(1\) or
> \(2\); hence \(g^2 = 1\) for all \(g\), and \(G\) is an elementary abelian
> \(2\)-group.

> **Corollary B.** A subgroup fixing more than \(26\) vertices has every orbit
> of size \(1\), \(2\) or \(3\), so every element has order \(1\), \(2\), \(3\)
> or \(6\).

## 4. What it removes from the order-4 row

Both published counts are reproduced exactly by the same code before the new
constraint is applied, which is the cross-check that the case lists are the
same objects:

| group | with the involution lemma alone | published | with the orbit lemma at \(\vert O\vert = 4\) | removed |
|---|---|---|---|---|
| \(Z_4\) cycle types | \(90\) | 90 ✓ | \(\mathbf{84}\) | 6 |
| \(Z_2\times Z_2\) actions | \(1347\) | 1347 ✓ | \(\mathbf{1328}\) | 19 |

The six \(Z_4\) types removed, all of them fixing more than \(26\) points while
carrying a \(4\)-cycle:

$$
(c_1,c_2,c_4) \in \{(28,1,3),\,(28,3,2),\,(30,0,3),\,(30,2,2),\,(32,1,2),\,(34,0,2)\}.
$$

The nineteen \(Z_2^2\) actions removed all have at least one regular orbit and
\(a \in \{28, 30, 32, 34\}\): ten with one regular orbit, seven with two, two
with three.

**Twenty-five of \(1437\) cases, which is not a lot.** It is worth having
because each case is a solver run that researcher-1 has priced at hours, and
because the lemma costs nothing to apply — but the honest headline is the
table, not the twenty-five.

**Ordered or unordered.** reviewer-1's review of `c81e3ad`, point (3), notes
that \(1347\) is the count *up to permuting the three subgroups of order two*,
that the ordered count is \(6465\), and that *"a successor who reads it as
ordered will build 6465 formulas instead of 1347"*. The same ambiguity would
attach to my number, so both are given. My independent enumeration reproduces
**\(6465\)** ordered before the new constraint, and gives **\(6401\)** after.
Unordered is the right one to enumerate — permuting the subgroups is an
automorphism of \(Z_2 \times Z_2\) and carries invariant graphs to isomorphic
ones — so the number to use is \(1328\).

## 4a. This answers a question reviewer-1 left open

Its review of `c81e3ad`, point (5), made the looseness exhaustive — every
involution of every one of the \(328\) catalogued graphs is fixed-point-free,
so the observed maximum is \(0\) against a bound of \(36\) — and concluded:

> *"anyone hoping to shrink the 90 types or the 1347 actions by sharpening this
> bound has a great deal of room and no evidence about where the truth lies."*

There is now evidence, and it points both ways. The bound **can** be sharpened
— \(36 \to 26\) at \(|O| = 4\), which is where the order-4 row lives — and the
sharpened bound is **exactly where the truth lies for any one-orbit argument**,
by §5 below. The remaining room is real but it is not reachable from this
direction.

## 5. I tried to sharpen the bound, and it is already tight

The bound \(26\) is arithmetic: it bounds \(|A|\) and \(|B|\) separately and
adds them. That ignores the fact that \(A\) and \(B\) sit inside **one** graph
and constrain each other, so it looked improvable. It is not.

In the mixed shapes (\(C_4\) and \(2K_2\) — every shape with both an edge and a
non-edge) the orbit turns out to impose nothing beyond what is already used:
\(A\) is exactly a \((3,5)\)-graph, \(B\) is exactly the complement of one, and
no clique or independent set can meet \(A\), \(B\) and \(O\) at once. So the
question collapses to a self-contained one:

> How large can \(|A| + |B|\) be, with \(A\) a \((3,5)\)-graph, \(B\) the
> complement of a \((3,5)\)-graph, and \(A \cup B\) together a \((5,5)\)-graph?

That is decidable, and small, because the catalogues involved are **complete
and tiny** at the sizes that matter: one \((3,5,13)\)-graph, twelve
\((3,5,12)\)-graphs. At \(f = 26\) it is a single pair of fixed graphs with
\(169\) free cross-edges.

**It is satisfiable.** The model was rebuilt into an actual graph on
\(13 + 13 + 4 = 30\) vertices and audited from scratch: it is a
\((5,5,30)\)-graph, \(A\) is a \((3,5,13)\)-graph, \(B\) is a
\((5,3,13)\)-graph, and every one of the \(26\) vertices is joined to all four
orbit vertices or to none. It is committed as `orbit4_witness.g6`.

So **\(26\) is exactly right**: no argument that looks only at one orbit, the
all-or-none split, and Ramsey numbers on the two parts can prove \(f \le 25\).

`orbit4_exact.py` also carries the analogous probe at \(|O| = 2\) and
\(|O| = 3\) — one witness each would show that researcher-1's \(37\) and the
\(28\) of the table are unimprovable in the same sense. Those instances are
much larger (\(37\) and \(28\) vertices against \(26\)) and did not resolve
inside a \(900\) s cap on a loaded host, so **they are open, and nothing above
depends on them.** The \(|O| = 4\) result is self-contained; §6 shows
separately that the bound is attained with zero slack by real Ramsey graphs at
several other orbit sizes.

This is a negative, and it is the useful kind: it says where to stop. Improving
the order-4 case list further needs an argument that uses the global count
\(n = 42\), not a better one-orbit argument.

**And the obvious next try does not work either.** A type such as
\((c_1,c_2,c_4) = (26,4,2)\) has *two* \(4\)-orbits, so one might hope to split
\(F\) twice and intersect. For \(f = 26\) both splits must be \(13 + 13\), and
at \(13\) the \((3,5)\)-graph is unique, so each orbit forces \(F = A \sqcup B\)
with \(A\) the unique \((3,5,13)\)-graph and \(B\) its complement. But
**nothing forces the two splits to be different**, and if the second orbit
induces the same partition it adds no constraint at all. So the two-orbit
argument has no content here unless one can first rule out \(A' = A\), which
the orbit structure does not do.

## 6. Positive control

A lemma that is stated wrongly still prunes. The control is real Ramsey graphs
with real automorphisms: for every graph, every nontrivial cyclic subgroup and
the full automorphism group, and **every orbit** of it, the fixed set must
respect the bound that orbit's own shape gives, and every fixed vertex must be
joined to all of the orbit or to none. \(\omega\) and \(\alpha\) are read off
the actual induced subgraph, so a wrong case in the derivation shows up here as
a violation.

| catalogue | graphs | nontrivial groups | violations | closest approach |
|---|---|---|---|---|
| \((3,5,n)\)-graphs, \(n = 7 \ldots 13\) (complete) | \(971\) | \(6562\) | 0 | **0** at \(n \ge 8\) |
| \((4,4,n)\)-graphs, \(n = 11 \ldots 14\) (prefix of \(4000\) each) | \(16000\) | \(724\) | 0 | 1 |
| \((4,4,n)\)-graphs, \(n = 15, 16, 17\) (complete) | \(643\) | \(550\) | 0 | **0** |
| \((4,5,24,132)\)-graphs | \(2\) | \(72\) | 0 | **0** |
| \((4,5,24)\)-graphs (prefix of \(3000\)) | \(3000\) | \(308\) | 0 | 12 |
| \((5,5,42)\)-graphs, all \(328\) known | \(328\) | \(232\) | 0 | 37 |
| **total** | \(\mathbf{20944}\) | \(\mathbf{8448}\) | \(\mathbf{0}\) | |

"Closest approach" is the smallest gap between a fixed-set size and the bound
its orbit gives. **It is \(0\) on three of the six families**: the bound is not
merely respected, it is *attained* by real Ramsey graphs, repeatedly. The
\((5,5,42)\) row reads \(37\) because every involution there is fixed-point-free
— which is the census, and is why the lemma has to be proved rather than
observed.

The automorphism search prunes with 1-WL colours. That is sound (automorphisms
preserve the colouring) but it is a filter, so it was checked rather than
trusted: on \(1363\) graphs from the \((3,5)\) and \((4,4)\) catalogues the
pruned search returns **exactly** the same automorphism groups as the unpruned
one, \(0\) mismatches.

## 7. What this establishes and what it does not

**Establishes.** The lemma, for every \((s,t)\), every group and every orbit;
the table for \((5,5)\); Corollaries A and B; the reduced case lists \(84\) and
\(1328\), with the pre-reduction counts reproducing researcher-1's \(90\) and
\(1347\); and that the \(|O| = 4\) bound cannot be improved by a one-orbit
argument, with an audited witness.

**Does not establish.** The witness of §5 is a \(30\)-vertex configuration, not
a \((5,5,42)\)-graph with a \(Z_4\) automorphism fixing \(26\) points. It shows
the *argument* is exhausted, not that the case occurs. Nothing here says any of
the \(84\) or \(1328\) surviving cases is realisable — that is the work
researcher-1's solver is doing.

**Cited, not proved.** \(R(3,5) = 14\), \(R(4,5) = 25\), \(R(3,4) = 9\),
\(R(4,4) = 18\) (Radziszowski, DS1), and the completeness of McKay's
\((3,5,n)\) and \((4,5,24)\) catalogues. The refutation in §4 does not depend on
completeness; the *maximality* claim in §5 does, and it is a satisfiability
result, which needs only the witness.

## 8. Reproduction

```bash
python3 orbitbound.py all        # lemma, table, corollaries, case lists, control
python3 orbit4_exact.py          # the sharpening attempt and its witness
```

No solver is needed for `orbitbound.py`; `orbit4_exact.py` calls CaDiCaL and
certifies every UNSAT through drat-trim to LRAT. The control run of §6 is
committed verbatim as `orbit_control.txt` (named `.txt`, not `.log`, because
this repository's `.gitignore` drops `*.log` and would have silently discarded
the evidence — a defect reviewer-1 caught in another lane).

## 9. For researcher-1

1. **Use \(84\) and \(1328\), not \(90\) and \(1347\)** — the removed cases are
   listed in §4 and the code prints them.
2. **Do not spend effort sharpening the one-orbit bound**; §5 shows it is
   exhausted at \(|O| = 4\).
3. **The table is forward-looking.** If a group of order \(8\) or \(16\) comes
   up, an orbit of size \(8\) caps the fixed set at \(17\) and an orbit of size
   \(9\) at \(13\) — those rows will be far cheaper to enumerate than this one,
   which is another face of your own observation that the method is weakest
   exactly where the real symmetry lives.
