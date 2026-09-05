"""Brute-force semantic test of (a) hybrid.py's Totalizer-based `card` and
(b) reviewer-1's Sinz-based `card`: for small literal lists (with repeats and
negative literals) and every assignment of inputs/guard, the auxiliary clauses
must be extendable iff the cardinality constraint holds."""
import sys, itertools, random
sys.path.insert(0, sys.argv[1])          # path to the published artifact (hybrid.py)
from hybrid import Totalizer
from indep_hybrid import Sinz


def sat_extend(clauses, fixed, aux):
    """Does an assignment of aux vars exist satisfying clauses under `fixed`?"""
    assign = dict(fixed)
    def value(l):
        v = assign.get(abs(l))
        return None if v is None else (v if l > 0 else not v)
    def rec(i):
        # unit propagation-free naive DPLL over aux list
        for c in clauses:
            vals = [value(l) for l in c]
            if all(v is False for v in vals):
                return False
        if i == len(aux):
            return True
        for b in (False, True):
            assign[aux[i]] = b
            if rec(i + 1):
                return True
        del assign[aux[i]]
        return False
    return rec(0)


def their_card(lits, lo, hi, cond, nv):
    tot = Totalizer(nv)
    outs = tot.build(list(lits))
    extra = []
    if hi < len(lits):
        extra.append([-outs[hi]] if cond is None else [-cond, -outs[hi]])
    if lo >= 1:
        extra.append([outs[lo - 1]] if cond is None else [-cond, outs[lo - 1]])
    return tot.clauses + extra, list(range(nv + 1, tot.nv + 1))


def my_card(lits, lo, hi, cond, nv):
    S = Sinz(nv)
    S.card(lits, lo, hi, cond)
    return S.cls, list(range(nv + 1, S.nv + 1))


random.seed(1)
tests = 0
for trial in range(400):
    nin = random.randint(1, 5)             # base variables 1..nin (+ guard var)
    m = random.randint(1, 6)               # literal list length (repeats allowed)
    lits = [random.choice([1, -1]) * random.randint(1, nin) for _ in range(m)]
    use_cond = random.random() < 0.5
    cond = (nin + 1) * random.choice([1, -1]) if use_cond else None
    nv = nin + 1
    lo = random.randint(0, m); hi = random.randint(lo, m)
    for name, fn in (('totalizer', their_card), ('sinz', my_card)):
        cls, aux = fn(lits, lo, hi, cond, nv)
        for bits in itertools.product([False, True], repeat=nv):
            fixed = {i + 1: bits[i] for i in range(nv)}
            cnt = sum(1 for l in lits if (fixed[abs(l)] if l > 0 else not fixed[abs(l)]))
            guard_on = True if cond is None else (fixed[abs(cond)] if cond > 0 else not fixed[abs(cond)])
            expect = (not guard_on) or (lo <= cnt <= hi)
            got = sat_extend(cls, fixed, aux)
            assert got == expect, (name, lits, lo, hi, cond, fixed, cnt, got, expect)
            tests += 1
print(f"{tests} (encoding, assignment) cases agree with the cardinality semantics")
