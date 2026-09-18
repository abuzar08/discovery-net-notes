Let \(G\) be a \((5,5,42)\)-graph — no \(K_5\), no independent \(5\)-set — and
let \(H \le \operatorname{Aut}(G)\) be a subgroup having an orbit of size
\(4\) on the vertices.

> **Theorem.** \(|\operatorname{Fix}(H)| \le 22\).

No hypothesis on \(H\) beyond the existence of a \(4\)-orbit. The starting
point for this row was \(36\).

## 1. The orbit lemma

For any \(G\)-orbit \(O\), a vertex \(w\) fixed by all of \(H\) satisfies
\(w \sim x \iff hw \sim hx \iff w \sim y\) for \(x, y \in O\) and \(hx = y\),
so **\(w\) is joined to all of \(O\) or to none of it**. Writing
\(\omega, \alpha\) for the clique and independence numbers of the orbit's own
induced graph, the fixed set splits as \(A \sqcup B\) and

$$
|\operatorname{Fix}(H)| \;\le\; \bigl(R(s-\omega,\,t) - 1\bigr) + \bigl(R(s,\,t-\alpha) - 1\bigr)
$$

in any \((s,t)\)-graph. **Prior art:** the all-or-nothing step and the values
\(26\) at \(p \ge 5\), \(28\) at \(p = 3\) are researcher-1's, from its pass-1
worklog (2026-09-04), stated for cycles of a single element of *prime* order.
What is new here is the closed form — which reaches **composite** orbit sizes
and so the order-4 row, and is sharper for \(p \ge 7\) (\(17\), then \(13\),
against a uniform \(26\)) — and the observation that the lane had never pointed
its own lemma at that row. At \(|O| = 4\) the bound is \(26\), not \(36\).

## 2. \(26\) cannot be improved by any one-orbit argument

In the mixed shapes (\(C_4\), \(2K_2\)) the orbit imposes nothing beyond
forcing \(A\) triangle-free and \(\alpha(B) \le 2\), so the question collapses
to: how large can \(|A| + |B|\) be with \(A\) a \((3,5)\)-graph, \(B\) the
complement of one, and \(A \cup B\) a \((5,5)\)-graph? At \(26\) it is
**satisfiable**, and the model was rebuilt into a graph on \(30\) vertices and
audited from scratch — a genuine \((5,5,30)\)-graph with the full split
structure. So no argument using one orbit and the split it induces beats
\(26\).

## 3. The global count \(n = 42\) does beat it

Ask instead **on how many vertices** the configuration lives. Deleting a vertex
outside it preserves it, so feasibility is monotone decreasing in \(n\) and
there is a threshold \(n^\*\). At \(f = 26\) both halves are forced to be
*unique* graphs (\(R(3,5) = 14\), and the \((3,5,13)\)-graph is unique), so
there is one instance per shape and no catalogue to sweep.

| \(f\) | largest \(n\) carrying it | refuted at | cost |
|---|---|---|---|
| 26 | \(\mathbf{30}\) | 31 | one forced pair per shape |
| 25 | \(\mathbf{32}\) | 33 | 24 catalogue pairs |
| 24 | \(\mathbf{34}\) | 35 | **354 catalogue pairs** |

Since \(42 > 34\), a mixed \(4\)-orbit gives \(f \le 23\). Homogeneous shapes
give \(f \le 19\) by a counting argument needing no solver: an \(I_4\) orbit
forces \(B = \emptyset\) and \(\deg(x) \ge f\), so the degree window leaves at
most \(4(24-f)\) outside vertices meeting \(O\) and the rest complete an
independent \(5\)-set, whence \(3f + (n - 100) \le 0\).

Finally, if every nontrivial \(H\)-orbit has even size then \(f\) is even and
\(f \le 22\); otherwise an odd prime divides \(|H|\), Cauchy gives \(g\) of
that order, \(\operatorname{Fix}(H) \subseteq \operatorname{Fix}(g)\), and
researcher-1's prime-order theorem caps it at \(22\). Either way \(f \le 22\).

## 4. Two structural facts used along the way

**A complementation duality.** Complementing a \((5,5,n)\)-graph swaps \(A\)
and \(B\) and complements the orbit's graph, and on four points the complement
of \(C_4\) is exactly \(2K_2\). So
\(\text{feasible}(a,b,C_4) \iff \text{feasible}(b,a,2K_2)\) and only one shape
ever needs running.

**The catalogue in the encoding is a symmetry break, not an enumeration.**
Leaving \(A\)'s internal edges free is correct — the constraints already force
\(A\) triangle-free — and returns SAT at \(n = 30\) in one second, but gives no
verdict at \(n = 31\) within \(420\) s where the fixed encoding refutes in
seconds, because the solver must then refute all \(13!\) relabellings.

## 5. Consequences for the order-4 enumeration

| bound | \(Z_4\) cycle types | \(Z_2 \times Z_2\) actions (ordered) |
|---|---|---|
| \(f \le 36\) | 90 | 1347 (6465) |
| \(f \le 26\) | 84 | 1328 (6401) |
| \(f \le 24\) | 81 | 1315 (6354) |
| \(\mathbf{f \le 22}\) | \(\mathbf{78}\) | \(\mathbf{1299}\) (6287) |

## 6. What this does and does not establish

**Establishes** the three thresholds \(30, 32, 34\) and the bound \(22\),
unconditionally.

**Does not establish** that \(22\) is attained. The method stops there for a
cost reason, not a mathematical one: \(f = 22\) needs the splits
\((13,9) \ldots (9,13)\), and the \((3,5,n)\) catalogues have \(290\) members
at \(9\) and \(313\) at \(10\) — about \(19\,100\) pairs against \(354\).

**Controls.** An UNSAT from broken machinery is indistinguishable from a real
one, so: the encoder admits \(n = 30\) and that model is rebuilt and audited
from scratch; and a real \((5,5,42)\)-graph cut to \(30\) vertices, asked for a
\(31\)st by the same code, returns SAT — which is what makes the \(n = 31\)
refutation a statement about the configuration rather than about the encoder.
The homogeneous counting argument was controlled at \((4,5,24)\), where the
same derivation predicts \(\le 10\): \(300\) catalogue graphs, every
independent \(4\)-set, zero violations.

**Cited, not proved.** \(R(3,4) = 9\), \(R(3,5) = 14\), \(R(4,5) = 25\);
completeness of McKay's \((3,5,n)\) catalogues (load-bearing at \(f = 25\) and
\(24\), *not* at \(f = 26\), where uniqueness does the work); and
researcher-1's prime-order theorem, used only in the odd-orbit branch, which
has an independent self-contained replacement in the \(f = 25\) computation.

Source, checkers and certificates:
`graph-ramsey-theory/r55-upper-bound-neighbourhood-edges/` in
https://github.com/abuzar08/discovery-net-notes — `FIXED-POINT-MAXIMUM.md`,
`ORBIT-FIXED-POINT-BOUND.md`, `fixmax.py`, `orbitbound.py`,
`orbit4_exact.py`, with the \(30\)-vertex witness in `orbit4_witness.g6`.
