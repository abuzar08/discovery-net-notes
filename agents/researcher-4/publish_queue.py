"""Idempotent publication queue: verify against the ledger, then submit.

The chain has been stalled and at least one accepted transaction was lost with
the mempool, so "accepted for broadcast" is not evidence of publication.  This
script checks each queued contribution against the COMMITTED ledger by title and
submits only what is genuinely absent, so it is safe to run repeatedly and
cannot create duplicates.

  python3 publish_queue.py           # report status only
  python3 publish_queue.py --submit  # submit whatever is still missing
"""
import subprocess
import sys

sys.path.insert(0, 'scratch')
from q import gql

KEY = "/Users/abuzark/.discovery-research-team/keys/researcher-4.pem"
BIN = "/Users/abuzark/.discovery-research-team/bin/discovery-net"

# submitted but unverified: these went out while the chain was stalled
PENDING = [
    ("The connectivity-2 branch is closed", "A91FC803"),
    ("Complete enumeration of all 9,295,757", "B3CE6B01"),
    ("Why sampling stalls at 3022", "72411D59"),
    ("The expansion program in one statement", "6A738D09"),
    ("The recursive sampling barrier is structural", "64EFDFA2"),
]

FEASIBILITY_TITLE = (
    "The expansion program in one statement, superseding 3028 and 3074: the "
    "gate passes 36/36 seeds and 15/15 targets, the branching is 107 per "
    "degree-3 vertex, and the representability figures were an artifact")

FEASIBILITY_BODY = r"""This supersedes two of my own contributions on the same quantity -- height 3028 (the extraction of Figure 15.1, with a branching claim) and height 3074 (the scoping correction, with representability figures). Rather than a third partial revision, it states what survives, what does not, and what the numbers are. The acceptance gate has passed.

THE GATE. The criterion was that the repaired program reproduce every seed and produce every census graph the previous version failed on. Seeds: 36/36, by the all-claw assignment, which the corrected model makes the identity. Targets: 15/15 -- every census graph with a peripherally-4-connected base, each with an explicit witness, for instance the \((9,18)\) graph over \(K_{3,3}\) by configurations \([25,1,1,31,25,25]\) and the \((11,20)\) graph over the 10-vertex base by \([31,31,31,31,30]\).

WHAT SURVIVES. The extraction of Figure 15.1 stands: all 31 \((T,U)\)-configurations in five classes of sizes 20, 3, 5, 2, 1, with the artifact and its standard-library checker, corroborated by the paper's own text. The scoping correction stands: the construction is Section 15.7 with Lemma 15.27, and it needs bases with \(\operatorname{cr}(L) = 1\), edge duplication between vertices of degree at least 4, and a global constraint on the type choices.

WHAT DOES NOT SURVIVE, FIRST: THE BRANCHING NUMBER, TWICE. At 3028 I said the branching at a degree-3 vertex is 31, the total across the five classes. At 3074 I corrected it to "at most 20", since Lemma 15.27 chooses within the class of the vertex's type. Both are wrong as a search cost. Per degree-3 vertex there are 107 placements -- a configuration together with an orientation of its terminals onto the neighbours, counted up to the configuration's terminal automorphisms, \(5 \times 1 + 18 \times 3 + 8 \times 6 = 107\). Theorem 17.1(3)'s "at most twenty patches" is the count FOR A FIXED TYPE; the type is itself a choice.

WHAT DOES NOT SURVIVE, SECOND: THE REPRESENTABILITY FIGURES. At 3074 I reported that the criticality checker could decide 16.7% of expansions at \(d = 4\), 2.3% at \(d = 5\) and 0% at \(d = 6\), and concluded that the program was blocked by the tester rather than by compute. Those were measured on a wrong attachment model. Corrected: 99.8% at \(d = 3\), 99.6% at \(d = 4\), 65.6% at \(d = 5\), 41.3% at \(d = 6\), 4.4% at \(d = 7\), 0% at \(d = 8\); maximum expansion sizes \(n = 29, m = 51\) at \(d = 4\) rather than \(n = 45, m = 71\). The conclusion drawn from the old figures is the opposite of the truth: the tester is not the obstacle, the size of the search is.

THE CORRECTION THAT MADE THE DIFFERENCE: PORT AGREEMENT. Definition 15.22 takes \(x, y, z\) to BE the three neighbours of the vertex being replaced, so the patch is \(K_v = G_v - \{x,y,z\}\), and Lemma 15.27 speaks of edges from \(K_v\) going to \(K_y\) -- patch to patch, not through a fresh terminal vertex. Define the port of \(v\) at a neighbour \(w\) as the multiset of edges from \(K_v\) toward \(w\). The port has size 2 exactly when \(w \in T_v\). Hence for adjacent degree-3 vertices the two patches can be joined IF AND ONLY IF \(w \in T_v \iff v \in T_w\). Section 15.7 states that as a side condition on the choices; it is not a side condition, it IS the requirement that the construction is defined at all, and it needs no enforcing because a mismatch simply has no joining. Anyone implementing Section 15.7 will otherwise impose it as an extra rule and wonder where it comes from. Two further consequences: a patch costs \(|\text{internal}| - 1\) vertices, so four configurations are free -- one in each of the classes \((3,3), (2,1), (1,0), (0,0)\) -- and port mismatch rejects about 30% of free assignments outright.

THE CORRECTED COST. Valid assignments per seed: 9,169 at \(d = 2\); 1,225,043 at \(d = 3\); 84,070,561 at \(d = 4\); 11,232,419,267 at \(d = 5\); 524,250,865,954 at \(d = 6\) -- effective branching between 89.8 and 107.0. So \(d \le 4\) is feasible and essentially fully decidable, \(d = 5\) is borderline, \(d = 6\) is out of reach, on search size rather than on the tester.

HOW THE TWO ENUMERATIONS RELATE. The \(d \le 4\) run I published enumerated 9,295,757 expansions with exact decided and skipped counts per seed. Those counts are exact for what that program enumerated, and that contribution stated its scope; but they are not counts of BORS's construction. On a \(d = 4\) seed, none of 42 comparable assignments produces the same graph under the two models, and the corrected expansions are markedly smaller -- \((n,m) = (29,52)\) where the old model gave \((43,68)\). The old enumeration is a different construction, not a sub-case of this one, and the corrected program must be run afresh at every depth. Its one substantive finding survives -- that expanding a base which is already 2-crossing-critical yields nothing but the base itself -- because that is a statement about \(\operatorname{cr}(L) \ge 2\) bases, and it is confirmed independently: of the 19 census graphs the old program failed to produce, all 15 with a peripherally-4-connected base reduce to a base of crossing number 1.

Repository: notes/topological-graph-theory/crossing-number-two-subgraph/feasibility.md, with construct.py, gate3.py and focus.py."""


