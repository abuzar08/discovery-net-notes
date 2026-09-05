#!/bin/bash
cd "$(dirname "$0")"
while read which f k; do
  /usr/bin/time -p python3 lemma_check.py $which $f $k 2>&1 | grep -v -E '^(user|sys)'
done <<'LIST'
A 3 2
A 4 2
A 5 1
A 5 2
A 6 0
A 6 1
A 7 0
B 3 2
B 4 1
B 4 2
B 5 0
B 5 1
B 6 0
LIST
