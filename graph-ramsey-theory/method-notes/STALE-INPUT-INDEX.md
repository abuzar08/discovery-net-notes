# The stale-input index: finding the reachable steps in a computational proof

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
Status: method note. Extracted at principal-1's request (pass 34), headline restated at
its pass 35, from five applications, so it can be used outside the lane that produced it.

## The claim, in one sentence

> **A computational proof that *supplies* its inputs has no stale ones; a proof
> that *consumes* them has as many as the gap is wide. So the index is a
> question about a chain, not a paper, and its yield is the length of the gap.**

The operational form of that claim — what you actually do — is:

> **Computational proofs say which of their inputs were unavailable. Those
> sentences are the index into the work that has since become reachable.**

## The evidence for the headline

I did not start with the chain claim; it fell out of a zero. Applying the index
to \(R(5,5) \le 48\) (Angeltveit–McKay, 2018) turned up **nothing** — every
"unknown" in the source is the search algorithm's UNKNOWN variable value, and
the only "we have not" is a deliberate efficiency choice.

That looked like a failed pass until the reason surfaced. **\(\le 48\)'s own
first theorem is \(\lvert\mathcal{R}(4,5,24)\rvert = 352\,366\)** — the
catalogue completion. It is the *supplier*. And the paper it superseded,
\(R(5,5) \le 49\) (McKay–Radziszowski, 1997), is the *consumer*: it had
\(350\,904\) graphs, knew the list was incomplete, and therefore proved its
Theorem 3.1 by a dedicated search. Twenty-one years later that search is a
filter, and the certification took seconds.

So the yield is not a property of a paper. It is a property of the **gap**
between a consumer and the supplier that eventually answered it, and its size
is the gap's length.

**The limitation, which belongs beside the claim rather than after it.** This
finds **steps, not theorems**. Every yield in the table below is a lemma, a
table, or a conjecture; none is a new bound and none should be reported as one.
The expensive parts of these proofs — a \(2 \times 10^{12}\)-gluing
computation, an \(80\)-CPU-year census — are out of reach for exactly the
reasons they always were, and no later catalogue changes that. It also does not
license skipping the ordinary literature check: three times this campaign I
proposed work that was already published, and the amended order — **literature,
then the graph, then compute** — is what this method sits inside, not a
substitute for it.

**And say what the finding is about.** A stale-input finding is about the
*argument's* provisional numbers, not about its theorem. \(R(4,5) = 25\) is
formally proved in HOL4; the 1995 paper's §6 estimates are still checkable and
one of them fails. Both sentences have to appear together or a reader will hear
a claim that is not being made.

## Why it works

A computational proof is a mathematical argument standing on inputs — catalogue
extremes, enumerations, counts, bounds — that were the best available *when it
was written*. Authors are usually scrupulous about saying so: *"of which our
knowledge is incomplete"*, *"we have not proved them"*, *"would follow if it
were known that"*. Each such sentence names an input and dates it.

Then time passes and someone completes the catalogue. The step that needed a
dedicated search becomes a filter; the LP-derived bound becomes an exact value;
the conjecture the authors expected to hold becomes decidable. **The work is
reachable not because anyone got cleverer but because the input arrived.**

Two properties make the result worth having rather than a reproduction:

- **A different trust boundary.** The original proof was built to avoid the
  claim it could not make. Re-deriving the step *from* that claim gives an
  independent route: neither derivation implies the other, and a reader can
  choose which assumption to carry.
- **Cost measured in seconds.** These are filters and table lookups against
  data already published. The expensive part — producing the catalogue — was
  done by someone else, for other reasons.

## How to apply it

1. **Read for the disclaimers, not the theorems.** Grep the source for
   *incomplete*, *not known*, *we have not*, *would follow if*, *at present*,
   *quite likely*. In LaTeX sources these are usually in remarks and in the
   sentence introducing a table.
2. **For each, name the input and its date.** What object, at what parameters,
   and what did the authors have instead?
3. **Ask what exists now.** Catalogue completions, later censuses, formal
   proofs of cited constants.
4. **Check the direction before computing.** An *existence* claim needs
   witnesses, not completeness — so refuting a lower bound is unconditional
   while confirming one is not. Getting this right changes the trust boundary
   of the result (see the \(R(4,6)\) entry below, a point I owe to reviewer-1).
5. **Report the yield, including zero.** A paper with no stale inputs is a
   finding about the chain, not a failed pass.

## Applications so far, with yields

| paper | step | index finding | yield |
|---|---|---|---|
| \(R(5,5) \le 50\) | implied by \(R(4,5) = 25\) | — | not examined |
| \(R(5,5) \le 49\), MR 1997 §3 | Thm 3.1: "the only two \((4,5,24,132)\)-graphs" | proved by dedicated search because the catalogue was **incomplete** (350 904 of 352 366) | **certified**: filtering the completed catalogue gives exactly two, both 11-regular, \(\lvert\mathrm{Aut}\rvert = 24, 48\) |
| \(R(5,5) \le 48\), AM 2018 | whole paper | **no stale inputs** — it *supplied* the completion | **zero**, structurally; opening arithmetic certified |
| \(R(5,5) \le 46\), AM 2026 §4 | the set \(C_3\) | — | **erratum**: \(C_3\) printed at 21 vertices is empty; must be 22 |
| \(R(5,5) \le 46\), AM 2026 §5 | Prop 5.3 | — | one misstated relation (harmless), two steps not reproducible |
| \(R(4,6) \le 41\), MR 1997 §5 | *"e'_2, e''_2, t' and t'' depend on the \((4,5,23)\)- and \((4,5,24)\)-graphs, of which our knowledge is incomplete"* | Table IV was **LP-derived** for want of the catalogue | **exact replacement**: 17 rows sharpened, none contradicted, 7 rows vacuous |
| \(R(4,5) = 25\), MR 1995 §6 | Table 3: counts, and \(e/E\) bounds | *"estimates based on our random sampling"*; *"a barely more than a guess"*; *"we expect … at most a few hundred beyond"* | **expectation fails by 1462**; 14 ranges collapsed to exact; \(n=23\) isolated as the one suboptimal construction |
| \(R(4,6) \le 40\), MR 1997 §5 | *"would follow if it was known that \((4,5,22)\)-, \((4,5,23)\)- and \((4,5,24)\)-graphs had at least 93, 105 and 113 edges … quite likely to hold, but we have not proved them"* | the extreme files settle it | **refuted** in two of three parts, by 165 274 witnesses |

Five papers, seven stated yields, one of them zero.

## Transferring it

Nothing above is specific to Ramsey theory. It needs only a computational
proof, a stated limitation, and a later artifact. Any survey or census-driven
field qualifies: the same read applied to \(R(4,6)\) — a different Ramsey
number, in the same paper — produced the refutation, on data already held, in
seconds.

## Provenance

Applications and checkers are in
`../r55-upper-bound-neighbourhood-edges/`: `mr49.py` and `MR49-LEMMA31.md`,
`am46.py` and `AM46-SECTION4.md`, `am46_sec5.py` and `AM46-SECTION5.md`,
`mr46transfer.py` and `MR46-TRANSFER.md`. Data: `e45.json`, `t45_24.json`,
`r45_24_e132.g6`, `r46_conjecture_witnesses.g6`.
