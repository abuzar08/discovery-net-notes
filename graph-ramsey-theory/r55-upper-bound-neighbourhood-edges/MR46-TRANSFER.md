# The method transfers: applied to \(R(4,6)\), it refutes a stated conjecture

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-09.
Subject: McKay and Radziszowski, *Subgraph Counting Identities and Ramsey
Numbers*, **JCTB 69 (1997) 193–209**, §5.
Checker: `mr46transfer.py`. Data: `e45.json`, `t45_24.json`.

principal-1, pass 33: *"apply the same question to the papers that bound
\(R(4,6)\) and the other lanes' problems, not only \(R(5,5)\): the method is not
specific to your seat, and if it transfers you should say so rather than keep
it."*

## The method, stated so it can be used elsewhere

> **What did the step need, and has a later catalogue, table or theorem since
> made that input available?**

Computational Ramsey proofs are built on inputs — catalogue extremes, counts,
enumerations — that were the best available *at the time*. Papers usually say
so explicitly, in a sentence about what is not yet known. Those sentences are
the index into the reachable work: each one names an input, and each input may
since have been supplied. The step is then re-derivable at negligible cost, by
a route with a **different trust boundary** from the original.

Yield so far, three papers: \(R(5,5) \le 46\) §4 — one erratum; §5 — one
misstated relation and two steps not reproducible; \(R(5,5) \le 49\) §3 — clean,
and now derivable from a catalogue completed twenty-one years later. This
document is the fourth, on a different Ramsey number.

## Applying it to \(R(4,6)\)

§5 proves \(R(4,6) \le 41\) by showing \(\mathrm{LP}(4,6,41)\) infeasible, and
says plainly where its inputs stop:

> "the values \(e'_2, e''_2, t'\) and \(t''\) depend on the
> \((4,5,23)\)-graphs and \((4,5,24)\)-graphs, **of which our knowledge is
> incomplete**."

and, in the same section:

> "the result \(R(4,6) \le 40\) would follow if it was known that
> \((4,5,22)\)-, \((4,5,23)\)- and \((4,5,24)\)-graphs had at least
> \(93\), \(105\) and \(113\) edges, respectively. **These bounds are quite
> likely to hold, but we have not proved them.**"

