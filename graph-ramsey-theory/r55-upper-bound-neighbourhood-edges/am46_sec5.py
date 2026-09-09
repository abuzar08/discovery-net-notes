"""Check the finite content of Section 5 of Angeltveit-McKay, R(5,5) <= 46.

Companion to `am46.py`, which checked Section 4.  Section 5 (Proposition
"gluered") reduces the gluing work to five cases.  Its proof is a dense case
analysis; most of it depends on censuses I cannot recompute here, but three
pieces are finite arithmetic and are checked below.

  (A) THE WEIGHTS.  The proof opens with alpha = 5 m_1 + 2 m_2 + m_3 and
      "excess(F) >= 46 - alpha - beta".  The coefficients 5, 2, 1 must be the
      largest amount by which a graph in E_1, E_2, E_3 can push its vertex's
      contribution below 1.  That is arithmetic on E(4,5,m), so it is checked.

  (B) THE FOUR-SET RELATION.  Three times the proof writes

          sum |A_i| = 2 sum |A_ij| - 3 sum |A_ijk|                     (*)

      for A_1..A_4 the neighbourhoods of a 4-clique.  As an EQUALITY this is
      false in general.  Writing x_s for the number of outside vertices
      adjacent to exactly s of the four, (*) demands s = 2*C(s,2) - 3*C(s,3)
      for every s that occurs, which holds for s = 0, 2, 3 and fails for
      s = 1 (1 vs 0) and s = 4 (4 vs 0).  Since no vertex is adjacent to all
      four (that would be a K_5), x_4 = 0; but x_1 is unconstrained.

      The general truth is the INEQUALITY sum |A_i| >= 2 sum |A_ij| -
      3 sum |A_ijk|, and this file checks that (i) equality genuinely fails,
      (ii) the inequality always holds, and (iii) BOTH places the paper uses
      (*) it is used in the direction where the inequality suffices, so the
      bounds obtained are valid.  A misstated lemma with a sound use.

  (C) THE THREE NUMERIC CONTRADICTIONS.  Each case ends by comparing a lower
      bound on |union A_i| with an upper bound.  Given only the hypotheses
      stated in the text, is the contradiction actually forced?  This is an
      integer feasibility question in (x_1, x_2, x_3) and is decided here by
      exhaustive search rather than by following the prose.

    python3 am46_sec5.py
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# E_i as in Section 5, using the corrected C_3 (see AM46-SECTION4.md).
LEVELS = {
    1: [("A", 24, 127, None), ("B1", 23, 121, None)],
    2: [("B2", 23, 120, 120), ("C2", 22, 114, 114)],
    3: [("B3", 23, 119, 119), ("C3", 22, 113, 113), ("D3", 21, 107, 107)],
}
# threshold b_m in the Section 4 regrouping, indexed by the ORDER of the graph
THRESHOLD = {24: 127, 23: 118, 22: 112, 21: 106}


def weights(emax):
    """Largest deficiency (threshold - e) magnitude over each level."""
    out = {}
    for i, members in LEVELS.items():
        worst = 0
        for _, m, lo, hi in members:
            top = emax[m] if hi is None else hi
            worst = max(worst, top - THRESHOLD[m])
        out[i] = worst
    return out


def counts(x1, x2, x3, x4=0):
    """(sum|A_i|, sum|A_ij|, sum|A_ijk|, |union A_i|) from the profile x_s."""
    sA = x1 + 2 * x2 + 3 * x3 + 4 * x4
    sAij = x2 + 3 * x3 + 6 * x4
    sAijk = x3 + 4 * x4
    union = x1 + x2 + x3 + x4
    return sA, sAij, sAijk, union


def check_relation(cap=12):
    """(B) equality fails, inequality holds, and both uses stay valid."""
    eq_fail = ineq_fail = 0
    use1_fail = use2_fail = 0
    for x1, x2, x3 in itertools.product(range(cap), repeat=3):
        sA, sAij, sAijk, union = counts(x1, x2, x3)
        if sA != 2 * sAij - 3 * sAijk:
            eq_fail += 1
        if sA < 2 * sAij - 3 * sAijk:
            ineq_fail += 1
        # use 1 (case m_2 = 4):  |union| >= (2/3) sum|A_i| - (1/3) sum|A_ij|
        if 3 * union < 2 * sA - sAij:
            use1_fail += 1
        # use 2 (cases m_2 = 2, 0):  |union| >= (1/2) sum|A_i| - (1/2) sum|A_ijk|
        if 2 * union < sA - sAijk:
            use2_fail += 1
    return eq_fail, ineq_fail, use1_fail, use2_fail


def structural_bounds():
    """Elementary caps on the A-sets, from F having no K_5 and no independent 5-set.

    Let {w_1..w_4} be a 4-clique of F and let the A_i be neighbourhoods of the
    w_i inside a set disjoint from the clique.

      * A vertex adjacent to all four gives a K_5, so x_4 = 0.
      * The common neighbourhood of a TRIPLE is independent (two adjacent
        members plus the triple make a K_5), so it has at most 4 vertices, and
        summing over the 4 triples, sum|A_ijk| <= 16.
      * The common neighbourhood of a PAIR has no triangle (a triangle plus the
        pair is a K_5) and no independent 5-set, so it is a (3,5)-graph and has
        at most R(3,5) - 1 = 13 vertices; summing, sum|A_ij| <= 78.
      * A single A_i has no K_4 and no independent 5-set, so it is a
        (4,5)-graph: |A_i| <= R(4,5) - 1 = 24.
    """
    return {"per_triple": 4, "sum_Aijk": 16, "per_pair": 13,
            "sum_Aij": 78, "per_A": 24}


def feasible(sA_min, union_max, per_pair_max=None, cap=40, use_structure=True):
    """(C) Is there an integer profile meeting the stated hypotheses?

    Returns a witness tuple or None.  x_4 = 0 throughout (no K_5).  With
    `use_structure` the elementary caps of `structural_bounds` are imposed too,
    so a surviving witness is not merely an arithmetic artefact.
    """
    B = structural_bounds()
    for x1, x2, x3 in itertools.product(range(cap), repeat=3):
        sA, sAij, sAijk, union = counts(x1, x2, x3)
        if sA < sA_min or union > union_max:
            continue
        if per_pair_max is not None and sAij > 6 * per_pair_max:
            continue
        if use_structure and (sAijk > B["sum_Aijk"] or sAij > B["sum_Aij"]):
            continue
        return (x1, x2, x3, sA, sAij, sAijk, union)
    return None


def endgame():
    """(D) The closing paragraph of Proposition 5.3, checked exhaustively.

    Suppose F in R(5,5,46) does NOT satisfy the conclusion.  The paragraph then
    has available:

        (i)  alpha + beta >= 46 + max(n_21 - mbar_1, 0) + max(nbar_21 - m_1, 0)
        (ii) claim 1: alpha >= 21  =>  m_1 <= 2   (and dually)
        (iii) claim 2: alpha >= 23  =>  (alpha, m_1, n_21) = (23, 2, 13)
                                        or (m_1 <= 1 and n_21 >= alpha - 21)
        (iv) m_1, mbar_1 <= 4, and n_21 <= alpha, nbar_21 <= beta
        (v)  WLOG alpha >= beta, and alpha + beta >= 46 gives alpha >= 23

    Claims 1 and 2 are proved earlier by arguments this file does not check.
    Given them, is the system satisfiable?  Every integer state is enumerated.
    Returns (n_with_excess, n_without_excess, examples_without).
    """
    with_ex, coarse, without_ex, examples = 0, 0, 0, []
    for alpha in range(23, 47):
        for beta in range(0, alpha + 1):
            for m1 in range(5):
                if alpha >= 21 and m1 > 2:
                    continue
                for mb1 in range(5):
                    if beta >= 21 and mb1 > 2:
                        continue
                    for n21 in range(alpha + 1):
                        if not ((alpha, m1, n21) == (23, 2, 13)
                                or (m1 <= 1 and n21 >= alpha - 21)):
                            continue
                        for nb21 in range(beta + 1):
                            if beta >= 23 and not (
                                    (beta, mb1, nb21) == (23, 2, 13)
                                    or (mb1 <= 1 and nb21 >= beta - 21)):
                                continue
                            without_ex += 1
                            if alpha + beta >= 46:
                                coarse += 1
                                if len(examples) < 3:
                                    examples.append((alpha, beta, m1, mb1,
                                                     n21, nb21))
                            if alpha + beta >= (46 + max(n21 - mb1, 0)
                                                + max(nb21 - m1, 0)):
                                with_ex += 1
    return with_ex, coarse, without_ex, examples


def main():
    with open(os.path.join(HERE, "e45.json")) as fh:
        emax = {int(k): v for k, v in json.load(fh)["emax"].items()}

    w = weights(emax)
    print(f"(A) level weights derived from E(4,5,m): {w}")
    if w != {1: 5, 2: 2, 3: 1}:
        raise SystemExit(f"weights {w} do not match the paper's 5, 2, 1")
    print("    match alpha = 5 m_1 + 2 m_2 + m_3.  The 5 is E(4,5,24) - 127 "
          f"= {emax[24]} - 127 = {emax[24] - 127}; B_1 gives only "
          f"{emax[23]} - 118 = {emax[23] - 118}.")
    print("    E_3 has weight 1 only because every member sits exactly one "
          "above its threshold")
    print("    (119=118+1, 113=112+1, 107=106+1) -- which is the same reason "
          "C_3 must be at 22 vertices.\n")

    eqf, inf_, u1, u2 = check_relation()
    print("(B) over all profiles (x1,x2,x3) < 12 with x4 = 0:")
    print(f"    'sum|A_i| = 2 sum|A_ij| - 3 sum|A_ijk|' FAILS on {eqf} of "
          f"{12**3} -- it is not an identity")
    print(f"    the inequality '>=' fails on {inf_} -- it always holds")
    print(f"    use 1, |U| >= (2 sum|A_i| - sum|A_ij|)/3 : fails on {u1}")
    print(f"    use 2, |U| >= (sum|A_i| - sum|A_ijk|)/2 : fails on {u2}")
    if inf_ or u1 or u2:
        raise SystemExit("a use of the relation is NOT valid under '>='")
    print("    so both uses need only '>=', and the bounds obtained are "
          "sound.  Smallest counterexample")
    print("    to the equality: one outside vertex adjacent to exactly one "
          "of the four (x1=1), giving 1 vs 0.\n")

    print("(C) are the three closing contradictions forced by the stated "
          "hypotheses alone?")
    cases = [
        ("m_2 = 4", 44, 15, 7,
         "|A_i| >= 11 each, |A_ij| <= 7 each, |union| = 19 - 4 = 15"),
        ("m_2 = 2", 63, 25, None,
         "sum|A_i| >= 63, |union| <= 46 - 21 = 25"),
        ("m_2 = 0", 60, 23, None,
         "sum|A_i| >= 60, |union| <= 46 - 23 = 23"),
    ]
    B = structural_bounds()
    print(f"    elementary caps proved here: sum|A_ijk| <= {B['sum_Aijk']} "
          f"(<= {B['per_triple']} per triple, its common neighbourhood is "
          f"independent),")
    print(f"    sum|A_ij| <= {B['sum_Aij']} (<= {B['per_pair']} per pair, a "
          f"(3,5)-graph), |A_i| <= {B['per_A']}.")
    for name, sA_min, union_max, pair_max, why in cases:
        wit = feasible(sA_min, union_max, pair_max)
        need = sA_min - 2 * union_max - 1     # sum|A_ijk| <= need closes it
        if wit is None:
            print(f"    {name}: CONTRADICTION FORCED ({why})")
        else:
            x1, x2, x3, sA, sAij, sAijk, union = wit
            print(f"    {name}: NOT forced ({why}).")
            print(f"       witness (x1,x2,x3)=({x1},{x2},{x3}) obeying every "
                  f"cap above: sum|A_i|={sA},")
            print(f"       sum|A_ij|={sAij}, sum|A_ijk|={sAijk}, "
                  f"|union|={union} -- no contradiction")
            print(f"       the chain closes iff sum|A_ijk| <= {need}; "
                  f"the elementary cap is {B['sum_Aijk']}, and the text "
                  f"states no sharper one")
    with_ex, coarse, without_ex, ex = endgame()
    print()
    print("(D) the closing paragraph of Proposition 5.3, over every integer "
          "state consistent with")
    print("    its stated inputs (claims 1 and 2 assumed, not checked here):")
    print(f"    states satisfying claims 1 and 2 alone:            "
          f"{without_ex}")
    print(f"    of those, also satisfying alpha + beta >= 46:      {coarse}"
          f"   e.g. (alpha,beta,m1,mbar1,n21,nbar21) = "
          f"{ex[0] if ex else None}")
    print(f"    of those, also satisfying the refined inequality:  {with_ex}")
    if with_ex:
        raise SystemExit("the endgame does NOT close: a state survives")
    print("    ZERO.  So the system is unsatisfiable and the paragraph closes "
          "-- and it closes for a")
    print("    simpler reason than the three-branch argument gives: the "
          "excess inequality alone,")
    print("    against claims 1 and 2, admits no state at all.  Verified, "
          "conditional on those claims.")
    print()
    print("READING.  (A) and (B) are settled: the weights are right, and the "
          "four-set relation is")
    print("misstated as an equality but used only where the inequality "
          "suffices.  (C) is NOT a claim")
    print("that the proposition is wrong -- it is a report that two of its "
          "three closing steps do not")
    print("follow from the hypotheses written down beside them, and that what "
          "is missing in each case")
    print("is an upper bound on sum|A_ijk|.  The bound may well hold for "
          "reasons omitted as routine;")
    print("I could not reconstruct it, and I record that rather than guess.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
