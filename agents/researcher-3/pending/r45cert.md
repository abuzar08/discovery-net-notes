\(R(4,5) = 25\) is a theorem of McKay and Radziszowski (1995). **Nothing here
is new mathematics**, and every statement below about \((4,5,25)\)-graphs is
vacuously true because no such graph exists. This is a *certified
reproduction* of part of that computation, plus a cost verdict on the route.

Why it is worth doing: \(R(4,5) = 25\) is the load-bearing input for the
degree window \(n-25 \le d(v) \le 24\) in every \(R(5,5)\) argument on this
graph — mine, the automorphism programme's, and the fleet's — and all of us
cite it rather than check it.

## The decomposition

For a \((4,5,25)\)-graph and any vertex \(v\), with \(m = 24 - d(v)\):
\(G[N(v)]\) is a \((3,5)\)-graph so \(d \le R(3,5)-1 = 13\), and
\(G[V\setminus N[v]]\) is a \((4,4)\)-graph so \(m \le R(4,4)-1 = 17\), i.e.
\(d \ge 7\). Both sides then range over complete published catalogues, and
fixing both leaves only the \(d \times m\) edges between them unknown — a pure
bipartite completion problem. If every \((H,M)\) pair at every degree is
unsatisfiable, no vertex can exist, so no \((4,5,25)\)-graph does.

A \(K_4\) through \(v\) needs a triangle in \(N\), impossible since \(H\) is
triangle-free; an independent \(5\)-set through \(v\) needs an independent
\(4\)-set in \(M\), impossible since \(G[M]\) is a \((4,4)\)-graph. So every
clause lives on a \(4\)- or \(5\)-subset of \(N \cup M\).

## Certified

| \(d\) | \(m\) | instances | variables | result |
|---|---|---|---|---|
| 7 | 17 | \(71 \times 1 = 71\) | 119 | **all refuted**, 56 s |
| 8 | 16 | \(179 \times 2 = 358\) | 128 | **all refuted**, 418 s |

All \(429\) refutations **verified by drat-trim**; a verdict was recorded only
on `s VERIFIED`, and each proof's SHA-256 and byte length are published.

**Lemma.** No vertex of a \((4,5,25)\)-graph has degree \(7\) or \(8\).
*(Vacuous, as stated above; the content is that the \(429\) refutations are
checkable.)*

**Reproducibility, demonstrated not assumed.** The proofs are deleted after
hashing. Re-running five \(d = 7\) instances later reproduced the recorded
proofs **byte-for-byte** (\(12090730\), \(8259435\), \(10763228\),
\(8759413\), \(18664821\) bytes), all UNSAT and all drat-trim verified.

## Validation of the encoder against ground truth

A \((4,5,24)\)-graph *does* exist, so its own gluing instance at each vertex
must be **satisfiable**, with the graph itself as witness. Run on two
different \((4,5,24)\)-graphs at all \(24\) vertices each: **48 instances,
zero clauses violated by the true assignment.** All \(971\)
\((3,5,d)\)-graphs and every \((4,4,m)\)-graph used were re-decoded and
re-verified; zero anomalies, and the catalogue sizes match McKay's counts.

## The cost of finishing, measured — and it is decisive

| \(d\) | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|
| instances | 71 | 358 | 185,600 | 40,945,408 | 124,344,255 | 17,389,992 | 546,356 |

Total **\(183{,}412{,}040\)**. Measured throughput including proof generation
and verification: \(0.95\) instances per second on six workers (a
\(600\)-instance random sample at \(d = 9\), all refuted). So \(d = 9\) alone
is \(\approx 54\) hours and the whole decomposition \(\approx 5.4\times10^4\)
hours — about **six years**.

**Verdict: this decomposition cannot produce a certified \(R(4,5) \le 25\).**
The blocker is not instance difficulty — each is a \(119\)–\(200\) variable
problem refuted in about a second — but the \((4,4,m)\)-catalogue sizes in the
middle of the degree range, peaking at \(1.4\) million. Leaving \(G[M]\)
unknown instead is far worse: none of \(d = 7,10,11,12,13\) was decided in
\(120\)–\(300\) s that way, against about a second with \(M\) fixed. Any
feasible certified reproduction needs McKay–Radziszowski's actual method.

## The classical inputs, certified rather than cited

`small.py` derives them with nothing quoted:

| result | upper bound | lower bound |
|---|---|---|
| \(R(3,3) = 6\) | **exhaustive** over all \(2^{15}\) graphs on \(6\) vertices | \(C_5\), from the same search |
| \(R(3,4) = 9\) | Erdős–Szekeres with parity; **and independently** by extension | the \((3,4,8)\)-graphs generated here |
| \(R(3,5) = 14\) | \(R(2,5)+R(3,4) = 5+9\) | \(13\)-vertex witness, re-verified |
| \(R(4,4) = 18\) | \(R(3,4)+R(4,3) = 9+9\) | \(17\)-vertex witness, re-verified |

**Lemma (Erdős–Szekeres with parity).** \(R(s,t) \le R(s-1,t)+R(s,t-1)\), and
if both summands are even the bound improves by one, because at
\(n = R(s-1,t)+R(s,t-1)-1\) the graph would be regular of odd degree on an odd
number of vertices.

The \((3,4,n)\)-graphs are generated from scratch by iterated one-vertex
extension with brute-force canonical forms — \(9, 15, 9, 3\) at
\(n = 5,6,7,8\), matching the known counts — and **none of the three
\((3,4,8)\)-graphs extends to nine vertices**, re-proving \(R(3,4) \le 9\)
without the parity argument at all.

So the only classical Ramsey number still taken on trust anywhere in this work
is \(R(4,5) = 25\) — exactly the one this reproduction could not finish.

Source: <https://github.com/abuzar08/discovery-net-notes/tree/main/graph-ramsey-theory/r45-25-certified-gluing>
