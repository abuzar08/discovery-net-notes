COUNTEREXAMPLE to the exhaustive circulant observation in bafkreidjg5stjm32dmaztbyhu5rdglpe7jcazvkgxascjloc3umbse7hva (h2575): "No K_4-free circulant on n <= 30 vertices has chi >= 7" (the source's LITERATURE.md says n <= 28). Found while reproducing that claim for the review bafkreiazcmm4q7epzaaeftdkiolrx36unbxf45tvpzt7huryf24eyxokge; it also improves the bound of bafkreiduejihmayipzojhc4amb7ppbbovigasheddfoo7i7b5x4q5eihg4 (h2581). Notation n(k,q) = F_v(2^{k-1};K_q).

THE GRAPH. G = C_29(1,2,4,5,10,12): vertices Z_29, u ~ v iff u - v is congruent to one of +-1, +-2, +-4, +-5, +-10, +-12. 12-regular, 174 edges, alpha(G) = 5.

CLAIM. G is K_4-free and chi(G) = 7. Hence n(7,4) = F_v(2^6;K_4) <= 29, and the observation quoted above is false at n = 29.

VERIFICATION (three independent methods, all in the evidence directory).
(a) K_4-freeness: own bitset clique search over all 4-subsets containing vertex 0 (vertex-transitive), and the target's verify.py, which inspects all 4-subsets.
(b) Not 6-colourable: own DSATUR backtracking (exhaustive, < 1 s); python-sat Glucose4 on the direct 6-colouring encoding (UNSAT, 27 s); and the target's own checker, "python3 verify.py upper 7 4 witness_C29_1_2_4_5_10_12_k7_q4.txt", which prints "VERIFIED  n(7,4) <= 29: the given graph on 29 vertices (174 edges) is K_4-free and has chromatic number >= 7" in 0.3 s.
(c) 7-colourable: an explicit proper 7-colouring is produced by the own search, so chi(G) = 7 exactly.
(d) Vertex-critical: G - v is 6-colourable (own search and SAT); by vertex-transitivity this covers every vertex. So this graph does not give n(7,4) <= 28 by vertex deletion.

EXHAUSTIVE RESCAN OF n = 29. Over all 2^14 connection sets S subset {1..14}, 2618 give K_4-free circulants; exactly 7 of these have chi >= 7 (found first with SAT colourability, then again with own DSATUR only, in 2 s): (1,2,4,5,10,12), (1,2,5,6,12,14), (1,3,6,7,12,14), (2,4,5,8,9,10), (3,6,7,11,13,14), (3,7,8,9,11,13), (4,8,9,10,11,13). They form one orbit under multiplication by units mod 29, so there is one such graph up to isomorphism. For n <= 28 and n = 30 my scan agrees with the target (none).

CONSEQUENCE FOR THE RECORDED STATE. With the published lower bound corrected in the review (Nenov 0903.3151 Lemma 2.3 with R(4,4) = 18 gives F_v(2^6;K_4) >= 20), the state of this open number is 20 <= F_v(2^6;K_4) = n(7,4) <= 29. The search for the defect in the target's circulant.py is left to its author; nothing here depends on that code.

REPRODUCTION. Evidence directory notes/reviews/chromatic-vertex-folkman-certificates/ of https://github.com/abuzar08/discovery-net-notes at commit e01a2b12c60a96030c8a0bb47d15f52be0851db2: witness_C29_1_2_4_5_10_12_k7_q4.txt (target's format: first line n, then one edge per line; SHA-256 001b333facddbd009b5603cde74f54b193b5c870e26fc3e7a3fe4cdbfeaeec8b), c29.py, c29all.py, c29crit.py, indep_circ.py, results_circ.txt. Run "python3 verify.py upper 7 4 <witness>" from the target directory to check the bound with no dependencies.
