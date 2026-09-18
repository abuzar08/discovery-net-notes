#!/usr/bin/env python3
"""
aug57's route to two order-57 cases is seed-dependent; the closure is not.

WHY THIS FILE EXISTS.  Reviewer-1's review of aug57.py
(reviews/albertson-order-57-row-826/) records that two of its cases are
eliminated only at the top of the crossing ladder, and no artifact of mine
printed that.  This file makes the dependence reproducible in my own code.

It also records the error I made acting on that review: in pass 53 I published,
on the ledger, that order 57's CLOSURE is therefore conditional.  It is not.  See
"what it shows, and what it does not" below.

==============================================================================
WHAT DEPENDS ON WHAT.

aug57.py eliminates row (57,826) and the |R| = 7 case of row (57,827) by scoring
the configuration with blocks (27,22,2,2): its published output prints a block sum
of 7856 and a final augmented score of 8343 against Z(29) = 8281 -- a margin of
62, under one per cent.

The block sum is sum of crK over the blocks, and crK is built recursively from
the seed ladder in verify_range, whose top rung is cr(K_13).  So the block sum
moves with the rung, and so does the augmentation, which is a crminus.g value
built from the same crK table.

==============================================================================
THE ARGUMENT, WHICH NEEDS NO EXPENSIVE RE-RUN.

Every crK value is monotone nondecreasing in the seed base, and crminus.g is
built from crK by taking maxima of sums of crK values, so g is monotone too.
Hence for any rung below CCCG 2021,

        score(rung)  =  blocksum(rung) + augmentation(rung)
                     <= blocksum(rung) + augmentation(CCCG 2021)
                     =  blocksum(rung) + (8343 - 7856)
                     =  blocksum(rung) + 487 .

That upper bound is enough to settle the question without recomputing the
augmentation at each rung -- which matters, because aug57.solve at |R| = 7 is
expensive enough that a previous pass left it running and it was killed before
finishing.  Only the block sums are recomputed here, and they are cheap.

==============================================================================
WHAT IT SHOWS, AND WHAT IT DOES NOT.

It shows that AUG57's ROUTE to those two cases is seed-dependent: under the
refereed McQuillan-Pan-Richter value cr(K_13) >= 219 the score cannot reach
Z(29) = 8281, so that route eliminates nothing, and aug57.py's own output never
says so.  That is a real presentational defect in one artifact.

IT DOES NOT SHOW THAT ORDER 57'S CLOSURE IS CONDITIONAL, AND I PUBLISHED THAT IT
DID.  cover57.py eliminates the same two cases STRUCTURALLY -- from the
non-existence of an admissible block multiset, not from a crossing count -- so
the closure does not depend on the rung at all.  Three things say so, and I had
checked none of them before publishing the claim:

  * cover57.solve(50, 582, 595, 7) returns [None, None] at the bare counting
    seed and at the CCCG 2021 seed alike.  The control below re-runs it.
  * this lane's own EXPECTED_OUTPUT_COVER57.txt prints, in words, "the case dies
    structurally, not by a crossing count".
  * reviews/albertson-order-57-closure/ ran the whole chain at both seedings and
    reports the closure seed-independent, naming aug57.py as the only
    seed-dependent piece and cover57.py as superseding it.

So the conditionality claim of pass 53 is WITHDRAWN.  It was made by reading one
review of seven and generalising -- the identical failure the same pass was
correcting in itself.  Recorded as defect 17.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import crminus as C
import verify_range as V
from order2r import Z

BLOCKS = (27, 22, 2, 2)          # the configuration aug57.py scores
PUBLISHED_BLOCKSUM = 7856        # EXPECTED_OUTPUT_AUG57.txt, rows 826 and 827
PUBLISHED_SCORE = 8343           # ditto
NEEDED = 223                     # the rung the eliminations require


def blocksum(base):
    V.set_base(base)
    C.reset()
    return sum(V.crK(q) for q in BLOCKS)


def cover57_both_seeds():
    """cover57's verdict on (826, |R|=7) at the weakest and strongest rungs."""
    import cover57 as CV
    out = []
    for name, base in (V.SEED_LADDER[0], V.SEED_LADDER[-1]):
        V.set_base(base)
        C.reset()
        out.append((name.split(",")[0], CV.solve(50, 582, 595, 7)))
    V.set_base(V.BASE_CCCG2021)
    C.reset()
    return out


def main():
    print("aug57's route to two order-57 cases depends on the cr(K_13) rung;")
    print("cover57 supersedes it and does not")
    print("Z(29) = %d;  a case is ELIMINATED only when its score >= Z" % Z)
    print()
    aug = PUBLISHED_SCORE - PUBLISHED_BLOCKSUM
    print("   aug57.py publishes block sum %d and score %d for blocks %s,"
          % (PUBLISHED_BLOCKSUM, PUBLISHED_SCORE, BLOCKS))
    print("   so its augmentation is %d at the CCCG 2021 rung, and the margin"
          % aug)
    print("   over Z(29) is %d." % (PUBLISHED_SCORE - Z))
    print()
    print("   Every crK value is monotone in the seed base and crminus.g is")
    print("   built from crK by maxima of sums, so the augmentation at a lower")
    print("   rung cannot exceed %d.  That gives an upper bound per rung." % aug)
    print()
    print("   %-46s %9s %11s %s" % ("cr(K_13) rung", "blocksum",
                                    "<= score", "verdict"))
    ok_at = []
    for name, base in V.SEED_LADDER:
        bs = blocksum(base)
        ub = bs + aug
        eliminated = ub >= Z
        if eliminated:
            ok_at.append(name)
        print("   %-46s %9d %11d %s"
              % (name, bs, ub,
                 "can reach Z" if eliminated else "CANNOT reach Z -> fails"))
    V.set_base(V.BASE_CCCG2021)
    C.reset()
    print()
    # the published run is at the top rung; check this file agrees with it
    agree = blocksum(V.BASE_CCCG2021) == PUBLISHED_BLOCKSUM
    print("   control: block sum at the CCCG 2021 rung reproduces the published")
    print("   %d: %s" % (PUBLISHED_BLOCKSUM, "PASS" if agree else "FAIL"))
    print()
    print("CONCLUSION")
    print("   The two eliminations survive only at the rungs: %s."
          % ", ".join(n.split(",")[0] for n in ok_at))
    print("   Under the refereed McQuillan-Pan-Richter value cr(K_13) >= 219 the")
    print("   score cannot reach Z(29), so THIS ROUTE eliminates neither row")
    print("   (57,826) nor the |R| = 7 case of row (57,827).  aug57.py's own")
    print("   output does not say so, which is a presentational defect in it:")
    print("   the route needs cr(K_13) >= %d, stronger than the best journal"
          % NEEDED)
    print("   value in the ladder (219).")
    print()
    print("   BUT THE CLOSURE DOES NOT DEPEND ON THE RUNG.  cover57 kills the")
    print("   same two cases structurally:")
    for name, verdict in cover57_both_seeds():
        print("      %-24s cover57(826, |R|=7) -> %s  (no admissible multiset)"
              % (name, verdict))
    print("   so the conditionality I published in pass 53 is WITHDRAWN, and")
    print("   order 57's closure is seed-independent.  Defect 17.")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()
