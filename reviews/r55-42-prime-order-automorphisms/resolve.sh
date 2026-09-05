#!/bin/zsh
# Independent re-solve of one type: my encoding -> cadical -> drat-trim.
# usage: resolve.sh tag kind   (tag = f<f>_p<p>_k<k>, kind = base|hybrid)
set -u
R=/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/scratch/r55auto
tag=$1; kind=$2
set -- $(echo $tag | tr 'fpk_' '    ')
f=$1; p=$2; k=$3
mkdir -p $R/indep
cnf=$R/indep/$tag.indep.cnf; drat=$R/indep/$tag.indep.drat; log=$R/indep/$tag.log
cd $R
if [ $kind = base ]; then
  python3 -c "
import sys; sys.path.insert(0,'$R')
from indep_encode import *
n,f,p,k=42,$f,$p,$k
sig=permutation(n,f,p,k); var,nv=orbits_of_pairs(n,sig); cl=base_clauses(n,var)
bl=sorted(sorted(c,key=lambda x:(abs(x),x)) for c in cl)
fh=open('$cnf','w'); fh.write('c reviewer-1 independent base CNF\np cnf %d %d\n'%(nv,len(bl)))
[fh.write(' '.join(map(str,c))+' 0\n') for c in bl]; fh.close(); print('base',nv,len(bl))" > $log 2>&1
else
  python3 indep_hybrid.py 42 $f $p $k $cnf > $log 2>&1
fi
t0=$(date +%s)
timeout 3600 $R/tools/cadical/build/cadical -q --binary=false $cnf $drat >> $log 2>&1
rc=$?
t1=$(date +%s)
echo "cadical exit $rc solve_s $((t1-t0))" >> $log
if [ $rc -eq 20 ]; then
  timeout 7200 $R/tools/drat-trim/drat-trim $cnf $drat -t 7000 >> $log 2>&1
  echo "drat-trim exit $? trim_s $(( $(date +%s) - t1 ))" >> $log
  echo "drat_bytes $(stat -f %z $drat)" >> $log
  rm -f $drat
fi
tail -3 $log | tr '\n' ' '; echo " [$tag]"
