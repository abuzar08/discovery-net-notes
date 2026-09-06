r"""reviewer-1: three supplementary checks on h3295.

  (a) symS at p = 2 — the contribution asserts it is sound and non-vacuous
      there; my completeness test is run at p = 2 as well;
  (b) a witness that symK does NOT subsume symC, which `encode.py` asserts
      when it says "Do not enable both: symK subsumes symC";
  (c) the clause and group-order arithmetic of the body.
"""
import itertools, sys, os
from indep_syms import (orbits, phi_shift, phi_cycle, induced, act, sym_s,
                        sym_c, internal_code)

print('(a) symS at p = 2, completeness of the break')
for (f, p, k) in [(0, 2, 3), (0, 2, 4), (1, 2, 3)]:
    oid, norb = orbits(f, p, k)
    gs = [tuple(induced(phi_shift(f, p, k, b), oid, norb))
          for b in itertools.product(range(p), repeat=k)]
    order = len(set(gs))
    unc = sum(1 for x in itertools.product((0, 1), repeat=norb)
              if not any(sym_s(f, p, k, oid, act(g, x)) for g in gs))
    surv = sum(1 for x in itertools.product((0, 1), repeat=norb)
               if sym_s(f, p, k, oid, x))
    print(f'  f={f} p={p} k={k}: {norb} orbits, induced group order {order} '
          f'(p^(k-1) = {p ** (k - 1)}), uncovered {unc}, survivors {surv} '
          f'of {2 ** norb}')

print('(b) does symK subsume symC?')
for (f, p, k) in [(0, 3, 2), (0, 5, 2), (0, 3, 3)]:
    oid, norb = orbits(f, p, k)
    kmaps = [tuple(induced(phi_cycle(f, p, k, tau), oid, norb))
             for tau in itertools.permutations(range(k))]
    wit = None
    for x in itertools.product((0, 1), repeat=norb):
        ok_k = all(list(act(g, x)) <= list(x) for g in kmaps)
        if ok_k and not sym_c(f, p, k, oid, x):
            wit = x
            break
    if wit is None:
        print(f'  f={f} p={p} k={k}: no witness — symK implies symC here')
    else:
        codes = [internal_code(f, p, k, oid, wit, j) for j in range(k)]
        print(f'  f={f} p={p} k={k}: witness {"".join(map(str, wit))} '
              f'satisfies symK but not symC (internal codes {codes})')

print('(c) arithmetic')
def chain_clauses(p):
    # one ordering clause per position; aux definitions 4 at the first, 5 after
    return p + (4 + 5 * (p - 2) if p >= 2 else 0)
for (p, k, name) in [(7, 5, '1^0 7^5'), (2, 18, '1^0 2^18')]:
    n = (k - 1) * (p - 1) * 1
    print(f'  {name}: {(k-1)*(p-1)} lex chains x {chain_clauses(p)} clauses = '
          f'{(k-1)*(p-1)*chain_clauses(p)}; group broken p^(k-1) = {p**(k-1)}')
for (p, k) in [(7, 6), (5, 8), (3, 14)]:
    print(f'  transfer table p={p} k={k}: p^(k-1) = {p**(k-1)}')
