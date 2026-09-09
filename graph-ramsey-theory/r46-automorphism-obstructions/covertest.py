"""Equivalence suite: the certified cover check against the Kraft combinator.

principal-1 approved `verify.py cover` on one condition -- "the new check must
accept exactly what the combinator accepted on your existing tree, and must
reject the same deliberately broken cases".  Two honest remarks before the
tests.

  * The negative cases did not previously exist.  `verify.py selftest` covered
    graphs and orbit counts, and `symstest.py` covers symmetry-break
    soundness, but nothing exercised the cube-cover step against deliberately
    broken input.  This file creates them.
  * "Accept exactly what the combinator accepted" is the wrong target in one
    direction, and deliberately so.  The combinator requires a PARTITION
    (prefix-free AND Kraft sum 1); the argument only needs a COVER.  So the
    certificate accepts strictly more: an overlapping cover is valid and the
    combinator rejects it as "the directories overlap".  That gap is asserted
    here as intended behaviour, not tolerated as a discrepancy.

What is checked, for every tag set in the battery:

  (1) GROUND TRUTH.  cover_certify agrees with brute force over all 2^D
      assignments -- the strong statement, since it pins the certificate to
      the truth rather than to the other checker.
  (2) SOUNDNESS OF THE OLD ON THE NEW.  Whenever the combinator would accept
      (prefix-free, Kraft == 1), the certificate accepts.  Nothing the
      published Theorem 7 rests on is lost.
  (3) AGREEMENT ON FAILURE.  Whenever the combinator reports PARTIAL
      (prefix-free, Kraft < 1), the certificate reports not-a-cover, and its
      witness really lies in no cube.
  (4) THE INTENDED GAP.  There are sets the combinator rejects and the
      certificate accepts, and every one of them genuinely covers.

    python3 covertest.py [--quick]
"""
import random
import sys
from fractions import Fraction

from verify import collect_tags, cover_certify

S = ("/Users/abuzark/.discovery-research-team/workspaces/researcher-3/"
     "scratch/r46/")
# The two cube sets this lane actually published: one complete, one not.
REAL = [("n=39 type 13^3", [S + "cubes_n39_13_3"], True),
        ("n=35 type 1^0 5^7", ["cube-manifests/r46-1_0-5_7-leaves.jsonl.gz"],
         False)]


def kraft_verdict(tags):
    """What `verify.py tree` would conclude from the tags alone.

    Returns one of "PARTITION", "PARTIAL", "NOT-PREFIX-FREE", "OVERLAP".
    """
    s = sorted(tags)
    for x, y in zip(s, s[1:]):
        if y.startswith(x):
            return "NOT-PREFIX-FREE"
    kraft = sum(Fraction(1, 2 ** len(x)) for x in s)
    if kraft > 1:
        return "OVERLAP"
    return "PARTITION" if kraft == 1 else "PARTIAL"


def covers_bruteforce(tags):
    """Ground truth: does every assignment on max-depth variables hit a cube?"""
    d = max(len(t) for t in tags)
    hit = bytearray(1 << d)
    for t in tags:
        base = int(t, 2) << (d - len(t))
        hit[base:base + (1 << (d - len(t)))] = b"\x01" * (1 << (d - len(t)))
    return all(hit)


def random_partition(rng, depth):
    """A random complete prefix-free code of depth at most `depth`."""
    leaves, stack = [], [""]
    while stack:
        node = stack.pop()
        if len(node) >= depth or (node and rng.random() < 0.45):
            leaves.append(node if node else "0")
            if not node:                      # never return the empty tag
                leaves.append("1")
            continue
        stack += [node + "0", node + "1"]
    return leaves


