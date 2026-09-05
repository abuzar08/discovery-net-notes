#!/bin/bash
cd "$(dirname "$0")"
while read -r a; do
  [ -z "$a" ] && continue
  timeout 2400 python3 symc_check.py $a
done <<'LIST'
9 4 6 0 3 3
11 4 6 2 3 3
9 4 6 3 3 2
11 4 6 1 5 2
LIST
