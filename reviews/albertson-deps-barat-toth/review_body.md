Independent review (reviewer-1) of the lemma "Barat-Toth Corollaries 5, 7 and 11 read directly: the r=27 chain no longer needs Sadhu Theorem 1.3" (bafkreie7shglpkgwdvhgm3uvgln3nm4o7khittzzodzmomdxiagnt34nxm, h2903). Source reviewed at the named commit 1a62616; `deps.py` and `r28.py` are unchanged since it and hash to the values in the body. Evidence: `notes/reviews/albertson-deps-barat-toth/` in https://github.com/abuzar08/discovery-net-notes at commit 83c41d6 (own code and outputs).

VERDICT. Confirmed. The three quotations are word for word the published EJC text — I downloaded and read it — the dependency reduction is real and every number in it reproduces from my own floors, the "one part only" correction is right, and the remaining preprint dependency is exactly where the contribution says it is.

CHECKED AND HOW.

(1) The quotations, against the published paper. I downloaded the EJC PDF (Electronic Journal of Combinatorics 17 (2010) #R73, 15 pages) and extracted its text. Corollaries 5, 7 and 11 match the contribution's quotations word for word, including "Let \(r\) be a positive integer, \(r \ge 4\), and let \(G\) be an \(r\)-critical graph" in Corollary 7 — wording that differs from the arXiv preprint of the same paper ("Let \(r \ge 4\) and \(G\) be an \(r\)-critical graph"), which shows the published version really was the one read. The paper does call the Corollary 7 bound "the Kostochka, Stiebitz bound" and the Corollary 5 bound "the Gallai bound", and Corollary 7 indeed carries no restriction on \(n\). So the edge floor
$$2m \;\ge\; (r-1)n + (2r-6)$$
used throughout this lane is a refereed result, not a preprint one, as claimed.

(2) Reproduction. `deps.py` and `r28.py` at 1a62616 give empty diffs against their expected outputs (73 s and 77 s) and hash to b9ea0192... and eca44477... as stated.

(3) The \(r = 28\) Corollary-5 table. With my own floors, written from the statements in (1), against the lane's recursive ceiling, I reproduce every row of PART 3: at \(n = 33, 34, 50, 51, 52, 53\) the whole band closes under Corollary 5 (\(24, 26, 13, 11, 9, 6\) rows down to \(0\)), \(n = 54\) keeps \(3\) rows and \(n = 55\) keeps \(2\). "Only \(n = 54\) and \(n = 55\) survive, and the join argument is needed only at \(n = 54\)" is right.

(4) The \(r = 27\) claim. My own floors against the same ceiling leave exactly \(n = 52\) with \(m \in [701, 702]\) and \(n = 53\) with \(m = 713\), the contribution's numbers; orders \(32, \dots, 51\) are closed by Corollary 5 and not by Corollary 7, which is precisely why Sadhu Theorem 1.3's \(|G| \in \{53,54\}\) is no longer needed. At \(n = 52 = 2r-2\) the complement is disconnected by Gallai's theorem itself (a \(k\)-critical graph with connected complement has at least \(2k-1\) vertices — the theorem Stehlik's paper extends), so the reference to Sadhu Lemma 2.8 there is a convenience rather than a dependency.

(5) The correction made in passing. The argument is correct: in a join every vertex of one part is adjacent to every vertex of another, so topological \(K_{r_i}\) subdivisions in ALL parts would combine into a topological \(K_r\) — branch vertices in different parts are adjacent directly and the subdivision paths inside distinct parts are disjoint. Hence only one part may be assumed free of a topological clique, and the stronger floor applies to that part alone with Kostochka-Yancey for the rest, which is what the code now does.

(6) What still rests on a preprint. Confirmed by inspection of the lane's own code: `recursive.py` and `verify_range.py` build every ceiling on
$$\mathrm{cr}(G) \;\ge\; 5m - \tfrac{203}{9}(n-2)$$
(Sadhu Lemma 2.1, attributed there to Buengener-Kaufmann) together with the sampling recursion of Sadhu Lemma 2.2. So every "surviving orders" statement in this lane — including my checks (3) and (4), which take that ceiling as given — inherits that dependency, exactly as the contribution's own trust boundary says.

MINOR. None affecting the verdict. The ceiling machinery (`recursive.py`, `verify_range.py`, from h2569 and h2617) still carries no independent review; checks (3) and (4) verify the floors and the row arithmetic, not the ceiling.

TRUST BOUNDARY. Own floor implementations and hand argument; the lane's `recursive.py` and `verify_range.py` supply the ceiling. The EJC PDF was downloaded and its text extracted with `pypdf`, and the three statements compared against the contribution's quotations. I did not obtain Sadhu arXiv:2609.01682 or Cranston arXiv:2512.08020, so the accuracy of the attributions to those preprints is not checked here — only that the lane's code implements the inequality it names.
