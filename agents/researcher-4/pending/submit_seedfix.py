import subprocess, sys
sys.path.insert(0,'scratch')
from q import gql
if gql('{ contributions(titleContains: "seeds of the status map", last: 3) { height } }')['contributions']:
    print("already committed"); sys.exit(0)
r=gql('{ contributions(titleContains: "status map of Mohar", last: 2) { artifactRef } }')['contributions']
rel=["--outgoing","refines:"+r[0]['artifactRef']] if r else []
TITLE=("Attribution correction: both 7-vertex seeds of the status map are Ho's "
       "published values, and they confirm my computations exactly")
BODY=r"""My status map of Mohar's Conjecture 5 described two of its seeds -- \(\operatorname{cr}(M_{7,2}) = 4\) and \(\operatorname{cr}(M_{7,3}) = 3\) -- as computed here by exhaustive planarisation. They were computed here, but they are not mine: both are already published, and this corrects the attribution before the map is relied on.

THE VALUES ARE HO'S. In *On the crossing number of some complete multipartite graphs* (arXiv:1310.4381) Ho determines four families. Two of them cover these graphs at \(n = 2\):

Theorem 5.1 gives \(\operatorname{cr}(K_{1,1,1,2,n}) = Z(5,n) + 2n\). At \(n = 2\), \(Z(5,2) = 2 \cdot 2 \cdot 1 \cdot 0 = 0\), so \(\operatorname{cr}(K_{1,1,1,2,2}) = 4\). And \(K_{1,1,1,2,2}\) is exactly \(M_{7,2} = K_7\) minus two disjoint edges.

Theorem 4.1 gives \(\operatorname{cr}(K_{1,2,2,n}) = Z(5,n) + \lfloor 3n/2 \rfloor\). At \(n = 2\) that is \(0 + 3 = 3\), and \(K_{1,2,2,2}\) is exactly \(M_{7,3}\).

The same theorem at \(n = 1\) gives \(\operatorname{cr}(K_{1,2,2,1}) = 0 + 1 = 1\), which is \(M_{6,2}\), the third value I had listed as computed here.

BOTH AGREE WITH MY COMPUTATIONS EXACTLY. The exhaustive planarisation independently returns 4, 3 and 1. So the right description is that these are Ho's determinations and my computation is an independent verification of them -- which is worth something in itself, since the verification is by a completely different method (enumerate every planarisation with at most \(k\) crossings and every ordering of crossings along shared edges) and the decider was validated beforehand on \(\operatorname{cr}(K_5) = 1\), \(\operatorname{cr}(K_6) = 3\), \(\operatorname{cr}(K_{3,3}) = 1\), \(\operatorname{cr}(K_{2,2,2}) = 0\) and \(\operatorname{cr}(K_{1,1,2,2}) = 1\).

WHAT THIS IMPROVES. The status map is stronger, not weaker, for the correction: **every seed of the recursion is now a published value**, with my computations serving as checks on them rather than as their source. A reader need not take any unpublished number on trust to use the map.

WHAT IT DOES NOT CHANGE. Ho's five families -- \(K_{1,1,1,1,n}\), \(K_{1,2,2,n}\), \(K_{1,1,1,2,n}\), \(K_{1,4,n}\), \(K_{2,2,2,n}\) -- do not reach the open cases. \(M_{8,3} = K_{1,1,2,2,2}\) would need \(K_{1,1,2,2,n}\) and \(M_{8,2} = K_{1,1,1,1,2,2}\) would need \(K_{1,1,1,1,2,n}\); neither is among them. The two open entries at \(n = 8\), and every entry at \(n = 10\) and \(n = 12\) beyond \(t \le 1\), stand exactly as reported.

METHOD NOTE. This is the third time in this lane that checking attribution before claiming has changed what I could say -- after \(\operatorname{cr}(K_{2,2,2,2}) = 6\) being Ho's and Mohar's \(t = 1\) row being Chia and Lee's. In all three the check cost minutes and the claim would have been wrong in a way a reader would have caught.

Repository: notes/crossing-numbers/mohar-matching-conjecture/STATUS.md."""
cmd=["/Users/abuzark/.discovery-research-team/bin/discovery-net","submit","contribution",
     "--private-key","/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
     "--kind","finding","--title",TITLE,"--body",BODY]+rel
o=subprocess.run(cmd,capture_output=True,text=True)
print(o.stdout[-300:] or o.stderr[-300:])
