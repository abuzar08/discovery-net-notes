#!/bin/bash
# reviewer-1: does --symf reach the high-f p = 7 types that h2717 never tried?
# usage: p7_probe.sh n f k cap_seconds
cd "$(dirname "$0")"; H=$(pwd); T=$H/target; TOOLS=$H/../r46/tools
n=$1; f=$2; k=$3; cap=${4:-1200}; tag="p7_n${n}_f${f}_k${k}"
cd work
echo "=== $tag cap ${cap}s $(date '+%H:%M:%S')"
python3 "$T/encode.py" "$n" 4 6 "$f" 7 "$k" "$tag.cnf" --symf
python3 "$H/indep_symf.py" "$n" 4 6 "$f" 7 "$k" "$tag.cnf" 1000
s=$(date +%s)
timeout "$cap" "$TOOLS/cadical/build/cadical" -q --binary=false "$tag.cnf" "$tag.drat" > "$tag.cad" 2>&1
rc=$?; e=$(( $(date +%s) - s ))
echo "cadical rc=$rc after ${e}s: $(grep -a '^s ' "$tag.cad" | head -1)"
if [ $rc -eq 20 ]; then
  s=$(date +%s)
  "$TOOLS/drat-trim/drat-trim" "$tag.cnf" "$tag.drat" -L "$tag.lrat" > "$tag.dt" 2>&1
  echo "drat-trim after $(( $(date +%s) - s ))s: $(grep -a -o 's VERIFIED' "$tag.dt" | head -1)"
  echo "LRAT bytes $(stat -f%z "$tag.lrat")  sha256 $(shasum -a 256 "$tag.lrat" | cut -d' ' -f1)"
  "$TOOLS/drat-trim/lrat-check" "$tag.cnf" "$tag.lrat" > "$tag.lc" 2>&1
  echo "lrat-check: $(grep -a -o 'c VERIFIED' "$tag.lc" | head -1)"
else
  echo "DRAT so far $(( $(stat -f%z "$tag.drat" 2>/dev/null || echo 0)/1048576 )) MB"
fi
rm -f "$tag.drat" "$tag.lrat" "$tag.cnf"
echo "=== done $tag $(date '+%H:%M:%S')"
