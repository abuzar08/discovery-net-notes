#!/bin/bash
# n = 13 census, sharded BY EDGE RANGE so the cheap prefix can run while the
# expensive range awaits a decision. m <= 24 is 141,284,276 graphs (~5 core-hours);
# m in [25,26] is 3,319,303,520 (~119 core-hours). Their union is the full natural
# scope m <= 2n = 26. Single fixed modulus within each range.
B="/Users/abuzark/.discovery-research-team/workspaces/researcher-4/scratch"
RANGE=$1; MOD=$2; RES=$3; OUT="$B/$4"
"$B/tools/nauty2_9_1/geng" -C -d3 -q 13 $RANGE $RES/$MOD \
  | "$B/tools/nauty2_9_1/crit2_r4" > "$OUT" 2>"$OUT.err"
echo "range $RANGE shard $RES/$MOD: $(grep -c CRIT2 "$OUT") CRIT2, $(grep -c CRIT_GE3 "$OUT") CRIT_GE3"
tail -1 "$OUT.err"
