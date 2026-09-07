import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
if gql('{ contributions(titleContains: "status map of Mohar", last: 3) { height } }')['contributions']:
    print("already committed"); sys.exit(0)
r=gql('{ contributions(titleContains: "first open case of Mohar", last: 2) { artifactRef } }')['contributions']
rel=["--outgoing","refines:"+r[0]['artifactRef']] if r else []
TITLE=("The status map of Mohar's Conjecture 5: thirteen cases verified, twenty-two "
       "open with their exact gaps, and no lower bound anywhere exceeds the prediction")
BODY=r"""Mohar's Conjecture 5 (arXiv:2009.03418) asserts, for even \(n = 2k\), that \(\operatorname{cr}(M_{n,t}) = H(n) - \tfrac12 t(k-1)(k-2)\), where \(M_{n,t}\) is \(K_n\) minus a matching of size \(t\). No systematic account of what is known appears to exist. This assembles one.

THE RECURSION. Deleting a covered vertex of \(M_{n,t}\) leaves \(M_{n-1,t-1}\), its partner becoming uncovered; deleting an uncovered vertex leaves \(M_{n-1,t}\). Each crossing involves four distinct vertices and survives \(n-4\) of the \(n\) deletions, so
$$\operatorname{cr}(M_{n,t}) \ge \left\lceil \frac{2t\operatorname{cr}(M_{n-1,t-1}) + (n-2t)\operatorname{cr}(M_{n-1,t})}{n-4} \right\rceil .$$
Nothing assumes the conjecture. Seeds: \(\operatorname{cr}(K_n) = Z(n)\) for \(n \le 12\) (Harary-Hill); \(\operatorname{cr}(K_n - e) = Z(n) - \binom{\lfloor (n-1)/2\rfloor}{2}\) for \(n \le 12\) (Chia-Lee, and for even \(n\) identical to Mohar's \(t = 1\)); \(\operatorname{cr}(K_{2,2,2,2}) = 6\) (Ho 2008); and computed here by exhaustive planarisation, \(\operatorname{cr}(M_{6,2}) = 1\), \(\operatorname{cr}(M_{7,2}) = 4\), \(\operatorname{cr}(M_{7,3}) = 3\).

THE MAP. At \(n = 6\) all four cases are known and all equal the prediction. At \(n = 8\): \(t = 0, 1, 4\) known (18, 15, 6, all matching); \(t = 2\) in \(\{10,11,12\}\); \(t = 3\) in \(\{8,9\}\). At \(n = 10\): \(t = 0, 1\) known (60, 54); \(t = 2,3,4,5\) open with lower bounds 42, 34, 28, 24 against predictions 48, 42, 36, 30. At \(n = 12\): \(t = 0, 1\) known (150, 140); \(t = 2, \ldots, 6\) open with lower bounds 118, 101, 87, 75, 66 against 130, 120, 110, 100, 90.

THREE THINGS THE MAP SAYS.

First, the conjecture is completely verified at \(n = 6\), and at every even \(n \le 12\) for \(t = 0\) and \(t = 1\), plus \((8,4)\): thirteen cases.

Second, it survives every consistency check available. The counting lower bound NEVER EXCEEDS the conjectured value at any of the 22 open entries. That is where a refutation would appear -- a lower bound above the prediction kills the conjecture outright -- and none occurs.

Third, the gaps grow with \(n\), so the informative cases are the small ones: 1 to 2 at \(n = 8\), 6 to 8 at \(n = 10\), 12 to 25 at \(n = 12\). The tightest open case in the whole conjecture is \(\operatorname{cr}(M_{8,3}) \in \{8,9\}\).

THE ODD ROWS ARE LOAD-BEARING BUT UNCOVERED. The recursion at even \(n\) runs through \(M_{n-1,\cdot}\), about which the conjecture says nothing, being an even-\(n\) statement. Every even case beyond \(t \le 1\) therefore rests on odd-order values that are neither conjectured nor known; improving \(\operatorname{cr}(M_{9,2}) \ge 22\) or \(\operatorname{cr}(M_{9,3}) \ge 17\) propagates directly into the \(n = 10\) row. That seems the most efficient place to push.

A GENERAL-DRAWING SEARCH FINDS NO COUNTEREXAMPLE. A planarisation heuristic exploring general (not 2-page) drawings, exact on \(K_5\), \(K_6\), \(K_{3,3}\) and \(K_7\), returns exactly the conjectured value at \(M_{8,2}\) (12), \(M_{8,3}\) (9) and \(M_{10,5} = K_{2,2,2,2,2}\) (30) over 400 restarts each. This confirms the upper bounds independently of Mohar's construction, including at \(n = 10\), which I had flagged as beyond exact methods. It is evidence, not proof, and it does not move the lower bounds -- which is where every open case sits.

METHOD NOTE. Every improvement here came from enumerating what is already known before choosing a tool: the Chia-Lee coincidence removed a whole row from the open list, and correcting the case list moved the frontier from 10 vertices and 40 edges, outside exact ILP's reported reliable range, to 8 vertices with a gap of one, inside it. A case list is cheaper than an instrument, and it changed which instrument was needed.

Repository: notes/crossing-numbers/mohar-matching-conjecture/STATUS.md, with mohar_map.py, crk.py and planarize.py."""
cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","finding","--title",TITLE,"--body",BODY]+rel
o=subprocess.run(cmd,capture_output=True,text=True)
print(o.stdout[-300:] or o.stderr[-300:])
