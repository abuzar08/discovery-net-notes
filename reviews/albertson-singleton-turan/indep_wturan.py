r"""reviewer-1: independent audit of the singleton-w Turan sharpening.

Two computations:
  (a) the K_4-free maximum is \(\lfloor n^2/3 \rfloor\) — verified exhaustively
      for \(n \le 9\) with my own \(K_4\) test over nauty's complete generation,
      and against the Turan graph \(T(n,3)\) for the whole range in use;
  (b) the sharpening \(\lfloor n^2/3 \rfloor - (\lfloor (n-1)^2/3 \rfloor + 4)\)
      over the whole range of \(\lvert R\rvert\), including where it turns
      positive.
"""
import subprocess
import sys

sys.path.insert(0, '../r45')
from indep_r45 import graph6, edges, has_clique

GENG = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/scratch/'
        'nauty/nauty2_8_9/geng')


def turan_graph_edges(n, parts=3):
    sizes = [n // parts + (1 if i < n % parts else 0) for i in range(parts)]
    return (n * n - sum(s * s for s in sizes)) // 2


def exhaustive_max(n):
    """largest edge count of a K_4-free graph on n vertices, over all graphs"""
    best = 0
    p = subprocess.run([GENG, '-q', str(n)], capture_output=True, text=True)
    for line in p.stdout.splitlines():
        if not line.strip():
            continue
        m, adj = graph6(line)
        e = edges(m, adj)
        if e > best and not has_clique(m, adj, 4):
            best = e
    return best


def main():
    print('(a) the K_4-free maximum, my own exhaustive check')
    for n in range(4, 10):
        ex = exhaustive_max(n)
        print(f'    n = {n}: exhaustive maximum {ex}, floor(n^2/3) = '
              f'{n*n//3}, T(n,3) has {turan_graph_edges(n)} edges -> '
              f'{"agree" if ex == n*n//3 == turan_graph_edges(n) else "DIFFER"}')
    print('    for the range in use the construction side is checked directly:')
    bad = [n for n in range(10, 60) if turan_graph_edges(n) != n * n // 3]
    print(f'      T(n,3) has exactly floor(n^2/3) edges for every '
          f'10 <= n <= 59: {"yes" if not bad else bad}')
    print()
    print('(b) the sharpening, over the whole range')
    print('    |R|  old floor(|R|^2/3)  new floor((|R|-1)^2/3)+4  gain')
    for R in list(range(5, 12)) + [16, 21, 26, 32]:
        old, new = R * R // 3, (R - 1) * (R - 1) // 3 + 4
        print(f'    {R:3d} {old:18d} {new:24d} {old-new:6d}')
    pos = [R for R in range(2, 60) if R * R // 3 - ((R - 1) ** 2 // 3 + 4) > 0]
    print(f'    strictly stronger from |R| = {min(pos)} upward; the class uses '
          f'|R| >= 11, where the gain is '
          f'{11*11//3 - (10*10//3 + 4)}, rising to '
          f'{32*32//3 - (31*31//3 + 4)} at |R| = 32')
    print()
    print('(c) the configuration that exposed it: |R| = 21, e(H[R]) = 142')
    print(f'    old cap {21*21//3}, new cap {20*20//3 + 4}; deleting w leaves '
          f'{142-4} edges on 20 vertices against a K_4-free maximum of '
          f'{20*20//3} -> {"a K_4 is forced" if 142-4 > 20*20//3 else "no contradiction"}')


if __name__ == '__main__':
    main()
