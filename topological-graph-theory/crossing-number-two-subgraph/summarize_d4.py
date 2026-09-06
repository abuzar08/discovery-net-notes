"""Exact per-seed summary of the d <= 4 expansion run.

Each seed's .done marker records the number of expansions, the number skipped
for exceeding the tester's limits (n > 28 or m >= 63), how many were
2-crossing-critical and how many had crossing number at least 3.  The coverage
claim is stated from the skipped counts, not estimated.
"""
import json
import glob
import os

rows = []
for f in sorted(glob.glob('expand_state/seed*.done')):
    rows.append(json.load(open(f)))
rows.sort(key=lambda r: (r['d'], r['n'], r['seed']))
print(f"{'seed':>5} {'n':>3} {'m':>3} {'d':>2} {'expansions':>12} "
      f"{'decided':>12} {'skipped':>12} {'coverage':>9} {'critical':>9} "
      f"{'cr>=3':>6} {'sec':>7}")
T = dict(exp=0, dec=0, skip=0, crit=0, ge3=0, sec=0.0)
for r in rows:
    dec = r['expansions'] - r['skipped_over_62_edges']
    T['exp'] += r['expansions']; T['dec'] += dec
    T['skip'] += r['skipped_over_62_edges']; T['crit'] += r['crossing_critical']
    T['ge3'] += r['cr_ge_3']; T['sec'] += r['seconds']
    print(f"{r['seed']:>5} {r['n']:>3} {r['m']:>3} {r['d']:>2} "
          f"{r['expansions']:>12,} {dec:>12,} {r['skipped_over_62_edges']:>12,} "
          f"{dec/r['expansions']:>8.2%} {r['crossing_critical']:>9} "
          f"{r['cr_ge_3']:>6} {r['seconds']:>7.0f}")
print(f"{'TOTAL':>5} {'':>3} {'':>3} {'':>2} {T['exp']:>12,} {T['dec']:>12,} "
      f"{T['skip']:>12,} {T['dec']/T['exp']:>8.2%} {T['crit']:>9} "
      f"{T['ge3']:>6} {T['sec']:>7.0f}")
print(f"\nseeds completed: {len(rows)}")
print(f"expansions enumerated: {T['exp']:,}")
print(f"decided by crit2: {T['dec']:,} ({T['dec']/T['exp']:.2%})")
print(f"skipped for exceeding n <= 28 or m <= 62: {T['skip']:,}")
print(f"2-crossing-critical among those decided: {T['crit']}")
print(f"with crossing number at least 3: {T['ge3']}")
print(f"total single-core time: {T['sec']/3600:.2f} core-hours")
