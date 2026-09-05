#!/bin/bash
# reviewer-1: re-solve a --symf type from scratch and time it (checks the "1 to 16 s" claim)
cd "$(dirname "$0")"; H=$(pwd); T=$H/target; TOOLS=$H/../r46/tools
n=$1; f=$2; k=$3; tag="ts_n${n}_f${f}_k${k}"
cd work
python3 "$T/encode.py" "$n" 4 6 "$f" 5 "$k" "$tag.cnf" --symf > /dev/null
s=$(date +%s%N)
timeout 1500 "$TOOLS/cadical/build/cadical" -q --binary=false "$tag.cnf" "$tag.drat" > "$tag.cad" 2>&1
rc=$?; e=$(( ($(date +%s%N) - s)/1000000 ))
echo "n=$n 1^$f 5^$k: rc=$rc solve ${e} ms $(grep -a '^s ' "$tag.cad" | head -1)"
rm -f "$tag.drat" "$tag.cnf" "$tag.cad"
