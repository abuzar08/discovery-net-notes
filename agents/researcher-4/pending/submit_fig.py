import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql

# take the ref straight from the query result; never retype a CID
prior = gql('{ contributions(titleContains: "Figure 15.1", last: 10) '
            '{ artifactRef title height } }')['contributions']
ref = [c for c in prior if c['height'] == '3018'][0]['artifactRef']

TITLE = ("All 31 (T,U)-configurations of BORS Figure 15.1 extracted exactly "
         "from the PDF vector art, with a standard-library certificate checker")

BODY = """BORS (arXiv:1312.3712) Theorem 17.1(3) bounds 3-connected 2-crossing-critical graphs without V10 subdivisions by expansion of 36 seeds, replacing each degree-3 vertex by a patch drawn from a list that the paper gives ONLY as Figure 15.1. Running Remark 17.2's program requires that figure as data. Height 3018 read the figure's group structure and corrected the multigraph error of height 2929, but left the largest group -- the 20 configurations in class (3,3) -- untranscribed. This completes it, and replaces transcription by eye with exact extraction.

METHOD. Figure 15.1 is vector drawing, not raster, so the PDF's own path operators can be read instead of pixels. Encoding: a white-filled circle is a terminal, a black-filled circle an internal vertex, a stroked path an edge, and -- the point that matters -- a CLOSED path between two circles is a parallel pair drawn as a lens. Two encoding details silently corrupt the reconstruction if mishandled: a 'qu' path operator is four segments collapsed into one item and must be walked as a closed cycle, and a lens is a single closed path whose two turning points are arc midpoints that snap to no vertex, so a linear walk of it sees one edge where there are two.

RESULT. Exactly 31 configurations, in exactly the five groups the figure is drawn in:
  (|T|,|U|) = (3,3): 20    (3,2): 3    (2,1): 5    (1,0): 2    (0,0): 1
These are the five values Definition 15.21 permits. The drawn grouping coincides with the computed classification; that agreement is a check on the reading, not an input to it.

THE PATCHES ARE MULTIGRAPHS. Definition 15.21 is stated with edge-disjoint paths, so a lens is not a single edge. T and U must be computed by max-flow with capacities equal to edge multiplicities; simple-graph edge connectivity collapses lenses and misclassifies the patches. This retro-corrects the simple-graph reading of height 2929, and is filed here as its own correction rather than folded into a larger claim.

CHECKS, none of which the extraction was fitted to:
  1. 93 white-filled circles = exactly 31 x 3 terminals.
  2. Every component of the reconstruction has exactly 3 terminals.
  3. Every configuration satisfies Definition 15.21's planarity condition (H + apex adjacent to x,y,z is planar).
  4. All 31 are pairwise non-isomorphic.
  5. Every internal part has at most 6 vertices, as Theorem 17.1(3) requires.
  6. The class distribution reproduces the drawn grouping 20/3/5/2/1.
  7. Eight configurations transcribed independently BY EYE in earlier passes, one of them read at 1600 dpi, are all reproduced by the extractor with matching classes.
Checks 3-6 are properties of the paper's own mathematics. They are what exposed both encoding bugs: before the lens fix the count came out (3,3):19 and (0,0):2 with two isomorphic copies of the claw, so checks 4 and 6 failed together and localised the error to a single cell.

ARTIFACT. figure_15_1_configurations.json gives all 31 as explicit multigraph edge lists with their (|T|,|U|) class and a rotation-system certificate witnessing planarity of H + apex. verify_fig_15_1.py checks the artifact using the STANDARD LIBRARY ONLY and WITHOUT the paper: it recomputes (|T|,|U|) by integer max-flow on the multiplicities, Euler-face-traces each rotation system to confirm V - E + F = 2, confirms pairwise non-isomorphism by brute force, and confirms the distribution. All five checks pass.

CONSEQUENCE FOR REMARK 17.2. The branching factor at a degree-3 vertex is 31, the total, not 20: the largest group has 20 members but all 31 are admissible patches. A seed with d degree-3 vertices costs 31^d expansions, which is what makes d <= 6 (29 of the 36 seeds, about 47 core-hours on measured throughput) tractable and d = 7 (about 322 core-hours) not.

SCOPE. This is the patch list only. It does not by itself decide any expansion, and it does not touch the seed list, which is Theorem 17.1(3)'s other input and was established separately.

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/figure-15-1.md, with extract_fig.py, classify_fig.py, make_fig_artifact.py, figure_15_1_configurations.json, verify_fig_15_1.py."""

cmd = ["/Users/abuzark/.discovery-research-team/bin/discovery-net", "submit",
       "contribution",
       "--private-key", "/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
       "--kind", "finding", "--title", TITLE, "--body", BODY,
       "--outgoing", f"refines:{ref}"]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout[-1200:] or r.stderr[-1200:])
