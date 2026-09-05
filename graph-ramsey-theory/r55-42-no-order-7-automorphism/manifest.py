"""results.jsonl -> manifest.json (per-cube sha256 of certificate, sizes, times).
usage: python3 manifest.py results.jsonl manifest.json"""
import sys, json
recs = {}
for l in open(sys.argv[1]):
    r = json.loads(l); recs[str(r['idx'])] = {k: r[k] for k in ('cube', 'status', 'time', 'drat_bytes', 'drat_trim', 'lrat_xz_bytes', 'sha256') if k in r}
json.dump(recs, open(sys.argv[2], 'w'), indent=0, sort_keys=True)
st = {}
for r in recs.values(): st[r['status']] = st.get(r['status'], 0) + 1
print(len(recs), 'records', st, 'total lrat.xz bytes', sum(r.get('lrat_xz_bytes', 0) for r in recs.values()), 'max time', max(r['time'] for r in recs.values()))
