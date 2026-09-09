# Clearing the \(k \ge 4\) formula gate

The tripartite search used \(A(n_1,n_2,n_3)\) from Gethner et al. Extending to
four or more parts needs Harborth's general function, and the instruction was
explicit: **clear the gate, do not guess the formula.** This records how it was
cleared.

## Where the formula was found

Not in DS21, which names the function but does not reproduce it, and not in
Gethner et al., which gives only the tripartite bound explicitly and otherwise an
asymptotic ratio \(\zeta(r) = \tfrac{3(r^2-r)}{8(r^2+r-3)}\) — and which never
cites Harborth by name.

It is stated in full as Theorem 2.1 of Clancy, Haythorpe and Newcombe,
*A survey of graphs with known or bounded crossing numbers* (arXiv:1901.05155),
attributed to Harborth (1971), *Über die Kreuzungszahl vollständiger,
\(n\)-geteilter Graphen*, Math. Nachr. **48**, 179–188.

For \(K_{x_1,\ldots,x_n}\) with \(s = \sum_i x_i\) and
\(c = \#\{i : x_i \text{ odd}\}\):

$$\operatorname{cr}(K_{x_1,\ldots,x_n}) \;\le\; \frac{1}{8}\Bigg( 3\!\!\sum_{i<j<k<\ell}\!\! x_i x_j x_k x_\ell \;+\; 3\binom{\lfloor c/2 \rfloor}{2} \;-\; \left\lfloor \tfrac{c}{2} \right\rfloor \!\!\sum_{\substack{i<j \\ x_i,\,x_j \text{ even}}}\!\! x_i x_j$$
$$\;-\; \left\lfloor \tfrac{c-1}{2} \right\rfloor \!\!\sum_{\substack{i<j \\ x_i,\,x_j \text{ opposite parity}}}\!\! x_i x_j \;-\; \left\lfloor \tfrac{c-2}{2} \right\rfloor \!\!\sum_{\substack{i<j \\ x_i,\,x_j \text{ odd}}}\!\! x_i x_j \Bigg)$$
$$\;+\; \sum_i X(x_i)\,X(s - x_i) \;-\; \sum_{i<j} X(x_i)X(x_j),$$

with \(X(m) = \lfloor m/2 \rfloor \lfloor (m-1)/2 \rfloor\).

## The reading that had to be resolved, and how

My text extraction printed the three parity conditions in terms of the **indices**
— "\(i \equiv j \equiv 0 \pmod 2\)" — rather than the part sizes. That cannot be
the intended meaning: it would make the bound depend on the order the parts
happen to be listed in, and it would make \(c\), which counts *odd parts*,
irrelevant to the sums it multiplies.

The natural reading is the parity of the **part sizes** \(x_i\). But per the
standing notation rule, a reading recovered from a lossy extraction is exactly
the kind of claim that must not be trusted on plausibility. **So it was not
assumed — it was gated.**

## The gate

The candidate reading had to reproduce two independent bodies of known values:

| gate | what it tests | result |
| --- | --- | --- |
| against \(A(n_1,n_2,n_3)\), from a **different source** (Gethner et al.), over every triple with parts to 10 | that the general formula specialises correctly | **220 agree, 0 mismatch** |
| against DS21's **4- and 5-partite** formulas — \(K_{1,1,3,n}\), \(K_{1,1,4,n}\), \(K_{1,2,2,n}\), \(K_{2,2,2,n}\), \(K_{1,1,1,n}\), \(K_{1,1,1,1,n}\), \(K_{1,1,1,2,n}\), each to \(n = 12\) | that the parity reading is right | **84 of 84 agree, 0 mismatch** |

The second gate is the one that matters. A wrong parity reading is invisible in
the tripartite case for most triples but changes the value as soon as several
parts share a parity — which is precisely the shape of \(K_{1,1,3,n}\),
\(K_{1,1,1,1,n}\) and \(K_{2,2,2,n}\). Passing 84 of those on the nose, against
formulas from a third source, is what makes the reading a determination rather
than a guess.

**Gate cleared.** Four or more parts are now in scope, on a formula that has been
checked against two independent sources and never against itself.

Source: `harborth_general.py`, gated by `harborth.py` and DS21's formula list.
