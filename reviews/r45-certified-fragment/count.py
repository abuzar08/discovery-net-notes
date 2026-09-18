import sys
sys.path.insert(0, '../r45')
from indep_r45 import graph6, has_clique, has_independent
mode = sys.argv[1]
n = int(sys.argv[2])
cnt = tot = 0
for line in sys.stdin:
    if not line.strip():
        continue
    tot += 1
    m, adj = graph6(line)
    if mode == '35':                      # triangle-free, no independent 5-set
        if has_independent(m, adj, 5):
            continue
    else:                                 # K_4-free, no independent 4-set
        if has_clique(m, adj, 4) or has_independent(m, adj, 4):
            continue
    cnt += 1
print(f'{mode} at n={n}: scanned {tot}, count {cnt}')
