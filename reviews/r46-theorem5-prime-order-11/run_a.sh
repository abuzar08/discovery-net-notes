#!/bin/sh
# reviewer-1: independent regeneration of the hash-only certificate n36_f3_p11_k3
cd "$(dirname "$0")"
T=../target2; CAD=../tools/cadical/build/cadical; DT=../tools/drat-trim/drat-trim; LC=../tools/drat-trim/lrat-check
tag=n36_f3_p11_k3
date
python3 $T/encode.py 36 4 6 3 11 3 $tag.cnf
python3 ../indep_orbit_encode.py 36 4 6 3 11 3 $tag.cnf
/usr/bin/time $CAD -q --binary=false $tag.cnf $tag.drat; echo "cadical rc=$?"
ls -l $tag.drat
/usr/bin/time $DT $tag.cnf $tag.drat -L $tag.lrat | grep -E "VERIFIED|FAILED|ERROR"
ls -l $tag.lrat; shasum -a 256 $tag.lrat
$LC $tag.cnf $tag.lrat | grep -E "VERIFIED|FAILED|ERROR|Added"
rm -f $tag.drat
date
