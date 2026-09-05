"""reviewer-1: for the b = 30, c = (3,1^25) class at m = 838, trace the split
bound over the excess split Y, to locate the configuration the body describes
("all 30 barrier vertices are low and carry 377 edges, forcing a K_28")."""
import verify_range as V
import k4free as K

r, n, m = 29, 58, 838
X = 2 * m - n * (r - 1)
eH = n * (n - 1) // 2 - m
c = tuple([3] + [1] * 25)
b, D = 30, sum(c)
CB, CD = b * (b - 1) // 2, D * (D - 1) // 2
Pmin = sum(s - 1 for s in c)
Pmax = sum(min(K.turan_cap(s), s * (s - 1) // 2) for s in c)
Ymin = sum(s * max(0, r + 3 - s - b) for s in c)
print(f'X = {X}, e(H) = {eH}, |B| = {b}, |D| = {D}, Y ranges over [{Ymin}, {X}]')
print(' Y   |B_low|  e(B_low)>=  forced   cr(K_q)   crB     crD    split')
best = None
for Y in range(Ymin, X + 1):
    Q = min(CB, Pmax - D * r + Y + eH)
    if Q < 6:
        continue
    P = D * r - Y - eH + Q
    if not (Pmin <= P <= Pmax):
        continue
    eB, eD = CB - Q, CD - P
    crD = max(V.crK(len(c)), K.L(D, eD), V.best_bipartition(list(c)))
    crB = K.L(b, eB) if eB > 0 else 0
    pB = b - (X - Y)
    eLB = eB - (X - Y) * (b - 1)
    qB = K.forced_clique(pB, eLB, r) if pB >= 2 else 1
    if qB is None:
        print(f'{Y:3d}   {pB:4d}     {eLB:6d}    (no Gallai forest with that many edges)')
        continue
    crB2 = max(crB, V.crK(qB))
    tot = crB2 + crD
    if best is None or tot < best[0]:
        best = (tot, Y)
    print(f'{Y:3d}   {pB:4d}     {eLB:6d}     K_{qB:<3d}  {V.crK(qB):6d}  {crB2:6d}  {crD:6d}  {tot:6d}')
print(f'minimum over Y: {best[0]} at Y = {best[1]}   (Z(29) = {K.Z})')
