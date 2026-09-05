#!/bin/bash
# geng's res/mod classes are NOT refinements across different mod values.
#
# nauty's geng splits a generation run into classes "res/mod".  For a FIXED
# mod, classes 0..mod-1 partition the search space exactly.  It is tempting to
# assume that class r mod M is the union of the classes r, r+M, r+2M, ...
# mod kM, so that a killed or slow shard can be resumed at a finer granularity.
# That assumption is FALSE in general: geng chooses where in the search tree to
# split according to mod, and different mod values split at different levels.
#
# It happens to hold for some parameters, which is what makes it dangerous:
# verifying it on a small case and then relying on it at the real size can
# silently produce incomplete or double-counted coverage.
#
# Run from a built nauty source tree (nauty 2.9.1 here).

set -e
echo "search space: geng -d3 <n> <17:29 style range>, counts only (-u)"
count () { ./geng -u "${@}" 2>&1 | grep -o '[0-9]* graphs generated' | grep -o '^[0-9]*'; }

echo
echo "n = 9,  -d3 9 14:23   (the refinement HOLDS here)"
for r in 4 5; do
  a=$(count -d3 9 14:23 $r/6)
  b=$(count -d3 9 14:23 $r/12)
  c=$(count -d3 9 14:23 $((r+6))/12)
  printf "   class %d/6 = %-10s   %d/12 + %d/12 = %-10s   %s\n" \
     "$r" "$a" "$r" "$((r+6))" "$((b+c))" \
     "$([ "$a" = "$((b+c))" ] && echo EQUAL || echo DIFFERENT)"
done

echo
echo "n = 11, -d3 11 17:29  (the refinement FAILS here)"
for r in 4 5; do
  a=$(count -d3 11 17:29 $r/6)
  b=$(count -d3 11 17:29 $r/12)
  c=$(count -d3 11 17:29 $((r+6))/12)
  printf "   class %d/6 = %-10s   %d/12 + %d/12 = %-10s   %s\n" \
     "$r" "$a" "$r" "$((r+6))" "$((b+c))" \
     "$([ "$a" = "$((b+c))" ] && echo EQUAL || echo DIFFERENT)"
done

echo
echo "the mod-6 partition itself is exact:"
tot=$(count -d3 11 17:29)
s=0
for r in 0 1 2 3 4 5; do s=$((s + $(count -d3 11 17:29 $r/6))); done
printf "   sum over 0..5 mod 6 = %s   unsharded total = %s   %s\n" \
  "$s" "$tot" "$([ "$s" = "$tot" ] && echo EQUAL || echo DIFFERENT)"
