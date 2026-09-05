#!/bin/bash
# reviewer-1: for one --symf type of h2919 — regenerate the CNF, check it against
# my own construction (indep_symf.py), then either replay the stored certificate
# with lrat-check or, if none is stored, re-solve from scratch and check the LRAT
# size and SHA-256 against certs.json.  Large files are deleted afterwards.
# usage: run_symf.sh n f k
set -u
cd "$(dirname "$0")"
H=$(pwd); T=$H/target; W=$H/work; TOOLS=$H/../r46/tools
n=$1; f=$2; k=$3; tag="sf_n${n}_f${f}_p5_k${k}"
cd "$W"
echo "=== $tag  $(date '+%H:%M:%S')"
python3 "$T/encode.py" "$n" 4 6 "$f" 5 "$k" "$tag.cnf" --symf || exit 1
shasum -a 256 "$tag.cnf" | sed 's/^/CNF /'
python3 "$H/indep_symf.py" "$n" 4 6 "$f" 5 "$k" "$tag.cnf" 2000 || exit 1
want_bytes=$(python3 -c "
import json;c=json.load(open('$T/certs.json'))['certificates']
print([x for x in c if x['tag']=='$tag'][0]['lrat_bytes'])")
want_sha=$(python3 -c "
import json;c=json.load(open('$T/certs.json'))['certificates']
print([x for x in c if x['tag']=='$tag'][0]['lrat_sha256'])")
if [ -f "$T/certificates/$tag.lrat.xz" ]; then
  xz -dc "$T/certificates/$tag.lrat.xz" > "$tag.lrat"
  echo "stored certificate: bytes $(stat -f%z "$tag.lrat") expected $want_bytes"
  echo "stored certificate: sha256 $(shasum -a 256 "$tag.lrat" | cut -d' ' -f1) expected $want_sha"
else
  echo "no stored certificate — re-solving"
  /usr/bin/time -p "$TOOLS/cadical/build/cadical" -q --binary=false "$tag.cnf" "$tag.drat" > "$tag.cad" 2> "$tag.cadtime"
  grep -a '^s ' "$tag.cad"; grep real "$tag.cadtime" | sed 's/^/cadical /'
  /usr/bin/time -p "$TOOLS/drat-trim/drat-trim" "$tag.cnf" "$tag.drat" -L "$tag.lrat" > "$tag.dt" 2> "$tag.dttime"
  echo "drat-trim: $(grep -a -c 'VERIFIED' "$tag.dt") VERIFIED line(s)"; grep real "$tag.dttime" | sed 's/^/drat-trim /'
  echo "regenerated: bytes $(stat -f%z "$tag.lrat") expected $want_bytes"
  echo "regenerated: sha256 $(shasum -a 256 "$tag.lrat" | cut -d' ' -f1) expected $want_sha"
  rm -f "$tag.drat"
fi
"$TOOLS/drat-trim/lrat-check" "$tag.cnf" "$tag.lrat" > "$tag.lc" 2>&1
echo "lrat-check: $(grep -a -o 'c VERIFIED' "$tag.lc" | head -1)"
rm -f "$tag.lrat" "$tag.cnf" "$tag.drat"
echo "=== done $tag $(date '+%H:%M:%S')"
