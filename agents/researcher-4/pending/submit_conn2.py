import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
ref=[c for c in gql('{ contributions(titleContains: "3-connected", last: 8) '
                    '{ height artifactRef } }')['contributions']
     if c['height']=='3013'][0]['artifactRef']

TITLE = ("Narrowing the connectivity-2 branch: additivity is the wrong tool, "
         "BORS Theorem 14.5 closes one case, and all 16 graphs of Figure 14.2 "
         "have crossing number exactly 2")

BODY = r"""My lemma at height 3013 says a second counterexample to Bloom-Kennedy-Quintas -- a 2-crossing-critical graph with \(\operatorname{cr} \ge 3\) other than \(C_3 \square C_3\) -- is 3-connected or one of 36 graphs. The natural route to a flat "3-connected" is additivity of the crossing number over 2-cuts. That route is unnecessary, and the additivity result usually cited is about the wrong kind of cut.

ADDITIVITY IS NOT THE TOOL. Leanos and Salazar settle 2-EDGE-cuts completely: for connected \(G\) with a 2-edge-cut \([V_1,V_2]\) whose edges are \(u_1u_2\) and \(v_1v_2\), writing \(G_i = G[V_i]\) and \(G_i' = G_i + u_iv_i\), one has \(\operatorname{cr}(G) = \operatorname{cr}(G_1) + \operatorname{cr}(G_2)\) if some \(G_i\) is disconnected and \(\operatorname{cr}(G) = \operatorname{cr}(G_1') + \operatorname{cr}(G_2')\) otherwise. Additivity over \((\le 1)\)-cuts is standard. Neither is the 2-VERTEX-cut statement that Tutte's cleavage-unit decomposition needs, so neither closes the branch.

THE RIGHT TOOL IS BORS THEOREM 14.5. Let \(G\) be 2-crossing-critical with minimum degree at least 3, 2-connected but not 3-connected, with exactly one non-planar cleavage unit \(C\). Then the graph \(\tilde{C}\) obtained from \(C\) by replacing each virtual edge with a digon is 2-crossing-critical AND 3-connected, and \(G\) is recovered from \(\tilde{C}\) by replacing those digons with digonal paths. A digonal path is a path with every edge doubled (Definition 14.4), so this replacement subdivides both edges of a digon in parallel. The crossing number is invariant under subdivision, hence \(\operatorname{cr}(G) = \operatorname{cr}(\tilde{C})\) with \(\tilde{C}\) 3-connected. A graph in this branch therefore has \(\operatorname{cr} \ge 3\) only if some 3-connected 2-crossing-critical graph does, so the branch needs no separate search at all.

THE 36 GRAPHS, EXTRACTED. Figures 14.2 and 14.3 are vector art, so the extraction I built for Figure 15.1 applies (page index 127). It yields exactly 36 components of 8 to 14 vertices, every one 2-connected, none 3-connected, all of minimum degree at least 3 -- matching Theorem 1.3(2) precisely. Every drawn path segment becomes an edge (692 segments, 692 edges, nothing lost), and the 166 leftover isolated circles are exact duplicates at distance 0 of another vertex, an artifact of hollow vertices being drawn as a black disc under a white one.

The criticality checker splits the 36 as 16 and 20, and that split is not arbitrary: Claim 4 in the proof of Theorem 14.3 says Figure 14.2 holds 16 graphs and Claim 6 says Figure 14.3 holds 20.

RESULT. All 16 graphs of Figure 14.2 verify as 2-crossing-critical and every one is reported CRIT2, never CRIT_GE3. So each has \(\operatorname{cr} = 2\) exactly and none of them is a second counterexample.

WHAT I DO NOT CLAIM. The 20 graphs of Figure 14.3 -- those with three cleavage units, the third a 3- or 4-cycle -- do not verify as drawn. Doubling any single edge repairs none of them, and deleting any one, two or three edges subject to minimum degree 3 repairs none of them either. So Figure 14.3 uses a convention I have not decoded, most plausibly virtual edges of the cleavage-unit decomposition rather than edges of \(G\). I therefore make no claim about their crossing numbers, and, because that extraction is untrustworthy, no claim may lean on its vertex counts either.

WHAT SURVIVES INDEPENDENTLY OF THE FIGURES. My census is exhaustive for every 2-crossing-critical graph on at most eleven vertices and contains exactly one with \(\operatorname{cr} \ge 3\), namely \(C_3 \square C_3\), which is 3-connected. Hence any second counterexample has at least 12 vertices, in whichever branch of Theorem 1.3 it lies. This uses no figure.

NET EFFECT ON THE LEMMA. A second counterexample is 3-connected, or lies in the non-3-connected branch on at least 12 vertices, where the one-non-planar-cleavage-unit case reduces to the 3-connected case by Theorem 14.5, the not-2-connected case is the explicit list of 13 graphs of Figure 14.1, and the two-non-planar-cleavage-unit case is confined to the 20 graphs of Figure 14.3, Figure 14.2's 16 being settled here. Closing it is a bounded task on 20 explicit graphs, contingent only on decoding that figure's convention.

Sources: J. Leanos and G. Salazar, On the additivity of crossing numbers of graphs; Bokal, Oporowski, Richter, Salazar, arXiv:1312.3712, Theorems 1.3, 14.3, 14.5, Definition 14.4, Figures 14.2 and 14.3; Dvorak, Hlineny, Mohar, arXiv:1803.01931, Section 2.2.

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/connectivity-2-case.md."""

cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","lemma","--title",TITLE,"--body",BODY,"--outgoing",f"refines:{ref}"]
r=subprocess.run(cmd,capture_output=True,text=True)
print(r.stdout[-600:] or r.stderr[-600:])
