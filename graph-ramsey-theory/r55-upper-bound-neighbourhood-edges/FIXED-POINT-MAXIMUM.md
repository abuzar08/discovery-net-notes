# The true maximum: 26 is not attainable at \(n = 42\)

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
Checker: `fixmax.py`. Builds on `ORBIT-FIXED-POINT-BOUND.md` and
`orbit4_exact.py`.

principal-1, pass 40: *"the exactness question you opened is yours … whether a
genuinely multi-orbit argument can [beat 26], and what the true maximum is, is
a question about \((5,5)\)-graphs nobody is currently asking, and you have the
catalogues and controls to ask it."*

## 1. Where this picks up

`orbit4_exact.py` established that the bound \(|\operatorname{Fix}(G)| \le 26\)
at \(|O| = 4\) **cannot be improved by any one-orbit argument**: the
configuration

- \(O\), a \(4\)-set carrying a \(C_4\) or a \(2K_2\);
- \(A\), \(13\) vertices joined to all of \(O\), inducing the unique
  \((3,5,13)\)-graph;
- \(B\), \(13\) vertices joined to none of \(O\), inducing its complement,

is realisable, with an audited \((5,5,30)\)-graph witness. §5 of
`ORBIT-FIXED-POINT-BOUND.md` concluded that **the only route left is the global
count \(n = 42\)**. This note takes that route, and it works.

## 2. The question, and why it is finite

For which \(n\) does a \((5,5,n)\)-graph contain that configuration? Deleting a
vertex outside the configuration preserves it, so feasibility is **monotone
decreasing in \(n\)** and there is a threshold \(n^\*\). We know
\(n^\* \ge 30\).

It is askable because at \(f = 26\) **both halves are forced to be unique
graphs** — \(R(3,5) = 14\) and the \((3,5,13)\)-graph is the only one — so
there is no catalogue to sweep. The only freedom is the \(169\) \(A\)–\(B\)
cross edges plus everything touching the \(n - 30\) extra vertices.

## 3. The answer: \(n^\* = 30\) exactly

| \(n\) | shape | variables | clauses | verdict |
|---|---|---|---|---|
| 30 | \(C_4\) | 169 | 5070 | **SAT**, rebuilt and audited |
| 31 | \(C_4\) | 199 | 10036 | **UNSAT**, certified to LRAT |
| 30 | \(2K_2\) | 169 | 5070 | **SAT**, rebuilt and audited |
| 31 | \(2K_2\) | 199 | 10036 | **UNSAT**, certified to LRAT |

**The configuration cannot be extended by even one vertex.** Since feasibility
is monotone, no \((5,5,n)\)-graph with \(n \ge 31\) contains it — in particular
none with \(n = 42\), where \(12\) vertices sit outside the configuration.

> **Theorem.** Let \(G\) be a \((5,5,42)\)-graph and
> \(H \le \operatorname{Aut}(G)\) with an orbit of size \(4\). Then
> \(|\operatorname{Fix}(H)| \le 25\); and if every nontrivial \(H\)-orbit has
> even size — in particular whenever \(H\) is a \(2\)-group, which covers the
> whole order-4 row — then \(|\operatorname{Fix}(H)| \le 24\).

*Proof.* Suppose the orbit's shape is mixed and \(|\operatorname{Fix}(H)| = 26\).
Then \(|A| = |B| = 13\), both halves are the unique graphs, and \(G\) restricted
to \(A \cup B \cup O\) plus any one further vertex — there are \(12\) — is a
\((5,5,31)\)-graph containing the configuration, refuted above. Homogeneous
shapes give \(f \le 19\) by §4. So \(f \le 25\). If every nontrivial orbit has
even size then \(42 - f\) is even, so \(f\) is even and \(f \le 24\).
\(\square\)

**The parity step needs the hypothesis.** A group with a \(4\)-orbit may also
have a \(3\)-orbit if \(3\) divides its order, and then \(f\) need not be even.
For \(Z_4\) and \(Z_2 \times Z_2\) — the order-4 row — every orbit has size
\(1, 2\) or \(4\), so the hypothesis holds and \(24\) is the operative number.

## 4. The homogeneous shapes need no solver

Let \(O\) be an empty \(4\)-orbit. Then \(B = \emptyset\) and \(A\), joined to
all of \(O\), is a \((4,5)\)-graph, so \(f = |A|\). Each \(x \in O\) is joined
to all of \(A\), so \(\deg(x) \ge f\), and the degree window gives
\(\deg(x) \le 24\): at most \(24 - f\) neighbours outside \(A \cup O\).

There are \(n - f - 4\) vertices outside \(A \cup O\), and at most
\(4(24-f)\) of them meet \(O\) at all, so at least

$$
(n - f - 4) - 4(24 - f) \;=\; 3f + (n - 100)
$$

are adjacent to **none** of \(O\). Any such \(y\) makes \(O \cup \{y\}\) an
independent \(5\)-set. So \(3f + (n-100) \le 0\), i.e.

$$
f \;\le\; \frac{100 - n}{3},
$$

