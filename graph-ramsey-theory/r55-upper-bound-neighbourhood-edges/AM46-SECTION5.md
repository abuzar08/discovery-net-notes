# Section 5 of \(R(5,5) \le 46\): two settled points and one I could not follow

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-09.
Subject: Angeltveit and McKay, *\(R(5,5) \le 46\)*, arXiv:2409.15709v2,
Proposition 5.3 (`p:gluered`). Checker: `am46_sec5.py`.
Companion to `AM46-SECTION4.md`.

Section 5 reduces the gluing work to five cases. Most of its proof leans on
censuses I cannot recompute here. Three pieces are finite arithmetic; this is
what they say.

## (A) The weights \(5, 2, 1\) are right — settled

The proof sets \(\alpha = 5m_1 + 2m_2 + m_3\) and asserts
\(\operatorname{excess}(F) \ge 46 - \alpha - \beta\). The coefficients must be
the largest amount by which a neighbourhood in \(E_i\) can push its vertex's
contribution below \(1\), i.e. the largest deficiency \(e - b_m\) over the
level, where \(b_m\) is Section 4's threshold at order \(m\). From
\(E(4,5,m)\):

| level | members | worst deficiency |
|---|---|---|
| \(E_1 = A \cup B_1\) | \(e \ge 127\) at \(24\); \(e \ge 121\) at \(23\) | \(132 - 127 = \mathbf{5}\) (\(B_1\) gives only \(122-118 = 4\)) |
| \(E_2 = B_2 \cup C_2\) | \(120\) at \(23\); \(114\) at \(22\) | \(120-118 = 114-112 = \mathbf{2}\) |
| \(E_3 = B_3 \cup C_3 \cup D_3\) | \(119\) at \(23\); \(113\) at \(22\); \(107\) at \(21\) | \(\mathbf{1}\) in all three |

Confirmed. Note that \(E_3\)'s weight is \(1\) precisely because each member
sits exactly one above its threshold — \(119 = 118{+}1\), \(113 = 112{+}1\),
\(107 = 106{+}1\) — which is the second, independent reason \(C_3\) must be at
\(22\) vertices rather than \(21\) (see `AM46-SECTION4.md`).

## (B) The four-set relation is misstated, and harmlessly — settled

Three times the proof writes, for \(A_1,\dots,A_4\) the neighbourhoods of a
\(4\)-clique \(\{w_1,\dots,w_4\}\),

$$
\sum |A_i| \;=\; 2\sum |A_{ij}| \;-\; 3\sum |A_{ijk}| . \tag{$*$}
$$

**As an equality this is false.** Let \(x_s\) be the number of outside vertices
adjacent to exactly \(s\) of the \(w_i\). Then
\(\sum|A_i| = \sum_s s\,x_s\), \(\sum|A_{ij}| = \sum_s \binom{s}{2} x_s\) and
\(\sum|A_{ijk}| = \sum_s \binom{s}{3} x_s\), so \((*)\) demands
\(s = 2\binom{s}{2} - 3\binom{s}{3}\) for every \(s\) that occurs. That holds
at \(s = 0, 2, 3\) and fails at \(s = 1\) (\(1\) against \(0\)) and \(s = 4\)
(\(4\) against \(0\)). No vertex is adjacent to all four — that is a \(K_5\) —
so \(x_4 = 0\); but \(x_1\) is unconstrained, and a single outside vertex
adjacent to exactly one \(w_i\) already breaks \((*)\).

**The true general statement is the inequality**

$$
\sum |A_i| \;\ge\; 2\sum |A_{ij}| \;-\; 3\sum |A_{ijk}| ,
$$

since \(s \ge 2\binom{s}{2} - 3\binom{s}{3}\) for all \(s \in \{0,1,2,3,4\}\).

**And that is all the proof needs.** Both derived forms follow from the
inequality, because \(\sum|A_{ij}|\) enters \(|\bigcup A_i|\) with a minus sign
and \(\sum|A_{ijk}|\) with a plus sign:

$$
\Big|\bigcup A_i\Big| \;\ge\; \tfrac{2}{3}\sum|A_i| - \tfrac{1}{3}\sum|A_{ij}|,
\qquad
\Big|\bigcup A_i\Big| \;\ge\; \tfrac{1}{2}\sum|A_i| - \tfrac{1}{2}\sum|A_{ijk}| .
$$

`am46_sec5.py` checks both over all profiles with \(x_1,x_2,x_3 < 12\): the
equality fails on \(1584\) of \(1728\), the inequality fails on none, and
neither derived bound fails on any. **A misstated lemma with a sound use** —
worth an erratum for the reader who checks it, not a defect in the argument.

## (C) Two closing steps I could not reproduce — *not* a claim of error

Each of the three sub-cases ends by comparing a lower bound on
\(|\bigcup A_i|\) with an upper bound. I asked whether the contradiction is
forced by what is written beside it, as an integer feasibility question in
\((x_1,x_2,x_3)\), decided by exhaustive search rather than by following prose.

To make the test meaningful I first proved the elementary caps available from
\(F\) having no \(K_5\) and no independent \(5\)-set, and imposed them too:

- the common neighbourhood of a **triple** is independent (two adjacent
  members plus the triple give a \(K_5\)), so it has at most \(4\) vertices and
  \(\sum|A_{ijk}| \le 16\);
- the common neighbourhood of a **pair** has no triangle and no independent
  \(5\)-set, so it is a \((3,5)\)-graph and has at most \(R(3,5) - 1 = 13\)
  vertices, giving \(\sum|A_{ij}| \le 78\);
- each \(A_i\) has no \(K_4\) and no independent \(5\)-set, so
  \(|A_i| \le R(4,5) - 1 = 24\).

| case | stated hypotheses | verdict |
|---|---|---|
| \(m_2 = 4\) | \(|A_i| \ge 11\), \(|A_{ij}| \le 7\), \(|\bigcup A_i| = 15\) | **contradiction forced** |
| \(m_2 = 2\) | \(\sum|A_i| \ge 63\), \(|\bigcup A_i| \le 25\) | **not forced**: witness \((x_1,x_2,x_3) = (0,8,16)\) |
| \(m_2 = 0\) | \(\sum|A_i| \ge 60\), \(|\bigcup A_i| \le 23\) | **not forced**: witness \((x_1,x_2,x_3) = (0,6,16)\) |

Both witnesses obey every cap above. In each the missing ingredient is the
same and is exactly identifiable: the chain closes iff
\(\sum|A_{ijk}| \le 12\) (case \(m_2 = 2\)) or \(\le 13\) (case \(m_2 = 0\)),
whereas the best elementary cap is \(16\) and the text states no sharper one.

**What this is and is not.** It is *not* a claim that Proposition 5.3 is false,
and it is not of the same character as the \(C_3\) erratum, which was
unambiguous and confirmed by the paper's own table. My model tracks only the
adjacency pattern of outside vertices to the four \(w_i\); the real
configuration carries much more structure — the outside set is itself
\((5,5)\)-Ramsey, the \(w_i\) have prescribed degrees in \(F\), and the case
hypotheses constrain \(F[E]\) further — and a witness in my model need not
correspond to any graph. So the honest report is: **two of the three closing
steps do not follow from the inequalities written beside them plus the
elementary structure, and what would close each is an upper bound on
\(\sum|A_{ijk}|\).** The bound may hold for reasons the authors omitted as
routine. I could not reconstruct it, and I am recording that rather than
guessing in either direction.

## Reproduction

```bash
python3 am46_sec5.py
```

Needs `e45.json` only; runs in seconds.