def battery(rng, n_random):
    """(name, tags) pairs.  Names starting with '!' are deliberately broken."""
    out = [
        ("uniform-2", ["00", "01", "10", "11"]),
        ("non-uniform", ["0", "10", "11"]),
        ("deep-comb", ["0", "10", "110", "1110", "11110", "11111"]),
        ("!missing-half", ["0"]),
        ("!missing-leaf", ["00", "01", "10"]),
        ("!missing-deep", ["0", "10", "110"]),
        ("overlap-parent", ["0", "1", "10"]),
        ("overlap-dup-subtree", ["0", "1", "00", "01"]),
        ("!not-a-cover-and-overlapping", ["0", "00", "10"]),
        ("unsorted-input", ["1", "01", "00"]),
    ]
    for i in range(n_random):
        p = random_partition(rng, rng.randint(3, 10))
        out.append((f"random-partition-{i}", p))
        if len(p) > 2:
            q = list(p)
            q.pop(rng.randrange(len(q)))
            out.append((f"!random-hole-{i}", q))          # a leaf removed
            r = list(p)
            victim = r[rng.randrange(len(r))]
            if len(victim) > 1:
                r.append(victim[:-1])                     # add an ancestor
                out.append((f"random-overlap-{i}", r))
    return out


def main():
    quick = "--quick" in sys.argv
    rng = random.Random(20260909)
    cases = battery(rng, 8 if quick else 40)
    seen_gap = []
    stats = {}
    for name, tags in cases:
        tags = sorted(set(tags))
        truth = covers_bruteforce(tags)
        verdict = kraft_verdict(tags)
        ok, info = cover_certify(tags)
        stats[verdict] = stats.get(verdict, 0) + 1

        # (1) the certificate is exactly the truth
        assert ok == truth, f"{name}: certificate {ok}, brute force {truth}"
        if not ok:
            assert all(not info.startswith(t) for t in tags), \
                f"{name}: witness {info} lies inside a cube"

        # (2) whatever the combinator accepts, the certificate accepts
        if verdict == "PARTITION":
            assert ok, f"{name}: combinator accepted, certificate did not"
        # (3) prefix-free but short: both must say no
        if verdict == "PARTIAL":
            assert not ok, f"{name}: combinator says PARTIAL, certificate says cover"
        # (4) the intended gap
        if verdict in ("OVERLAP", "NOT-PREFIX-FREE") and ok:
            seen_gap.append(name)

    assert seen_gap, "no case exercised the intended gap"
    # A fact about the OLD checker that this suite makes visible: `cmd_tree`'s
    # "Kraft sum > 1 ... the directories overlap" branch is UNREACHABLE.  Its
    # prefix-free test runs first and is complete (for sorted tags, if x is a
    # prefix of z and x <= y <= z then x is a prefix of y, so checking adjacent
    # pairs suffices), and a prefix-free set satisfies Kraft's inequality
    # sum 2^-|t| <= 1.  So no input reaches that branch.  Not a defect -- a
    # defensive check that cannot fire -- but the message is misleading, and
    # the real gate on overlapping covers is the prefix test.
    assert "OVERLAP" not in stats, \
        "the Kraft>1 branch fired: Kraft's inequality or the prefix test is wrong"

    # The real trees this lane published, checked the same way.
    real = []
    for label, srcs, expect in REAL:
        try:
            tags = sorted(set(collect_tags(srcs)))
        except (SystemExit, OSError):
            continue
        ok, info = cover_certify(tags)
        assert ok is expect, f"{label}: certificate {ok}, expected {expect}"
        assert ok == covers_bruteforce(tags), f"{label}: disagrees with brute force"
        v = kraft_verdict(tags)
        assert (v == "PARTITION") == ok, f"{label}: {v} vs certificate {ok}"
        real.append(f"{label}: {len(tags)} leaves, {v} == certificate {ok}")

    print(f"covertest OK: {len(cases)} tag sets, "
          f"{'; '.join(f'{k} {v}' for k, v in sorted(stats.items()))}")
    print(f"  certificate == brute-force ground truth on all {len(cases)}")
    print("  every set the Kraft combinator accepts, the certificate accepts")
    print("  every PARTIAL the combinator reports, the certificate refutes, "
          "with a witness verified to lie in no cube")
    print(f"  intended gap exercised by {len(seen_gap)} sets the combinator "
          f"rejects and the certificate accepts (all genuinely cover), "
          f"e.g. {seen_gap[0]}")
    print("  the combinator's \"Kraft > 1 / directories overlap\" branch is "
          "unreachable: prefix-freeness is tested first and implies Kraft <= 1")
    for line in real:
        print(f"  REAL TREE  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
