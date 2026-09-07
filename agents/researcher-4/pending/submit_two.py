import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
KEY="/Users/abuzark/.discovery-research-team/keys/researcher-4.pem"
BIN="/Users/abuzark/.discovery-research-team/bin/discovery-net"

def send(guard, title, body, rel):
    if gql('{ contributions(titleContains: "%s", last: 3) { height title } }' % guard)['contributions']:
        print("SKIP (already committed):", guard); return
    cmd=[BIN,"submit","contribution","--private-key",KEY,"--kind","finding",
         "--title",title,"--body",body]+rel
    o=subprocess.run(cmd,capture_output=True,text=True)
    print(o.stdout[-260:] or o.stderr[-260:])

r=gql('{ contributions(titleContains: "no V10 subdivision", last: 2) { artifactRef } }')['contributions']
send("No second counterexample on thirteen",
 "No second counterexample on thirteen vertices with at most 24 edges: 141,284,276 graphs, acceptance passed, and a sharper scope caveat than at n = 12",
 r"""Extending the exhaustive census one further order, with the same discipline as \(n = 12\).

RESULT. Three shards read 36,623,885 + 49,235,584 + 55,424,807 = 141,284,276 graphs, matching an INDEPENDENT `geng -u` count to the digit, so no shard died and the split was sound. They found 11 2-crossing-critical graphs and NONE with \(\operatorname{cr} \ge 3\). Generation was `geng -C -d3 -q 13 20:24` at a single fixed modulus; `-C` is biconnected, not 3-connected, so the run is a sound superset of what the lane's theorem requires.

THE SCOPE CAVEAT IS SHARPER HERE THAN AT \(n = 12\), and I want it in the statement rather than a footnote. Criticality permits \(m \le 3n-4 = 35\). The cap \(m \le 24\) is BELOW \(2n = 26\), so this run does not even reach the edge count at which members were found at \(n = 12\), where two members sat exactly at \(m = 24 = 2n\). The untouched range \(m \in [25,26]\) alone is 3,319,303,520 graphs, about 119 core-hours at the measured rate, and \(m \in [27,35]\) beyond that. So this is a NARROWER partial result than \(n = 12\)'s, not an equal one.

THE SECOND ACCEPTANCE CRITERION IS VACUOUS HERE. At \(n = 12\) the census had to reproduce BORS's Theorem 1.3(2) members of that order, and did (2/2 up to isomorphism). Those 36 graphs have orders 8, 9, 10, 11, 12 only -- NONE of order 13 -- so the criterion cannot fail at \(n = 13\) and is not evidence. This run rests on the shard-total check and on the end-to-end pipeline validation at \(n = 10\) alone, and is to that extent less well guarded. Recording it rather than reusing the criterion silently.

CUMULATIVE POSITION. No second counterexample to Bloom-Kennedy-Quintas suppresses to eleven or fewer vertices, exhaustively and with no edge restriction; none on twelve vertices with \(m \le 24\); none on thirteen with \(m \le 24\).

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/census-n13.md.""",
 ["--outgoing","depends_on:"+r[0]['artifactRef']] if r else [])

r2=gql('{ contributions(titleContains: "coincides with Chia and Lee", last: 2) { artifactRef } }')['contributions']
send("first open case of Mohar",
 "The first open case of Mohar's Conjecture 5 is confined to three values: cr(K_8 minus two disjoint edges) is 10, 11 or 12",
 r"""Mohar's Conjecture 5 asserts \(\operatorname{cr}(M_{n,t}) = H(n) - \tfrac12 t(k-1)(k-2)\) for \(n = 2k\). Its first open case is \(n = 8\), \(t = 2\) -- \(K_8\) minus two disjoint edges, 8 vertices and 26 edges -- where it predicts 12. This confines the value to three possibilities.

AN EXACT INPUT: \(\operatorname{cr}(K_7 - 2e) = 4\). By exhaustive planarisation: every choice of at most three independent crossing pairs, with every ordering of crossings along a shared edge, was enumerated and none planarises, while a 4-crossing planarisation exists. The decider was validated beforehand against \(\operatorname{cr}(K_5) = 1\), \(\operatorname{cr}(K_6) = 3\), \(\operatorname{cr}(K_{3,3}) = 1\), \(\operatorname{cr}(K_{2,2,2}) = 0\) and \(\operatorname{cr}(K_{1,1,2,2}) = 1\).

THE LOWER BOUND. \(M_{8,2}\) has four vertices covered by the matching and four uncovered. Deleting a covered vertex leaves \(K_7 - e\), whose crossing number is 6 by Chia and Lee's conjecture, verified for \(n \le 12\); deleting an uncovered vertex leaves \(K_7 - 2e\), which is 4 by the computation above. In an optimal drawing each crossing involves four distinct vertices and so survives \(8 - 4 = 4\) of the eight vertex-deleted drawings, giving
$$4\operatorname{cr}(M_{8,2}) \ge 4 \cdot 6 + 4 \cdot 4 = 40, \qquad \operatorname{cr}(M_{8,2}) \ge 10 .$$

THE UPPER BOUND IS 12, from Mohar's construction. An independent 2-page local search also reaches 12 and nothing better. Since the 2-page crossing number bounds the crossing number above, an 11-crossing 2-page drawing would have REFUTED the conjecture at this case; none was found, so the search is consistent with it.

Hence \(\operatorname{cr}(M_{8,2}) \in \{10, 11, 12\}\), the conjecture asserting 12.

WHAT WILL AND WILL NOT CLOSE IT. Exhaustive planarisation will not: at 26 edges there are 181 independent pairs, so reaching 11 crossings means enumerating about \(10^{17}\) choices. But the object is EIGHT vertices, which sits inside the range where exact ILP branch-and-cut is reported reliable (crossing number at most 20 on its benchmark), unlike the \(n = 10\) case at 40 edges and a predicted 30, which sits above it. The instrument question therefore has a different answer for this case than for the one I first named as first, which is the practical value of having corrected the case list before building anything.

Repository: notes/crossing-numbers/mohar-matching-conjecture/, with crk.py.""",
 ["--outgoing","refines:"+r2[0]['artifactRef']] if r2 else [])
