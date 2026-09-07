# Can any exact crossing-number instrument be made to work here?

The principal authorised **one pass** to establish whether *any* exact
crossing-number instrument can be made to work on this machine at eight vertices
and twenty-five edges — the size of \(M_{8,3}\), whose crossing number is confined
to \(\{8,9\}\) and is the tightest open entry in Mohar's Conjecture 5. If nothing
works, stop the lane at the status map. This is the report.

**Verdict: nothing works.** Three routes, each tried to the point of a definite
answer.

## 1. Exhaustive planarisation — correct, and provably out of range

Enumerating every set of \(k\) crossing pairs and every ordering of crossings
along shared edges is exact, and it is what established
\(\operatorname{cr}(K_{1,2,2,2}) = 3\) and \(\operatorname{cr}(K_7 - 2e) = 4\). At
\(M_{8,3}\) it needs \(k = 8\) among 168 independent pairs:
$$\binom{168}{8} \;\approx\; 10^{13}.$$
Out of range, and not by a margin that any constant-factor speedup closes.

## 2. Branching on Kuratowski subdivisions — correct, does not scale

The standard alternative (`krcr.py`): every Kuratowski subdivision must carry a
crossing, and in an optimal drawing crossings join only independent edges, so it
suffices to branch over the independent pairs *within one subdivision*.
Memoisation buckets by a Weisfeiler–Lehman hash — which is an isomorphism
**invariant**, so it can only refine buckets — with exact isomorphism deciding
membership inside each bucket. Using WL alone as the key would be unsound, and
that distinction is the reason this implementation is trustworthy where an
earlier count of mine was not.

It returns \(\operatorname{cr}(K_5) = 1\), \(\operatorname{cr}(K_6) = 3\) and
\(\operatorname{cr}(K_{3,3}) = 1\) correctly and quickly. It **does not reach the
depth required**. The measured branching factors are 15 for \(K_7\) and **24** for
\(M_{8,3}\), giving trees of \(15^8 \approx 2.6\times10^9\) and
\(24^8 \approx 1.1\times10^{11}\); the hard direction — proving a bound is *not*
met, which is what an open case needs — does not clear \(k = 6\) on \(K_7\) in
several minutes.

## 3. OGDF — unavailable on this machine

The published instrument is ILP branch-and-cut in OGDF. Two obstacles, in order.

* The exact minimiser's ILP wants an external solver, and the one named in the
  literature is **CPLEX**, which is commercial and not present here. OGDF bundles
  COIN-OR, so this alone might not have been fatal.
* `ogdf-python`, the pip-installable binding, **does not load**. Its `cppyy`
  backend is linked against `/opt/local/lib/libzstd.1.dylib`, a MacPorts path
  absent on this machine. The library itself is present via Homebrew, and
  bridging with `DYLD_FALLBACK_LIBRARY_PATH` gets past the missing-library error
  — after which the backend **crashes**. Not a configuration problem this pass
  can fix.

## 4. A hand-rolled ILP — declined on soundness grounds

A MILP solver *is* available (HiGHS via `scipy.optimize.milp`, verified working).
What is not available in one pass is a formulation I can vouch for. The natural
encoding — binary variables for crossing pairs, minimise their sum, add
Kuratowski cuts lazily — is only correct with the ordering and realizability
constraints of the published OOCM/SECM formulations. The obvious simplification,
cutting on the Kuratowski subdivision found in a partial planarisation, is *not*
obviously valid: the subdivision lives in the planarised graph, and its shadow in
the original graph need not be non-planar, so the cut can exclude feasible
solutions and return a lower bound that is too large.

**A wrong lower bound is the worst failure mode available here** — it would read
as settling an open case. I would rather report a formulation not built than ship
one I cannot verify.

## Consequence

Per the principal's instruction, **the lane stops at the status map**. The
conjecture is characterised rather than advanced: thirteen verified cases, all
seeds published, twenty-two open entries with their exact gaps, and a consistency
check that holds at every one of them. The two \(n = 8\) entries remain confined
to \(\{10,11,12\}\) and \(\{8,9\}\), and closing either needs branch-and-cut on a
machine that has it.
