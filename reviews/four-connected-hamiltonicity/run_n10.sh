#!/bin/zsh
G=/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/scratch/nauty/nauty2_8_9/geng
cd /Users/abuzark/.discovery-research-team/workspaces/reviewer-1/scratch/ham4
for r in 0 1 2 3 4 5; do
  ( $G -d4 10 20:27 $r/6 2>/dev/null | uv run --quiet --with networkx python3 indep_ham4.py 10 > n10_$r.out 2>&1 ) &
done
wait
echo "ALL SHARDS DONE"
grep -h "^n = 10" n10_*.out
python3 - <<'PY'
import glob, re
tot=c4=nh=0; surv=[]
for f in sorted(glob.glob('n10_*.out')):
    for l in open(f):
        m=re.match(r'n = 10: read (\d+), 4-connected (\d+), 4-connected and non-Hamiltonian (\d+)', l)
        if m:
            tot+=int(m.group(1)); c4+=int(m.group(2)); nh+=int(m.group(3))
        elif l.strip().startswith('I'):
            surv.append(l.strip())
print('AGGREGATE n=10: read %d (acceptance criterion 705929: %s), 4-connected %d, 4-connected non-Hamiltonian %d, survivor lines %d'
      % (tot, 'PASS' if tot==705929 else 'FAIL', c4, nh, len(surv)))
bad=[s for s in surv if 'skewness >= 4: True' not in s]
print('survivors NOT excluded by skewness >= 4:', len(bad))
for s in bad[:10]: print('   ', s)
open('n10_survivors.txt','w').write('\n'.join(surv)+'\n')
PY
