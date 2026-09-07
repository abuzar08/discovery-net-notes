import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
hits=gql('{ contributions(titleContains: "sampling barrier", last: 3) { height } }')
if hits and hits['contributions']:
    print("already committed:", hits['contributions']); sys.exit(0)
r=gql('{ contributions(titleContains: "recursive integer-aware sampling bound", last: 2) '
      '{ artifactRef } }')['contributions']
ref=r[0]['artifactRef']
TITLE=("The recursive sampling barrier is structural and instance-independent: "
       "Jensen is never the lossy step and the recursion is scale-free, measured "
       "across nine dense instances")
BODY=r"""Researcher-2's remaining Albertson frontiers bottleneck on lower bounds for the crossing number of dense graphs at intermediate density -- \(\operatorname{cr}(G) \ge 3557\) for a 32-vertex graph with 383 edges, and an order-57 form on 50 vertices. My recursive integer-aware sampling bound (height 2713) is the incumbent tool. This establishes what that family can do, in a form that does not depend on which instance is asked.

TWO MEASUREMENTS, ACROSS NINE INSTANCES spanning \(n = 32, 40, 50\) and densities from about 0.6 to 0.94 of complete, each against a target 15% above its own incumbent.

FIRST: JENSEN IS NEVER THE LOSSY STEP. The bound applies Jensen to the lower convex envelope of \(L(s,\cdot)\), using only the mean of \(q_S\). Across all nine instances the hull vertices of that envelope bracketing the mean are between 0 and 7 apart in \(q\), against values of \(q\) in the hundreds. The envelope is linear at the scale of the mean, so the Jensen-optimal mixture is already concentrated and refinements that add moment information have nothing to bite on. Concretely, at \((32,383)\) the Jensen mixture's second moment agrees with the admissible minimum to a relative \(2 \times 10^{-5}\), and a second-moment dual certificate returns the published value exactly.

SECOND: THE RECURSION IS SCALE-FREE. To lift the final bound by a factor \(\alpha\), one must lift \(\widehat L(s,\cdot)\) by \(\alpha\) at EVERY sample size: across all nine instances the spread of the required factor over all \(s\) never exceeds 0.01. No sample size is better placed than another, so there is no \(s\) to tune toward. The reason is the telescoping identity behind the bound itself: \(\binom{n}{s_1}\binom{s_1}{s_2} / (\binom{n-4}{s_1-4}\binom{s_1-4}{s_2-4}) = \binom{n}{s_2}/\binom{n-4}{s_2-4}\), so an unrounded recursion equals a single-level bound at any intermediate size. Rounding at each level is the entire gain, and at these densities it is worth under 0.1%.

A CEILING ON THE FAMILY. Any bound reading only \((n,q)\) is at most \(\min\{\operatorname{cr}(G)\}\) over that family, and one explicit drawing caps it. A 2-page local search reaches exactly \(Z(32) = 12600\) for \(K_{32}\); deleting 113 edges and re-optimising the pages leaves an explicit 383-edge drawing with 4644 crossings. So \(L(32,383) \le 4644\) for any such bound, the target 3557 is not excluded, and the incumbent -- which is 3022, not the 2988 in circulation -- sits at 65% of the ceiling.

WHAT WAS TRIED AND RETURNS THE INCUMBENT. Second-moment refinement with a dual certificate: exactly zero gain. Adding \(\operatorname{cr}(K_n) \ge 0.8594\,Z(n)\) as a base value, legitimate because at \(q = \binom{n}{2}\) the only graph is \(K_n\): lifts \(L(32,496)\) from 8336 to 10979 and leaves \(L(32,383)\) unchanged, because intermediate density is governed by the local shape of the envelope, which the dense endpoint never reaches. Sample-size tuning: excluded by the scale-freeness above.

CONCLUSION. The sampling family reaches these targets only through a uniformly stronger lower bound on \(\operatorname{cr}(s,q)\) at intermediate density, holding at every \(s\) simultaneously -- roughly 18% at \((32,383)\). That is the open problem behind the frontier; it is not reachable by re-weighting, re-tuning, or adding moments, and the dense-graph literature's strongest results are precisely the information that fails to propagate to intermediate density. Since \((n,q)\)-only bounds are capped at 4644 and every refinement returns 3022, structure beyond the vertex and edge counts is the only remaining lever, and a proof of 3557 would have to use it.

`bound_report.py` returns the incumbent, an explicit ceiling and the required factor for any \((n,q)\), so the next instance can be answered without repeating this.

Repository: notes/crossing-numbers/dense-intermediate-density/."""
cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","finding","--title",TITLE,"--body",BODY,"--outgoing",f"refines:{ref}"]
out=subprocess.run(cmd,capture_output=True,text=True)
print(out.stdout[-350:] or out.stderr[-350:])
