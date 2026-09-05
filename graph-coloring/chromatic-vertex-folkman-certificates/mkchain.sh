#!/bin/bash
# mkchain.sh K Q MSTART MSTOP  -- build + externally verify + independently
# replay one certificate per m.  Together these establish n(K,Q) > MSTOP.
cd "$(dirname "$0")"
k=$1; q=$2; ms=$3; me=$4
d=$((k-1))
mkdir -p certificates
for (( m=ms; m<=me; m++ )); do
  tag="n${m}_k${k}_q${q}"
  p="parts_$tag.txt"
  [ -f "$p" ] || { echo "$tag SKIP (no partitions)"; continue; }
  python3 encode.py $m $k $q "$p" "c_$tag.cnf" --symbreak --mindeg $d >/dev/null
  ../tools/cadical/build/cadical -q --binary=false "c_$tag.cnf" "c_$tag.drat" >/dev/null 2>&1
  rc=$?
  dt=$(../tools/drat-trim/drat-trim "c_$tag.cnf" "c_$tag.drat" -L "c_$tag.lrat" 2>&1 | grep -c "s VERIFIED")
  vr=$(python3 verify.py lower $m $k $q "$p" "c_$tag.cnf" "c_$tag.lrat" --symbreak --mindeg $d 2>&1 | grep -c VERIFIED)
  ls=$(stat -f%z "c_$tag.lrat" 2>/dev/null)
  parts=$(grep -c . "$p")
  sh=$(shasum -a 256 "c_$tag.lrat" | cut -c1-16)
  echo "$tag cadical=$rc drattrim_verified=$dt replay_verified=$vr parts=$parts lrat=${ls}B sha=$sh"
  rm -f "c_$tag.drat"
done
