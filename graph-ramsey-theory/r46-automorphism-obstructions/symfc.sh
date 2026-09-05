#!/bin/bash
cd "$(dirname "$0")"
n=$1; f=$2; p=$3; k=$4; cap=${5:-1500}
tag="fc_n${n}_f${f}_p${p}_k${k}"
python3 encode.py $n 4 6 $f $p $k "$tag.cnf" --symf --symc > "$tag.enc" 2>&1
s=$(date +%s)
timeout $cap ../tools/cadical/build/cadical -q --binary=false "$tag.cnf" "$tag.drat" >/dev/null 2>&1
rc=$?; e=$(( $(date +%s) - s ))
if [ $rc -eq 20 ]; then
  dt=$(timeout 3600 ../tools/drat-trim/drat-trim "$tag.cnf" "$tag.drat" -L "$tag.lrat" 2>&1 | grep -c "s VERIFIED")
  echo "$(cat $tag.enc) | UNSAT ${e}s drat-trim=$dt lrat=$(( $(stat -f%z $tag.lrat)/1024 ))KB" >> symfc_results.txt
else
  echo "$(cat $tag.enc) | rc=$rc ${e}s" >> symfc_results.txt
fi
rm -f "$tag.drat" "$tag.cnf"
