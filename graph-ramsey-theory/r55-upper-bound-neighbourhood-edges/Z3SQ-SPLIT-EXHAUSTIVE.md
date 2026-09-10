# The \(Z_3 \times Z_3\) cube splits are exhaustive — certified before they land

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
Checker: `../r46-automorphism-obstructions/verify.py cover`.
**None of researcher-1's instances were solved here.** Only the cube files were
read, and only to certify that they cover.

principal-1, pass 38: *"researcher-1's two surviving \(Z_3\times Z_3\) actions
are being attacked by cube splits, and if they fall, Theorem 2 and both
corollaries promote — which makes the exhaustiveness of those splits the
load-bearing step, and it is exactly your kind. Be ready to check it the moment
it lands, by your own route rather than by reading theirs."*

Ready, and done: the splits currently in flight are already certified.

## What was checked

| split | cubes | split variables | verdict | certificate |
|---|---|---|---|---|
| `a0_b2000_c4` | \(1024\) | \(10\) (vars \(34\)–\(43\)) | **covers every assignment** | \(64\,022\) B LRAT |
| `a0_b2000_c4_d14` | \(16\,384\) | \(14\) (vars \(34\)–\(47\)) | **covers every assignment** | \(1\,963\,045\) B LRAT |
| `a0_b1100_c4` | \(1024\) | \(10\) | **covers** | as above |
| `a0_b1100_c4_d14` | \(16\,384\) | \(14\) | **covers** | as above |

Each certificate was produced by refuting the **negated-cubes formula** — one
clause per cube asserting that cube is false — and then **replayed to the empty
clause by this repository's own LRAT checker**, the same one that replays every
leaf elsewhere in this lane.

## Why this is not the obvious check

The obvious check is to count: \(2^{10} = 1024\) and \(2^{14} = 16384\), so if
the file has that many distinct sign patterns on the right variables it covers.
That is true, and it is an argument rather than a certificate — it relies on the
counting being right, on the variables being the ones you think, and on no cube
being duplicated.

The negated-cubes refutation asserts none of that. It asks the solver whether
any assignment escapes every cube, gets **UNSAT**, and hands the proof to the
same checker as everything else. If a cube were missing, duplicated, or over the
wrong variables, the formula would be **satisfiable** and the tool would print
the escaping assignment. Nothing is counted and nothing is assumed.

It also costs nothing: the whole set is four refutations, the largest \(2\) MB.

## What it does and does not establish

**Establishes:** that these four cube sets partition nothing out — every total
assignment lies in at least one cube. So *if* every cube is refuted, the parent
formula is refuted, and the exhaustiveness half of the cube-and-conquer argument
holds.

**Does not establish:** that any cube *is* refuted. That is researcher-1's half
and its certificates. Nor does it say anything about the two \(Z_3 \times Z_3\)
actions themselves, which are still open.

`verify.py cover` now reads iCNF (`a <literals> 0`) directly, so the check needs
nothing but the split file — no reproduction of whatever produced it.

---

# A structural prediction: which cases resist, before anyone runs them

principal-1, same pass: *"your finding that fixed-point-freeness is necessary
and not sufficient, with \(c = 4\) separating the two survivors and those being
the two smallest formulas of the 39, is a structural fact about the family
rather than an observation about instances — publish it as such, because it
predicts which cases resist before anyone runs them."*

## The claim

For an orbit encoding of \((s,t,n)\)-graphs invariant under a group \(V\), let

- \(\mathrm{fix}(V)\) be the points \(V\) fixes, and
- \(\mathrm{free}(V)\) be the points with trivial stabiliser.

Then, as a **prediction about solver difficulty, not a theorem**:

> **The instances that resist are those with no fixed points and the largest
> free part. Formula size runs the other way, so the smallest formula in a
> family is the one to expect trouble from.**

## The mechanism

A variable is a \(V\)-orbit of vertex pairs. Fix a vertex \(v\); its incident
pairs fall into blocks, one per orbit, and **one variable decides every
adjacency at \(v\) in its block at once**. The block size is the leverage a
single decision has.

If \(v\) is \(V\)-fixed and \(O\) is a regular orbit, the pairs \(\{v\} \times
O\) form **one** orbit of size \(|V|\): \(v\) joins all of \(O\) or none of it.
A vertex inside a nontrivial orbit has no such block.

So fixed points are where propagation lives, and a fixed-point-free action has
none of it.

## The evidence, on two families

**Order 9, three types** (researcher-1's Theorem B chain):

| type | fixed points | vars | max block | solve |
|---|---|---|---|---|
| \(1^6 9^4\) | 6 | 109 | 9 | \(8.4\) s |
| \(1^3 3^1 9^4\) | 3 | 101 | 9 | \(179\) s |
| \(3^2 9^4\) | 0 | 99 | **3** | **open at \(2400\) s** |

**\(Z_3 \times Z_3\), all 39 actions**, which is where the claim earns the word
*structural*:

| | max block weight | actions |
|---|---|---|
| has fixed points | \(9\) | 17 |
| fixed-point-free | \(3\) | 22 |

A perfect dichotomy — and **22 are fixed-point-free while only 2 survive**, so
fixed-point-freeness is **necessary and not sufficient**. What separates the two
survivors is \(c = 4\), the maximum possible number of regular orbits: \(6\) of
\(42\) points carry a nontrivial stabiliser, against \(15\) at \(c = 3\). The
fixed-point-free actions split by \(c\) as \(\{4{:}2,\,3{:}5,\,2{:}8,\,1{:}5,\,
0{:}2\}\), and the survivors are exactly the \(c = 4\) pair — also **ranks 1 and
2 of 39 by formula size**, at \(97\) and \(99\) variables.

## How to use it, and how it could fail

**Use**: given a family of symmetry types to attack, sort by free part
descending and expect the hardest at the top — which is the opposite of sorting
by formula size ascending, the natural instinct. Budget accordingly, and if the
cheap-looking instance is also the freest, expect it to need cube splitting.

**Falsification**: a family where a fixed-point-free instance falls quickly
while one with fixed points resists. Two families and 42 instances is not many,
both come from one lane and one solver, and difficulty is not a graded quantity
— an instance either finished under the cap or did not. **Treat it as a
heuristic with a mechanism, not a law.**
