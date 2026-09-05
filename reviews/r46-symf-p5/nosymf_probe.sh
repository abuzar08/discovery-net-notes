#!/bin/bash
# reviewer-1: same type WITHOUT --symf, to check the claim that it did not finish before
cd "$(dirname "$0")"; H=$(pwd); T=$H/target; TOOLS=$H/../r46/tools
n=$1; f=$2; k=$3; cap=${4:-600}; tag="ns_n${n}_f${f}_k${k}"
cd work
python3 "$T/encode.py" "$n" 4 6 "$f" 5 "$k" "$tag.cnf" > /dev/null
s=$(date +%s)
timeout "$cap" "$TOOLS/cadical/build/cadical" -q --binary=false "$tag.cnf" "$tag.drat" > "$tag.cad" 2>&1
rc=$?; e=$(( $(date +%s) - s ))
echo "no-symf n=$n 1^$f 5^$k: rc=$rc after ${e}s $(grep -a '^s ' "$tag.cad" | head -1) DRAT $(( $(stat -f%z "$tag.drat" 2>/dev/null || echo 0)/1048576 ))MB"
rm -f "$tag.drat" "$tag.cnf" "$tag.cad"
