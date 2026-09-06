# Chosen target and the evidence for choosing it

The principal handed me target choice at pass 17 with four tests: first result
reachable in a few core-hours under contention; certificate-checkable;
publishable either way; uncrowded on the graph.

## The target

> **Settle the \(V_8\)-containing, \(V_{10}\)-free branch — the only place a
> second counterexample to Bloom–Kennedy–Quintas can now live.**

## Why this one

**It is the only branch left, and that is my own result.** The theorem published
this pass says a second counterexample is 3-connected, on at least 12 vertices,
with no \(V_{10}\) subdivision. BORS Theorem 17.1(3) then splits the survivor in
two, and one half — Remark 17.2's expansion program — I have already closed as a
computation at \(3.6\times10^{4}\) core-hours. What remains is Remark 17.3's
class, and BORS say of it: Urrutia and Austin "have found many of these, but more
work is needed to find a complete set", with "each of these ... at most 60
vertices or so". It is explicitly the least explored part of the classification.

**The prior art does not settle it, and I checked why.** Urrutia-Schroeder found
326 graphs, of which only 214 are actually 2-crossing-critical; Austin corrected
that and reached 312; Oporowski had 201 in this class, of which 8 are outside
Austin's 312. Austin's thesis was retrieved and read: her definition is the
correct one — \(\operatorname{cr}(G) \ge k\) with \(\operatorname{cr}(G-e) < k\)
for every edge, not \(\operatorname{cr}(G) = k\) — so her graphs *could* include
one of crossing number 3, and nobody appears to have asked. But the 312 are
produced by an algorithm in Chapter 3 rather than listed, and BORS state the
enumeration is not known to be complete. So the branch is genuinely open, and it
is open in a direction my tools already point at.

## Against the four tests

| test | answer |
| --- | --- |
| first result in a few core-hours | yes — extend the exhaustive census to \(n = 12\) under the constraints the theorem now supplies |
| certificate-checkable | yes — the same census certificates, checkable with the standard library |
| publishable either way | yes — a second counterexample, or the floor rises from 12 to 13 |
| uncrowded | yes — no other agent is in this lane, and this branch has no contributions on the graph |

## The first result, concretely

A 2-crossing-critical graph on \(n\) vertices with \(\operatorname{cr} \ge 3\)
must, by the theorem, be 3-connected; it has minimum degree at least 3 (BORS
17.1(1), up to subdivision); and \(\operatorname{cr}(G-e) \le 1\) forces
\(m - 1 \le 3n - 5\), so
$$m \le 3n - 4 = 32 \quad\text{at } n = 12 .$$
Generating exactly `geng -C -d3 12 18:32` and testing with `crit2` therefore
decides \(n = 12\) outright. That is a strictly smaller search than the \(n = 11\)
census (312,416,755 candidates), because 3-connectivity is now a *theorem* rather
than an assumption — it was not available when the earlier census was run.

Outcome either way: a second counterexample on 12 vertices, or the floor rises
and the search space shrinks again.
