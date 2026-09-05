#!/bin/bash
cd "$(dirname "$0")"
while read -r a; do
  [ -z "$a" ] && continue
  timeout 3000 python3 lemma_test.py $a
done <<'LIST'
3 20000
4 200000
5 40000
LIST
