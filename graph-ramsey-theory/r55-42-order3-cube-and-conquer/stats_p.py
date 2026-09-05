"""Summarise results.jsonl (latest record per cube) + xz sizes.  usage: python3 stats_p.py outdir ncubes"""
import sys, json, os
d, n = sys.argv[1], int(sys.argv[2]); rec = {}
for l in open(os.path.join(d, 'results.jsonl')):
    r = json.loads(l); rec[r['cube']] = r
ok = [r for r in rec.values() if r['status'] == 'UNSAT-VERIFIED']
t = [r['solve_s'] for r in ok]; raw = sum(r['lrat_bytes'] for r in ok)
xz = sum(os.path.getsize(os.path.join(d, f'c{i}.lrat.xz')) for i in rec if rec[i]['status'] == 'UNSAT-VERIFIED' and os.path.exists(os.path.join(d, f'c{i}.lrat.xz')))
print(f'{len(ok)}/{n} cubes UNSAT-VERIFIED; solve time total {sum(t):.0f} s, median {sorted(t)[len(t)//2]:.1f} s, max {max(t):.1f} s (cube {max(ok, key=lambda r: r["solve_s"])["cube"]}); LRAT raw total {raw/1e9:.2f} GB, max {max(r["lrat_bytes"] for r in ok)/1e6:.1f} MB; xz total {xz/1e6:.0f} MB')
other = [r for r in rec.values() if r['status'] != 'UNSAT-VERIFIED']
if other: print('non-verified:', other)
