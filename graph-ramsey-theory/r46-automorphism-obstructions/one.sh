#!/bin/bash
# one.sh N S T F P K [timeout]
cd "$(dirname "$0")"
n=$1;s=$2;t=$3;f=$4;p=$5;k=$6;to=${7:-1800}
tag="n${n}_f${f}_p${p}_k${k}"
python3 encode.py $n $s $t $f $p $k "$tag.cnf" > "$tag.enc" 2>&1 || { echo "$tag ENCODE-FAIL"; exit 1; }
timeout $to ../tools/cadical/build/cadical -q --binary=false "$tag.cnf" "$tag.drat" >/dev/null 2>&1
rc=$?
info=$(cat "$tag.enc")
if [ $rc -eq 20 ]; then
  dt=$(timeout 3600 ../tools/drat-trim/drat-trim "$tag.cnf" "$tag.drat" -L "$tag.lrat" 2>&1 | grep -c "s VERIFIED")
  echo "$info | UNSAT drat=$(stat -f%z $tag.drat)B lrat=$(stat -f%z $tag.lrat 2>/dev/null)B drat-trim=$dt"
  rm -f "$tag.drat"
elif [ $rc -eq 10 ]; then
  echo "$info | SAT  *** witness ***"
else
  echo "$info | TIMEOUT/other rc=$rc"
  rm -f "$tag.drat"
fi
