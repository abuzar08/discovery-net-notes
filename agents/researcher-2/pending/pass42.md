# Summary

A correction of framing, a tool, and two errors the tool caught.

My previous contribution stopped the \(r=29\) lane, saying the remaining question
"needs either a new dependency or a hand-written Blossom", and put that to the
principal as a **dependency decision**. That framing was wrong, and the
correction matters because it mis-stated the decision I was asking for.

# The correction

Writing a matching routine is **not adding a dependency**. Every file in this
directory is standard library only, exact integer arithmetic, and the instruction
about dependencies applies to third-party packages, not to code I write myself.

The real question was only whether the error surface is acceptable — and for
matching it is, because **both answers are self-certifying**:

$$\nu\ge k \text{ is certified by exhibiting } k \text{ disjoint edges};\qquad
\nu\le k \text{ by a Tutte set } S \text{ with } o(G-S)-\lvert S\rvert\ge n-2k.$$

The algorithm does not have to be trusted; its output is checked. That is exactly
the opposite of the situation in the rest of this lane, where the arguments are
what carry the risk — and it is why I should not have stopped on it.

# The tool

Blossom for maximum matching in a general graph, standard library only, checked
three ways: against brute-force enumeration on 300 random graphs of 2 to 9
vertices at varied densities; the returned pairing verified to be a matching of
the graph; and the Tutte–Berge deficiency of the Gallai–Edmonds set cross-checked
against \(n-2\nu\). All pass.

# Two errors it caught immediately

**1. A gap in the Tutte case analysis.** The third family of Tutte sets — cut a
set \(C\) of \(R\)-vertices off from \(L'\) — was stated as needing \(S\) to
contain \(N_{L'}(C)\) only. But \(S\) must **also** contain the
\(H[R]\)-neighbours of \(C\) outside \(C\), or those edges keep \(C\) attached to
the chunk. The correct condition is

$$o(H[C])\;\ge\;\lvert N_{L'}(C)\rvert+\lvert N_{H[R]}(C)\setminus C\rvert+2,$$

and the second term is expensive, because a \(C\) independent in \(H[R]\) has a
large \(H[R]\)-neighbourhood. Under the wrong version the adversary appeared to
win easily; the first explicit computation returned \(\nu=24\) instead, and that
disagreement is what located the error.

**2. An inadmissible construction.** The first adversarial \(H\) I built, for
\(m=838\), \(\lvert R\rvert=21\), multiset \((21,8,8)\), had \(\max d_H(z)=32\)
over \(R\) against the constraint \(d_H(z)=29-x_z\le28\), and a degree sum of 518
against the required \(29\lvert R\rvert-X=557\). **Its \(\nu\) therefore
certifies nothing**, and the \(\nu=24\) figure above must not be read as a
statement about admissible \(H\).

Both were caught before anything was published, by computation disagreeing with
argument. Given that this lane has produced seven items of a single defect family
— *verify on the favourable case, generalise without re-deriving* — a tool whose
output is checkable rather than argued is worth more here than another layer of
case analysis.

# Next

Building an **admissible** adversary — degrees respected, \(K_4\)-free,
\(e(H[R])\) exact, \(w\) of degree at most 4 — for a configuration in the 2116 is
the next concrete step. It is now tractable, and its answer will be checked
rather than argued: a matching of 24 closes that configuration's \((3,24)\) route
positively, a Tutte set of deficiency 3 kills it.

# Scope

Order 57 at \(r=29\) is closed. Order 58 is open in 8945 configurations. Nothing
here changes either count. Albertson's conjecture is **not** proved for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`matching.py`, SHA-256
`cd6d66dd5a18962e691f2846300d1859cd3e5483f779d7fbe9398604e1e3d5c3`, at
https://github.com/abuzar08/discovery-net-notes/tree/459864e/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 matching.py | diff -u EXPECTED_OUTPUT_MATCHING.txt -`
(empty diff; under 2 s, standard library only).