Those are lower bounds on \(e\) over **every** \((4,5,i)\)-graph — their
\(e'_2(i)\) inputs. All three are now settled.

### The conjecture is false, in two of its three parts

| \(i\) | hoped \(H(i)\) | true \(e_{\min}(4,5,i)\) | verdict |
|---|---|---|---|
| 22 | \(93\) | \(\mathbf{88}\) | **false**, by \(5\) |
| 23 | \(105\) | \(\mathbf{101}\) | **false**, by \(4\) |
| 24 | \(113\) | \(116\) | holds |

There are \((4,5,22)\)-graphs with \(88\) edges and \((4,5,23)\)-graphs with
\(101\). **So the stated sufficient condition does not hold, and that route to
\(R(4,6) \le 40\) is closed.**

### The refutation is unconditional — it needs witnesses, not completeness

*(Sharpening due to reviewer-1, pass 43, which certified the same graphs
independently with its own decoder and its own \(K_4\) and independent-5-set
searches. Adopted here because it removes a trust dependency I had left in.)*

I first stated this as "\(e_{\min}(4,5,22) = 88\)", which reads as leaning on
McKay's completeness claim. It does not. The refutation is an **existence**
claim — *there is* a \((4,5,22)\)-graph with fewer than \(93\) edges — so
what carries it is the graphs themselves. `r46_conjecture_witnesses.g6` holds
the four minimum-edge counterexamples, and `mr46transfer.py` re-verifies each
one on every run: correct order, correct edge count, no \(K_4\), no
independent \(5\)-set.

**So this refutation is independent of the completeness claim that the rest of
this directory's \((4,5)\) work cites.** That is worth stating because it is
unusual here: nearly everything else in this repository certifies a negative
and inherits a completeness assumption; this one certifies a positive and does
not.

And the conjecture fails by a wide margin rather than at a single point.
Verified across McKay's extreme-edge files:

| \(m\) | \(e\) | graphs, all verified | conjecture needs |
|---|---|---|---|
| 22 | 88 | 3 | \(\ge 93\) |
| 22 | 89 | 94 | \(\ge 93\) |
| 23 | 101 | 1 | \(\ge 105\) |
| 23 | 102 | 76 | \(\ge 105\) |
| 23 | 103 | 4424 | \(\ge 105\) |
| 23 | 104 | 160676 | \(\ge 105\) |

**\(165\,274\) counterexamples**, every one decoded and re-checked here — and
that is a lower bound on the true number, because the extreme files hold only
the smallest and largest edge counts, so \(e = 90, 91, 92\) at \(m = 22\)
are not even in them. Only the four minimum-edge graphs are committed; the rest
regenerate from `r45extreme.tar.gz`.

Scope, precisely: \(R(4,6) \le 41\) is **unaffected** — it does not use the
condition. And \(R(4,6) \le 40\) is true, obtained later by Angeltveit and
McKay, so this is a historical clarification of one route rather than a
statement about the bound. What it settles is a question the authors left open
and expected to go the other way.

The values are from `e45.json`, recomputed here from McKay's primary
catalogues, and they agree with Angeltveit and McKay's own Appendix Table 1 in
\(R(5,5) \le 46\) at \(i = 21,\dots,24\) — checked while doing
`AM46-SECTION4.md`, so this refutation rests on numbers confirmed twice.

### Their own LP-derived bounds, against the exact ones

| \(i\) | their \([e'_2, e''_2]\) | exact \([e_{\min}, e_{\max}]\) | sharpened |
|---|---|---|---|
| 23 | \([98, 130]\) | \([101, 122]\) | lower \(+3\), upper \(-8\) |
| 24 | \([109, 132]\) | \([116, 132]\) | lower \(+7\), upper \(-0\) |

Their \(e''_2(24) = 132\) was already exact, which is Theorem 3.1's input.

### Table IV, the triangle bounds, now exact at \(n = 24\)

Table IV gives \(t'(i,j) \le t(X) \le t''(i,j)\) for \((4,5,n,e)\)-graphs,
derived by LP because the catalogue was incomplete. Its columns three and four
are the extremes of the number of **induced three-vertex paths**,
\(p(X) = s(T_{2,1}, X) = \sum_v \binom{\deg v}{2} - 3t(X)\) — reviewer-1 had
to identify that by inspection, so `t45_24.json` now carries a `_schema` key
naming all five fields. The complete
\(352\,366\)-graph catalogue gives them exactly (`t45_24.json`, computed in
\(22\) s):

| \(e\) | Table IV | exact | | \(e\) | Table IV | exact |
|---|---|---|---|---|---|---|
| 109–115 | various | **empty** | | 124 | \([125,162]\) | \([140,154]\) |
| 116 | \([107,138]\) | \([123,128]\) | | 125 | \([127,165]\) | \([144,157]\) |
| 117 | \([107,142]\) | \([122,132]\) | | 126 | \([130,168]\) | \([147,160]\) |
| 118 | \([109,145]\) | \([120,136]\) | | 127 | \([133,169]\) | \([152,162]\) |
| 119 | \([112,148]\) | \([124,140]\) | | 128 | \([135,170]\) | \([156,164]\) |
| 120 | \([114,151]\) | \([127,144]\) | | 129 | \([138,172]\) | \([162,166]\) |
| 121 | \([117,154]\) | \([130,146]\) | | 130 | \([142,173]\) | \([166,169]\) |
| 122 | \([119,156]\) | \([133,149]\) | | 131 | \([146,174]\) | \([172,172]\) |
| 123 | \([122,159]\) | \([136,152]\) | | 132 | \([176,176]\) | \([176,176]\) |

**Every exact range lies strictly inside theirs.** Seventeen rows sharpened —
by up to \(+26\) on the lower side and \(-10\) on the upper — none contradicted,
which is a two-way consistency check: on their 1995 linear programs and on my
computation from the catalogue. And **seven rows are vacuous**: \(e = 109\) to
\(115\) is below \(e_{\min}(4,5,24) = 116\), so no graph has those edge counts.
Row \(132\) they already had exactly.

## Verdict on the transfer

**The method transfers, and it is not specific to \(R(5,5)\).** On a different
Ramsey number it produced a refutation of a stated conjecture, an exact
replacement for a published table, and the identification of seven vacuous rows
in it — all from data this directory already held, in seconds.

What makes it work is the same thing every time: the papers *say* which inputs
were unavailable, and thirty years of catalogue work has supplied some of them.
Anyone auditing a computational proof of this era should read those sentences
first.

## Reproduction

```bash
python3 mr46transfer.py
```

Seconds; needs only `e45.json` and `t45_24.json`.
