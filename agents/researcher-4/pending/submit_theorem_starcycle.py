import subprocess, sys
sys.path.insert(0, 'scratch')
from q import gql

# relate to the counterexample it upgrades
ref = gql('{ contributions(titleContains: "Chia and Sim", last: 3) '
          '{ height artifactRef } }')['contributions'][0]['artifactRef']

TITLE = ("The skewness of the star-cycle product at n = 3 is exactly m - 2 for "
         "all m, proved: a K_{3,3} minor gives the lower bound and a nesting "
         "drawing gives the upper, upgrading five instances to a theorem")

BODY = r"""This upgrades my counterexample to Chia and Sim's question from five verified instances to a theorem covering the whole \(n = 3\) column.

SETUP. \(K_{1,m} \square C_3\) has \(3(m+1)\) vertices and \(3(2m+1)\) edges. Write \(c_0, c_1, c_2\) for the three copies of the star's centre and \(l_{j,0}, l_{j,1}, l_{j,2}\) for the copies of leaf \(j\). The edges are the centre triangle \(T_0\) on \(c_0c_1c_2\); a leaf triangle \(T_j\) on \(l_{j,0}l_{j,1}l_{j,2}\) for each \(j\); and the rungs \(c_i l_{j,i}\). So the graph is \(m\) triangular prisms glued along the common triangle \(T_0\). Call leaf \(j\) fully attached in a subgraph if all three of its rungs are present.

LEMMA. If three leaves are fully attached in a subgraph \(H\), then \(H\) is non-planar.

Proof. Contract each of the three leaf triangles to a single vertex. Each contracted vertex is adjacent to \(c_0\), \(c_1\) and \(c_2\) by its three rungs, so \(K_{3,3}\) is a minor of \(H\), and \(H\) is non-planar by Wagner's theorem.

The lemma never mentions \(T_0\), and that is not an artefact of the write-up. Let \(L(t)\) be the largest number of fully attached leaves that can coexist planarly after \(t\) edges of \(T_0\) are deleted. Measured, \(L(0) = L(1) = L(2) = L(3) = 2\): deleting the centre triangle buys nothing, because the obstruction was never there. I had conjectured \(L(t) = 2 + t\), which would have made the bound a case analysis; that conjecture is false and its failure is what produced the shorter argument.

THEOREM (lower bound). \(\mathrm{sk}(K_{1,m} \square C_3) \ge m-2\).

Proof. Let \(S\) be an edge set with \(G - S\) planar. By the Lemma at most two leaves are fully attached in \(G - S\), so at least \(m-2\) leaves have lost a rung. Rungs of distinct leaves are distinct edges, so \(|S| \ge m-2\).

THEOREM (upper bound). \(\mathrm{sk}(K_{1,m} \square C_3) \le m-2\).

Proof. Delete the \(m-2\) layer-0 rungs \(c_0 l_{j,0}\) for \(j = 1, \ldots, m-2\), and draw the remainder as follows. Draw \(T_0\) as a triangle. Draw leaf \(m-1\) inside it with all three rungs; the result is a triangular prism whose interior faces include the quadrilateral \(Q\) bounded by \(c_1c_2\), \(c_2 l_{m-1,2}\), \(l_{m-1,2} l_{m-1,1}\) and \(l_{m-1,1} c_1\), and both \(c_1\) and \(c_2\) lie on the boundary of \(Q\). Draw leaf \(m\) outside \(T_0\), symmetrically; it does not meet \(Q\). Each remaining leaf \(j \le m-2\) has lost its layer-0 rung and so attaches only at \(c_1\) and \(c_2\): draw \(T_j\) inside the current face having both \(c_1\) and \(c_2\) on its boundary, with \(l_{j,1}\) towards \(c_1\), \(l_{j,2}\) towards \(c_2\) and \(l_{j,0}\) away, then draw the two rungs. This adds no crossing and leaves a new face bounded by \(c_1c_2\), \(c_2 l_{j,2}\), \(l_{j,2} l_{j,1}\) and \(l_{j,1} c_1\), again with both \(c_1\) and \(c_2\) on its boundary. By induction all \(m-2\) reduced leaves nest side by side along \(c_1c_2\), and the drawing is planar.

Checked as well as argued: the deletion set planarises the graph for every \(m\) from 2 to 20, and at \(m = 30, 50, 80\), the last on 243 vertices and 483 edges.

CONSEQUENCE. \(\mathrm{sk}(K_{1,m} \square C_3) = m-2\) for all \(m \ge 2\). DS21 records Chia and Sim as asking whether \(\mathrm{sk}(K_{1,m} \square C_n) = (m-2)(\lfloor \frac{n-1}{2} \rfloor + 1)\), which at \(n = 3\) gives \(2(m-2)\). The proposed value is therefore too large by a factor of two along the WHOLE \(n = 3\) column, not merely at the five values I first computed.

The identity agrees with every exact value I have at \(n \ge 4\) -- \((m,n) = (3,4), (3,5), (3,6), (4,4), (4,5), (5,4)\) -- so the defect stays localised to \(n = 3\) and the correction is a range condition rather than a new formula.

WHAT I DO NOT CLAIM. Nothing about what Chia and Sim actually asked; reference [209], Discrete Appl. Math. 342 (2024) 295-303, is paywalled and unread. If their question carried a restriction such as \(n \ge 4\), the defect belongs to DS21's rendering rather than to them.

Repository: notes/crossing-numbers/skewness-star-cycle/, files THEOREM.md, RESULT.md, chiasim.py, caseB.py."""

cmd = ["/Users/abuzark/.discovery-research-team/bin/discovery-net", "submit", "contribution",
       "--private-key", "/Users/abuzark/.discovery-research-team/keys/researcher-4.pem",
       "--kind", "lemma", "--title", TITLE, "--body", BODY,
       "--outgoing", f"refines:{ref}"]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout[-700:] or r.stderr[-700:])
