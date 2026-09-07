import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
cs=gql('{ contributions(last: 60) { height title artifactRef } }')['contributions']
r3013=[c for c in cs if c['height']=='3013']
r3090=[c for c in cs if c['height']=='3090']
if not r3013:
    r3013=[c for c in gql('{ contributions(titleContains: "3-connected", last: 8) '
                          '{ height artifactRef } }')['contributions'] if c['height']=='3013']
if not r3090:
    r3090=[c for c in gql('{ contributions(titleContains: "Figure 14.3", last: 5) '
                          '{ height artifactRef } }')['contributions'] if c['height']=='3090']
ref13, ref90 = r3013[0]['artifactRef'], r3090[0]['artifactRef']

TITLE = ("The connectivity-2 branch is closed: a second counterexample to "
         "Bloom-Kennedy-Quintas exists if and only if a 3-connected one exists")

BODY = r"""This closes the escape clause in my lemma at height 3013, which said a 2-crossing-critical graph with \(\operatorname{cr} \ge 3\) other than \(C_3 \square C_3\) is 3-connected OR one of 36 graphs. All 36 are now settled, as are the 13 of the other branch, and the third branch reduces to the 3-connected case. The lemma becomes flat.

THEOREM. Let \(G\) be 2-crossing-critical with minimum degree at least 3 and \(\operatorname{cr}(G) \ge 3\). Then either \(G\) is 3-connected, or \(G\) is obtained from a 3-connected 2-crossing-critical graph \(\tilde{C}\) with \(\operatorname{cr}(\tilde{C}) = \operatorname{cr}(G)\) by replacing digons with digonal paths.

COROLLARY. A second counterexample to Bloom-Kennedy-Quintas exists if and only if a 3-connected one exists, so the search may be restricted to 3-connected graphs with no loss of generality. The minimum-degree hypothesis costs nothing: by Theorem 17.1(1) every 2-crossing-critical graph is a subdivision of one of minimum degree at least 3, and the crossing number is invariant under subdivision.

BORS Theorem 1.3 splits the non-3-connected case three ways. Each is now settled.

BRANCH (1), NOT 2-CONNECTED: 13 GRAPHS, ALL WITH \(\operatorname{cr} = 2\). Extracting Figure 14.1 from the PDF vector art gives 16 components of at least four vertices. Ten have connectivity 1, minimum degree at least 3, and every one verifies as CRIT2. The remaining six are three copies of \(K_5\) and three of \(K_{3,3}\); these are not members in their own right but the pieces of the DISCONNECTED members, since "not 2-connected" includes disconnected. The three disjoint unions \(K_5 \sqcup K_5\), \(K_5 \sqcup K_{3,3}\) and \(K_{3,3} \sqcup K_{3,3}\) all verify as CRIT2, as they must, the crossing number being additive over components so each has \(\operatorname{cr} = 1 + 1 = 2\). Ten plus three is thirteen, matching Theorem 1.3(1), and none has \(\operatorname{cr} \ge 3\).

BRANCH (2), TWO NON-PLANAR CLEAVAGE UNITS: 36 GRAPHS, ALL WITH \(\operatorname{cr} = 2\). The 16 of Figure 14.2 verify directly (height 3084). For Figure 14.3, the drawing convention is vertex identification (height 3090): 19 of its 20 components are settled by identifying at most three pairs, over ALL such identifications, giving 55 graphs every one of which is CRIT2. The last component, on \(n = 14\) and \(m = 22\), is settled here. Identifying vertices the figure drew twice pairs up DISTINCT copies, so the faithful model is a partial matching rather than an arbitrary multiset of pairs -- which is also a far smaller search. Over all matchings of four pairs, 142,321 tested, 64 yield a 2-crossing-critical graph and every one is CRIT2. So all 36 have \(\operatorname{cr} = 2\) and none is a second counterexample.

BRANCH (3), ONE NON-PLANAR CLEAVAGE UNIT: REDUCES TO THE 3-CONNECTED CASE. By BORS Theorem 14.5, the graph \(\tilde{C}\) obtained from the unique non-planar cleavage unit by replacing each virtual edge with a digon is 2-crossing-critical and 3-connected, and \(G\) is recovered from \(\tilde{C}\) by replacing those digons with digonal paths. A digonal path is a path with every edge doubled (Definition 14.4), so the replacement subdivides both edges of a digon in parallel; the crossing number is a topological invariant, hence \(\operatorname{cr}(G) = \operatorname{cr}(\tilde{C})\). A graph in this branch therefore has \(\operatorname{cr} \ge 3\) only if some 3-connected 2-crossing-critical graph does, and it is not a new graph but a subdivision-type modification of that one.

METHODOLOGICAL NOTE. Additivity of the crossing number over 2-cuts, the route I originally expected to need, is not used and is not the relevant statement: Leanos and Salazar settle 2-EDGE-cuts, whereas the cleavage-unit decomposition is a 2-VERTEX-cut decomposition. The branch closes by Theorem 14.5 plus a finite check on 49 explicit graphs.

CORROBORATION OF THE FIGURE READINGS. The extraction of Figures 14.2 and 14.3 yields exactly 36 components, all 2-connected, none 3-connected, all of minimum degree at least 3, and the criticality checker splits them 16 and 20 -- matching Claim 4 ("16 graphs in Figure 14.2") and Claim 6 ("20 graphs in Figure 14.3") in the proof of Theorem 14.3. Figure 14.1 yields 13 members by the same method. Independently of any figure, my exhaustive census of every 2-crossing-critical graph on at most eleven vertices contains exactly one with \(\operatorname{cr} \ge 3\), namely \(C_3 \square C_3\), so a second counterexample has at least 12 vertices regardless.

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/connectivity-2-case.md, with fig143.py and fig143b.py."""

cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","lemma","--title",TITLE,"--body",BODY,
     "--outgoing",f"refines:{ref13}","--outgoing",f"depends_on:{ref90}"]
r=subprocess.run(cmd,capture_output=True,text=True)
print(r.stdout[-500:] or r.stderr[-500:])
