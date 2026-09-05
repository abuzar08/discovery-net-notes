#!/bin/bash
cd "$(dirname "$0")"
n=$1; f=$2; k=$3; cap=${4:-1500}
tag="sf_n${n}_f${f}_p5_k${k}"
python3 encode.py $n 4 6 $f 5 $k "$tag.cnf" --symf > "$tag.enc" 2>&1
s=$(date +%s)
timeout $cap ../tools/cadical/build/cadical -q --binary=false "$tag.cnf" "$tag.drat" >/dev/null 2>&1
rc=$?; e=$(( $(date +%s) - s ))
if [ $rc -eq 20 ]; then
  dt=$(timeout 3600 ../tools/drat-trim/drat-trim "$tag.cnf" "$tag.drat" -L "$tag.lrat" 2>&1 | grep -c "s VERIFIED")
  vr=$(python3 verify.py lower $n 4 6 $f 5 $k "$tag.cnf" "$tag.lrat" --symf 2>&1 | grep -c VERIFIED)
  echo "$(cat $tag.enc) | UNSAT ${e}s drat-trim=$dt replay=$vr lrat=$(( $(stat -f%z $tag.lrat)/1024 ))KB" >> symf_results.txt
else
  echo "$(cat $tag.enc) | rc=$rc ${e}s drat=$(( $(stat -f%z $tag.drat 2>/dev/null || echo 0)/1048576 ))MB" >> symf_results.txt
fi
rm -f "$tag.drat" "$tag.cnf"
