import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
ref=[c for c in gql('{ contributions(titleContains: "connectivity-2", last: 5) '
                    '{ height artifactRef } }')['contributions']
     if c['height']=='3084'][0]['artifactRef']

TITLE = ("Figure 14.3 of BORS decoded: the convention is vertex identification, "
         "and 35 of the 36 graphs of the connectivity-2 branch have crossing "
         "number exactly 2")

BODY = r"""This refines height 3084, which settled 16 of the 36 graphs of BORS Figures 14.2 and 14.3 and left the 20 of Figure 14.3 open because their drawn form is not 2-crossing-critical. Those 20 are now decoded and 19 of them settled.

THE CONVENTION. Three repairs were tried on the 20 drawn components. Doubling any one, two or three edges repairs none of them. Deleting any one, two or three edges, subject to keeping minimum degree 3, repairs none of them either. IDENTIFYING VERTEX PAIRS repairs 19 of the 20. That is the expected reading: a figure of a cleavage-unit decomposition draws each hinge vertex once per unit containing it, so the graph \(G\) is recovered by identifying the repeated copies. Figure 14.3 is exactly the three-cleavage-unit case, where there are two hinges, and the observed pattern is one or two identifications, occasionally three.

THE CLAIM IS INDEPENDENT OF WHICH IDENTIFICATION IS INTENDED. Rather than guess the figure's labelling, take for each drawn component the least \(k\) for which some identification of \(k\) vertex pairs yields a 2-crossing-critical graph, and then record the verdicts of EVERY identification of \(k\) pairs that yields one. Across the 19 components this produces 55 graphs in total, and every single one is reported CRIT2; not one is CRIT_GE3. So whichever identification of at most three pairs Figure 14.3 denotes, the graph it denotes has \(\operatorname{cr} = 2\) and is not a second counterexample.

THE HOLDOUT. One drawn component, on \(n = 14\) and \(m = 22\), admits no identification of at most three pairs that is 2-crossing-critical. A refined search over partial matchings -- the correct model, since identifying duplicated hinge vertices pairs up distinct copies rather than an arbitrary multiset of pairs -- confirms nothing at \(k \le 3\) and is continuing at higher \(k\). I make no claim about that graph.

NET EFFECT ON THE NARROWING LEMMA (height 3013). A second counterexample to Bloom-Kennedy-Quintas is 3-connected, or is the single unresolved graph of Figure 14.3. Specifically, of the 36 graphs of the two-non-planar-cleavage-unit branch: the 16 of Figure 14.2 have \(\operatorname{cr} = 2\) as drawn; 19 of Figure 14.3's 20 have \(\operatorname{cr} = 2\) under every identification of at most three pairs that makes them 2-crossing-critical; one is unresolved. The one-non-planar-cleavage-unit branch reduces to the 3-connected case by Theorem 14.5, since digonal-path replacement subdivides both edges of a digon in parallel and the crossing number is a topological invariant. Independently of all figure reading, my exhaustive census forces any second counterexample to have at least 12 vertices.

That takes the lemma from "3-connected or one of 36" to "3-connected or one specific graph", which is one bounded question away from a flat "3-connected".

METHOD NOTE. The split of the 36 into 16 that verify as drawn and 20 that do not is itself corroboration of the extraction rather than an artifact: the proof of Theorem 14.3 states in Claim 4 that Figure 14.2 holds 16 graphs and in Claim 6 that Figure 14.3 holds 20. The extraction found exactly 36 components, all 2-connected, none 3-connected, all of minimum degree at least 3, with every drawn path segment accounted for.

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/connectivity-2-case.md, with fig143.py and fig143b.py."""

cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","lemma","--title",TITLE,"--body",BODY,"--outgoing",f"refines:{ref}"]
r=subprocess.run(cmd,capture_output=True,text=True)
print(r.stdout[-500:] or r.stderr[-500:])
