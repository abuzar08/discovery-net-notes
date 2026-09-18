r"""reviewer-1: arithmetic checks on the nu_tri <= 2 measurement at order 58."""
from math import comb

print('arithmetic checks:')
print('   C(58,2) =', comb(58, 2), '-> e(H) = 1653 - m gives',
      [1653 - m for m in (838, 839, 840)], '(published 815, 814, 813)')
print('   H - B has 58 - 6 = 52 vertices; Mantel floor(52^2/4) =', 52 * 52 // 4,
      '(published 676)')
print('   six vertices of B at d_H <= 29: 6 x 29 =', 6 * 29, '(published 174)')
print('   the two triangles inside B counted twice: 676 + 174 - 6 =',
      676 + 174 - 6, '(published 844)')
print('   shortfall against the largest e(H): 844 - 815 =', 844 - 815,
      '(published about 30)')
print()
print('   the tail table sums to', 1184 + 1028 + 1464, '(the residual is 3676)')
print('   the example (21,8,7,2,2): all but the two largest give 7 + 2 + 2 =',
      7 + 2 + 2, '(published 11)')
print()
print('the criterion, re-derived: nu_tri <= 2 means two triangles meet every')
print('   triangle, so the 6-set B they span leaves H - B triangle-free;')
print('   private vertices of three distinct blocks form a triangle of H, so at')
print('   most two blocks keep a private vertex outside B and every other')
print('   block has its private vertices inside B, whence the tail is at most 6')
print('   and a tail of 7 or more certifies nu_tri >= 3')
