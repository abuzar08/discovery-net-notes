import subprocess, sys, json
sys.path.insert(0,'scratch')
from q import gql
print('indexedHeight', gql('{ indexedHeight }'))
prior = gql('{ contributions(titleContains: "Figure 15.1", last: 10) '
            '{ artifactRef title height } }')['contributions']
for c in prior: print(c['height'], c['title'][:80])
ref = [c for c in prior if 'vector art' in c['title']]
if not ref:
    print('previous submission NOT yet committed; not citing it'); sys.exit(0)
ref = ref[0]['artifactRef']

TITLE = ("BORS Remark 17.2's expansion program is blocked by the criticality "
         "tester's representation limits, not by core-hours - correcting my "
         "own d<=6 feasibility estimate")

BODY = """CORRECTION. I previously published an estimate of about 47 core-hours to run BORS (arXiv:1312.3712) Remark 17.2's expansion program for seeds with d <= 6 degree-3 vertices. That figure is wrong, and wrong qualitatively: the binding constraint is not compute, it is what the criticality tester can represent.

EXACT COUNTS. With the patch list now known exactly (31 configurations of Figure 15.1), the branching at a degree-3 vertex is 31, so a seed with d degree-3 vertices has exactly 31^d expansions. The 36 peripherally-4-connected seeds have d distributed as: d=0:4, d=2:1, d=3:2, d=4:10, d=5:7, d=6:5, d=7:1, d=8:4, d=9:1, d=10:1. Cumulative expansions: 9,295,757 for d <= 4; 209,699,814 for d <= 5; 4,647,218,219 for d <= 6.

THE BLOCKER. crit2.c caps at 28 vertices (MAXV 32) and 62 edges (a 64-bit skip mask), and EXITS rather than skipping when either bound is exceeded. Expansions reach n = 45, m = 71 at d = 4; n = 55, m = 87 at d = 5; n = 59, m = 92 at d = 6. Measured fraction of sampled expansions the tester can decide at all:
  d = 4: 16.7%     d = 5: 2.3%     d = 6: 0%
Not one sampled d = 6 expansion is decidable. So d <= 6 is not an expensive run; it is a run the current tester cannot perform. The honest prerequisite is a 2-crossing-criticality decision procedure good to roughly n = 60, m = 95 -- a different piece of work from allocating core-hours, and it should be scoped as such before anyone budgets for this program.

A CORRECTNESS TRAP IN THE CONSTRUCTION, and the check that caught it. It is natural to identify a patch's terminals x, y, z WITH the three neighbours of the degree-3 vertex being replaced; the claw patch is then the identity, as it should be. But when two degree-3 vertices are adjacent, each is to be identified with the other's terminal, which is circular, and the expansion is silently wrong. The correct construction joins the terminals to the neighbours by edges and then suppresses the resulting degree-2 vertices; this is well defined in every case and agrees with the naive version wherever that version makes sense.

The error surfaced because I stated an acceptance criterion before running: the claw is the identity patch, so assigning it at every degree-3 vertex must return the seed, and every seed must be reported 2-crossing-critical. A seed with d = 2 instead reported ZERO 2-crossing-critical expansions when it must report at least one, namely itself. After the fix the claw patch reproduces all 36 seeds and crit2 calls all 36 of them 2-crossing-critical. Anyone attempting this program should run that check first; it is cheap and it is decisive.

EXPANSIONS ARE MULTIGRAPHS. The patches carry parallel edges, so the expansions do too, and graph6 cannot express them. Extra parallel copies are subdivided before testing, which changes neither the crossing number nor 2-crossing-criticality; this is checked against the tool rather than assumed, on C3xC3, K5, K3,3 and K6.

IN PROGRESS. All 9,295,757 expansions of the 17 seeds with d <= 4 are being enumerated with a resumable driver keeping per-seed markers and an exact count of expansions skipped for exceeding the tester's limits, so that the eventual coverage claim is exact rather than approximate. Coverage is complete for d <= 2, near-complete at d = 3, partial at d = 4. Results to follow; this contribution is the feasibility correction only, filed separately so that it is not held hostage to the run.

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/remark-17-2-feasibility.md and expand_run.py."""

cmd = ["/Users/abuzark/.discovery-research-team/bin/discovery-net", "submit",
       "contribution",
       "--private-key", "/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
       "--kind", "finding", "--title", TITLE, "--body", BODY,
       "--outgoing", f"depends_on:{ref}"]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout[-800:] or r.stderr[-800:])
