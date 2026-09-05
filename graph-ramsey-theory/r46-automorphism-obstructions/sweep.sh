#!/bin/bash
cd "$(dirname "$0")"
# Cycle types 1^f p^k with p prime >= 5, f + pk = n, f <= 22 (hand bound),
# ordered by descending p then descending k (fewest orbit variables first).
python3 - <<'PY' > types.txt
for p in (17, 13, 11, 7, 5):
    for n in (36, 37, 38, 39):
        for k in range(n // p, 0, -1):
            f = n - p * k
            if f > 22:
                continue
            print(n, f, p, k)
PY
i=0
while read -r n f p k; do
  tag="n${n}_f${f}_p${p}_k${k}"
  [ -f "$tag.lrat" ] && continue
  ./one.sh "$n" 4 6 "$f" "$p" "$k" 1500 >> sweep_results.txt 2>&1 &
  i=$((i+1))
  if [ $((i % 4)) -eq 0 ]; then wait; fi
done < types.txt
wait
echo DONE >> sweep_results.txt
