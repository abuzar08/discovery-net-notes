# Screening a subdivision-based lower bound before looking for one

Crossing number is monotone under **topological** minors but not under minors,
so transporting a lower bound from \(H\) to \(G\) means finding a *subdivision*
of \(H\) inside \(G\). That search can be expensive, and it is often doomed for a
reason visible in one line of arithmetic.

## The criterion

A branch vertex of a subdivision of \(H\) sitting inside \(G\) must be a vertex
of \(G\), and its \(G\)-degree is at least its \(H\)-degree, since the
subdivided paths leaving it are internally disjoint. Counting branch vertices of
each degree therefore gives:

> **Screen.** If \(H\) is a topological minor of \(G\), then for every
> \(d \ge 3\),
> $$\#\{v \in V(H) : \deg_H v \ge d\} \;\le\; \#\{v \in V(G) : \deg_G v \ge d\}.$$

Check it at every \(d\) before searching. It costs two degree histograms.

## Why it is worth stating separately

It is close to trivial, and it still settled a question I had spent two passes
circling. For \(K_{1,m} \square C_n\) with \(n \ge 4\): every leaf vertex has
degree 3 — two cycle edges and one rung — so **only the \(n\) centre vertices
have degree \(\ge 4\)**. The intended target \(C_n + D_m\) needs \(m\) vertices
of degree \(n \ge 4\) and \(n\) of degree \(m+2 \ge 4\), so \(m+n\) against \(n\)
available. Closed, for every choice of deleted edges and for every target of that
shape.

**That converts "my attempt failed" into "no attempt can succeed",** which is the
distinction that makes a boundary worth publishing. The same arithmetic shows why
\(n = 3\) works: there the target's large-part vertices have degree 3, the screen
demands 3 against 3, and it passes by exactly one unit.

## What it does *not* say

**It is a screen, not a theorem about the strength of bounds.** Passing it does
not mean a subdivision exists. And failing it does not mean \(\operatorname{cr}(G)\)
is small — \(G\) itself is always a topological minor of \(G\), so no such
counting argument can cap what \(\operatorname{cr}(G)\) might be. What it bounds
is **which targets are available**, not the size of the answer.

I state that explicitly because the loose version — *"an almost-cubic graph
cannot carry a quadratic bound out through topological minors"* — is the sentence
I first reached for, and it is false as written.

## Companion to the rule that produced it

This sits directly under **a correct obstruction is about one reduction, not
about the pair of objects** in `out-of-range-verdicts.md`. That rule says: when a
reduction is rejected for being the wrong *kind*, look for a reduction of the
right kind between the same two objects. This screen is what you run next — it
tells you cheaply whether the right-kind reduction can exist at all, so the two
together give a complete cheap answer instead of an open-ended search.
