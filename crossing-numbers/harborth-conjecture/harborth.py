"""Harborth's tripartite bound A(n1,n2,n3), and the gate it must pass.

A is taken verbatim from Gethner, Hogben, Lidicky, Pfender, Ruiz and Young
(arXiv:1410.0720), who state cr(K_{n1,n2,n3}) <= A(n1,n2,n3) and note that A
agrees in value with Harborth's function.  Harborth's conjecture is that
equality holds.

GATE: before spending any compute searching for a counterexample, A must
reproduce every tripartite value DS21 records as PROVED.  If it does not, I have
the wrong function and any "refutation" would be an artifact.
"""
def X(n): return (n//2)*((n-1)//2)
def Z(m,n): return X(m)*X(n)

def A(a, b, c):
    ns = (a, b, c)
    tot = 0
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        tot += Z(ns[j], ns[k]) + X(ns[i]) * ((ns[j]*ns[k])//2)
    return tot

if __name__ == "__main__":
    checks, bad = [], 0
    for n in range(1, 13):
        checks.append((f"K_(1,3,{n})", A(1,3,n), Z(4,n) + n//2))
        checks.append((f"K_(2,3,{n})", A(2,3,n), Z(5,n) + n))
        checks.append((f"K_(1,4,{n})", A(1,4,n), n*(n-1)))
        checks.append((f"K_(2,4,{n})", A(2,4,n), Z(6,n) + 2*n))
        checks.append((f"K_(3,3,{n})*", A(3,3,n), Z(6,n) + 2*n + 2*(n//2) + 1))
    for m in range(1, 11):
        for n in range(m, 11):
            checks.append((f"K_(1,{m},{n})*", A(1,m,n), Z(m+1,n+1) - (m//2)*(n//2)))
    print(f"{'graph':>14} {'A':>7} {'DS21':>7}  ok    (* = conditional)")
    for name, a, d in checks:
        ok = a == d
        bad += not ok
        if not ok or name.endswith("3)*") or "1,3," in name:
            print(f"{name:>14} {a:>7} {d:>7}  {'OK' if ok else 'MISMATCH'}")
    print(f"\ntotal checks {len(checks)}, mismatches {bad}")
