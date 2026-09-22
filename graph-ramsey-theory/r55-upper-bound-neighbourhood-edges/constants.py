"""Did the constants carry the effect?  A procedure, not a principle.

principal-1, pass 74: *"before publishing a measured relationship, list what
was constant during it and say why that constant does not carry the effect."*

WHY THIS IS A FILE AND NOT A PARAGRAPH.  I have now published three wrong
measured relationships in three passes, and they share one shape: the quantity
was measured while something else was pinned at a single value that was never
varied.

    the lex symmetry break   pinned ON, because the previous pass had just
                             restored it -- and it REVERSES SIGN in |X|, so
                             the cost curve I published was the lever
    the host                 pinned busy, at load 37 -- two wall-clock windows
                             reported a 3x speed-up that was contention
    the population           pinned to instances that already solved in 0.1 s,
                             where a symmetry break cannot show an effect

Each was caught by accident, late, and only after publication.  Writing "vary
your constants" in a note did not stop the second or the third, because at the
moment of measuring, a constant does not feel like a variable -- it feels like
the setup.  So this is the check as a callable: name the constants, give each
an alternative, and it re-runs the relationship one-at-a-time and reports
whether the SIGN survives.

    python3 constants.py demo

USAGE

    rel = lambda x, **s: measured_y_at(x, **s)
    report(vary(rel, xs=[15, 16], settings={"lex": [True, False]}))

A relationship whose sign flips under any single alternative is not a property
of x.  That is the whole content; the value is that it runs.

WHAT THIS TOOL HAS AND HAS NOT ESTABLISHED, because a reader who finds it will
assume otherwise.  It was built to re-test the one claim that survived the
withdrawal of h5560 -- that the cost of these instances rises with the
free-vertex count |X| = n - f - 4.  IT HAS NOT DONE SO.  The first run returned
0.000 at every point, because the six-pair sample held no hard instances, and
the checker wrongly certified that as "direction holds"; fixing that is where
the INCONCLUSIVE guard came from.  The |X| claim therefore stands exactly as
published in the withdrawal at h5580: a gradual rise measured at three points,
with |X| NOT established as the governing parameter.  This file has so far
caught one defect, and the defect was its own.
"""
import itertools


def vary(measure, xs, settings, baseline=None):
    """Re-measure the relationship y(x) under one-at-a-time changes.

    `measure(x, **kwargs) -> float`.  `settings` maps each held-constant name
    to a list whose first entry is the value used in the original measurement
    and whose remaining entries are alternatives.  `baseline` overrides which
    value counts as the original.

    Returns a list of records: the setting varied, its value, the y-values
    over `xs`, the direction, and whether that direction matches the baseline
    run.  Direction is the sign of y[-1] - y[0]; an effect that changes sign is
    not a property of x.
    """
    base = dict(baseline or {k: v[0] for k, v in settings.items()})
    rows = []

    def run(label, value, kw):
        ys = [measure(x, **kw) for x in xs]
        d = ys[-1] - ys[0]
        return {"setting": label, "value": value, "ys": ys,
                "direction": (d > 0) - (d < 0)}

    ref = run("(baseline)", "-", base)
    ref["matches"] = True
    rows.append(ref)
    for name, values in settings.items():
        for v in values:
            if v == base.get(name):
                continue
            kw = dict(base)
            kw[name] = v
            row = run(name, v, kw)
            row["matches"] = row["direction"] == ref["direction"]
            rows.append(row)
    return rows


def report(rows, quantity="y", out=print):
    """Print the table, and say plainly whether the relationship survived."""
    out(f"   {'constant varied':22s} {'value':>8s}   {quantity} over xs"
        f"        dir  same?")
    for r in rows:
        ys = " ".join(f"{y:7.3f}" for y in r["ys"])
        arrow = {1: "up", -1: "down", 0: "flat"}[r["direction"]]
        out(f"   {r['setting']:22s} {str(r['value']):>8s}   {ys}   "
            f"{arrow:4s} {'yes' if r['matches'] else '*** NO ***'}")
    # A FLAT BASELINE CERTIFIES NOTHING.  The first time this function was run
    # for real, every measurement came back 0.000 -- the sample held no hard
    # instances -- and it printed "direction holds under all 3 alternatives".
    # That is the failure this whole file exists to prevent, reappearing
    # inside it: a check that cannot fail proves nothing, and with no
    # variation in the baseline no alternative could have disagreed.
    ref = rows[0]
    if len(set(ref["ys"])) <= 1:
        out("\n   INCONCLUSIVE: the baseline does not vary over xs "
            f"(every value {ref['ys'][0]:.3f}).")
        out("   No alternative could have disagreed, so nothing was tested. "
            "Widen the")
        out("   sample until the baseline shows the effect, then re-run.")
        return None

    bad = [r for r in rows if not r["matches"]]
    if bad:
        out(f"\n   THE EFFECT DOES NOT SURVIVE: {len(bad)} of "
            f"{len(rows) - 1} alternatives reverse or flatten it.")
        out("   Whatever was measured is a property of those constants, not "
            "of x.")
    else:
        out(f"\n   Direction holds under all {len(rows) - 1} alternatives.")
    return not bad


def demo():
    """A synthetic relationship that is really a property of its constant.

    y rises with x when `lever` is on and is flat when it is off.  Measuring
    with `lever` pinned on -- which is exactly what I did with the lex break --
    reports a clean rising law.  This is the case the checker must catch, so
    the demo asserts that it does rather than merely printing.
    """
    def measure(x, lever=True, host="idle"):
        base = 1.0 if host == "idle" else 2.0
        return base + (0.5 * x if lever else 0.0)

    print(__doc__.strip().splitlines()[0] + "\n")
    print("  A law that is really its lever:\n")
    rows = vary(measure, xs=[15, 16],
                settings={"lever": [True, False], "host": ["idle", "busy"]})
    survived = report(rows)
    assert survived is False, "failed to catch a lever-carried effect"
    print("\n  Caught it: `lever` carries the effect, `host` shifts the level")
    print("  without changing the direction -- which is the distinction that")
    print("  matters, and the one I got wrong three times.\n")

    # The guard on the checker itself.  This is the case that caught me the
    # first time I ran the file for real, so it is asserted, not described.
    print("  A sample that could not have shown the effect:\n")
    flat = vary(lambda x, lever=True: 0.0, xs=[15, 16],
                settings={"lever": [True, False]})
    verdict = report(flat)
    assert verdict is None, "a flat baseline was certified rather than refused"
    print("\n  Refused rather than certified.  Without this guard the first")
    print("  real run of this file reported 'direction holds' over a sample")
    print("  of all zeros.")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(demo() if "demo" in sys.argv[1:] else demo())
