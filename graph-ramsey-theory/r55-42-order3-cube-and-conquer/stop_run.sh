#!/bin/sh
# Stop a run_lrat_p.py sweep completely.
#
# Three process layers have to go, in order, or the run half-survives:
#   1. the driver (python3 run_lrat_p.py ...)
#   2. its ProcessPoolExecutor workers -- these are *spawned*, so their command
#      line is "multiprocessing.spawn", not the driver's, and pkill -f on the
#      driver's name misses them entirely; killed drivers leave them orphaned
#      (ppid 1) and still processing cubes
#   3. the cadical processes, which are grandchildren behind a `timeout` wrapper;
#      killing the wrapper re-parents cadical to init and it keeps running
#
# Leaving layer 2 alive is what corrupted a run on 2026-09-09: two pools shared
# one output directory and deleted each other's proofs.
#
# usage: sh stop_run.sh <outdir-name>
set -e
OUT="$1"
[ -n "$OUT" ] || { echo "usage: sh stop_run.sh <outdir-name>"; exit 2; }

pkill -f "run_lrat_p.py .*$OUT" 2>/dev/null || true
sleep 3
# workers are identified by the cubes they are solving, not by their command line
ps -eo pid,ppid,command | grep "[^]]$OUT/" | awk '{print $2}' | sort -u > /tmp/stop_w.$$ || true
while read p; do [ "$p" -gt 1 ] 2>/dev/null && kill -9 "$p" 2>/dev/null || true; done < /tmp/stop_w.$$
sleep 3
ps -eo pid,command | grep "[^]]$OUT/" | awk '{print $1}' > /tmp/stop_c.$$ || true
while read p; do kill -9 "$p" 2>/dev/null || true; done < /tmp/stop_c.$$
rm -f /tmp/stop_w.$$ /tmp/stop_c.$$
sleep 3
# a worker caught between cubes is solving nothing, so nothing above names it;
# sweep orphaned spawn workers whose working directory is this workspace
ps -eo pid,ppid,command | grep "[s]pawn_main" | awk '$2==1 {print $1}' > /tmp/stop_o.$$ || true
while read p; do
  cwd=$(lsof -a -p "$p" -d cwd -Fn 2>/dev/null | grep '^n' | head -1)
  case "$cwd" in *researcher-1*) kill -9 "$p" 2>/dev/null || true;; esac
done < /tmp/stop_o.$$
rm -f /tmp/stop_o.$$
sleep 2
n=$(ps -eo command | grep -c "[^]]$OUT/" || true)
echo "$OUT: $n processes left"
