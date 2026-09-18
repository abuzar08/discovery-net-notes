#!/bin/zsh
G=/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/scratch/nauty/nauty2_8_9/geng
cd /Users/abuzark/.discovery-research-team/workspaces/reviewer-1/scratch/ham4
for r in 0 32 64 96 128 160 192 224 256 288 320 352 384 416 448 480; do
  ( $G -d4 11 22:30 $r/512 2>/dev/null | uv run --quiet --with networkx python3 indep_ham4.py 11 > s11_$r.out 2>&1 ) &
  while [ $(jobs -r | wc -l) -ge 6 ]; do sleep 2; done
done
wait
echo SPREAD_DONE
