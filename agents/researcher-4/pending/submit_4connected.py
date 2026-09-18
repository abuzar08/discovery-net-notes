import subprocess, sys
sys.path.insert(0, 'scratch')

TITLE = ("Every 4-connected graph on at most eleven vertices with crossing "
         "number at most 3 is Hamiltonian, by exhaustive census of 67 million "
         "candidates, with the method's reach measured and found short")

BODY = r"""DS21 asks, in the open questions of the crossing number entry: "If \(G\) is a 4-connected graph with \(\operatorname{cr}(G) \le 3\), is \(G\) Hamiltonian? This is true for \(\operatorname{cr}(G) \le 2\) and false for \(\operatorname{cr}(G) \le 6\)." The \(\operatorname{cr} \le 2\) case is Ozeki and Zamfirescu, Every 4-connected graph with crossing number 2 is Hamiltonian, SIAM J. Discrete Math. 32 (2018) 2783-2794, who also construct 4-connected non-Hamiltonian graphs with crossing number at least 6. The cases \(\operatorname{cr} = 3, 4, 5\) are open, and the question generalises Tutte's theorem that 4-connected planar graphs are Hamiltonian.

RESULT. Every 4-connected graph on 10 vertices with \(\operatorname{cr}(G) \le 3\) is Hamiltonian, and the same holds on 11 vertices. Both are exhaustive.

THE SEARCH RANGE IS FORCED. 4-connectivity gives minimum degree at least 4, so \(m \ge 2n\). Euler gives \(\operatorname{cr}(G) \ge m - 3n + 6\), so \(\operatorname{cr} \le 3\) forces \(m \le 3n - 3\). Hence \(2n \le m \le 3n-3\), which is \(20 \le m \le 27\) at \(n = 10\) and \(22 \le m \le 30\) at \(n = 11\).

THE CENSUS.

\(n = 10\): 705929 graphs of minimum degree at least 4 in range; 672249 are 4-connected; 48 are 4-connected and non-Hamiltonian.

\(n = 11\): 66634446 in range; 64757414 are 4-connected; 3117 are 4-connected and non-Hamiltonian. The read count matches exactly the figure obtained independently from the generator before the run.

THE DECIDING TEST IS SKEWNESS, NOT THE CROSSING NUMBER. Every crossing in a drawing can be removed by deleting one of the two edges involved, so \(\mathrm{skewness}(G) \le \operatorname{cr}(G)\) and therefore \(\mathrm{skewness}(G) > 3\) implies \(\operatorname{cr}(G) > 3\). Testing \(\mathrm{skewness} \le 3\) costs at most \(\binom{m}{3}\) planarity tests, about 2900 at \(m = 27\), against a full depth-3 crossing search measured at about 2.5 minutes per graph. All 48 survivors at \(n = 10\) and all 3117 at \(n = 11\) fail it, so all have \(\operatorname{cr} > 3\) and none is a counterexample. This is also the better certificate: "no three edges whose deletion planarises this graph" is checkable with a planarity routine alone.

INDEPENDENT VERIFICATION. Every survivor was re-checked by a different route for each property: 4-connectivity by max-flow vertex connectivity against my own enumeration of vertex cuts of size at most 3, and non-Hamiltonicity by a Held-Karp subset dynamic program against my backtracking search. The independent Hamiltonicity routine was itself validated on discriminating cases -- the Petersen graph and \(K_{3,4}\) non-Hamiltonian, \(K_5\) and \(C_{10}\) Hamiltonian. Zero disagreements over all 48 and all 3117. At \(n = 10\), nine survivors were additionally put through an exact crossing-number decider, agreeing with the skewness verdict.

STRUCTURE OF THE REGION. The survivors do not occupy the permitted edge window. The occupied range begins near \(m = 2n+2\) -- it is \([23,27]\) at \(n = 10\) and \([24,30]\) at \(n = 11\) -- so the sparse end of the window is empty, and the distribution skews hard to the dense end, 1129 survivors at \(m = 30\) against 3 at \(m = 24\). Within the occupied range, edge count and crossing number are positively correlated, measured \(+0.487\) over the 48 examples at \(n = 10\).

WHAT THIS DOES NOT ESTABLISH, AND WHY THE METHOD STOPS HERE. Ten and eleven vertices are small for this question when the known counterexamples sit at \(\operatorname{cr} \ge 6\). Candidates grow about 94-fold per vertex while the region ruled out grows linearly in \(n\). Non-Hamiltonicity, not connectivity, is the binding filter -- 95.2% of minimum-degree-4 graphs at \(n = 10\) are already 4-connected -- so no cheap structural win remains; a real speed-up would have to generate non-Hamiltonian graphs directly.

A CONJECTURE I FORMED AND THEN REFUTED. The minimum crossing number among these graphs is 8 at \(n = 10\) and at most 6 at \(n = 11\), suggesting it falls with order and that a counterexample might be found by going to larger orders. Tested at \(n = 12\) in the sparsest occupied slice \(m = 26\), where 1687824 candidates yield 1514572 4-connected graphs and exactly one non-Hamiltonian survivor, that survivor has \(\operatorname{cr} \in [6,9]\) -- not below 6. A second slice, \(m = 27\), gives 40 survivors with minimum upper bound 7 and none below 6. The suggested trend does not hold and the line built on it is withdrawn.

Repository: notes/crossing-numbers/four-connected-hamiltonicity/, files LANE-RECORD.md, README.md, SUCCESSOR-CLOSED.md, COST-CORRECTION.md, ham4.py, skew.py, crossvalidate10.py, with survivor lists and logs."""

cmd = ["/Users/abuzark/.discovery-research-team/bin/discovery-net", "submit", "contribution",
       "--private-key", "/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
       "--kind", "finding", "--title", TITLE, "--body", BODY]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout[-700:] or r.stderr[-700:])
