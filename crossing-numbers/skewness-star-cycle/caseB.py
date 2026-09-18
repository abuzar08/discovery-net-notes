"""Closing the remaining case of sk(K_{1,m} box C_3) = m-2.

Case A is proved: if the planarising set avoids E(T_0), the centre triangle
survives and at most TWO leaves can keep all three rungs, so at least m-2 leaves
lose one.

Case B is what is left: the set may delete edges of T_0 itself.  The hypothesis
that would close it uniformly is

    L(t) = 2 + t,

where L(t) is the largest number of fully-attached leaves that can coexist
planarly once t edges of T_0 have been deleted.  If true, spending t edges on
T_0 buys exactly t extra fully-attached leaves, so the total is

    t + (m - L(t)) = t + m - 2 - t = m - 2

for every t, and the bound is uniform across all cases.

L(t) is computed here directly: build T_0 minus t edges, attach L leaves with
all three rungs each, and test planarity.
"""
import sys, networkx as nx

def build(t, L):
    """T_0 minus t edges, with L fully attached leaf triangles."""
    G = nx.Graph()
    T0 = [(('c',0),('c',1)), (('c',1),('c',2)), (('c',2),('c',0))]
    for e in T0[t:]:
        G.add_edge(*e)
    for i in range(3):
        G.add_node(('c', i))
    for j in range(L):
        for i in range(3):
            G.add_edge((('l',j),i), (('l',j),(i+1) % 3))   # leaf triangle
            G.add_edge((('l',j),i), ('c', i))              # rung
    return G

def planar(G):
    return nx.check_planarity(G, counterexample=False)[0]

def L_max(t, cap=12):
    last = 0
    for L in range(1, cap+1):
        if planar(build(t, L)):
            last = L
        else:
            return last
    return last

if __name__ == "__main__":
    print("L(t) = largest number of fully-attached leaves that stay planar")
    print("after deleting t edges of the centre triangle T_0\n")
    print(f"{'t':>2} {'L(t)':>5} {'2+t':>5}  hypothesis")
    ok = True
    for t in range(0, 4):
        L = L_max(t)
        good = (L == 2 + t)
        ok &= good
        print(f"{t:>2} {L:>5} {2+t:>5}  {'holds' if good else '*** FAILS ***'}")
    print()
    print("HYPOTHESIS", "HOLDS for t = 0,1,2,3" if ok else "FAILS")
    if ok:
        print("=> spending t edges on T_0 buys exactly t extra leaves,")
        print("   so any planarising set costs t + (m - (2+t)) = m - 2, for every t.")
