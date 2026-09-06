#!/bin/bash
# End-to-end acceptance test of the exact n=12 pipeline, at n=10 where the
# published census gives the answer.
#
# geng -C is BIconnected, not 3-connected, so the target is the 2-connected
# members: the n=10 census splits by vertex connectivity as {0:1, 1:2, 2:6, 3:23},
# so 29 of its 32 members are 2-connected.  The pipeline must find exactly those
# 29, and none with cr >= 3.
B="/Users/abuzark/.discovery-research-team/workspaces/researcher-4/scratch"
"$B/tools/nauty2_9_1/geng" -C -d3 -q 10 15:26 \
  | "$B/tools/nauty2_9_1/crit2_r4" > "$B/n10val.txt" 2>"$B/n10val.err"
echo "read: $(grep -oE 'read [0-9]+ graphs' "$B/n10val.err")"
echo "found $(grep -c CRIT2 "$B/n10val.txt") CRIT2 and $(grep -c CRIT_GE3 "$B/n10val.txt") CRIT_GE3"
echo "expected 29 CRIT2 and 0 CRIT_GE3"
if [ "$(grep -c CRIT2 "$B/n10val.txt")" -eq 29 ] && [ "$(grep -c CRIT_GE3 "$B/n10val.txt")" -eq 0 ]; then
  echo "PIPELINE VALIDATION: PASS"
else
  echo "PIPELINE VALIDATION: FAIL"
fi
