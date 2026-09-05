#!/bin/bash
# reviewer-1: all 24 --symf types of h2919, in order of increasing certificate size
cd "$(dirname "$0")"
for n in 36 37 38 39; do
  for spec in "31 1" "26 2" "21 3" "16 4" "11 5" "6 6"; do
    set -- $spec
    f=$(( $1 + n - 36 )); k=$2
    ./run_symf.sh $n $f $k
  done
done
echo "ALL SYMF DONE $(date)"
