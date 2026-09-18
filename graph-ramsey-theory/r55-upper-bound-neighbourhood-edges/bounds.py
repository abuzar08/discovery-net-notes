"""The bounds registry, and the check that code is using the strongest one.

principal-1, pass 44: *"recording that your first version ignored your own
<= 22 theorem -- the exact failure you diagnosed in another lane two passes
earlier -- is worth more than the caps table, because it establishes that the
rule does not self-apply and needs to be a step in a procedure rather than a
principle in a note.  Work out what that step looks like concretely."*

Here is the concrete step.

THE FAILURE, STATED MECHANICALLY.  A bound is proved in one artifact and then
used by code written for a different row.  The code hard-codes whatever value
was current when it was written.  Nothing connects the two, so when the bound
improves the old number survives in the new row's code and the row is sized too
loosely.  Re-reading the note does not help, because the note is not what the
code consults.

THE FIX.  Put every bound in `BOUNDS.json` with its scope, have code call
`cap(orbit_size, group, n)` instead of writing a literal, and provide a check
that FAILS -- exit code, not a printed summary -- when a consumer's effective
cap is weaker than the registry's.  The rule then runs rather than being
remembered.

    python3 bounds.py            # show the registry and check the consumers
    python3 bounds.py --mutate   # prove the check can fail
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(HERE, "BOUNDS.json")


def load():
    with open(REGISTRY) as fh:
        return json.load(fh)


def cap(orbit_size, group="any", n=42, reg=None):
    """The strongest registered bound applying to this orbit.

    An entry applies if its orbit size matches, its group is "any" or the one
    given, and its n is "any" or the one given.  The strongest is the minimum,
    which is what makes adding a better bound automatically tighten every
    consumer instead of only the artifact that proved it.
    """
    reg = reg or load()
    best, why = None, None
    for e in reg["entries"]:
        if e["orbit_size"] != orbit_size:
            continue
        if e["group"] != "any" and e["group"] != group:
            continue
        if e["n"] != "any" and e["n"] != n:
            continue
        if best is None or e["bound"] < best:
            best, why = e["bound"], e["source"]
    return best, why


def consumers():
    """What each consumer in this directory should be using.

    Listed explicitly rather than scraped, because the point is to state the
    contract: this file uses a bound for that orbit, and here is the scope.
    """
    return [
        ("order8_exact.py", "cap_of", 4, "any", 42),
        ("order8_exact.py", "cap_of", 8, "cyclic", 42),
        ("order8_exact.py", "cap_of", 8, "elementary_abelian", 42),
        ("order8.py", "orbit_cap", 4, "any", 42),
        ("orbitbound.py", "z4_types/klein_actions", 4, "any", 42),
    ]


def effective_cap(module, orbit_size, group, n):
    """What the consumer actually computes, by calling it."""
    sys.path.insert(0, HERE)
    if module in ("order8.py", "order8_exact.py"):
        import order8 as O8
        mod = __import__(module[:-3])
        els = dict(O8.groups_of_order_8())
        name = {("cyclic", 8): "Z_8",
                ("elementary_abelian", 8): "Z_2^3",
                ("any", 4): "Z_4 x Z_2"}[(group, orbit_size)]
        tab = O8.table(els[name])
        fn = getattr(mod, "cap_of", None) or getattr(mod, "orbit_cap")
        best = None
        for H in O8.subgroups(tab):
            if 8 // len(H) != orbit_size:
                continue
            v = fn(tab, H)
            if v is not None and (best is None or v < best):
                best = v
        return best
    if module == "orbitbound.py":
        import orbitbound as OB
        # the effective cap is the largest c_1 the reduced Z_4 list allows
        return max(t[0] for t in OB.z4_types(cap(4, "any", 42)[0]))
    raise SystemExit(f"no probe for {module}")


def check(verbose=True):
    reg = load()
    bad = []
    if verbose:
        print("REGISTRY\n")
        print("   orbit  group                 n     bound   source")
        for e in reg["entries"]:
            sup = "   (supersedes " + e["supersedes"] + ")" \
                if "supersedes" in e else ""
            print(f"   {e['orbit_size']:5d}  {e['group']:20s} "
                  f"{str(e['n']):5s} {e['bound']:7d}   {e['source']}{sup}")
        print("\nCONSUMERS\n")
        print("   file                 orbit  group                 "
              "registry  in use")
    for module, fn, size, group, n in consumers():
        want, src = cap(size, group, n, reg)
        got = effective_cap(module, size, group, n)
        ok = got is not None and got <= want
        if not ok:
            bad.append((module, size, group, want, got))
        if verbose:
            print(f"   {module:20s} {size:5d}  {group:20s} "
                  f"{want:8d}  {got}"
                  + ("" if ok else "   <-- STALE, weaker than the registry"))
    if verbose:
        print()
        if bad:
            print(f"   FAIL: {len(bad)} consumer(s) using a weaker bound than "
                  f"this lane has proved.")
            for m, s, g, w, go in bad:
                print(f"     {m}: orbit {s} ({g}) uses {go}, registry has {w}")
        else:
            print("   PASS: every consumer is using the strongest registered "
                  "bound.")
    return not bad


def mutate():
    """A check that cannot fail proves nothing.

    Reintroduce the *actual* pass-59 defect -- a consumer hard-coding the
    arithmetic 26 at orbit size 4 instead of consulting the registry -- and
    require `check` to report it and return False.  Testing that the registry
    lookup changes when you delete an entry would not be a test of the check;
    this is.
    """
    print("MUTATION TEST -- would this check have caught the pass-59 defect?\n")
    sys.path.insert(0, HERE)
    import order8_exact as OE
    import order8 as O8

    clean = check(verbose=False)
    print(f"   unmutated:                          check passes: {clean}")

    original = OE.cap_of

    def defective(tab, H):
        """Exactly what I wrote at pass 59: the raw lemma, no registry."""
        m, perms = O8.coset_action(tab, H)
        if m == 1:
            return None
        import orbitbound as OB
        b, _, _ = OB.orbit_bound(perms, m, 5, 5)
        return b                                   # the missing min(b, 22)

    OE.cap_of = defective
    caught = not check(verbose=False)
    OE.cap_of = original
    restored = check(verbose=False)

    print(f"   with the pass-59 defect reinstated: check FAILS:  {caught}")
    print(f"   after restoring:                    check passes: {restored}")
    ok = clean and caught and restored
    print("\n   " + ("The check is discriminating: it passes on the real code,"
                     "\n   fails on the exact defect that shipped, and recovers."
                     if ok else "MUTATION TEST FAILED -- the check is "
                     "decorative."))
    return ok


def main():
    if "--mutate" in sys.argv:
        return 0 if mutate() else 1
    return 0 if check() else 1


if __name__ == "__main__":
    sys.exit(main())
