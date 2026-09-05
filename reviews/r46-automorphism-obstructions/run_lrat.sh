#!/bin/sh
# reviewer-1: for every stored certificate: (1) regenerate the orbit CNF with the target's
# encode.py, (2) compare it as a clause set with an independent union-find construction
# (indep_orbit_encode.py), (3) check the decompressed LRAT's SHA-256 against certs.json,
# (4) replay the proof with drat-trim's C lrat-check, a checker the target does not use.
# usage: sh run_lrat.sh TARGET_DIR LRATCHECK_BIN   (tags.txt: tag n f p k sha256)
T=$1; LC=$2; mkdir -p tmp
while read tag n f p k sha; do
  python3 $T/encode.py $n 4 6 $f $p $k tmp/$tag.cnf >/dev/null
  python3 indep_orbit_encode.py $n 4 6 $f $p $k tmp/$tag.cnf
  xz -dkc $T/certificates/$tag.lrat.xz > tmp/$tag.lrat
  s=$(shasum -a 256 tmp/$tag.lrat | cut -d' ' -f1)
  if [ "$s" = "$sha" ]; then echo "  sha256 matches manifest"; else echo "  SHA256 MISMATCH $s"; fi
  $LC tmp/$tag.cnf tmp/$tag.lrat 2>&1 | grep -E "VERIFIED|FAILED|ERROR|Added clauses" | sed 's/^/  /'
  rm -f tmp/$tag.cnf tmp/$tag.lrat
done < tags.txt