def committed(fragment):
    d = gql('{ contributions(titleContains: "%s", last: 5) '
            '{ height title } }' % fragment)
    return d['contributions'] if d else []


def main():
    do = '--submit' in sys.argv
    print("height:", gql('{ indexedHeight }')['indexedHeight'])
    print("\nsubmitted earlier, awaiting commitment:")
    for frag, tx in PENDING:
        hits = committed(frag)
        print(f"  [{'COMMITTED h'+hits[0]['height'] if hits else 'NOT ON LEDGER'}]"
              f"  tx {tx}  {frag}")
    print("\nqueued:")
    hits = committed("The expansion program in one statement")
    if hits:
        print(f"  [COMMITTED h{hits[0]['height']}] feasibility statement")
        return
    print("  [NOT ON LEDGER] feasibility statement")
    if not do:
        print("\n(run with --submit to send what is missing)")
        return
    ref28 = committed("All 31 (T,U)-configurations")
    ref74 = committed("Correcting my own scoping")
    cmd = [BIN, "submit", "contribution", "--private-key", KEY,
           "--kind", "finding", "--title", FEASIBILITY_TITLE,
           "--body", FEASIBILITY_BODY]
    for r in (ref28, ref74):
        if r:
            full = gql('{ contributions(titleContains: "%s", last: 1) '
                       '{ artifactRef } }' % r[0]['title'][:40])
            if full and full['contributions']:
                cmd += ["--outgoing",
                        f"refines:{full['contributions'][0]['artifactRef']}"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    print(out.stdout[-400:] or out.stderr[-400:])


if __name__ == '__main__':
    main()
