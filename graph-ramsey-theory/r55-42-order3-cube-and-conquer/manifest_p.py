"""results.jsonl + cubes.icnf -> manifest.json {i: {cube, sha256, bytes, solve_s}}  usage: python3 manifest_p.py cubes.icnf results.jsonl out.json"""
import sys, json
cubes = [list(map(int, l.split()[1:-1])) for l in open(sys.argv[1]) if l.startswith('a ')]
man = {}
for l in open(sys.argv[2]):
    r = json.loads(l)
    if r['status'] == 'UNSAT-VERIFIED':
        man[str(r['cube'])] = {'cube': cubes[r['cube']], 'sha256': r['lrat_sha256'], 'bytes': r['lrat_bytes'], 'solve_s': r['solve_s']}
json.dump(man, open(sys.argv[3], 'w'), indent=0)
print(len(man), 'of', len(cubes), 'cubes in manifest')
