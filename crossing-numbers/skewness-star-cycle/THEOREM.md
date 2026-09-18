# \(\mathrm{sk}(K_{1,m} \square C_3) = m-2\) for all \(m \ge 2\)

Both bounds proved. This replaces the five verified instances with which the
lane opened, and it settles the \(n = 3\) column of Chia and Sim's question
outright rather than at finitely many points.

## Notation

\(K_{1,m} \square C_3\) has \(3(m+1)\) vertices and \(3(2m+1)\) edges. Write
\(c_0, c_1, c_2\) for the three copies of the star's centre and \(l_{j,0},
l_{j,1}, l_{j,2}\) for the copies of leaf \(j\). The edges are

- the **centre triangle** \(T_0\) on \(c_0c_1c_2\);
- for each leaf \(j\), the **leaf triangle** \(T_j\) on \(l_{j,0}l_{j,1}l_{j,2}\);
- for each leaf \(j\) and each \(i\), the **rung** \(c_i l_{j,i}\).

So the graph is \(m\) triangular prisms glued along the common triangle \(T_0\).
Call leaf \(j\) **fully attached** in a subgraph if all three of its rungs are
present.

## Lower bound

> **Lemma.** If three leaves are fully attached in a subgraph \(H\), then \(H\)
> is non-planar.

*Proof.* Contract each of the three leaf triangles to a single vertex. Each
contracted vertex is adjacent to \(c_0\), \(c_1\) and \(c_2\), by its three
rungs. Hence \(K_{3,3}\) is a minor of \(H\), and \(H\) is non-planar by
Wagner's theorem. \(\square\)

Note the lemma **never mentions \(T_0\)**. That is not an accident of the write-up:
measuring the largest number \(L(t)\) of fully attached leaves that stay planar
after deleting \(t\) edges of \(T_0\) gives \(L(0) = L(1) = L(2) = L(3) = 2\).
Deleting the centre triangle buys nothing, because the obstruction was never
there.

> **Theorem (lower bound).** \(\mathrm{sk}(K_{1,m} \square C_3) \ge m-2\).

*Proof.* Let \(S\) be a set of edges with \(G - S\) planar. By the Lemma at most
two leaves are fully attached in \(G - S\), so at least \(m-2\) leaves have lost
a rung. Rungs of distinct leaves are distinct edges, so \(|S| \ge m-2\).
\(\square\)

## Upper bound

> **Theorem (upper bound).** \(\mathrm{sk}(K_{1,m} \square C_3) \le m-2\).

*Proof.* Delete the \(m-2\) layer-0 rungs \(c_0 l_{j,0}\) for
\(j = 1, \ldots, m-2\), and draw the remainder as follows.

1. Draw \(T_0\) as a triangle in the plane.
2. Draw leaf \(m-1\) inside \(T_0\) with all three rungs. The result is a
   triangular prism, whose faces inside \(T_0\) include the quadrilateral \(Q\)
   bounded by \(c_1c_2\), \(c_2 l_{m-1,2}\), \(l_{m-1,2} l_{m-1,1}\) and
   \(l_{m-1,1} c_1\). **Both \(c_1\) and \(c_2\) lie on \(\partial Q\).**
3. Draw leaf \(m\) outside \(T_0\), symmetrically. It does not meet \(Q\).
4. Each remaining leaf \(j \le m-2\) has lost its layer-0 rung, so it attaches
   only at \(c_1\) and \(c_2\). Draw \(T_j\) inside the current face having both
   \(c_1\) and \(c_2\) on its boundary, with \(l_{j,1}\) towards \(c_1\) and
   \(l_{j,2}\) towards \(c_2\) and \(l_{j,0}\) away from them, then draw the two
   rungs. This adds no crossing, and it leaves a new face bounded by \(c_1c_2\),
   \(c_2 l_{j,2}\), \(l_{j,2} l_{j,1}\) and \(l_{j,1} c_1\) — again **with both
   \(c_1\) and \(c_2\) on its boundary.**

Step 4 therefore applies again, and by induction all \(m-2\) reduced leaves nest
side by side along \(c_1c_2\). The drawing is planar. \(\square\)

**Checked as well as argued:** the deletion set above planarises the graph for
every \(m\) from 2 to 20, and at \(m = 30, 50, 80\) — the last on 243 vertices
and 483 edges.

## Consequence

$$\mathrm{sk}(K_{1,m} \square C_3) = m-2 \qquad \text{for all } m \ge 2 .$$

Chia and Sim's proposed identity, as DS21 prints it, gives
\((m-2)(\lfloor \tfrac{n-1}{2} \rfloor + 1) = 2(m-2)\) at \(n = 3\). **So it is
too large by a factor of two along the whole \(n = 3\) column**, not merely at
the five values first computed.

The identity is consistent with every exact value found at \(n \ge 4\) —
\((m,n) = (3,4), (3,5), (3,6), (4,4), (4,5), (5,4)\) — so the defect remains
localised to \(n = 3\), and the correction is a **range** condition rather than a
new formula.

Source: `chiasim.py`, `caseB.py`.
