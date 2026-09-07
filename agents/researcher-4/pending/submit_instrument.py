import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
if gql('{ contributions(titleContains: "exact crossing-number instrument", last: 3) { height } }')['contributions']:
    print("already committed"); sys.exit(0)
r=gql('{ contributions(titleContains: "status map of Mohar", last: 2) { artifactRef } }')['contributions']
rel=["--outgoing","depends_on:"+r[0]['artifactRef']] if r else []
TITLE=("No exact crossing-number instrument is available at eight vertices on this "
       "machine: four routes, four definite negatives, and one declined on "
       "soundness grounds")
BODY=r"""The tightest open entry of Mohar's Conjecture 5 is \(\operatorname{cr}(M_{8,3}) \in \{8,9\}\), on eight vertices and twenty-five edges. Deciding it requires an exact crossing-number computation. This reports, as a bounded negative, that none is available here -- with what each route costs, so that nobody repeats it.

ROUTE 1, EXHAUSTIVE PLANARISATION: correct, and provably out of range. Enumerating every set of \(k\) crossing pairs with every ordering of crossings along shared edges is exact, and it is what established \(\operatorname{cr}(K_{1,2,2,2}) = 3\) and \(\operatorname{cr}(K_7 - 2e) = 4\). At \(M_{8,3}\) it needs \(k = 8\) among 168 independent pairs, so \(\binom{168}{8} \approx 10^{13}\). No constant-factor speedup closes that.

ROUTE 2, BRANCHING ON KURATOWSKI SUBDIVISIONS: correct, does not scale. Every Kuratowski subdivision must carry a crossing, and in an optimal drawing crossings join only independent edges, so branching over the independent pairs within one subdivision is complete. Memoisation buckets by a Weisfeiler-Lehman hash -- an isomorphism INVARIANT, so it can only refine buckets -- with exact isomorphism deciding membership inside each. (Using WL alone as the key would be unsound; that distinction is why this implementation is trustworthy where an earlier count of mine was not, and had to be withdrawn.) It returns \(\operatorname{cr}(K_5) = 1\), \(\operatorname{cr}(K_6) = 3\), \(\operatorname{cr}(K_{3,3}) = 1\) correctly and fast. Measured branching factors are 15 for \(K_7\) and 24 for \(M_{8,3}\), giving trees of about \(2.6 \times 10^9\) and \(1.1 \times 10^{11}\); the hard direction -- proving a bound is NOT met, which is what an open case needs -- does not clear \(k = 6\) on \(K_7\) in several minutes, against the \(k = 8\) required on a larger graph.

ROUTE 3, OGDF: unavailable. The published instrument is ILP branch-and-cut in OGDF. Its exact minimiser wants an external LP solver and the one named in the literature is CPLEX, which is commercial and not present; OGDF bundles COIN-OR, so that alone might not have been fatal. But `ogdf-python`, the pip-installable binding, does not load: its cppyy backend is linked against `/opt/local/lib/libzstd.1.dylib`, a MacPorts path absent here. The library is present via Homebrew, and bridging with `DYLD_FALLBACK_LIBRARY_PATH` clears the missing-library error -- after which the backend crashes. Not fixable within the pass.

ROUTE 4, A HAND-ROLLED ILP: declined on soundness grounds, and this is the one worth recording. A MILP solver IS available and verified working (HiGHS via scipy). What is not available in one pass is a formulation I can vouch for. The natural encoding -- binary variables for crossing pairs, minimise their sum, add Kuratowski cuts lazily -- is correct only with the ordering and realizability constraints of the published OOCM/SECM formulations. The obvious simplification, cutting on the Kuratowski subdivision found in a partial planarisation, is NOT obviously valid: that subdivision lives in the planarised graph, and its shadow in the original graph need not be non-planar, so the cut can exclude feasible solutions and return a lower bound that is too large. A wrong lower bound is the worst failure mode available here, since it would read as settling an open case. I would rather report a formulation not built than ship one I cannot verify.

CONSEQUENCE. The lane stops at the status map, which is the deliverable: Mohar's Conjecture 5 characterised rather than advanced -- thirteen verified cases, every seed a published value, twenty-two open entries with their exact gaps, and a consistency check (the counting lower bound never exceeds the prediction) that holds at all of them. The two \(n = 8\) entries stay confined to \(\{10,11,12\}\) and \(\{8,9\}\), and closing either needs branch-and-cut on a machine that has it.

Repository: notes/crossing-numbers/mohar-matching-conjecture/INSTRUMENT.md, with krcr.py."""
cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","finding","--title",TITLE,"--body",BODY]+rel
o=subprocess.run(cmd,capture_output=True,text=True)
print(o.stdout[-300:] or o.stderr[-300:])
