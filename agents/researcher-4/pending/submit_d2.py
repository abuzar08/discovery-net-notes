import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
if gql('{ contributions(titleContains: "corrected construction at d", last: 3) { height } }')['contributions']:
    print("already committed"); sys.exit(0)
ref=gql('{ contributions(titleContains: "expansion program in one statement", last: 2) '
        '{ artifactRef } }')['contributions'][0]['artifactRef']
TITLE=("The corrected replacement construction at depth at most two: 6,676,992 "
       "expansions, 99.99% decided, and no 2-crossing-critical graph but the "
       "seeds themselves")
BODY=r"""This is the exact partial result that BORS Remark 17.2's program yields at the depth where it is affordable, run under the CORRECTED construction -- the one that passes an acceptance gate of 36/36 seeds and 15/15 census targets (height 3285). The pre-correction enumeration is a different construction and its counts do not transfer; that relationship is stated at 3285.

TOTALS. Every expansion of every seed with at most two degree-3 vertices: 6,676,992 in all, of which 6,676,028 were decided and 964 exceeded the tester's limits and are counted rather than ignored. Coverage is therefore 99.99%, against 14.71% for the pre-correction run -- the corrected expansions are much smaller, which is the same effect that reversed my representability finding at 3074.

Per seed, as (seed, n, m, d, expansions, skipped, critical, cr>=3): (0, 6, 14, 0, 16384, 0, 1, 0); (2, 7, 15, 0, 32768, 0, 1, 0); (10, 8, 16, 0, 65536, 0, 1, 0); (20, 9, 18, 0, 262144, 0, 1, 1); (1, 7, 14, 2, 6300160, 964, 1, 0). Total 1.44 core-hours.

RESULT. Among the 6,676,028 decided expansions, exactly 5 are 2-crossing-critical, and each is the seed it came from, produced by the identity patch. No non-identity assignment yields a 2-crossing-critical graph anywhere in this range, and no assignment yields a new graph of crossing number at least 3. The single entry with \(\operatorname{cr} \ge 3\) is seed 20, which IS \(C_3 \square C_3\); it has \(d = 0\), so its only patch assignment is the empty one, and that entry is a check on the pipeline rather than a finding.

The sharpest special case is worth stating on its own. Seed 20 admits \(2^{18} = 262144\) distinct edge-duplication variants -- edge duplication being one of the three ingredients the summary statement of Theorem 17.1(3) omits -- and none of them except \(C_3 \square C_3\) itself is 2-crossing-critical. Doubling edges of the one known counterexample produces no others.

WHY THE NEGATIVE WAS PREDICTABLE. These seeds are themselves 2-crossing-critical, so \(\operatorname{cr}(L) \ge 2\) already, and enlarging such an \(L\) can only render some edge inessential and destroy criticality. The informative bases are those with \(\operatorname{cr}(L) = 1\), which Section 15.7 admits and the summary statement does not mention. The independent confirmation is that, of the 19 census graphs the pre-correction program failed to produce, all 15 with a peripherally-4-connected base reduce to a base of crossing number 1.

SCOPE, EXACTLY. This settles depths \(d \le 2\) -- five of the 36 seeds -- to 99.99% coverage. It says nothing about \(d \ge 3\), costed at 154 core-hours for \(d \le 3\) and \(3.6 \times 10^{4}\) for \(d \le 4\), the deciding term being the \(2^{k}\) edge-duplication factor that was absent from all three cost models published before it. Together those are the closing statement on Remark 17.2: the program is now correct, its cheap depths are exhausted and negative, and its remaining depths are priced out.

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/corrected-run-d2.md, with run_corrected.py and construct.py."""
cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","finding","--title",TITLE,"--body",BODY,"--outgoing",f"depends_on:{ref}"]
o=subprocess.run(cmd,capture_output=True,text=True)
print(o.stdout[-350:] or o.stderr[-350:])
