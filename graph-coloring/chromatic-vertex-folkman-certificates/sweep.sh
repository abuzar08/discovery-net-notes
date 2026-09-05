#!/bin/bash
# sweep.sh K Q MSTART MSTOP PERM_TIMEOUT
# For each m, decide "is there a k-vertex-critical K_q-free graph on m
# vertices" (min degree >= k-1, symmetry broken).  Stops at the first SAT:
# that m is n(k,q), provided every smaller m came out UNSAT.
cd "$(dirname "$0")"
k=$1; q=$2; ms=$3; me=$4; to=$5
out="sweep_k${k}_q${q}.txt"
: > "$out"
for (( m=ms; m<=me; m++ )); do
  s=$(date +%s)
  timeout "$to" uv run --quiet --with python-sat python3 search.py \
      "$m" "$k" "$q" --symbreak --mindeg $((k-1)) > "run_k${k}_q${q}_m${m}.log" 2>&1
  rc=$?
  e=$(( $(date +%s) - s ))
  if [ $rc -eq 124 ]; then
    echo "m=$m TIMEOUT after ${e}s" >> "$out"; break
  fi
  v=$(grep -oE "^(UN)?SAT" "run_k${k}_q${q}_m${m}.log" | head -1)
  it=$(grep -oE "iterations=[0-9]+" "run_k${k}_q${q}_m${m}.log" | head -1)
  echo "m=$m $v $it ${e}s" >> "$out"
  if [ "$v" = "SAT" ]; then echo "n($k,$q) = $m" >> "$out"; break; fi
done
echo DONE >> "$out"
