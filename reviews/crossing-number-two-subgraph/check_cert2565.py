"""reviewer-1: checks on census_certificate.json / claims of finding h2565
that verify_census.py itself does not make."""
import copy, json, subprocess, sys, itertools
sys.path.insert(0, 'target2')
import verify_census as vc
import verify_certificate as vf
import networkx as nx

cert = json.load(open('target2/census_certificate.json'))
M = cert['members']
kur = sum(1 + len(r['one_crossing']) for r in M)
rot = sum(1 + len(r['delete']) for r in M)
print(f"members {len(M)}; Kuratowski witnesses {kur}; rotation systems {rot}  (claimed 5563 / 1123)")

# pairwise non-isomorphism of the 64 restricted census graphs (geng is trusted for this in the target)
G = []
for n in range(6, 11):
    for line in open(f'target2/n{n}.txt'):
        p = line.split()
        E = [tuple(map(int, x.split('-'))) for x in p[3].strip(',').split(',')]
        G.append((p[0], nx.Graph(E)))
iso = sum(1 for a, b in itertools.combinations(range(len(G)), 2) if nx.is_isomorphic(G[a][1], G[b][1]))
print(f"census graphs {len(G)}; isomorphic pairs {iso}")
C33 = nx.cartesian_product(nx.cycle_graph(3), nx.cycle_graph(3))
ge3 = [g for t, g in G if t == 'CRIT_GE3']
print(f"CRIT_GE3 lines {len(ge3)}; isomorphic to C3 [] C3: {[nx.is_isomorphic(g, C33) for g in ge3]}")
# every certified member is, as a labelled graph, one of the CRIT2 lines; and members with cr=2 are non-isomorphic to C3[]C3
print("certified member isomorphic to C3 [] C3:", sum(nx.is_isomorphic(nx.Graph([tuple(e) for e in r['edges']]), C33) for r in M))

# old (971a152) checker rejects a disconnected planar embedding; new accepts
sys.path.insert(0, 'target'); import importlib
old = importlib.import_module('verify_certificate')  # resolves to target2 (already imported) -> load old by path
import importlib.util
spec = importlib.util.spec_from_file_location('old_vf', 'target/verify_certificate.py'); old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
E2 = K4 + [(u+4, v+4) for u, v in K4]
rotK4 = {'0':[1,2,3],'1':[0,3,2],'2':[0,1,3],'3':[0,2,1]}
rot2 = dict(rotK4); rot2.update({str(v+4): [w+4 for w in rotK4[str(v)]] for v in range(4)})
print("K4+K4 planar embedding: old checker", old.check_planar_embedding(8, E2, rot2), "| new checker", vf.check_planar_embedding(8, E2, rot2))

# mutation tests on the new checker
def run(m):
    ok, why = vc.check_member(m); return ok, why
base = M[5]
assert run(base)[0]
m = copy.deepcopy(base); m['nonplanar'] ^= 1; print("flip bit of Kuratowski mask:", run(m))
m = copy.deepcopy(base); m['one_crossing'][3] ^= 4; print("flip bit of 1-crossing mask:", run(m))
m = copy.deepcopy(base); m['one_crossing'] = m['one_crossing'][:-1]; print("drop a witness:", run(m))
m = copy.deepcopy(base); k = next(iter(m['cr_le_2']['rotation'])); m['cr_le_2']['rotation'][k] = m['cr_le_2']['rotation'][k][::-1]; print("reverse one rotation list:", run(m))
m = copy.deepcopy(base); e = m['edges'][0]; f = next(x for x in m['edges'] if set(x) & set(e) and x != e); m['cr_le_2']['config'] = [['x', e, f], m['cr_le_2']['config'][1]] if len(m['cr_le_2']['config']) == 2 else [['xx', e, f, m['cr_le_2']['config'][0][3]]]; print("adjacent pair declared crossing:", run(m))
m = copy.deepcopy(base); m['edges'] = m['edges'][:-1] + [[0, 1]] if [0,1] not in m['edges'] else m['edges'][:-1] + [[0,2]]; print("substitute an edge:", run(m))
# a member with cr = 3 (C3[]C3) with a fake cr<=2 witness must fail
c = json.load(open('target2/certificate.json'))
fake = {'n': 9, 'edges': c['graph']['edges'], 'nonplanar': c['G_nonplanar'], 'one_crossing': c['one_crossing_witnesses'],
        'cr_le_2': {'config': [['x', c['cr_le_3']['crossings'][0], c['cr_le_3']['crossings'][1]]], 'rotation': c['cr_le_3']['rotation']},
        'delete': [{'e': w['deleted'], 'crossing': w['crossing'], 'rotation': w['rotation']} for w in c['cr_G_minus_e_le_1']]}
print("C3[]C3 with two of its three crossings as a cr<=2 witness:", run(fake))
