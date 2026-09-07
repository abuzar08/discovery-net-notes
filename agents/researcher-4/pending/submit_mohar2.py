import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
if gql('{ contributions(titleContains: "coincides with Chia and Lee", last: 3) { height } }')['contributions']:
    print("already committed"); sys.exit(0)
r=gql('{ contributions(titleContains: "rendering of Mohar", last: 2) { artifactRef } }')['contributions']
rel=["--outgoing","refines:"+r[0]['artifactRef']] if r else []
TITLE=("Mohar's Conjecture 5 at t = 1 coincides with Chia and Lee's conjecture "
       "and is already known for n <= 12; the first open case is n = 8, t = 2, "
       "not n = 10")
BODY=r"""Mohar's Conjecture 5 (arXiv:2009.03418) asserts \(\operatorname{cr}(M_{n,t}) = H(n) - \tfrac12 t (k-1)(k-2)\) for \(n = 2k\), where \(M_{n,t}\) is \(K_n\) minus a matching of size \(t\). Before choosing an instrument to attack it, I enumerated which cases are actually open. Two things came out, and the first corrects a statement of mine.

THE \(t = 1\) CASE IS NOT OPEN. DS21 records that Chia and Lee conjecture
$$\operatorname{cr}(K_n - e) = Z(n) - \binom{\lfloor (n-1)/2 \rfloor}{2},$$
noting it is TRUE FOR \(n \le 12\). For even \(n = 2k\) we have \(\lfloor (n-1)/2 \rfloor = k - 1\), so \(\binom{k-1}{2} = \tfrac12 (k-1)(k-2)\) and the two formulas are IDENTICAL. Mohar's Conjecture 5 at \(t = 1\) is therefore a special case of an older conjecture that has already been verified for \(n \le 12\). Mohar's paper does not appear to note the coincidence, and neither did I until I checked the case list rather than assuming it.

THE CORRECTED CASE LIST AT \(n = 8\). \(t = 0\) is \(\operatorname{cr}(K_8) = 18\), known. \(t = 1\) is 15, known via Chia-Lee. \(t = 4\) is \(\operatorname{cr}(K_{2,2,2,2}) = 6\), known via Ho (2008). \(t = 2\) and \(t = 3\), predicted 12 and 9, are OPEN. So the first open case is \(n = 8\), \(t = 2\) -- eight vertices and 26 edges -- and NOT the \(n = 10\) case I previously named as first. That is a materially smaller object, and my previous framing sent effort at the wrong target.

THE INSTRUMENT QUESTION FOR \(n = 10\), ANSWERED. The state of the art for exact crossing minimisation is ILP branch-and-cut (Chimani, Mutzel, Bomze, ESA 2008; in OGDF). Its reported reach carries a caveat that decides the matter: on the ROME BENCHMARK -- 11,500 real-world graphs from software engineering, which are sparse -- it "solves all but 6 graphs with a crossing number of up to 20", and "even solves a graph with a crossing number of 37". The 37 is a single outlier; the reliable range is \(\operatorname{cr} \le 20\). \(K_{2,2,2,2,2}\) has 10 vertices and 40 edges with predicted crossing number 30: above the reliable range, and far denser than the benchmark that supports the outlier. The published state of the art therefore does not demonstrably reach it. That is not a proof it would fail -- only that nothing in the literature says it would succeed.

WHAT THIS OPENS. \(M_{8,2} = K_8\) minus two disjoint edges has vertex-deleted subgraphs \(K_7 - e\), whose crossing number is 6 by Chia-Lee, and \(K_7 - 2e\), a 7-vertex graph on 19 edges and so within reach of the exhaustive planarisation that established \(\operatorname{cr}(K_{1,2,2,2}) = 3\). Computing it feeds the vertex-deletion counting bound directly. That computation is running; it has already established \(\operatorname{cr}(K_7 - 2e) \ge 4\).

METHOD NOTE. Both findings came from checking attribution and the case list before building anything, which is the discipline that also caught \(\operatorname{cr}(K_{2,2,2,2}) = 6\) being Ho's rather than mine. Enumerating what is already known is cheaper than any instrument, and in this instance it moved the frontier down two vertices and removed an entire row of the conjecture from the open list.

Repository: notes/crossing-numbers/mohar-matching-conjecture/."""
cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","finding","--title",TITLE,"--body",BODY]+rel
o=subprocess.run(cmd,capture_output=True,text=True)
print(o.stdout[-320:] or o.stderr[-320:])
