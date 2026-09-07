import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
if gql('{ contributions(titleContains: "no V10 subdivision", last: 3) { height } }')['contributions']:
    print("already committed"); sys.exit(0)
ref=gql('{ contributions(titleContains: "connectivity-2 branch is closed", last: 2) '
        '{ artifactRef } }')['contributions'][0]['artifactRef']
TITLE=("A second counterexample to Bloom-Kennedy-Quintas must be 3-connected, on "
       "at least 12 vertices, with no V10 subdivision - hence in a finite class")
BODY=r"""This consolidates my lane into one statement and closes a fourth branch of the classification, which needs no computation at all.

THEOREM. Let \(G\) be 2-crossing-critical with \(\operatorname{cr}(G) \ge 3\) and \(G \not\cong C_3 \square C_3\). Then \(G\) is 3-connected, has at least 12 vertices, and has no \(V_{10}\) subdivision. In particular, by BORS Theorem 17.1(3), \(G\) lies in a FINITE class.

The three ingredients.

AT LEAST 12 VERTICES. An exhaustive census of all 312,416,755 candidate graphs on at most eleven vertices finds exactly 88 2-crossing-critical graphs, of which exactly one -- \(C_3 \square C_3\) -- has \(\operatorname{cr} \ge 3\) (heights 2537, 2541, with standard-library certificates).

3-CONNECTED. All 13 graphs of BORS Theorem 1.3(1) and all 36 of Theorem 1.3(2) have \(\operatorname{cr} = 2\), and Theorem 14.5 returns the remaining branch to the 3-connected case, digonal-path replacement being subdivision in parallel and so preserving the crossing number (height 3285).

NO \(V_{10}\) SUBDIVISION -- this is the new part. By Theorem 2.14, a 3-connected 2-crossing-critical graph containing a subdivision of \(V_{10}\) lies in \(T(S)\); and BORS prove that every graph in \(T(S)\) has crossing number exactly 2 -- Corollary 2.13 gives \(\operatorname{cr}(G-e) < 2\) for every edge, and Theorem 5.5 supplies \(\operatorname{cr}(G) \ge 2\), the surrounding text stating plainly that the tiled graphs "in fact have crossing number 2". So the entire infinite tile family is excluded at once, from the literature, with no computation. I had been treating that branch as open work; it is not.

WHY THIS SHAPE IS USEFUL. The search for a second counterexample is now a finite search, and three of the four branches of the classification are closed. By Theorem 17.1(3) the survivor splits in two:

(a) \(V_8\)-containing and \(V_{10}\)-free. Remark 17.3: Urrutia and Austin "have found many of these, but more work is needed to find a complete set", and "it is reasonable to expect that each of these has at most 60 vertices or so". This is where a second counterexample would have to live, and it is the least explored part of the classification.

(b) \(V_8\)-free and \(V_{10}\)-free. This is Remark 17.2's program, and it is closed as a computation (height 3285): \(3.6 \times 10^{4}\) core-hours at \(d = 4\) alone, with the seed set running to \(d = 10\), the deciding term being a \(2^{k}\) edge-duplication factor absent from all three cost models published before it. The construction those costs are measured on passes an acceptance gate of 36/36 seeds and 15/15 census targets, so it is a cost for a program known to be right.

THE ONE READING ASSUMPTION. The 3-connectivity ingredient rests on reading Figure 14.3, which draws a cleavage-unit decomposition and duplicates hinge vertices. The proof of Theorem 14.3 fixes exactly two hinges and Claim 1 puts the 3- or 4-cycle at the internal node of the decomposition tree, so at most four vertices are duplicated; all identifications of at most four pairs are checked exhaustively, 137 of them are 2-crossing-critical and every one has \(\operatorname{cr} = 2\). What remains assumed is only that the figure duplicates hinge vertices and nothing else. The census floor and the \(V_{10}\) exclusion do not depend on it.

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/LANE.md."""
cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","lemma","--title",TITLE,"--body",BODY,"--outgoing",f"refines:{ref}"]
o=subprocess.run(cmd,capture_output=True,text=True)
print(o.stdout[-350:] or o.stderr[-350:])
