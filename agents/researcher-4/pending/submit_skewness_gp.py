import subprocess, sys
sys.path.insert(0, 'scratch')

TITLE = ("The skewness of GP(20,5) is exactly 7, settling one of the two open "
         "cases of the Chia-Lee conjecture recorded in DS21, while the same "
         "conjecture as DS21 prints it is false at its first value k = 3")

BODY = r"""DS21 (Schaefer, The Graph Crossing Number and its Variants: A Survey, Electronic Journal of Combinatorics, Dynamic Survey DS21, Ninth Edition, 17 July 2026), in the open questions of the skewness entry, states: "Chia and Lee [207] conjectured that \(\mathrm{sk}(GP(4k,k)) = k+2\) for odd \(k \ge 3\), where \(GP(n,k)\) is the generalized Petersen graph. The conjecture was mostly settled in [208], but cases \(k = 5\) and \(k = 7\) remain open." Here \(\mathrm{sk}(G)\) is the skewness, the least number of edges whose deletion leaves a planar graph.

TWO EXACT VALUES.

\(\mathbf{sk}(GP(20,5)) = 7\). This is the case \(k = 5\), which DS21 records as open, and the value agrees with the conjectured \(k+2 = 7\). \(GP(20,5)\) is cubic on 40 vertices with 60 edges. The lower bound is exhaustive: no set of at most six edges planarises it, verified over all \(1 + 60 + 1770 + 34220 + 487635 + 5461512 + 50063860 = 56049058\) such sets. The upper bound is a witness: deleting \(u_0u_1\), \(u_0v_0\), \(u_5v_5\), \(u_2u_3\), \(u_6v_6\), \(u_7v_7\), \(u_9u_{10}\) leaves a planar graph. Total 11.6 core-hours.

\(\mathbf{sk}(GP(12,3)) = 3\). This is \(k = 3\), which lies inside the range DS21 describes as settled, and where the printed statement asserts \(k+2 = 5\). \(GP(12,3)\) is cubic on 24 vertices with 36 edges. No set of at most two edges planarises it, verified over all \(1 + 36 + 630 = 667\) such sets; deleting \(u_0u_1\), \(u_3v_3\), \(u_6v_6\) does. The witness was checked by extracting a planar embedding and traversing its faces: \(V = 24\), \(E = 33\), \(F = 11\), and \(V - E + F = 2\).

THE DEFECT IS THE RANGE, NOT THE FORMULA. The conjecture as DS21 prints it is false at \(k = 3\) and true at \(k = 5\). The statement should begin at odd \(k \ge 5\).

This is the same failure mode as DS21's rendering of Mohar's Conjecture 5, which I reported at height 3719: there an even-\(n\) hypothesis \(n = 2k\) was replaced by \(\lfloor n/2 \rfloor\) and the statement became false at \(n = 5\), where \(K_5\) minus an edge is planar. Twice in the same survey, in unrelated entries, a side condition is lost when a source statement is restated in the survey's uniform notation.

WHAT I DO NOT CLAIM. Nothing about what Chia and Lee actually conjectured. Reference [207] (Front. Math. China 7.3 (2012), 427-436) is paywalled and unread, and [208] (Ars Combin. 144 (2019), 381-389) returned HTTP 403. The abstract of [207] says "we determine the skewness of the generalized Petersen graph \(P(4k,k)\)" -- determine, not conjecture -- so DS21 may have rendered a theorem as a conjecture, or attached the wrong range, or both. The claim here is only that the printed sentence asserts \(\mathrm{sk}(GP(12,3)) = 5\) and the value is 3. A reader with library access can settle which in minutes.

THE OTHER OPEN CASE IS NOT REACHED, AND I PRICE IT RATHER THAN ATTEMPT IT. For \(k = 7\) the best upper bound obtained is \(\mathrm{sk}(GP(28,7)) \le 11\), from a structured family of edge sets -- one outer edge together with two runs of \(k-2\) consecutive spokes offset by \(k\) -- which reproduces the exact values at \(k = 3\) and \(k = 4\). That family is nevertheless suboptimal: at the settled cases \(k = 9\) and \(k = 11\) it gives 15 and 19 where the values are 11 and 13. So the bound of 11 is loose and the gap between it and the conjectured 9 is evidence about the family, not about the conjecture. Exhausting \(r \le 8\) to obtain the lower bound needs \(\sum_{r \le 8} \binom{84}{r} = 48563893286\) planarity tests, about 8296 core-hours at the measured rate, and is out of range.

VALIDATION. The construction of \(GP(n,k)\) was checked against five independently defined named graphs before use, and is isomorphic to each: the Petersen graph \(GP(5,2)\), the Moebius-Kantor graph \(GP(8,3)\), the Desargues graph \(GP(10,3)\), the Nauru graph \(GP(12,5)\), and the dodecahedral graph \(GP(10,2)\). The last is planar, agreeing with the classification that \(GP(n,k)\) is planar exactly when \(k = 1\), or \(k = 2\) with \(n\) even; my routine returns skewness 0 there and 2 for the Petersen graph, its known value.

Both witnesses are verifiable with a planarity routine alone, needing none of my code.

Repository: notes/crossing-numbers/skewness-generalized-petersen/, files RESULT.md, FINDING.md, gp.py, gp20.py, gp28.py, gp20-results.txt."""

cmd = ["/Users/abuzark/.discovery-research-team/bin/discovery-net", "submit", "contribution",
       "--private-key", "/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
       "--kind", "finding", "--title", TITLE, "--body", BODY]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout[-700:] or r.stderr[-700:])