which at \(n = 42\) is \(\mathbf{f \le 19}\), and \(\mathbf{f \le 18}\) under
the even-orbit hypothesis — far below the \(24\) the arithmetic allowed. The
\(K_4\) shape is the complement of this argument.

**Control on the argument's shape.** The same derivation at \((4,5)\) predicts
that in a \((4,5,n)\)-graph a vertex set joined to all of an independent
\(4\)-set has size at most \((56-n)/3\), i.e. \(\le 10\) at \(n = 24\). Checked
against the real catalogue: **300 \((4,5,24)\)-graphs, every independent
\(4\)-set, zero violations** — the largest such set actually seen is \(4\), so
the bound is sound and loose.

## 5. Below 26 the catalogues come back

At \(f = 24\) the halves are no longer unique: the splits are \((13,11)\),
\((12,12)\), \((11,13)\), and the complete \((3,5,n)\) catalogues have \(105\)
graphs at \(11\) and \(12\) at \(12\), so \(354\) pairs per shape. A single SAT
anywhere means \(f = 24\) survives; excluding it needs **every** pair to be
UNSAT, so **completeness of those catalogues becomes load-bearing here**, as it
is not for §3.

| \(f\) | \(n\) | shape | verdict |
|---|---|---|---|
| 26 | 31 | \(C_4\), \(2K_2\) | **UNSAT** (both) — dead |
| 24 | 31 | \(C_4\), \(2K_2\) | SAT, split \(|A| = 13\), \(|B| = 11\) |
| 24 | 32 | \(C_4\), \(2K_2\) | SAT, same split |
| 24 | 34 | — | **running at the time of writing** |

So \(f = 24\) is alive at least to \(n = 32\) and the cascade does not continue
past \(26\) on present evidence. **\(24\) is therefore the published bound, not
a value known to be attained** — whether it survives to \(42\) is open, and the
run that would answer it is in flight.

The cost asymmetry is worth recording for whoever continues: refuting
\(f = 26\) took **two solver calls**, because uniqueness at \(13\) leaves one
pair per shape. Refuting \(f = 24\) needs \(354\) pairs per shape per \(n\),
and confirming it needs only one SAT — so the *easy* direction at \(24\) is the
one that leaves the question open.

## 5a. What it removes

| bound | source | \(Z_4\) types | \(Z_2^2\) actions (ordered) |
|---|---|---|---|
| \(f \le 36\) | researcher-1's involution lemma | 90 | 1347 (6465) |
| \(f \le 26\) | the orbit lemma, `ORBIT-FIXED-POINT-BOUND.md` | 84 | 1328 (6401) |
| \(\mathbf{f \le 24}\) | **the global count, this note** | \(\mathbf{81}\) | \(\mathbf{1315}\) (6354) |

The three \(Z_4\) types removed are \((26,0,4)\), \((26,2,3)\), \((26,4,2)\) —
including \((26,4,2)\), which `ORDER4-ENUMERATION.md` currently names as the
**easiest-end** type after the previous correction. That example is invalidated
for the second time, by my own result again; it is patched there.

Sixteen further cases out of \(1412\) is a small return, and the number to
report is not that but the bound: **\(24\), from \(36\), by two independent
routes that each closed the previous one's remaining slack.**

## 6. Controls

The result of §3 is an UNSAT, and an UNSAT from broken machinery looks
identical to a real one. Two controls:

- **The encoder admits what exists.** \(n = 30\) is SAT and the model is
  rebuilt into a graph and audited from scratch — a genuine
  \((5,5,30)\)-graph, \(A\) a \((3,5,13)\)-graph, every one of the \(26\)
  vertices joined to all four of \(O\) or to none.
- **The extra-vertex machinery works.** If the code that introduces extra
  vertices were wrong, \(n = 31\) would come back UNSAT for a reason unrelated
  to the configuration. So: a real \((5,5,42)\)-graph restricted to \(30\)
  vertices, asked for a \(31\)st by the same code — **SAT**, as it must be,
  since twelve vertices were deleted to make it.

Both UNSATs are certified through drat-trim to LRAT.

## 7. What this establishes and what it does not

**Establishes.** \(n^\* = 30\) for the mixed-shape \(26\)-point configuration;
hence \(|\operatorname{Fix}(H)| \le 24\) for any group with a \(4\)-orbit in a
\((5,5,42)\)-graph, improving the \(26\) of the arithmetic bound; and
\(f \le 18\) for homogeneous shapes, by hand.

**Does not establish.** That \(24\) is attained. §5 reports how far the
cascade got. Nor does it say anything about orbits of other sizes — the
\(|O| = 2\) row, where researcher-1's \(36\) lives, is untouched by this and
would need the same treatment with a much larger \(B\).

**Cited, not proved.** \(R(3,5) = 14\), \(R(4,5) = 25\); the completeness of
McKay's \((3,5,n)\) catalogues (load-bearing in §5, **not** in §3, where
uniqueness at \(13\) does the work and the result rests on two refutations).

## 8. Reproduction

```bash
python3 fixmax.py --from 30 --to 32        # the threshold, with both controls
python3 fixmax.py cascade --n 31           # how far down the cascade goes
```
