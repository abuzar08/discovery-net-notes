#!/bin/bash
# reviewer-1: one type of the fixed-vertex lex-leader artifact.
# usage: run_type.sh f p k base|hybrid stored.lrat.xz|-  expected_cnf_sha  expected_lrat_sha  expected_lrat_bytes
set -u
W=/Users/abuzark/.discovery-research-team/workspaces/reviewer-1
S=$W/scratch/r55L
T=$S/target
P=$S/r55-42-prime-order-automorphisms
CAD=$W/scratch/r46/tools/cadical/build/cadical
DT=$W/scratch/r46/tools/drat-trim/drat-trim
LC=$W/scratch/r46/tools/drat-trim/lrat-check
f=$1; p=$2; k=$3; mode=$4; stored=$5; cnfsha=$6; lratsha=$7; lratbytes=$8
tag=f${f}_p${p}_k${k}_${mode}
cd $S/work || exit 1
echo "=== $tag  $(date)"
if [ $mode = base ]; then python3 $P/encode.py 42 $f $p $k $tag.raw.cnf; else python3 $P/hybrid.py 42 $f $p $k $tag.raw.cnf; fi
python3 $T/symF.py $tag.raw.cnf $tag.cnf 42 $f $p $k
got=$(shasum -a 256 $tag.cnf | cut -d' ' -f1)
echo "CNF sha256 $got  expected $cnfsha  $([ $got = $cnfsha ] && echo MATCH || echo MISMATCH)"
python3 $S/indep_lex.py 42 $f $p $k $mode $tag.cnf || { echo "INDEP CHECK FAILED $tag"; exit 1; }
if [ "$stored" != "-" ]; then
  echo "stored certificate $stored"
  xz -dkc $T/certificates/$stored > $tag.lrat
else
  /usr/bin/time -p $CAD -q --binary=false $tag.cnf $tag.drat > $tag.cadical.log 2>&1
  echo "cadical: $(grep -E '^s ' $tag.cadical.log) $(grep -E '^(real|user)' $tag.cadical.log | tr '\n' ' ')"
  /usr/bin/time -p $DT $tag.cnf $tag.drat -L $tag.lrat > $tag.drattrim.log 2>&1
  echo "drat-trim: $(grep -E '^s ' $tag.drattrim.log) $(grep -E '^(real|user)' $tag.drattrim.log | tr '\n' ' ')"
  rm -f $tag.drat
fi
bytes=$(stat -f %z $tag.lrat)
got=$(shasum -a 256 $tag.lrat | cut -d' ' -f1)
echo "LRAT bytes $bytes expected $lratbytes  $([ $bytes = $lratbytes ] && echo MATCH || echo MISMATCH)"
echo "LRAT sha256 $got  expected $lratsha  $([ $got = $lratsha ] && echo MATCH || echo MISMATCH)"
$LC $tag.cnf $tag.lrat > $tag.lratcheck.log 2>&1
echo "lrat-check: $(grep -E 'VERIFIED|FAIL|ERROR' $tag.lratcheck.log | head -2 | tr '\n' ' ')"
rm -f $tag.lrat
echo "=== done $tag $(date)"
