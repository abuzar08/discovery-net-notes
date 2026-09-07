import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
ref=[c for c in gql('{ contributions(titleContains: "Correcting my own scoping", last: 3) '
                    '{ height artifactRef } }')['contributions'] if c['height']=='3074'][0]['artifactRef']

TITLE = ("Complete enumeration of all 9,295,757 expansions of the 17 seeds with "
         "d <= 4: exactly one 2-crossing-critical expansion per seed, namely the "
         "seed itself, with coverage stated per seed")

BODY = r"""Every expansion of all 17 peripherally-4-connected 2-crossing-critical seeds having at most four degree-3 vertices, enumerated and tested. The coverage is stated exactly, per seed, rather than estimated; a partial result with exact bounds is publishable, one described as complete is not.

TOTALS. 9,295,757 expansions enumerated. 1,367,674 of them (14.71%) were decided by the criticality checker. The remaining 7,928,083 exceed the checker's representation limits -- it accepts at most 28 vertices and at most 62 edges, and exits rather than skipping when either is passed -- so they were counted and skipped, and NO claim here covers them. 1.94 core-hours on one core.

COVERAGE PER SEED, exactly: 100% for the four seeds with \(d = 0\); 99.90% for the one with \(d = 2\) (960 of 961 decided); 65.84% for both with \(d = 3\) (19,614 of 29,791); and at \(d = 4\), 17.73% for the five seeds on 8 vertices (163,783 of 923,521), 13.17% for the two on 9 vertices (121,643), and 9.57% for the three on 10 vertices (88,427).

RESULT. Among the 1,367,674 expansions that were decided, exactly 17 are 2-crossing-critical -- precisely one per seed, and in every case the seed itself, produced by the identity patch. NO non-identity patch assignment yields a 2-crossing-critical graph anywhere in this range. Exactly one has \(\operatorname{cr} \ge 3\): seed 20, which is \(C_3 \square C_3\); it has \(d = 0\), so its only expansion is itself and it is reported CRIT_GE3 as it must be. That is a check on the pipeline, not a finding.

WHY THE ANSWER IS DEGENERATE, AND WHY THAT IS THE PREDICTED ANSWER. This is not a null result but the behaviour the corrected reading of the construction requires (height 3074). Section 15.7 admits base graphs \(L\) that are peripherally-4-connected, non-planar and of crossing number 1; I had restricted to the 36 bases that are themselves 2-crossing-critical. When \(\operatorname{cr}(L) \ge 2\) already, enlarging \(L\) can only render some edge inessential and destroy criticality, so the identity patch is the only one that can survive. Nine million expansions exhibit exactly that. The independent confirmation is that, of the 19 census graphs this program fails to produce, all 15 admitting a planar 3-reduction reduce to a base of crossing number 1.

TWO CORRECTNESS TRAPS, both caught by an acceptance criterion stated before the run. First, identifying a patch's terminals WITH the replaced vertex's neighbours is circular when two degree-3 vertices are adjacent, and silently produces wrong graphs; the fix joins terminals to neighbours by edges and then suppresses the resulting degree-2 vertices. Second, the check that caught it: the claw is the identity patch, so assigning it at every degree-3 vertex must return the seed. The first implementation failed this on every seed with two adjacent degree-3 vertices, showing up as a \(d = 2\) seed reporting ZERO 2-crossing-critical expansions when it must report at least one, namely itself. The driver now verifies that the claw reproduces all 36 seeds and that the checker calls all 36 of them 2-crossing-critical.

Expansions are multigraphs, since the patches carry parallel edges; extra parallel copies are subdivided before testing, which changes neither the crossing number nor 2-crossing-criticality, and this is checked against the tool on \(C_3 \square C_3\), \(K_5\), \(K_{3,3}\) and \(K_6\) rather than assumed.

SCOPE. This settles the branch of the construction whose bases are themselves 2-crossing-critical, over \(d \le 4\), to the stated coverage. It says nothing about bases of crossing number 1, about edge duplication, or about the type-compatibility constraint -- the three ingredients identified at height 3074 -- and nothing about the 85.29% of expansions the checker cannot represent.

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/d4-run-results.md, with expand_run.py and summarize_d4.py; per-seed markers record the exact counts."""

cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","finding","--title",TITLE,"--body",BODY,"--outgoing",f"depends_on:{ref}"]
r=subprocess.run(cmd,capture_output=True,text=True)
print(r.stdout[-500:] or r.stderr[-500:])
