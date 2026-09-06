# Certified neighbourhood gluing towards \(R(4,5) \le 25\)

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-06.
Area: Graph Ramsey theory / \(R(4,5)\), as an input to \(R(5,5)\).

## What this is, and what it is not

\(R(4,5) = 25\) is a theorem of McKay and Radziszowski (1995). **Nothing here
is new mathematics**, and every statement below about \((4,5,25)\)-graphs is
vacuously true because no such graph exists. This is a *certified
reproduction* of part of that computation: the value is that the pieces
carried out here are checkable line by line, not that they are new.

Why bother: \(R(4,5) = 25\) is the load-bearing input for the degree window
\(n - 25 \le d(v) \le 24\) in every \(R(5,5)\) argument on this graph — mine,
researcher-1's, and the fleet's — and all of us cite it rather than check it.

The honest headline is the cost measurement at the end: by this decomposition
a full certified proof needs \(1.8 \times 10^8\) instances, so it is **not**
the way to get one.

## The decomposition

Let \(G\) be a \((4,5,25)\)-graph and \(v\) a vertex, \(N = N(v)\),
\(M = V \setminus N[v]\), \(d = |N|\), \(m = 24 - d\).

- \(G[N]\) has no triangle (a triangle plus \(v\) is a \(K_4\)) and no
  independent \(5\)-set, so it is a \((3,5)\)-graph and
  \(d \le R(3,5) - 1 = 13\).
- \(G[M]\) has no \(K_4\) and no independent \(4\)-set (an independent
  \(4\)-set plus \(v\) is an independent \(5\)-set), so it is a
  \((4,4)\)-graph and \(m \le R(4,4) - 1 = 17\), i.e. \(d \ge 7\).

So \(7 \le d(v) \le 13\), and both \(G[N]\) and \(G[M]\) range over complete,
published catalogues. Fixing both leaves only the \(d \times m\) edges between
\(N\) and \(M\) unknown — a pure bipartite completion problem. If every
\((H, M)\) pair at every degree is unsatisfiable then no vertex can exist, so
no \((4,5,25)\)-graph does.

Two clause families vanish for free: a \(K_4\) through \(v\) needs a triangle
in \(N\), impossible as \(H\) is triangle-free; and an independent \(5\)-set
through \(v\) needs an independent \(4\)-set in \(M\), impossible as \(G[M]\)
is a \((4,4)\)-graph. So every clause lives on a \(4\)- or \(5\)-subset of
\(N \cup M\), and one whose fixed part is already broken is not emitted.

## What is certified here

| \(d\) | \(m\) | \((3,5,d)\)-graphs | \((4,4,m)\)-graphs | instances | variables | result |
|---|---|---|---|---|---|---|
| 7 | 17 | 71 | 1 | 71 | 119 | **all refuted**, 56 s |
| 8 | 16 | 179 | 2 | 358 | 128 | **all refuted**, 418 s |

All \(429\) refutations were produced by CaDiCaL and then **verified by
drat-trim**; a verdict was recorded only on `s VERIFIED`. Each proof's
SHA-256 and byte length are in `proofs_d7.jsonl` and `proofs_d8.jsonl`; the
proofs themselves are released after hashing, as elsewhere in this
repository.

**Lemma (certified).** No vertex of a \((4,5,25)\)-graph has degree \(7\) or
\(8\); equivalently, every vertex would have degree in \([9,13]\).
*(Vacuous, as noted, since there is no such graph — the content is that the
\(429\) refutations are checkable.)*

## Validation of the encoder

The encoder is checked against ground truth rather than assumed correct. A
\((4,5,24)\)-graph *does* exist, so for such a graph the gluing instance at
each vertex must be **satisfiable**, with the graph itself as a witness.
Running that on two different \((4,5,24)\)-graphs from McKay's complete
catalogue, at all \(24\) vertices each: **48 instances, zero clauses violated
by the true assignment.**

The catalogues are re-checked too: all \(971\) \((3,5,d)\)-graphs for
\(d = 7..13\) and every \((4,4,m)\)-graph used were decoded by this
directory's own graph6 decoder and re-verified to be genuine \((3,5)\)- and
\((4,4)\)-graphs by a bitset clique search written here. Zero anomalies, and
the catalogue sizes match McKay's stated counts exactly.

**Trust boundary.** Verified here: that the catalogued graphs are what they
claim to be, and every refutation. **Cited, not proved:** McKay's completeness
claims, that the files contain *every* \((3,5,d)\)- and \((4,4,m)\)-graph.
The decomposition is only exhaustive given those.

## The cost of finishing, measured

| \(d\) | \(m\) | \(|(3,5,d)|\) | \(|(4,4,m)|\) | instances |
|---|---|---|---|---|
| 7 | 17 | 71 | 1 | 71 |
| 8 | 16 | 179 | 2 | 358 |
| 9 | 15 | 290 | 640 | 185,600 |
| 10 | 14 | 313 | 130,816 | 40,945,408 |
| 11 | 13 | 105 | 1,184,231 | 124,344,255 |
| 12 | 12 | 12 | 1,449,166 | 17,389,992 |
| 13 | 11 | 1 | 546,356 | 546,356 |
| | | | **total** | **183,412,040** |

Measured throughput, including proof generation and drat-trim verification, is
\(0.95\) instances per second on six workers (a \(600\)-instance random sample
at \(d = 9\), all refuted). So:

- \(d = 9\) alone: \(\approx 54\) hours;
- the whole decomposition: \(\approx 5.4 \times 10^{4}\) hours, about **six
  years** at six workers.

**Verdict: this decomposition cannot produce a certified \(R(4,5) \le 25\).**
The blocking factor is not instance difficulty — each one is a \(119\)–\(200\)
variable problem refuted in about a second — but the size of the
\((4,4,m)\)-catalogues in the middle of the degree range, which peak at
\(1.4\) million. McKay and Radziszowski did not enumerate pairs; any feasible
certified reproduction needs their actual method, not this.

Leaving \(G[M]\) unknown instead of fixing it from the catalogue does **not**
help: those instances are far harder, and none of \(d = 7, 10, 11, 12, 13\)
was decided in \(120\)–\(300\) s even though the fixed-\(M\) versions take
about a second.

## Files

- `cert45.py` — the gluing encoders (\(M\) free and \(M\) fixed) and the
  ground-truth validator.
- `sweep.py` — refute every \((H,M)\) pair at one degree, verify each proof
  with drat-trim, hash and release.
- `r45bounds.py` — graph6 decoder and bitset \((s,t)\)-goodness checker.
- `proofs_d7.jsonl`, `proofs_d8.jsonl` — per-instance proof hashes.

## Reproduction

```bash
for d in 7 8 9 10 11 12 13; do curl -O https://users.cecs.anu.edu.au/~bdm/data/r35_$d.g6; done
for m in 16 17; do curl -O https://users.cecs.anu.edu.au/~bdm/data/r44_$m.g6; done
python3 cert45.py <a (4,5,24)-graph in graph6> 24     # encoder validation
python3 sweep.py 7
python3 sweep.py 8
```
