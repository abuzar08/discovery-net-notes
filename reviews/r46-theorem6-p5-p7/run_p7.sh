#!/bin/bash
# reviewer-1: for one of the four new p = 7 certificates of h3014 --- regenerate
# the CNF, check it clause for clause against my own construction, decompress the
# stored certificate, compare its size and SHA-256 with certs.json AND with the
# value I obtained independently in my h2947 review, and verify it with
# lrat-check.  usage: run_p7.sh n f k
set -u
cd "$(dirname "$0")"
H=$(pwd); T=$H/target; W=$H/work; TOOLS=$H/../r46/tools
mkdir -p "$W"; cd "$W"
n=$1; f=$2; k=$3; tag="sf7_n${n}_f${f}_p7_k${k}"
echo "=== $tag  $(date '+%H:%M:%S')"
python3 "$T/encode.py" "$n" 4 6 "$f" 7 "$k" "$tag.cnf" --symf || exit 1
python3 "$H/indep_symf.py" "$n" 4 6 "$f" 7 "$k" "$tag.cnf" 2000 || exit 1
want=$(python3 -c "
import json;c=json.load(open('$T/certs.json'))['certificates']
x=[y for y in c if y['tag']=='$tag'][0];print(x['lrat_bytes'],x['lrat_sha256'])")
xz -dc "$T/certificates/$tag.lrat.xz" > "$tag.lrat"
got="$(stat -f%z "$tag.lrat") $(shasum -a 256 "$tag.lrat" | cut -d' ' -f1)"
echo "certs.json : $want"
echo "stored file: $got"
[ "$want" = "$got" ] && echo "MATCH certs.json" || echo "MISMATCH certs.json"
mine=$(grep -a -A3 "$(echo $tag | sed 's/sf7_n\([0-9]*\)_f\([0-9]*\)_p7_k\([0-9]*\)/p7_n\1_f\2_k\3/')" "$H/../../notes/reviews/r46-symf-p5/p7_summary.txt" | grep -a "LRAT bytes" | head -1)
echo "my h2947 run: $mine"
"$TOOLS/drat-trim/lrat-check" "$tag.cnf" "$tag.lrat" > "$tag.lc" 2>&1
echo "lrat-check: $(grep -a -o 'c VERIFIED' "$tag.lc" | head -1)"
rm -f "$tag.lrat" "$tag.cnf"
echo "=== done $tag $(date '+%H:%M:%S')"
